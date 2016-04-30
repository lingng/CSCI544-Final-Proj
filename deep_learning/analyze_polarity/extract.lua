--[[ Tester for Crepe
By Xiang Zhang @ New York University
--]]

require("sys")

local Extract = torch.class("Extract")

-- Initialization of the testing script
-- data: Testing dataset
-- model: Testing model
-- config: (optional) the configuration table
function Extract:__init(data,model,layer)
   

   -- Store the objects
   self.data = data
   self.model = model
   self.layer = layer
   --self.loss = loss

   -- Move the type
   --self.loss:type(model:type())

   -- Create time table
   self.time = {}


end

-- Execute testing for a batch step
function Extract:run()
   -- Initializing the errors and losses
   
   self.output = {}
   self.output[1]= torch.CudaTensor()
   self.output[2] = torch.CudaTensor()
   -- Start the loop
   self.clock = sys.clock()
   for batch,idx,labels,n in self.data:iterator() do
      self.batch = self.batch or batch:transpose(2,3):contiguous():type(self.model:type())
      self.labels = self.labels or labels:type(self.model:type())
      self.batch:copy(batch:transpose(2, 3):contiguous())
      self.labels:copy(labels)
      -- Record time
      if self.model:type() == "torch.CudaTensor" then cutorch.synchronize() end
      self.time.data = sys.clock() - self.clock

      self.clock = sys.clock()
      -- Forward propagation
      --print(self.output:size())
      --print(self.model:forward(self.batch):size())
      self.model:forward(self.batch)
      if self.output[1]:numel()==0 then
         self.output[1] = self.model:extract(self.layer)
         self.output[2]= self.labels
      else
         self.output[1] = torch.cat(self.output[1],self.model:extract(self.layer),1)
         self.output[2] = torch.cat(self.output[2],self.labels)
      end
      -- Record time
      if self.model:type() == "torch.CudaTensor" then cutorch.synchronize() end
      self.time.forward = sys.clock() - self.clock

      self.clock = sys.clock()      
     
      
   end
   return self.output
end
