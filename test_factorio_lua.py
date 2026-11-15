"""Run the Lua codec inside Factorio and check its output independently in Python."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

from benchmark_sites import serialized
from compact import decode, native_decode

ROOT = Path(__file__).parent

CONTROL = r'''
local codec=require("blueprint")
local cases=require("cases")
script.on_init(function()
  local outputs={}
  local decoder_checks,clean,warnings,portable_imports=0,0,0,0
  for i,case in ipairs(cases) do
    local original=codec.parse_json(assert(helpers.decode_string(case.original:sub(2))))
    local expected=codec.pack(original,true)
    for _,frame in ipairs(case.decodes) do
      assert(codec.pack(codec.decode(frame),true)==expected,"Python -> Lua mismatch: "..case.key)
      decoder_checks=decoder_checks+1
    end
    local encoded=codec.encode_native(case.original)
    assert(codec.pack(codec.decode(encoded),true)==expected,"Lua self-roundtrip mismatch: "..case.key)
    local inv=game.create_inventory(3)
    local a=inv[1].import_stack(case.original)
    local b=inv[2].import_stack(codec.decode_native(encoded))
    assert(a==b and a~=1,"Lua import status mismatch: "..case.key)
    if inv[1].export_stack()~=inv[2].export_stack() then
      helpers.write_file("lua-failure.json",helpers.table_to_json({key=case.key,
        encoded=encoded,original=case.original,restored=codec.decode_native(encoded),
        export_original=inv[1].export_stack(),export_restored=inv[2].export_stack()}),false)
      error("Lua re-export mismatch: "..case.key)
    end
    if case.portable and #case.portable>0 then
      local c=inv[3].import_stack(codec.decode_native(case.portable))
      assert(c==a and inv[3].export_stack()==inv[1].export_stack(),"Python portable import mismatch: "..case.key)
      portable_imports=portable_imports+1
    end
    if a==0 then clean=clean+1 else warnings=warnings+1 end
    inv.destroy()
    outputs[#outputs+1]={key=case.key,encoded=encoded,status=a}
    localised_print("LUA_CODEC_CASE "..i.." "..case.key.." "..#encoded)
  end
  helpers.write_file("lua-encoded.json",helpers.table_to_json(outputs),false)
  localised_print("LUA_CODEC_RESULT "..helpers.table_to_json({
    total=#cases,decoder_checks=decoder_checks,portable_imports=portable_imports,clean=clean,warnings=warnings,
    mismatches=0,mods=script.active_mods
  }))
  script.finish_test(true)
end)
'''


def lua_string(value):
    assert "]=]" not in value
    return "[=[" + value + "]=]"


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("factorio",type=Path)
    parser.add_argument("cases",type=Path)
    args=parser.parse_args()
    binary=args.factorio.resolve()
    data=binary.parent.parent.parent/"data"
    cases=json.loads(args.cases.read_text())
    version=subprocess.check_output([str(binary),"--version"],text=True).splitlines()[0]
    with tempfile.TemporaryDirectory(prefix="factorio-lua-codec-") as folder:
        work=Path(folder)
        scenario=work/"scenarios/codec-audit"
        scenario.mkdir(parents=True)
        (work/"mods").mkdir()
        shutil.copyfile(ROOT/"lua/blueprint.lua",scenario/"blueprint.lua")
        (scenario/"control.lua").write_text(CONTROL)
        body=[]
        for case in cases:
            frames=",".join(lua_string(t) for t in case["decodes"])
            body.append("{key="+lua_string(case["key"])+",original="+lua_string(case["original"])+
                        ",portable="+lua_string(case.get("portable", ""))+",decodes={"+frames+"}}")
        (scenario/"cases.lua").write_text("return {\n"+",\n".join(body)+"\n}\n")
        (work/"config.ini").write_text(f"[path]\nread-data={data}\nwrite-data={work}\n")
        (work/"mods/mod-list.json").write_text(json.dumps({"mods":[{"name":name,"enabled":True}
                        for name in ("base","quality","elevated-rails","space-age")]}))
        command=[str(binary),"--config",str(work/"config.ini"),"--mod-directory",str(work/"mods"),
                 "--test-scenario","codec-audit"]
        log=work/"audit-output.log"
        started=time.monotonic()
        with log.open('w') as stream:
            process=subprocess.Popen(command,stdout=stream,stderr=subprocess.STDOUT,text=True)
            cursor=0
            while process.poll() is None:
                if time.monotonic()-started>1200:
                    process.kill(); process.wait()
                    raise TimeoutError('Factorio Lua audit timed out')
                with log.open() as reader:
                    reader.seek(cursor)
                    for line in reader:
                        if line.startswith('LUA_CODEC_CASE '):print(line.rstrip(),flush=True)
                    cursor=reader.tell()
                time.sleep(0.25)
        transcript=log.read_text()
        result=None
        for line in transcript.splitlines():
            if line.startswith("LUA_CODEC_RESULT "):
                result=json.loads(line.removeprefix("LUA_CODEC_RESULT "))
        if process.returncode!=0 or result is None:
            failure=work/'script-output/lua-failure.json'
            if failure.exists():
                shutil.copyfile(failure,Path(tempfile.gettempdir())/'factorio-lua-failure.json')
            print(transcript[-10000:])
            raise RuntimeError(f"Factorio Lua audit failed: exit {process.returncode}")
        encoded=json.loads((work/"script-output/lua-encoded.json").read_text())
        assert len(encoded)==len(cases)
        measurements=[]
        for source,actual in zip(cases,encoded):
            assert actual["key"]==source["key"]
            expected=native_decode(source["original"])
            restored=decode(actual["encoded"])
            assert serialized(restored)==serialized(expected),source["key"]
            measurements.append({"key":source["key"],"lua_chars":len(actual["encoded"]),
                                 "python_portable_chars":len(source["portable"]),
                                 "native_chars":len(source["original"]),"status":actual["status"],
                                 "mode":actual["encoded"][4:6]})
        result.update(version=version,python_decoder_checks=len(encoded),seconds=round(time.monotonic()-started,3),
                      lua_sha256=__import__("hashlib").sha256((ROOT/"lua/blueprint.lua").read_bytes()).hexdigest(),
                      measurements=measurements)
        (ROOT/"lua-audit-results.json").write_text(json.dumps(result,indent=2)+"\n")
        print(json.dumps({k:v for k,v in result.items() if k!="measurements"},indent=2))


if __name__=="__main__":
    main()
