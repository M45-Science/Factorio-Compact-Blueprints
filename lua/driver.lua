-- Line-oriented standalone test driver. Compression is tested in Factorio.
local codec=require('lua.blueprint')
local action=assert(arg[1],'expected action')
for line in io.lines() do
  if action=='json' then io.write(codec.to_json(codec.parse_json(line)),'\n')
  elseif action=='decode' then io.write(codec.decode_json(line),'\n')
  elseif action=='pack' then
    local bytes=codec.pack(codec.parse_json(line))
    io.write((bytes:gsub('.',function(c) return string.format('%02x',c:byte()) end)),'\n')
  elseif action=='encode' or action=='encode-blocks' then io.write(codec.encode_json(line,{codec='n',blocks=action=='encode-blocks'}),'\n')
  else error('unknown action') end
end
