-- Factorio Compact Blueprints. Lua 5.2; no external Lua dependencies.
-- JSON numbers retain their integer/float distinction and large integers.
local M = {}
local floor, abs, concat = math.floor, math.abs, table.concat
local SAFE, U32 = 9007199254740991, 4294967296
local array_mt, object_mt, float_mt, integer_mt, binary_mt, ext_mt = {}, {}, {}, {}, {}, {}
local object_orders=setmetatable({}, {__mode='k'})
local ordered_keys, keys
M.null = setmetatable({}, {__tostring=function() return "null" end})
local null = M.null
local function arr(t) return setmetatable(t or {}, array_mt) end
local function obj(t) return setmetatable(t or {}, object_mt) end
local function float(n, raw) return setmetatable({value=n, raw=raw}, float_mt) end
local function binary(s) return setmetatable({data=s}, binary_mt) end
local function ext(code, s) return setmetatable({code=code, data=s}, ext_mt) end
local function num(n) return getmetatable(n) == float_mt and n.value or n end
local function isint(n) return type(n)=="number" and abs(n)<=SAFE and n==floor(n) end
local function isnumber(n) return isint(n) or getmetatable(n)==float_mt end
local function copy(v)
  if type(v)~="table" or v==null then return v end
  local out={}
  if getmetatable(v)==object_mt then
    local order={}
    for _,k in ipairs(ordered_keys(v)) do local key=copy(k); order[#order+1]=key; out[key]=copy(v[k]) end
    object_orders[out]=order
  else for k,x in pairs(v) do out[copy(k)]=copy(x) end end
  return setmetatable(out,getmetatable(v))
end
ordered_keys=function(t)
  local saved=object_orders[t]
  if not saved then return keys(t) end
  local order,seen={},{}
  for _,k in ipairs(saved) do if t[k]~=nil then order[#order+1]=k; seen[k]=true end end
  for _,k in ipairs(keys(t)) do if not seen[k] then order[#order+1]=k end end
  return order
end
keys=function(t)
  local out={}; for k in pairs(t) do out[#out+1]=k end
  table.sort(out,function(a,b)
    if type(a)=='string' and type(b)=='string' then return a<b end
    return M.pack(a)<M.pack(b)
  end); return out
end
M.array, M.object, M.float, M.binary = arr, obj, float, binary

-- Integer arithmetic outside the double's exact range is decimal, never rounded.
local function exact_integer(raw)
  local n=tonumber(raw)
  if n and abs(n)<=SAFE then return n end
  return setmetatable({raw=raw},integer_mt)
end
local function integer_text(v)
  return getmetatable(v)==integer_mt and v.raw or string.format('%.0f',v)
end
local function add_integer(a,b)
  if type(a)=='number' and type(b)=='number' and abs(a)+abs(b)<=SAFE then return a+b end
  local x,y=integer_text(a),integer_text(b)
  local nx,ny=x:sub(1,1)=='-',y:sub(1,1)=='-'
  if nx then x=x:sub(2) end; if ny then y=y:sub(2) end
  local subtract=nx~=ny
  if subtract and (#x<#y or #x==#y and x<y) then x,y,nx=y,x,ny end
  local out,carry={},0
  for i=0,math.max(#x,#y)-1 do
    local dx=(#x-i>0 and x:byte(#x-i) or 48)-48
    local dy=(#y-i>0 and y:byte(#y-i) or 48)-48
    local n=dx+(subtract and -dy or dy)+carry
    if subtract then carry=n<0 and -1 or 0; n=n%10 else carry=floor(n/10); n=n%10 end
    out[#out+1]=string.char(48+n)
  end
  if carry>0 then out[#out+1]=string.char(48+carry) end
  local digits={}; for i=#out,1,-1 do digits[#digits+1]=out[i] end
  local raw=concat(digits):gsub('^0+',''); if raw=='' then return 0 end
  return exact_integer((nx and '-' or '')..raw)
end
local function half_integer(v)
  if type(v)=='number' then return floor(v/2) end
  local raw=v.raw; assert(raw:sub(1,1)~='-','expected nonnegative integer')
  local out,carry={},0
  for i=1,#raw do local n=carry*10+raw:byte(i)-48; out[i]=string.char(48+floor(n/2)); carry=n%2 end
  local digits=concat(out):gsub('^0+',''); return exact_integer(digits=='' and '0' or digits)
end
local function unzig_integer(v)
  if type(v)=='number' then return v%2==0 and v/2 or -(v+1)/2 end
  local odd=(v.raw:byte(-1)-48)%2==1
  if not odd then return half_integer(v) end
  local q=half_integer(add_integer(v,1)); return exact_integer('-'..integer_text(q))
end

local function utf8(n)
  if n<128 then return string.char(n) end
  if n<2048 then return string.char(192+floor(n/64),128+n%64) end
  if n<65536 then return string.char(224+floor(n/4096),128+floor(n/64)%64,128+n%64) end
  return string.char(240+floor(n/262144),128+floor(n/4096)%64,128+floor(n/64)%64,128+n%64)
end

function M.parse_json(text)
  local p, length = 1, #text
  local function ws() while text:sub(p,p):match("[ \t\r\n]") do p=p+1 end end
  local function str()
    assert(text:sub(p,p)=='"',"expected JSON string"); p=p+1
    local out, start={},p
    while p<=length do
      local c=text:byte(p)
      if c==34 then out[#out+1]=text:sub(start,p-1); p=p+1; return concat(out) end
      if c==92 then
        out[#out+1]=text:sub(start,p-1); p=p+1
        local e=text:sub(p,p); p=p+1
        local escapes={['"']='"',['\\']='\\',['/']='/',b='\b',f='\f',n='\n',r='\r',t='\t'}
        if e=='u' then
          local hex=text:sub(p,p+3); assert(#hex==4 and hex:match('^%x+$'),"bad Unicode escape")
          local n=tonumber(hex,16); p=p+4
          if n>=55296 and n<=56319 then
            assert(text:sub(p,p+1)=='\\u',"missing low surrogate"); p=p+2
            local low=tonumber(text:sub(p,p+3),16); p=p+4
            assert(low and low>=56320 and low<=57343,"bad low surrogate")
            n=65536+(n-55296)*1024+low-56320
          else assert(n<56320 or n>57343,"unpaired surrogate") end
          out[#out+1]=utf8(n)
        else assert(escapes[e],"bad JSON escape"); out[#out+1]=escapes[e] end
        start=p
      else assert(c>=32,"control character in JSON string"); p=p+1 end
    end
    error("unterminated JSON string")
  end
  local value
  value=function(depth)
    assert(depth<256,"JSON nesting limit"); ws()
    local c=text:sub(p,p)
    if c=='"' then return str() end
    if c=='{' then
      p=p+1; ws(); local out=obj(); object_orders[out]={}
      if text:sub(p,p)=='}' then p=p+1; return out end
      while true do
        ws(); local k=str(); ws(); assert(text:sub(p,p)==':',"missing colon"); p=p+1
        assert(out[k]==nil,"duplicate JSON key"); out[k]=value(depth+1); ws()
        object_orders[out][#object_orders[out]+1]=k
        c=text:sub(p,p); p=p+1
        if c=='}' then return out end
        assert(c==',',"missing object comma")
      end
    end
    if c=='[' then
      p=p+1; ws(); local out=arr()
      if text:sub(p,p)==']' then p=p+1; return out end
      while true do
        out[#out+1]=value(depth+1); ws(); c=text:sub(p,p); p=p+1
        if c==']' then return out end
        assert(c==',',"missing array comma")
      end
    end
    for literal,result in pairs({['true']=true,['false']=false,['null']=null}) do
      if text:sub(p,p+#literal-1)==literal then p=p+#literal; return result end
    end
    local token=text:match('^-?%d+',p)
    assert(token and not token:match('^-?0%d'),"invalid JSON value")
    local q=p+#token
    if text:sub(q,q)=='.' then
      local fraction=text:match('^%.%d+',q); assert(fraction,'invalid JSON fraction')
      token=token..fraction; q=p+#token
    end
    if text:sub(q,q):match('[eE]') then
      local exponent=text:match('^[eE][+-]?%d+',q); assert(exponent,'invalid JSON exponent')
      token=token..exponent
    end
    p=p+#token
    if token:match('[%.eE]') then
      local n=tonumber(token); assert(n and n==n and abs(n)~=math.huge,"nonfinite JSON number")
      return float(n,token)
    end
    local n=tonumber(token)
    if n and abs(n)<=SAFE then return n end
    return setmetatable({raw=token},integer_mt)
  end
  local out=value(0); ws(); assert(p==length+1,"extra JSON input"); return out
end

local function quote(s)
  local escapes={['"']='\\"',['\\']='\\\\',['\b']='\\b',['\f']='\\f',['\n']='\\n',['\r']='\\r',['\t']='\\t'}
  return '"'..s:gsub('[%z\1-\31\\"]',function(c) return escapes[c] or string.format('\\u%04x',c:byte()) end)..'"'
end
function M.to_json(v)
  if v==null then return "null" end
  local kind=type(v)
  if kind=="string" then return quote(v) end
  if kind=="boolean" then return tostring(v) end
  if kind=="number" then assert(isint(v),"use float() for floating-point JSON values"); return string.format('%.0f',v) end
  local mt=getmetatable(v)
  if mt==integer_mt then return v.raw end
  if mt==float_mt then
    if v.raw then return v.raw end
    local s=string.format('%.17g',v.value)
    if v.value==0 and 1/v.value<0 then return '-0.0' end
    if not s:find('[%.eE]') then s=s..'.0' end
    return s
  end
  local out={}
  if mt==array_mt then
    for i=1,#v do out[i]=M.to_json(v[i]) end
    return '['..concat(out,',')..']'
  end
  assert(mt==object_mt,"expected JSON object or array")
  for _,k in ipairs(ordered_keys(v)) do out[#out+1]=quote(k)..':'..M.to_json(v[k]) end
  return '{'..concat(out,',')..'}'
end

local function uint(n,width)
  local out={}; for i=width,1,-1 do out[i]=string.char(n%256); n=floor(n/256) end
  assert(n==0,"integer overflow"); return concat(out)
end
local function decimal(hi,lo)
  if hi==0 and lo==0 then return '0' end
  local out={}
  while hi>0 or lo>0 do
    local qhi=floor(hi/10); local mixed=(hi%10)*U32+lo
    out[#out+1]=string.char(48+mixed%10); hi,lo=qhi,floor(mixed/10)
  end
  local result={}; for i=#out,1,-1 do result[#result+1]=out[i] end
  return concat(result)
end
local function limbs(raw)
  local hi,lo=0,0
  for digit in raw:gmatch('%d') do
    local nextlo=lo*10+tonumber(digit); hi=hi*10+floor(nextlo/U32); lo=nextlo%U32
    if hi>=U32 then return nil end
  end
  return hi,lo
end
local function extpack(code,data)
  local sizes={[1]=212,[2]=213,[4]=214,[8]=215,[16]=216}; local n=#data
  local head=sizes[n] and string.char(sizes[n]) or
    (n<256 and string.char(199)..uint(n,1) or n<65536 and string.char(200)..uint(n,2) or string.char(201)..uint(n,4))
  return head..string.char(code%256)..data
end
local function double(v)
  local sign=(v<0 or v==0 and 1/v<0) and 2147483648 or 0
  v=abs(v); local exponent,fraction=0,0
  if v>0 then
    local m,e=math.frexp(v); exponent=e+1022
    if exponent<=0 then exponent=0; fraction=v/2^-1074 else fraction=(m*2-1)*2^52 end
  end
  return uint(sign+exponent*1048576+floor(fraction/U32),4)..uint(fraction%U32,4)
end
function M.pack(v,canonical)
  if v==null then return string.char(192) end
  if type(v)=='boolean' then return string.char(v and 195 or 194) end
  if type(v)=='number' then
    assert(isint(v),'unsafe integer')
    if v>=0 then
      if v<128 then return string.char(v) end
      if v<256 then return string.char(204)..uint(v,1) end
      if v<65536 then return string.char(205)..uint(v,2) end
      if v<U32 then return string.char(206)..uint(v,4) end
      return string.char(207)..uint(floor(v/U32),4)..uint(v%U32,4)
    end
    if v>=-32 then return string.char(256+v) end
    if v>=-128 then return string.char(208)..uint(256+v,1) end
    if v>=-32768 then return string.char(209)..uint(65536+v,2) end
    if v>=-2147483648 then return string.char(210)..uint(U32+v,4) end
    local hi,lo=floor(-v/U32),(-v)%U32
    hi,lo=U32-1-hi,U32-1-lo; lo=lo+1; if lo==U32 then hi,lo=hi+1,0 end
    return string.char(211)..uint(hi,4)..uint(lo,4)
  end
  if type(v)=='string' then
    local n=#v
    local head=n<32 and string.char(160+n) or n<256 and string.char(217)..uint(n,1) or
      n<65536 and string.char(218)..uint(n,2) or string.char(219)..uint(n,4)
    return head..v
  end
  local mt=getmetatable(v)
  if mt==float_mt then return string.char(203)..double(v.value) end
  if mt==integer_mt then
    local hi,lo=limbs(v.raw)
    if not hi then return extpack(3,v.raw) end
    if v.raw:sub(1,1)=='-' then
      if hi>2147483648 or hi==2147483648 and lo>0 then return extpack(3,v.raw) end
      hi,lo=U32-1-hi,U32-1-lo; lo=lo+1; if lo==U32 then hi,lo=hi+1,0 end
      return string.char(211)..uint(hi,4)..uint(lo,4)
    end
    return string.char(207)..uint(hi,4)..uint(lo,4)
  end
  if mt==binary_mt then
    local n=#v.data
    return (n<256 and string.char(196)..uint(n,1) or n<65536 and string.char(197)..uint(n,2) or string.char(198)..uint(n,4))..v.data
  end
  if mt==ext_mt then return extpack(v.code,v.data) end
  local out={}
  if mt==array_mt then
    local n=#v; out[1]=n<16 and string.char(144+n) or n<65536 and string.char(220)..uint(n,2) or string.char(221)..uint(n,4)
    for i=1,n do out[#out+1]=M.pack(v[i],canonical) end
  else
    assert(mt==object_mt,'expected typed MessagePack value')
    local order=canonical and keys(v) or ordered_keys(v); local n=#order
    out[1]=n<16 and string.char(128+n) or n<65536 and string.char(222)..uint(n,2) or string.char(223)..uint(n,4)
    for _,k in ipairs(order) do out[#out+1]=M.pack(k,canonical); out[#out+1]=M.pack(v[k],canonical) end
  end
  return concat(out)
end

function M.unpack(data)
  local p=1
  local function take(n) assert(n<=#data-p+1,'truncated MessagePack'); local s=data:sub(p,p+n-1); p=p+n; return s end
  local function u(n) local v=0; for i=1,n do v=v*256+take(1):byte() end; return v end
  local read
  read=function(depth)
    assert(depth<256,'MessagePack nesting limit')
    local c=u(1)
    if c<128 then return c end
    if c>=224 then return c-256 end
    if c==192 then return null end
    if c==194 or c==195 then return c==195 end
    if c==204 or c==205 or c==206 then return u(2^(c-204)) end
    if c==208 or c==209 or c==210 then local bytes=2^(c-208); local n=u(bytes); return n>=2^(bytes*8-1) and n-2^(bytes*8) or n end
    if c==207 or c==211 then
      local hi,lo=u(4),u(4); local negative=c==211 and hi>=2147483648
      if negative then hi,lo=U32-1-hi,U32-1-lo; lo=lo+1; if lo==U32 then hi,lo=hi+1,0 end end
      if hi<2097152 then return (negative and -1 or 1)*(hi*U32+lo) end
      return setmetatable({raw=(negative and '-' or '')..decimal(hi,lo)},integer_mt)
    end
    if c==202 or c==203 then
      local hi,lo=u(4),0
      local sign=hi>=2147483648 and -1 or 1; hi=hi%2147483648
      local e,f,bias,unit
      if c==203 then lo=u(4); e=floor(hi/1048576); f=(hi%1048576)*U32+lo; bias,unit=1023,2^52
      else e=floor(hi/8388608); f=hi%8388608; bias,unit=127,2^23 end
      assert(e<(c==203 and 2047 or 255),'nonfinite float')
      local n=e==0 and f/unit*2^(1-bias) or (1+f/unit)*2^(e-bias)
      return float(sign*n)
    end
    local n
    if c>=160 and c<192 then n=c-160
    elseif c==217 or c==218 or c==219 then n=u(2^(c-217)) end
    if n then return take(n) end
    if c==196 or c==197 or c==198 then return binary(take(u(2^(c-196)))) end
    if c>=212 and c<=216 or c>=199 and c<=201 then
      n=c>=212 and 2^(c-212) or u(2^(c-199)); local code=u(1); local bytes=take(n)
      if code==3 then
        local value=M.parse_json(bytes)
        assert(isnumber(value) or getmetatable(value)==integer_mt,'invalid literal number'); return value
      end
      return ext(code,bytes)
    end
    if c>=144 and c<160 then n=c-144 elseif c==220 or c==221 then n=u(c==220 and 2 or 4) end
    if n then
      assert(n<=#data-p+1,'invalid array length'); local out=arr()
      for i=1,n do out[i]=read(depth+1) end; return out
    end
    if c>=128 and c<144 then n=c-128 elseif c==222 or c==223 then n=u(c==222 and 2 or 4) end
    if n then
      assert(n<=floor((#data-p+1)/2),'invalid map length'); local out=obj(); object_orders[out]={}
      for i=1,n do
        local k=read(depth+1); assert(out[k]==nil,'duplicate map key'); out[k]=read(depth+1)
        object_orders[out][i]=k
      end
      return out
    end
    error('unsupported MessagePack tag '..c)
  end
  local out=read(0); assert(p==#data+1,'extra MessagePack input'); return out
end

local alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
local function base64(data)
  local out={}
  for i=1,#data,3 do
    local a,b,c=data:byte(i,i+2); b,c=b or 0,c or 0
    local n=a*65536+b*256+c
    out[#out+1]=alphabet:sub(floor(n/262144)+1,floor(n/262144)+1)
    out[#out+1]=alphabet:sub(floor(n/4096)%64+1,floor(n/4096)%64+1)
    if i+1<=#data then out[#out+1]=alphabet:sub(floor(n/64)%64+1,floor(n/64)%64+1) end
    if i+2<=#data then out[#out+1]=alphabet:sub(n%64+1,n%64+1) end
  end
  return concat(out)
end
local function unbase64(text)
  assert(#text%4~=1 and not text:find('[^%w_-]'),'invalid Base64URL')
  local lookup={}; for i=1,64 do lookup[alphabet:sub(i,i)]=i-1 end
  local out,acc,bits={},0,0
  for i=1,#text do
    local digit=lookup[text:sub(i,i)]; assert(digit,'invalid Base64URL digit')
    acc=acc*64+digit; bits=bits+6
    if bits>=8 then bits=bits-8; out[#out+1]=string.char(floor(acc/2^bits)); acc=acc%2^bits end
  end
  assert(acc==0,'nonzero Base64URL padding'); return concat(out)
end
local function varint(n)
  assert(isint(n) and n>=0,'unsafe varint'); local out={}
  repeat local digit=n%128; n=floor(n/128); out[#out+1]=string.char(digit+(n>0 and 128 or 0)) until n==0
  return concat(out)
end
local function varints(bytes)
  local out,digits={},{}
  for i=1,#bytes do
    local b=bytes:byte(i); digits[#digits+1]=b%128; assert(#digits<=19,'oversized varint')
    if b<128 then
      local n=0
      for j=#digits,1,-1 do
        if type(n)=='number' and n<=(SAFE-digits[j])/128 then n=n*128+digits[j]
        else for k=1,7 do n=add_integer(n,n) end; n=add_integer(n,digits[j]) end
      end
      out[#out+1]=n; digits={}
    end
  end
  assert(#digits==0,'truncated varint'); return out
end
local function zig(n) return n>=0 and n*2 or -n*2-1 end
local function unzig(n) return n%2==0 and n/2 or -(n+1)/2 end
local function shortest(choices)
  local best,size
  for _,v in ipairs(choices) do local n=#M.pack(v); if not size or n<size then best,size=v,n end end
  return best
end
local function sequence(values)
  local n=#values; local choices={arr{0,values}}
  if n==0 then return choices[1] end
  local step=n>1 and values[2]-values[1] or 0; local regular=isint(step)
  if regular then
    local expected=values[1]
    for _,v in ipairs(values) do
      if v~=expected then regular=false; break end
      expected=add_integer(expected,step)
    end
  end
  if regular then choices[#choices+1]=arr{1,n,values[1],step} end
  local deltas,runs={},{}; local safe=true; local last,count
  for i=2,n do
    local d=values[i]-values[i-1]
    if not isint(zig(d)) then safe=false; break end
    deltas[#deltas+1]=varint(zig(d))
    if d==last then count=count+1 else
      if last then runs[#runs+1]=varint(zig(last))..varint(count) end
      last,count=d,1
    end
  end
  if safe then
    if last then runs[#runs+1]=varint(zig(last))..varint(count) end
    choices[#choices+1]=arr{2,values[1],binary(concat(deltas))}
    choices[#choices+1]=arr{3,values[1],binary(concat(runs))}
  end
  local low,high=values[1],values[1]
  for _,v in ipairs(values) do low,high=math.min(low,v),math.max(high,v) end
  if isint(high-low) then
    local width=0; while 2^width<=high-low do width=width+1 end
    local bytes,acc,bits={},0,0
    for _,v in ipairs(values) do
      v=v-low
      for b=width-1,0,-1 do
        acc=acc*2+floor(v/2^b)%2; bits=bits+1
        if bits==8 then bytes[#bytes+1]=string.char(acc); acc,bits=0,0 end
      end
    end
    if bits>0 then bytes[#bytes+1]=string.char(acc*2^(8-bits)) end
    choices[#choices+1]=arr{4,n,low,width,binary(concat(bytes))}
  end
  return shortest(choices)
end
local function unsequence(v)
  local mode=v[1]
  if mode==0 then return copy(v[2]) end
  local out=arr()
  if mode==1 then local n=v[3]; for i=1,v[2] do out[i]=n; n=add_integer(n,v[4]) end; return out end
  if mode==2 or mode==3 then
    out[1]=v[2]; local ints=varints(v[3].data)
    if mode==2 then for _,d in ipairs(ints) do out[#out+1]=add_integer(out[#out],unzig_integer(d)) end
    else
      assert(#ints%2==0,'truncated delta run')
      for i=1,#ints,2 do
        assert(isint(ints[i+1]),'oversized delta-run count')
        for k=1,ints[i+1] do out[#out+1]=add_integer(out[#out],unzig_integer(ints[i])) end
      end
    end
    return out
  end
  assert(mode==4,'unknown integer-sequence mode')
  local n,low,width,data=v[2],v[3],v[4],v[5].data
  assert(width<=128,'unsupported integer width')
  local p,bit=1,7
  for i=1,n do
    local x=0
    for j=1,width do
      assert(p<=#data,'truncated packed sequence')
      local digit=floor(data:byte(p)/2^bit)%2
      if width<=52 then x=x*2+digit else x=add_integer(add_integer(x,x),digit) end
      bit=bit-1
      if bit<0 then p,bit=p+1,7 end
    end
    out[i]=add_integer(low,x)
  end
  return out
end
M.sequence, M.unsequence = sequence, unsequence

local function coordinates(values)
  local choices={arr{0,values}}
  for _,scale in ipairs{1,2,256} do
    local scaled,types,valid=arr(),arr(),true
    for i,v in ipairs(values) do
      local n=num(v)
      if not isint(n*scale) then valid=false; break end
      scaled[i]=n*scale
      types[i]=getmetatable(v)==float_mt and (n==0 and 1/n<0 and 3 or 1) or 0
    end
    if valid then choices[#choices+1]=arr{1,scale,sequence(scaled),sequence(types)} end
  end
  return shortest(choices)
end
local function uncoordinates(v)
  if v[1]==0 then return copy(v[2]) end
  local values,types=unsequence(v[3]),unsequence(v[4]); assert(#values==#types,'coordinate column mismatch')
  for i,n in ipairs(values) do
    n=n/v[2]; if types[i]>=2 then n=-0.0 end
    values[i]=types[i]%2==1 and float(n) or n
  end
  return values
end
local function supported(rows,entity)
  if getmetatable(rows)~=array_mt or #rows==0 then return false end
  for _,r in ipairs(rows) do
    if getmetatable(r)~=object_mt or getmetatable(r.position)~=object_mt then return false end
    if #keys(r.position)~=2 or not isnumber(r.position.x) or not isnumber(r.position.y) then return false end
    if entity and not isint(r.entity_number) then return false end
  end
  return true
end
local function flat_table(rows,entity)
  local palette,lookup,indices,xs,ys,ids=arr(),{},arr(),arr(),arr(),arr()
  for i,row in ipairs(rows) do
    local template=obj()
    for k,v in pairs(row) do if k~='position' and (not entity or k~='entity_number') then template[k]=v end end
    local signature=M.pack(template); local id=lookup[signature]
    if id==nil then id=#palette; lookup[signature]=id; palette[#palette+1]=template end
    indices[i],xs[i],ys[i]=id,row.position.x,row.position.y
    if entity then ids[i]=row.entity_number end
  end
  return arr{palette,sequence(indices),coordinates(xs),coordinates(ys),entity and sequence(ids) or null}
end
local function untable(v)
  local indices,xs,ys=unsequence(v[2]),uncoordinates(v[3]),uncoordinates(v[4])
  local ids=v[5]~=null and unsequence(v[5]) or nil
  assert(#indices==#xs and #xs==#ys and (not ids or #ids==#xs),'table column mismatch')
  local rows=arr()
  for i,id in ipairs(indices) do
    assert(v[1][id+1],'invalid template index')
    local row=copy(v[1][id+1]); row.position=obj{x=xs[i],y=ys[i]}
    if ids then row.entity_number=ids[i] end; rows[i]=row
  end
  return rows
end
local function normalize(rows,entity)
  local out=copy(rows); if not entity then return out end
  local idmap={}; for i,r in ipairs(rows) do idmap[r.entity_number]=i-1 end
  local function refs(v,index)
    local mt=getmetatable(v)
    if mt~=object_mt and mt~=array_mt then return v end
    for k,x in pairs(v) do
      if k=='entity_id' and isint(x) and idmap[x] then v[k]=ext(1,varint(zig(idmap[x]-index)))
      else v[k]=refs(x,index) end
    end
    return v
  end
  for i,r in ipairs(out) do
    if r.connections then r.connections=refs(r.connections,i-1) end
    if getmetatable(r.neighbours)==array_mt then
      for j,n in ipairs(r.neighbours) do if isint(n) and idmap[n] then r.neighbours[j]=ext(1,varint(zig(idmap[n]-(i-1)))) end end
    end
  end
  return out
end
local function unnormalize(rows)
  local ids={}; for i,r in ipairs(rows) do ids[i]=r.entity_number end
  local function visit(v,index)
    local mt=getmetatable(v)
    if mt==ext_mt and v.code==1 then
      local ints=varints(v.data); assert(#ints==1,'invalid entity reference')
      local id=ids[index+unzig(ints[1])]; assert(id~=nil,'entity reference out of range'); return id
    end
    if mt==object_mt or mt==array_mt then for k,x in pairs(v) do v[k]=visit(x,index) end end
    return v
  end
  for i,r in ipairs(rows) do rows[i]=visit(r,i) end
  return rows
end
local function path_get(root,path,skip)
  local node=root
  for i=1,#path-(skip or 0) do local k=path[i]; node=node[type(k)=='number' and k+1 or k]; assert(node~=nil,'invalid payload path') end
  return node
end
local function path_set(root,path,value)
  local node=path_get(root,path,1); local k=path[#path]; node[type(k)=='number' and k+1 or k]=value
end
local function append(path,...)
  local out=copy(path); for _,v in ipairs{...} do out[#out+1]=v end; return out
end

local function expand_dictionary(payload)
  local records,resolved=payload[1],arr()
  local function visit(v)
    local mt=getmetatable(v)
    if mt==ext_mt and v.code==2 then
      local ints=varints(v.data); assert(#ints==1 and ints[1]<#resolved,'invalid dictionary reference')
      return copy(resolved[ints[1]+1])
    end
    if mt==array_mt then local out=arr(); for i,x in ipairs(v) do out[i]=visit(x) end; return out end
    if mt==object_mt then
      local out=obj(); local order={}
      for _,k in ipairs(ordered_keys(v)) do local key=visit(k); out[key]=visit(v[k]); order[#order+1]=key end
      object_orders[out]=order; return out
    end
    return v
  end
  for _,record in ipairs(records) do resolved[#resolved+1]=visit(record) end
  return visit(payload[2])
end
local function restore_block_table(v)
  local mode=v[1]
  if mode==0 then return unnormalize(untable(v[2])) end
  if mode==1 then
    local rows,order=untable(v[2]),unsequence(v[3]); local out=arr()
    assert(#rows==#order,'permutation length mismatch')
    for i,index in ipairs(order) do assert(not out[index+1],'duplicate permutation index'); out[index+1]=rows[i] end
    return unnormalize(out)
  end
  assert(mode==2,'unknown block-table mode')
  local palette,patterns=v[2],v[3]
  local pids,axs,ays,order=unsequence(v[4]),unsequence(v[5]),unsequence(v[6]),unsequence(v[7])
  local ids=v[8]~=null and unsequence(v[8]) or nil
  local tx,ty,scale=unsequence(v[9]),unsequence(v[10]),v[11]
  local out,k=arr(),1
  for j,pid in ipairs(pids) do
    local p=patterns[pid+1]; assert(p,'invalid pattern index')
    local types,dxs,dys=unsequence(p[1]),unsequence(p[2]),unsequence(p[3])
    for s,tid in ipairs(types) do
      local index=order[k]+1; k=k+1; assert(not out[index],'duplicate block permutation index')
      local row=copy(palette[tid+1]); local x,y=add_integer(axs[j],dxs[s])/scale,add_integer(ays[j],dys[s])/scale
      if tx[index]>=2 then x=-0.0 end; if ty[index]>=2 then y=-0.0 end
      row.position=obj{x=tx[index]%2==1 and float(x) or x,y=ty[index]%2==1 and float(y) or y}
      if ids then row.entity_number=ids[index] end; out[index]=row
    end
  end
  assert(k==#order+1,'block row count mismatch'); return unnormalize(out)
end
local function restore(form,payload)
  if form=='i' then return restore(payload[1],expand_dictionary(payload[2])) end
  local root,tables=payload[1],payload[2]
  if form=='s' then
    for _,record in ipairs(tables) do path_set(root,record[1],untable(record[2])) end
    return root
  end
  assert(form:match('^[goarptu]$'),'unknown representation')
  local global=#payload==5
  for _,record in ipairs(tables) do
    local v=record[2]
    if global then
      if v[1]==0 or v[1]==1 then v[2][1]=payload[4]
      else
        v[2]=payload[4]; local patterns=arr()
        for i,pid in ipairs(v[3]) do patterns[i]=payload[5][pid+1] end
        v[3]=patterns
      end
    end
    path_set(root,record[1],restore_block_table(v))
  end
  for _,record in ipairs(payload[3]) do
    local bp=path_get(root,record[1]); local ids={}
    for i,r in ipairs(bp.entities) do ids[i]=r.entity_number end
    local v=record[2]; local a,b,c,d=unsequence(v[1]),unsequence(v[2]),unsequence(v[3]),unsequence(v[4])
    local wires=arr()
    for i,source in ipairs(a) do wires[i]=arr{ids[source+1],b[i],ids[source+c[i]+1],d[i]} end
    bp.wires=wires
  end
  return root
end

local function frame(form,data,codec,options)
  local body
  if codec=='n' then body=base64(data)
  elseif options.codecs and options.codecs[codec] then body=base64(options.codecs[codec].encode(data))
  elseif codec=='d' and helpers and helpers.encode_string then
    body=assert(helpers.encode_string(data),'deflate failed'):gsub('%+','-'):gsub('/','_'):gsub('=+$','')
  else error('compressor unavailable: '..codec) end
  return 'BX0:'..form..codec..body
end
function M.decode(text,options)
  text=text:match('^%s*(.-)%s*$')
  options=options or {}; assert(text:sub(1,4)=='BX0:' and #text>=6,'expected BX0 string')
  local form,codec,body=text:sub(5,5),text:sub(6,6),text:sub(7)
  local data
  if codec=='n' then data=unbase64(body)
  elseif options.codecs and options.codecs[codec] then data=options.codecs[codec].decode(unbase64(body))
  elseif codec=='d' and helpers and helpers.decode_string then
    local standard=body:gsub('%-','+'):gsub('_','/')..string.rep('=',(-#body)%4)
    data=assert(helpers.decode_string(standard),'invalid deflate stream')
  else error('decompressor unavailable: '..codec) end
  if form=='j' then return M.parse_json(data) end
  return restore(form,M.unpack(data))
end
function M.decode_json(text,options) return M.to_json(M.decode(text,options)) end

local function wire_columns(wires,rows)
  if getmetatable(wires)~=array_mt or #wires==0 then return nil end
  local lookup={}; for i,r in ipairs(rows) do lookup[r.entity_number]=i-1 end
  local a,b,c,d=arr(),arr(),arr(),arr()
  for i,w in ipairs(wires) do
    if getmetatable(w)~=array_mt or #w~=4 then return nil end
    for _,n in ipairs(w) do if not isint(n) then return nil end end
    if lookup[w[1]]==nil or lookup[w[3]]==nil then return nil end
    a[i],b[i],c[i],d[i]=lookup[w[1]],w[2],lookup[w[3]]-lookup[w[1]],w[4]
  end
  return arr{sequence(a),sequence(b),sequence(c),sequence(d)}
end
local function cost(payload,options)
  local data=M.pack(payload)
  if options.codec=='n' then return #data end
  return #frame('g',data,options.codec,options)
end
local function block_table(rows,entity,flat,width,height)
  if #rows<16 then return nil end
  local scale
  for _,candidate in ipairs{1,2,256} do
    local valid=true
    for _,r in ipairs(rows) do
      if not isint(num(r.position.x)*candidate) or not isint(num(r.position.y)*candidate) then valid=false; break end
    end
    if valid then scale=candidate; break end
  end
  if not scale then return nil end
  local indices=unsequence(flat[2]); local cells,lookup={},{}
  for i,r in ipairs(rows) do
    local x,y=num(r.position.x)*scale,num(r.position.y)*scale
    local cx,cy=width==0 and 0 or floor(x/(width*scale)),height==0 and 0 or floor(y/(height*scale))
    local key=cx..','..cy; local cell=lookup[key]
    if not cell then cell={x=cx,y=cy,rows={}}; cells[#cells+1]=cell; lookup[key]=cell end
    cell.rows[#cell.rows+1]={id=indices[i],x=x,y=y,index=i-1}
  end
  table.sort(cells,function(a,b) return a.y==b.y and a.x<b.x or a.y<b.y end)
  local patterns,pattern_lookup,pids,axs,ays,order=arr(),{},arr(),arr(),arr(),arr()
  for i,cell in ipairs(cells) do
    local ax,ay=cell.rows[1].x,cell.rows[1].y
    for _,r in ipairs(cell.rows) do ax,ay=math.min(ax,r.x),math.min(ay,r.y) end
    table.sort(cell.rows,function(a,b)
      if a.y~=b.y then return a.y<b.y end
      if a.x~=b.x then return a.x<b.x end
      if a.id~=b.id then return a.id<b.id end
      return a.index<b.index
    end)
    local ids,dxs,dys=arr(),arr(),arr()
    for j,r in ipairs(cell.rows) do ids[j],dxs[j],dys[j]=r.id,r.x-ax,r.y-ay; order[#order+1]=r.index end
    local pattern=arr{sequence(ids),sequence(dxs),sequence(dys)}; local signature=M.pack(pattern)
    local pid=pattern_lookup[signature]
    if pid==nil then pid=#patterns; pattern_lookup[signature]=pid; patterns[#patterns+1]=pattern end
    pids[i],axs[i],ays[i]=pid,ax,ay
  end
  local ids,tx,ty=arr(),arr(),arr()
  for i,r in ipairs(rows) do
    if entity then ids[i]=r.entity_number end
    for axis,types in pairs{x=tx,y=ty} do
      local v=r.position[axis]; local n=num(v)
      types[i]=getmetatable(v)==float_mt and (n==0 and 1/n<0 and 3 or 1) or 0
    end
  end
  return arr{2,flat[1],patterns,sequence(pids),sequence(axs),sequence(ays),sequence(order),
             entity and sequence(ids) or null,sequence(tx),sequence(ty),scale}
end
local function build_forms(value,options)
  local root=copy(value); local tables={g=arr(),o=arr(),a=arr(),r=arr()}; local wires=arr()
  local function walk(node,path)
    if getmetatable(node)~=object_mt then return end
    local bp=node.blueprint
    if getmetatable(bp)==object_mt then
      for _,field in ipairs{'entities','tiles'} do
        local entity=field=='entities'; local rows=bp[field]
        if supported(rows,entity) then
          local normalized=normalize(rows,entity); local flat=flat_table(normalized,entity)
          local g=arr{0,flat}; local order={}
          for i=1,#rows do order[i]=i end
          table.sort(order,function(a,b)
            local x,y=normalized[a].position,normalized[b].position
            if num(x.y)~=num(y.y) then return num(x.y)<num(y.y) end
            if num(x.x)~=num(y.x) then return num(x.x)<num(y.x) end
            return a<b
          end)
          local sorted,permutation=arr(),arr()
          for i,index in ipairs(order) do sorted[i],permutation[i]=normalized[index],index-1 end
          local o=arr{1,flat_table(sorted,entity),sequence(permutation)}
          local a=cost(g,options)<=cost(o,options) and g or o
          local r,best=a,cost(a,options)
          if options.blocks then
            for _,dimension in ipairs{{4,4},{8,8},{16,16},{0,3},{0,4},{0,8},{3,0},{4,0},{8,0}} do
              local candidate=block_table(normalized,entity,flat,dimension[1],dimension[2])
              if candidate then local size=cost(candidate,options); if size<best then r,best=candidate,size end end
            end
          end
          local target=append(path,'blueprint',field)
          for mode,payload in pairs{g=g,o=o,a=a,r=r} do tables[mode][#tables[mode]+1]=arr{target,payload} end
          if entity then
            local encoded=wire_columns(bp.wires,rows)
            if encoded then wires[#wires+1]=arr{append(path,'blueprint'),encoded}; bp.wires=null end
          end
          bp[field]=null
        end
      end
    end
    local book=node.blueprint_book
    if getmetatable(book)==object_mt and getmetatable(book.blueprints)==array_mt then
      for i,child in ipairs(book.blueprints) do walk(child,append(path,'blueprint_book','blueprints',i-1)) end
    end
  end
  walk(root,arr())
  local forms={g=arr{root,tables.g,wires},o=arr{root,tables.o,wires},a=arr{root,tables.a,wires}}
  if options.blocks then forms.r=arr{root,tables.r,wires} end
  local palette,palette_lookup,shared=arr(),{},copy(tables.a)
  for _,record in ipairs(shared) do
    local flat=record[2][2]; local remap={}
    for i,template in ipairs(flat[1]) do
      local signature=M.pack(template); local id=palette_lookup[signature]
      if id==nil then id=#palette; palette_lookup[signature]=id; palette[#palette+1]=template end
      remap[i]=id
    end
    local indices=unsequence(flat[2]); for i,id in ipairs(indices) do indices[i]=remap[id+1] end
    flat[1],flat[2]=null,sequence(indices)
  end
  forms.p=arr{root,shared,wires,palette,arr()}
  return forms
end
local function intern_strings(value)
  local counts={}
  local function scan(v)
    if type(v)=='string' and #v>=4 then counts[v]=(counts[v] or 0)+1 end
    local mt=getmetatable(v)
    if mt==array_mt then for _,x in ipairs(v) do scan(x) end
    elseif mt==object_mt then for k,x in pairs(v) do scan(k); scan(x) end end
  end
  scan(value)
  local selected={}
  for s,n in pairs(counts) do if (n-1)*#M.pack(s)>n*4+2 then selected[s]=true end end
  local records,index=arr(),{}
  local function emit(v)
    if type(v)=='string' and selected[v] then
      local id=index[v]
      if id==nil then id=#records; index[v]=id; records[#records+1]=v end
      return ext(2,varint(id))
    end
    local mt=getmetatable(v)
    if mt==array_mt then local out=arr(); for i,x in ipairs(v) do out[i]=emit(x) end; return out end
    if mt==object_mt then
      local out=obj(); local order={}
      for _,k in ipairs(ordered_keys(v)) do local key=emit(k); out[key]=emit(v[k]); order[#order+1]=key end
      object_orders[out]=order; return out
    end
    return v
  end
  local root=emit(value); return arr{records,root}
end
function M.encode(value,options)
  options=options or {}; local settings={}
  for k,v in pairs(options) do settings[k]=v end
  settings.codec=settings.codec or (helpers and 'd' or 'n')
  settings.blocks=settings.blocks~=false
  local best=frame('j',M.to_json(value),settings.codec,settings)
  local raw=frame('j',M.to_json(value),'n',settings)
  if #raw<#best then best=raw end
  local function candidate(form,payload)
    local bytes=M.pack(payload)
    local text=frame(form,bytes,settings.codec,settings)
    if #text<#best then best=text end
    if settings.codec~='n' then
      text=frame(form,bytes,'n',settings); if #text<#best then best=text end
    end
  end
  local forms=build_forms(value,settings)
  for _,form in ipairs{'g','o','a','p','r'} do
    if forms[form] then
      candidate(form,forms[form])
      if settings.dictionary~=false then candidate('i',arr{form,intern_strings(forms[form])}) end
    end
  end
  return best
end
function M.encode_json(text,options) return M.encode(M.parse_json(text),options) end
local function native_compress(text,options)
  if options and options.codecs and options.codecs.d then
    local result=base64(options.codecs.d.encode(text)):gsub('%-','+'):gsub('_','/')
    return result..string.rep('=',(-#result)%4)
  end
  assert(helpers and helpers.encode_string,'native compression requires Factorio helpers or a deflate callback')
  return assert(helpers.encode_string(text),'native compression failed')
end
local function native_decompress(text,options)
  if options and options.codecs and options.codecs.d then
    local data=unbase64(text:gsub('%+','-'):gsub('/','_'):gsub('=+$',''))
    return options.codecs.d.decode(data)
  end
  assert(helpers and helpers.decode_string,'native decompression requires Factorio helpers or a deflate callback')
  return assert(helpers.decode_string(text),'invalid native blueprint string')
end
function M.encode_native(text,options)
  text=text:match('^%s*(.-)%s*$')
  if text:sub(1,1)=='0' then text=native_decompress(text:sub(2),options) end
  return M.encode_json(text,options)
end
function M.decode_native(text,options)
  return '0'..native_compress(M.decode_json(text,options),options)
end
return M
