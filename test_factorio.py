"""Compare native original/restored imports in an isolated Factorio test scenario.

Requires a local Factorio 2.1+ headless binary and native pairs from audit.py.
No production saves, mods, config, or network server are used.
"""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile


CONTROL = r'''
local cases = require("pairs")
script.on_init(function()
  local passed, clean, warning, rejected = 0, 0, 0, 0
  local results = {}
  for i, case in ipairs(cases) do
    local inv = game.create_inventory(2)
    local ok_a, a = pcall(function() return inv[1].import_stack(case[2]) end)
    local ok_b, b = pcall(function() return inv[2].import_stack(case[3]) end)
    if ok_a ~= ok_b then error("Import exception mismatch: " .. case[1]) end
    if ok_a and a ~= b then error("Import status mismatch: " .. case[1]) end
    if ok_a and a ~= 1 then
      if inv[1].export_stack() ~= inv[2].export_stack() then
        error("Re-export mismatch: " .. case[1])
      end
      passed = passed + 1
      if a == 0 then clean = clean + 1 else warning = warning + 1 end
    else
      rejected = rejected + 1
    end
    localised_print("BLUEPRINT_AUDIT_CASE " .. i .. " " .. case[1] .. " " .. tostring(ok_a and a or "exception"))
    results[#results + 1] = {key=case[1], status=ok_a and a or "exception", exports_equal=ok_a and a ~= 1}
    inv.destroy()
  end
  localised_print("BLUEPRINT_AUDIT_RESULT " .. helpers.table_to_json({
    imported_equal=passed, clean=clean, warnings=warning, both_rejected=rejected, total=#cases,
    cases=results, mods=script.active_mods
  }))
  script.finish_test(passed > 0 and passed + rejected == #cases)
end)
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("factorio", type=Path)
    parser.add_argument("pairs", type=Path)
    args = parser.parse_args()
    binary = args.factorio.resolve()
    data = binary.parent.parent.parent / "data"
    pairs = json.loads(args.pairs.read_text())
    version = subprocess.check_output([str(binary), "--version"], text=True).splitlines()[0]
    with tempfile.TemporaryDirectory(prefix="factorio-blueprint-audit-") as temp:
        work = Path(temp)
        scenario = work / "scenarios/blueprint-audit"
        scenario.mkdir(parents=True)
        (work / "mods").mkdir()
        (scenario / "control.lua").write_text(CONTROL)
        lua = "return {\n" + ",\n".join(
            "{" + json.dumps(p["key"]) + ",[=[" + p["original"] + "]=],[=[" + p["restored"] + "]=]}"
            for p in pairs) + "\n}\n"
        (scenario / "pairs.lua").write_text(lua)
        (work / "config.ini").write_text(f"[path]\nread-data={data}\nwrite-data={work}\n")
        mods = ["base", "elevated-rails", "quality", "space-age"]
        (work / "mods/mod-list.json").write_text(json.dumps({"mods": [{"name": m, "enabled": True} for m in mods]}))
        command = [str(binary), "--config", str(work / "config.ini"), "--mod-directory", str(work / "mods"),
                   "--test-scenario", "blueprint-audit"]
        run = subprocess.run(command, capture_output=True, text=True, timeout=300)
        result = None
        for line in (run.stdout + "\n" + run.stderr).splitlines():
            if "BLUEPRINT_AUDIT_" in line:
                print(line, flush=True)
            if line.startswith("BLUEPRINT_AUDIT_RESULT "):
                result = json.loads(line.removeprefix("BLUEPRINT_AUDIT_RESULT "))
        if run.returncode != 0 or result is None:
            print((run.stdout + "\n" + run.stderr)[-6000:])
            raise RuntimeError(f"Factorio test failed with exit code {run.returncode}")
        result.update(version=version, requested_mods=mods, reexport_comparison="byte-identical", mismatches=0)
        Path(__file__).with_name("factorio-audit-results.json").write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
