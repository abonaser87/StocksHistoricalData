# import numpy as np
import os,sys,re
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
dir = r"""D:\SEC-OneDrive\OneDrive - ITC - Saudi Electicity Company\Studies\Nimar Grants\\"""
os.chdir(dir)
os.chdir('Nimar')
year = '2023'
fault = 'Fault @ 8061 - 8317-8061 Outage'
outFolder='Figuers/'
skipSVC = True
with PdfPages(outFolder+year+fault+'.pdf') as pdf:
    ######################
    # PLOT VOLTAGES      #
    ######################

    # infile=open('Channels/voltages.txt')
    # var = []
    # for lines in infile:      # go through the input file, one line at a time
    #     lines = lines.split(None,0)
    #     for line in lines:
    #         if line.startswith('Time(s)'):
    #             names=line.split('Time(s)')[1].split('VOLT')
    #         elif re.match('^\d\.\d',line) or line.startswith('0 ') :
    #             var.append(line.split())
    #         else:
    #             continue
    #
    # outfile=open('Channels/voltages.csv','w')
    # i = 1
    # for name in names:
    #     if i == len(names):
    #         outfile.write(name[:-4].strip())
    #         continue
    #     if name==' ':
    #         outfile.write('Time,')
    #         i=i+1
    #         continue
    #     outfile.write(name[:-4].strip()+',')
    #     i=i+1
    # for time in var:
    #     outfile.write('\n')
    #     i = 1
    #     for k in time:
    #         if i == len(time):
    #             outfile.write(str(k))
    #             continue
    #         outfile.write(str(k)+',')
    #         i = i + 1
    data = pd.read_excel('Channels/voltages.xlsx',header=3,index_col=0)
    data.rename(columns=lambda x: x.split('VOLT')[1][:7].strip(), inplace=True)
    # data = pd.read_csv('Channels/voltages.csv',index_col='Time')

    fig_size = plt.rcParams["figure.figsize"]
     # Set figure width to 12 and height to 9
    fig_size[0] = 11.69
    fig_size[1] = 8.27
    plt.rcParams["figure.figsize"] = fig_size
    data.plot()
    plt.xlabel('Time (sec)')
    plt.ylabel('Voltage (pu)')
    plt.legend(loc='lower right')
    plt.xlim([0,5])
    plt.suptitle(year+' Voltages ,'+fault)
    plt.savefig(outFolder+year+' Voltages , '+fault+'.png')
    pdf.savefig()

    plt.close()

    ######################
    # PLOT SPEEDS        #
    ######################
    # infile=open('Channels/speeds.txt')
    # var = []
    # for lines in infile:      # go through the input file, one line at a time
    #     lines = lines.split(None,0)
    #     for line in lines:
    #         if line.startswith('Time(s)'):
    #             names=line.split('Time(s)')[1].split('LV')
    #
    #         elif re.match('^\d\.\d',line)or line.startswith('0 ') :
    #             var.append(line.split())
    #         else:
    #             continue
    #
    # outfile=open('Channels/speeds.csv','w')
    #
    # i = 1
    # for name in names:
    #     if i == len(names)-1:
    #         outfile.write(name[:-5].strip())
    #         continue
    #     if name==' ':
    #         outfile.write('Time,')
    #         i=i+1
    #         continue
    #     if i==1 and name!=' ':
    #         outfile.write('Time,')
    #     if name=='\n':
    #         i=i+1
    #         continue
    #     outfile.write(name[:-5].strip()+',')
    #     i=i+1
    # for time in var:
    #     outfile.write('\n')
    #     i = 1
    #     for k in time:
    #         if i == len(time):
    #             outfile.write(str(k))
    #             continue
    #         outfile.write(str(k)+',')
    #         i = i + 1
    #
    # data = pd.read_csv('Channels/speeds.csv',index_col='Time')
    data = pd.read_excel('Channels/speeds.xlsx',header=3,index_col=0)
    data.rename(columns=lambda x: x[:6].strip(), inplace=True)
    data.plot()
    plt.xlabel('Time (sec)')
    plt.ylabel('Speed')
    plt.legend(loc='lower right')
    plt.xlim([0,5])
    plt.suptitle(year +' MotorSpeed , '+ fault)
    plt.savefig(outFolder + year + ' MotorSpeed , ' + fault + '.png')
    pdf.savefig()
    plt.close()

    # ######################
    # # PLOT SVC        #
    # ######################
    # infile=open('Channels/svc.txt')
    # var = []
    # for lines in infile:      # go through the input file, one line at a time
    #     lines = lines.split(None,0)
    #     for line in lines:
    #         if line.startswith('Time(s)'):
    #             names=line.split('Time(s)')
    #             names = names[1].split('SVC')[0][:-6]
    #         elif re.match('^\d\.\d',line)or line.startswith('0 ') :
    #             var.append(line.split())
    #         else:
    #             continue
    # outfile=open('Channels/svc.csv','w')
    # i = 1
    # for name in names:
    #     if i == len(names):
    #         outfile.write(name[:-4].strip())
    #         continue
    #     if name==' ':
    #         outfile.write('Time,')
    #         i=i+1
    #         continue
    #     outfile.write(name[:-4].strip()+',')
    #     i=i+1
    # for time in var:
    #     outfile.write('\n')
    #     i = 1
    #     for k in time:
    #         if i == len(time):
    #             outfile.write(str(k))
    #             continue
    #         outfile.write(str(k)+',')
    #         i = i + 1
    if not skipSVC:
        data = pd.read_excel('Channels/svc.xlsx',header=3,index_col=0)
        # data.rename(columns=lambda x: x[:6].strip(), inplace=True)
        # df = pd.read_csv('Channels/svc.csv',index_col='Time')
        data.plot()

        plt.xlabel('Time (sec)')
        plt.ylabel('SVC Output')
        plt.legend(loc='lower right')
        plt.xlim([0,5])
        plt.suptitle(year +' SVC Output , '+ fault)
        plt.savefig(outFolder + year + ' SVC Output , ' + fault + '.png')
        pdf.savefig()
        plt.close()