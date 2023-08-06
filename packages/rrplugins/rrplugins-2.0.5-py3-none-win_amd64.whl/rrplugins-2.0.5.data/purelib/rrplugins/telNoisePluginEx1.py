import roadrunner
import rrplugins as tel

# Create a roadrunner instance and create some data
rr = roadrunner.RoadRunner()
rr.load("sbml_test_0001.xml")    
data = rr.simulate(0, 10, 511) # Want 512 points

#Add noise to the data
noisePlugin = tel.Plugin ("tel_add_noise")

# Get the dataseries from data returned by roadrunner
d = tel.getDataSeries (data)

# Assign the dataseries to the plugin inputdata
noisePlugin.InputData = d

# Tell it that the first column is time, since the labels get stripped.
noisePlugin.AssumeTime = True

# Set parameter for the 'size' of the noise
noisePlugin.Sigma = 3.e-6

# Add the noise
noisePlugin.execute()

# Get the data to plot
noisePlugin.InputData.plot()
