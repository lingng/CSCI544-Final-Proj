--[[
Main Driver for Crepe
By Xiang Zhang @ New York University
]]

-- Necessary functionalities
require("nn")
require("cutorch")
require("cunn")
require("gnuplot")

-- Local requires
require("data")
require("model")
require("extract")
--json=require("json")
-- Configurations
dofile("config.lua")

-- Prepare random number generator
math.randomseed(os.time())
torch.manualSeed(os.time())

-- Create namespaces
main = {}

-- The main program
function main.main()
   -- Setting the device
   if config.main.device then
      cutorch.setDevice(config.main.device)
      print("Device set to "..config.main.device)
   end

   main.clock = {}
   main.clock.log = 0

   main.argparse()
   main.new()
   main.run()
end

-- Parse arguments
function main.argparse()
   local cmd = torch.CmdLine()

   -- Options
   cmd:option("-resume",0,"Resumption point in epoch. 0 means not resumption.")
   cmd:option("-layer_id",0,"To extract features in layer[layer_id]")
   cmd:option("-savename","","File name to be saved")
   cmd:text()
   
   -- Parse the option
   local opt = cmd:parse(arg or {})
   
   main.layer_id=opt.layer_id
   if opt.savename=="" then
     main.savename = "extracted_layer_"..tostring(main.layer_id)..".t7b"
   else
     main.savename= opt.savename
   end   
-- Resumption operation
   if opt.resume > 0 then
      -- Find the main resumption file
      local files = main.findFiles(paths.concat(config.main.save,"main_"..tostring(opt.resume).."_*.t7b"))
      if #files ~= 1 then
	 error("Found "..tostring(#files).." main resumption point.")
      end
      config.main.resume = files[1]
      print("Using main resumption point "..config.main.resume)
      -- Find the model resumption file
      local files = main.findFiles(paths.concat(config.main.save,"sequential_"..tostring(opt.resume).."_*.t7b"))
      if #files ~= 1 then
	 error("Found "..tostring(#files).." model resumption point.")
      end
      config.model.file = files[1]
      print("Using model resumption point "..config.model.file)
      -- Resume the training epoch
      config.train.epoch = tonumber(opt.resume) + 1
      print("Next training epoch resumed to "..config.train.epoch)
      -- Don't do randomize
      if config.main.randomize then
	 config.main.randomize = nil
	 print("Disabled randomization for resumption")
      end
   end

   return opt
end

-- Train a new experiment
function main.new()
   -- Load the data
   print("Loading datasets...")
   --main.train_data = Data(config.train_data)
   main.val_data = Data(config.val_data)

   -- Load the model
   print("Loading the model...")
   -- only get first layer_id layers of the model
   print(main.layer_id)
   -- if main.layer_id > 0 then
   --    model_deduced =config.model
   --    for i=1,main.layer_id do
   --       model_deduced[i] = config.model[i]
   --    end
   --    config.model = model_deduced
   -- end
   main.model = Model(config.model)

   if config.main.randomize then
      main.model:randomize(config.main.randomize)
      print("Model randomized.")
   end
   main.model:type(config.main.type)
   print("Current model type: "..main.model:type())
   collectgarbage()
   
 

   -- Initiate the tester
   print("Loading the tester...")
   
   main.extract = Extract(main.val_data, main.model,main.layer_id)

   -- The record structure
   main.record = {}
   if config.main.resume then
      print("Loading main record...")
      local resume = torch.load(config.main.resume)
      main.record = resume.record
      
      --main.show()
   end

   -- The visualization
   --main.mui = Mui{width=config.mui.width,scale=config.mui.scale,n=config.mui.n,title="Model Visualization"}
   --main.draw()
   collectgarbage()
end

-- Start the training
function main.run()
   --Run for this number of era
    
	   main.output = main.extract:run()
      
      
      
      
      print("Saving data")
      main.save()
      collectgarbage()
   
end

-- Final cleaning up
function main.clean()
   print("Cleaning up...")
   gnuplot.closeall()
end


-- Save a record
function main.save()
   -- Record necessary configurations
   --config.train.epoch = main.train.epoch

   -- Make the save
   local time = os.time()
   torch.save(paths.concat(config.main.save, main.savename),
   {features = main.output[1], labels = main.output[2]});   
   collectgarbage()
end

-- Utility function: find files with the specific 'ls' pattern
function main.findFiles(pattern)
   require("sys")
   local cmd = "ls "..pattern
   local str = sys.execute(cmd)
   local files = {}
   for file in str:gmatch("[^\n]+") do
      files[#files+1] = file
   end
   return files
end

-- Execute the main program
main.main()
