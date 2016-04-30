m = require 'manifold'
gfx = require("gfx.js")
require("nn")
require("cutorch")
require("cunn")
ffi = require("ffi")
require("parse_data")
function main()
--layer_id =21
--print(table.getn(arg))
if table.getn(arg) < 2 then
	error('The input format should be:\n visualize.lua DATAFILE FEATURE_FILE')
end
print(arg[1])
print(arg[2])
obj = torch.load(arg[2])
source  = torch.load(arg[1])


inputs,labels,n = parse_data(source)
sp = n

--print(source)
--print(source.)
--text = source[{:,2}]
--rating = source[{}]
--sp=source:size(1)
cls_n=2
f = obj.features:double()
print(f:size())
f = f[{{1,sp},{}}]

if f:dim()>2 then
	f=f:reshape(sp,f:size(2)*f:size(3))
end
l = obj.labels:double()
print(l:size())
l = l[{{1,sp}}]
print(f:size())
print(l[1])
print(labels[1])

-- check consistency

local i
for i=1,sp do
	if l[i]~=labels[i] then
		error('labels are not match at '..i)

		break
	end
end
print(inputs[1])
--os.exit()
p = m.embedding.tsne(f,{dim=2, perplexity=20})

class_points={}
for i=1,cls_n do
	class_points[i] = {}
	class_points[i].values = {}
	
end
class_points[1].key = 'Negative reviews'
class_points[2].key = 'Positive reviews'
for i=1,sp do
	table.insert(class_points[l[i]].values,
     {
         x = p[i][1],
         y = p[i][2],
         size = 2,
         tag = inputs[i]
	})
end
local config = {
	chart='scatter',
	width = 700,
	height = 700
}
gfx.chart(class_points,config)

end

main()