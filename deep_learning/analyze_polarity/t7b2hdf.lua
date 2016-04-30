require("nn")
require("cutorch")
require("cunn")
require("gnuplot")

-- Local requires
require("data")
require("model")
require("extract")
require 'hdf5'
local cmd = torch.CmdLine()

-- Options
cmd:option("-input","","input filename")
cmd:option("-output","","output filename")
cmd:text()
   
-- Parse the option
local opt = cmd:parse(arg or {})
if opt.input=="" then
	error("input filename is not provided")
end
if opt.output=="" then
	error("output filename is not provided")
end
in_path = opt.input
out_path = opt.output
data = torch.load(in_path)
-- print(data)

--feats = torch.totable(data['features']:float())
--labels = torch.totable(data['labels'])
-- print(feats)
--string = json.encode({scores=feats})
-- print(string)
file = hdf5.open(out_path,'w')
file:write('features', data['features']:float())
file:write('labels', data['labels']:int())
file:close()
collectgarbage()
