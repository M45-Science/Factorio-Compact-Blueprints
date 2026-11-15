"""Exercise the independent Lua codec through a real Lua 5.2 process."""
import base64
import json
import os
from pathlib import Path
import shutil
import subprocess
import unittest

from compact import candidates, decode, pack, varint, zigzag
from test_subassemblies import repeated_factory

ROOT = Path(__file__).parent
IMAGE = "nickblah/lua:5.2-alpine"


def lua_command():
    binary = os.environ.get("LUA52") or shutil.which("lua5.2")
    if binary:
        return [binary, "lua/driver.lua"]
    if shutil.which("docker"):
        status = subprocess.run(["docker", "image", "inspect", IMAGE], capture_output=True)
        if status.returncode == 0:
            return ["docker", "run", "--rm", "-i", "-v", str(ROOT) + ":/work", "-w", "/work",
                    IMAGE, "lua", "lua/driver.lua"]
    return None


class LuaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.command = lua_command()
        if cls.command is None:
            if os.environ.get("REQUIRE_LUA_TESTS"):
                raise RuntimeError("Lua 5.2 is required for this test run")
            raise unittest.SkipTest("Install Lua 5.2 or pull " + IMAGE)

    def driver(self, action, lines):
        run = subprocess.run(self.command + [action], input="\n".join(lines) + "\n",
                             cwd=ROOT, text=True, capture_output=True, timeout=180)
        self.assertEqual(run.returncode, 0, run.stderr)
        return run.stdout.splitlines()

    def test_json_types_and_precision(self):
        values = [{"empty-array": [], "empty-object": {}, "null": None, "flag": False},
                  [0, 0.0, -0.0, 1/3, 5e-324, 1.7976931348623157e308, 2**64-1, -2**63, 2**100],
                  {"label": "🏭 снежок ☃", "escape": "\n\t\\\""}]
        encoded = [json.dumps(v, ensure_ascii=False) for v in values]
        for original, result in zip(values, self.driver("json", encoded)):
            self.assertEqual(json.dumps(json.loads(result), sort_keys=True, ensure_ascii=False),
                             json.dumps(original, sort_keys=True, ensure_ascii=False))

    def test_fixed_reference_vectors(self):
        for vector in json.loads((ROOT/'test-vectors.json').read_text()):
            expected=json.dumps(vector['value'],sort_keys=True)
            texts=list(vector['frames'].values())
            for frame in texts:
                self.assertEqual(json.dumps(decode(frame),sort_keys=True),expected)
            for output in self.driver('decode',texts):
                self.assertEqual(json.dumps(json.loads(output),sort_keys=True),expected)

    def test_python_encoder_lua_decoder_all_forms(self):
        value = {"blueprint_book": {"blueprints": [dict(index=3, **repeated_factory(4, 4)),
                                                  dict(index=77, **repeated_factory(8, 4))]}}
        options = candidates(value, interned=True, codecs=["n"])
        self.assertEqual(len(options), 25)
        output = self.driver("decode", list(options.values()))
        self.assertEqual(len(output), len(options))
        for mode, result in zip(options, output):
            self.assertEqual(json.loads(result), value, mode)

    def test_lua_encoder_python_decoder_and_optional_blocks(self):
        value = repeated_factory(8, 4)
        value["blueprint"]["version"] = 2**63 + 5
        for i, row in enumerate(value["blueprint"]["entities"]):
            row["connections"] = {"1": {"red": [{"entity_id": (i+5) % 128 * 7+11}]}}
            row["tags"] = {"big": 2**100, "tiny": 5e-324, "minus-zero": -0.0}
        value["blueprint"]["wires"] = [[11, 1, 46, 2], [46, 2, 11, 1]]
        text = json.dumps(value)
        for action in ("encode", "encode-blocks"):
            encoded = self.driver(action, [text])[0]
            result = decode(encoded)
            self.assertEqual(json.dumps(result, sort_keys=True), json.dumps(value, sort_keys=True))
            self.assertEqual(json.loads(self.driver("decode", [encoded])[0]), value)

    def test_empty_and_unsupported_entities(self):
        values = [{"blueprint": {"entities": [], "tiles": []}},
                  {"blueprint": {"entities": [{"entity_number": 1, "name": "mod",
                                               "position": {"x": 1, "y": 2, "z": 3}}]}},
                  {"blueprint": {"entities": [{"entity_number": 2**60, "name": "mod",
                                               "position": {"x": 1/3, "y": 1e100}}]}}]
        for value, encoded in zip(values, self.driver("encode", [json.dumps(v) for v in values])):
            self.assertEqual(json.dumps(decode(encoded), sort_keys=True), json.dumps(value, sort_keys=True))

    def test_large_integer_id_columns(self):
        for ids in ([2**63+i*7 for i in range(20)],
                    [-2**63+i*7 for i in range(20)],
                    [2**64-1-i*7 for i in range(20)],
                    [2**63+n for n in [3,1,9,2,0,15,5,13]*3],
                    [-2**63, 2**64-1, -2**63+9, 17]):
            value={"blueprint":{"entities":[{"entity_number":n,"name":"test",
                       "position":{"x":i,"y":0}} for i,n in enumerate(ids)]}}
            options=candidates(value,interned=True,codecs=["n"])
            for result in self.driver("decode",list(options.values())):
                self.assertEqual(json.loads(result),value)

    def test_wide_delta_and_bitpacked_sequences(self):
        ids=[-2**63,2**64-1,-2**63+9,17]
        deltas=[ids[i]-ids[i-1] for i in range(1,len(ids))]
        width=(max(ids)-min(ids)).bit_length()
        bits=''.join(format(n-min(ids),f'0{width}b') for n in ids)
        bits+='0'*(-len(bits)%8)
        encoded=[
            [2,ids[0],b''.join(varint(zigzag(d)) for d in deltas)],
            [3,ids[0],b''.join(varint(zigzag(d))+varint(1) for d in deltas)],
            [4,len(ids),min(ids),width,int(bits,2).to_bytes(len(bits)//8,'big')],
        ]
        frames=[]
        for column in encoded:
            payload=[{'blueprint':{'entities':None}},[[['blueprint','entities'],
                     [[{'name':'test'}],[0,[0]*len(ids)],[0,list(range(len(ids)))],
                      [0,[0]*len(ids)],column]]]]
            frames.append('BX0:sn'+base64.urlsafe_b64encode(pack(payload)).decode().rstrip('='))
        for result in self.driver('decode',frames):
            actual=json.loads(result)
            self.assertEqual([r['entity_number'] for r in actual['blueprint']['entities']],ids)

    def test_large_coordinate_progression_is_not_rounded(self):
        positions=[-9000000000000000,-2999999999999999,3000000000000002,9000000000000004]
        value={"blueprint":{"entities":[{"entity_number":i+1,"name":"test",
                    "position":{"x":x,"y":0}} for i,x in enumerate(positions)]}}
        text=self.driver("encode",[json.dumps(value)])[0]
        self.assertEqual(decode(text),value)

    def test_legacy_module_map_order_is_preserved(self):
        rows=[]
        for i in range(16):
            items=({'speed-module':1,'productivity-module':3} if i%2==0
                   else {'productivity-module':3,'speed-module':1})
            rows.append({'entity_number':i+1,'name':'assembling-machine-3',
                         'position':{'x':i*4+1.5,'y':1.5},'items':items})
        value={'blueprint':{'item':'blueprint','version':281479275151360,'entities':rows}}
        encoded=self.driver('encode-blocks',[json.dumps(value)])[0]
        restored=decode(encoded)
        for a,b in zip(value['blueprint']['entities'],restored['blueprint']['entities']):
            self.assertEqual(list(a['items']),list(b['items']))

    def test_malformed_inputs(self):
        for text in ("BX0:", "BX0:gn!", "BX0:gnAA", "BX0:gnwQ", "BX0:gn3f____8", "BX0:in"):
            run = subprocess.run(self.command + ["decode"], input=text + "\n", cwd=ROOT,
                                 text=True, capture_output=True, timeout=15)
            self.assertNotEqual(run.returncode, 0, text)
        for text in ('1.e2', '01', '1e', '[1,]', '{"x":1,"x":2}'):
            run = subprocess.run(self.command + ['json'], input=text+'\n', cwd=ROOT,
                                 text=True, capture_output=True, timeout=15)
            self.assertNotEqual(run.returncode, 0, text)


if __name__ == "__main__":
    unittest.main()
