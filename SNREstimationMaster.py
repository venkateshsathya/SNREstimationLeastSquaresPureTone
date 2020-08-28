# we first call the function to collect data via USRP.
# We then call the python file to parse the IQsamples collected to estimte SNR

import os
import time
import sys
IQsamplesfilename = sys.argv[1]
filelocation = "/home/gelu/Desktop/IQSamples/SNREstimate/" 
commandto_collectdata = "sshpass -v -p \'123456789\' sudo python2 CollectDataEstimateSNR.py  " + IQsamplesfilename
snrestimatefilename = "SNREstimationLeastSquaresFromTone.py"
commandto_estimateSNR = 'sshpass -v -p \'123456789\' sudo python ' + snrestimatefilename + ' ' + filelocation + IQsamplesfilename

os.system(commandto_collectdata)
os.system(commandto_estimateSNR)
