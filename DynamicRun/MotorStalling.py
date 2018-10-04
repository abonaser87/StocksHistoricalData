# import numpy as np
import os,sys,re
import pandas as pd
import matplotlib.pyplot as plt
target_folder=os.path.dirname(sys.argv[0])  # script directory
os.chdir(target_folder)

data = pd.read_csv('Channels/AllSpeeds.csv',index_col='Time')
check = data.iloc[0]-data.iloc[-1]
check = check.loc[check>0.01]
print check
check = check.index.tolist()
outfile = open('Channels/stalling.txt','w')
for i in check:
	outfile.write(str(i)+' ')
outfile.close()
