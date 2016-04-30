require("cutorch")
require("cunn")
ffi = require("ffi")
function parse_data(data)
	local i=1
	local j=0
     if data.index[i] == nil then return end

      local inputs = {}
      local labels = {}--torch.Tensor(samples)

      local n = 0
      --local k=1
      while true do
	 j = j + 1
	 if j > data.index[i]:size(1) then
	    i = i + 1
	    if data.index[i] == nil then
	       break
	    end
	    j = 1
	 end
	 n = n + 1
	 local s = ffi.string(torch.data(data.content:narrow(1, data.index[i][j][data.index[i][j]:size(1)], 1)))
	 for l = data.index[i][j]:size(1) - 1, 1, -1 do
	    s = s.." "..ffi.string(torch.data(data.content:narrow(1, data.index[i][j][l], 1)))
	 end
	 inputs[n] = s:lower()
	 labels[n] = i
	 
      end

      return inputs, labels,n
end