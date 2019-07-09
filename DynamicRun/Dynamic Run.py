import os, sys
import re
import pandas as pd
import matplotlib.pyplot as plt

def convert():
    psspy.cong(0)
    psspy.conl(0, 1, 1, [0, 0], [100.0, 0.0, 0.0, 100.0])
    psspy.conl(0, 1, 2, [0, 0], [100.0, 0.0, 0.0, 100.0])
    psspy.conl(0, 1, 3, [0, 0], [100.0, 0.0, 0.0, 100.0])
    psspy.ordr(0)
    psspy.fact()
    psspy.tysl(0)


def dataextract(zone):
    target_folder = os.path.dirname(sys.argv[0])  # script directory
    os.chdir(target_folder)
    out = open('varchannels.py', 'w')
    out.write('import psspy\n')
    psspy.lines_per_page_one_device(1, 10000000)
    psspy.report_output(2, 'Logs/models.log', [0, 0])
    psspy.bsys(0, 0, [0.0, 380.], 0, [], 0, [], 0, [], len(zone), zone)
    psspy.ldlist(0, 0, [1, 1])
    infile = open('Logs/models.log')
    for lines in infile:  # go through the input file, one line at a time
        lines = lines.split(None, 0)
        for line in lines:
            varNum = []
            varName = []
            if line.startswith('1'):
                varNum = line.split('CIM5BL')  # Create a list of all the columns except the first 10 and the last 2.
                varNum = varNum[1].split()
                if re.search(r'(33.000|13.800|132.00|380.00)', line):
                    varName = re.split(r'(33.000|13.800|132.00|380.00)', line)  # Get the name
                    varName = varName[0].strip()  # Get the name
                else:
                    varName = line.split()[:2]
                    varName = varName[0] + " " + varName[1]
                var = varNum[5]
                test = int(var[:-1]) + 3
                channel = """psspy.var_channel([-1,""" + str(test) + """], '""" + varName + """ SPEED')""" + "\n"
                out.write(channel)
    out.close()
    psspy.close_report()


def svcChannels(zone):
    target_folder = os.path.dirname(sys.argv[0])  # script directory
    os.chdir(target_folder)
    out = open('varchannels.py', 'a')
    psspy.lines_per_page_one_device(1, 10000000)
    psspy.report_output(2, 'Logs/svcModels.log', [0, 0])
    psspy.bsys(0, 0, [0.0, 380.], 0, [], 0, [], 0, [], len(zone), zone)
    psspy.mlst(0, 0, [1, 1, 2])
    infile = open('Logs/svcModels.log')
    for lines in infile:  # go through the input file, one line at a time
        lines = lines.split(None, 0)
        for line in lines:
            varNum = []
            varName = []
            if 'CSVGN1' in line:
                varNum = line.split(
                    'CSVGN1')  # Create a list of all the columns except the first 10 and the last 2.
                varNum = varNum[1].split()
                if re.search(r'(33.000|13.800|132.00|380.00)', line):
                    varName = re.split(r'(33.000|13.800|132.00|380.00)', line)  # Get the name
                    varName = varName[0].strip()  # Get the name
                else:
                    varName = line.split()[:2]
                    varName = varName[0] + " " + varName[1]
                var = varNum[5]
                channel = """psspy.var_channel([-1,""" + var + """], '""" + varName + """ SVC')""" + "\n"
                out.write(channel)
    out.close()
    psspy.close_report()

def statcomChannels(zone):
    target_folder = os.path.dirname(sys.argv[0])  # script directory
    os.chdir(target_folder)
    out = open('varchannels.py', 'a')
    psspy.lines_per_page_one_device(1, 10000000)
    psspy.report_output(2, 'Logs/statcomModels.log', [0, 0])
    psspy.bsys(0, 0, [0.0, 380.], 0, [], 0, [], 0, [], len(zone), zone)
    psspy.fclist(0, 0, 0)
    infile = open('Logs/statcomModels.log')
    for lines in infile:  # go through the input file, one line at a time
        lines = lines.split(None, 0)
        for line in lines:
            varNum = []
            varName = []
            if 'SVSMO3U2' in line:
                varNum = line.split(
                    'SVSMO3U2')  # Create a list of all the columns except the first 10 and the last 2.
                varNum = varNum[1].split()
                if re.search(r'(33.000|13.800|132.00|380.00)', line):
                    varName = re.split(r'(33.000|13.800|132.00|380.00)', line)  # Get the name
                    varName = varName[0].strip()  # Get the name
                else:
                    varName = line.split()[:2]
                    varName = varName[0] + " " + varName[1]
                var = varNum[5]
                channel = """psspy.var_channel([-1,""" + var + """], '""" + varName + """ STCM I')""" + "\n"
                out.write(channel)
                var = int(varNum[5])+2
                channel = """psspy.var_channel([-1,""" + str(var) + """], '""" + varName + """ STCM VAR')""" + "\n"
                out.write(channel)
    out.close()
    psspy.close_report()

def solve(savfile, fault, zone, outfile,dyrefile):
    psspy.case(savfile)
    convert()
    psspy.lines_per_page_one_device(1, 10000000)
    psspy.progress_output(2, 'Logs/'+outfile[6:-3]+'.log', [0, 0])
    psspy.addmodellibrary(r"""D:\SEC-OneDrive\OneDrive - ITC - Saudi Electicity Company\Studies\2023 Reinforcment\dsusr.dll""")
    psspy.dyre_new([1, 1, 1, 1], dyrefile, "", "", "")
    psspy.dynamics_solution_param_2(intgar1=200, realar1=0.4, realar3=0.0008333, realar4=0.0033333)
    psspy.set_relang(1, 0, "")
    psspy.bsys(1, 0, [0.0, 380.], 0, [], 0, [], 0, [], len(zone), zone)
    psspy.chsb(1, 0, [-1, -1, -1, 1, 13, 0])
    dataextract(zone)
    svcChannels(zone)
    statcomChannels(zone)
    import varchannels
    # psspy.bus_frequency_channel([178, 19039], r"""Freq""")
    # psspy.chsb(0, 0, [-1, -1, -1, 1, 1, 0])
    psspy.strt(0, outfile)
    psspy.run(0, 0.1, 600, 0, 51)
    psspy.dist_scmu_fault([0, 0, 1, fault], [0.0, 0.0, 0.0, 0.0])
    psspy.run(0, 0.21667, 600, 0, 11)
    psspy.dist_clear_fault(1)
    # psspy.dist_3wind_trip(fault,19030,193301,r"""1""")
    psspy.dist_branch_trip(fault, 18914, r"""1""")
    # psspy.dist_machine_trip(177691,r"""5""")
    psspy.set_osscan(1, 0)
    psspy.set_vltscn(1, 1.15, 0.8)
    psspy.run(0, 1.0, 600, 0, 31)
    psspy.run(0, 5.0, 600, 0, 51)
    psspy.close_report()


def checkmotorstalled(channels,outfile):
    inname = 'Logs/'+outfile[6:-3]+'log'
    infile = open(inname)
    chNum = []
    # Get all speed channel numbers
    for line in infile:
        if re.match('^CHANNEL  \d', line) and 'SPEED' in line:
            chNum.append(int(line.split()[1]))
    channels.txtout(channels=chNum, txtfile='Channels/AllSpeeds.txt')
    infile = open('Channels/AllSpeeds.txt')
    # Prepare the data of all speeds to be checked to a dataframe
    outfile = open('Channels/AllSpeeds.csv', 'w')
    outfile.write('Time,')
    i = 1
    for Num in chNum:
        if i == len(chNum):
            outfile.write(str(Num))
            continue
        outfile.write(str(Num) + ',')
        i = i + 1
    outfile.write("\n")

    for lines in infile:  # go through the input file, one line at a time
        lines = lines.split(None, 0)
        for line in lines:
            if re.match('^\d\.\d', line) or line.startswith('0 '):
                data = line.split()
                i = 1
                for t in data:
                    if i == len(data):
                        outfile.write(str(t))
                        continue
                    outfile.write(str(t) + ',')
                    i = i + 1
                outfile.write("\n")


def getStalled():
    data = pd.read_csv('Channels/AllSpeeds.csv',index_col='Time')
    check = data.iloc[0]-data.iloc[-1]
    check = check.loc[check>0.01]
    print check
    check = check.index.tolist()
    outfile = open('Channels/stalling.txt','w')
    for i in check:
        outfile.write(str(i)+' ')
    outfile.close()
    infile = open('Channels/stalling.txt')
    for lines in infile:
        lines = lines.split()
    chNum=[]
    for i in lines:
        chNum.append(int(i))
    return chNum

'''
Get a list of keys from dictionary which has value that matches with any value in given list of values
'''
def getKeysByValues(dictOfElements, listOfValues):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        try:
            if re.search('|'.join(listOfValues),item[1]):
                listOfKeys.append(item[0])
        except:
            continue
    return  listOfKeys


pssedir = 'C:\Program Files (x86)\PTI\PSSE33'
pssedir = str(pssedir)  # convert unicode to str

# =============================================================================================
# Files Used

pssbindir = os.path.join(pssedir, 'PSSBIN')
exampledir = os.path.join(pssedir, 'EXAMPLE')
# =============================================================================================
# Check if running from Python Interpreter
exename = sys.executable
p, nx = os.path.split(exename)
nx = nx.lower()
if nx in ['python.exe', 'pythonw.exe']:
    os.environ['PATH'] = pssbindir + ';' + os.environ['PATH']
    sys.path.insert(0, pssbindir)
import redirect

redirect.psse2py()
import psspy

ierr = psspy.psseinit(buses=150000)

import dyntools

target_folder = os.path.dirname(sys.argv[0])  # script directory
os.chdir(target_folder)
try:
    os.makedirs('Output')
    os.makedirs('Channels')
    os.makedirs('Logs')
    os.makedirs('Figuers')
except OSError:
    print'Error creating directory'
    pass

dir = r'D:\SEC-OneDrive\OneDrive - ITC - Saudi Electicity Company\Studies\2023 Reinforcment\\'
outfile = 'Output/Hail-9030-8914Outage2023-Statcom.out'
savfile = dir + 'SEC-2022_Peak Base Case_5Feb2018_511MW-Hail Load 2023-withSTATCOMS.sav'
dyrefile = dir + 'SEC-2022_8Feb2018-Statcom.dyr'
zone = [120]
fault = 11930

# solve(savfile, fault, zone, outfile,dyrefile)


channels = dyntools.CHNF(outfile)
checkmotorstalled(channels,outfile)
chNum = getStalled()
print   chNum
sh_ttl, ch_id, ch_data = channels.get_data()
print ch_id

motors = ['179141','179151','179181','179171']
voltagesBuses = [str(fault),'18914','18915']
volt = getKeysByValues(ch_id,['VOLT '+ i for i in voltagesBuses])
svc = getKeysByValues(ch_id,['SVC'])
statcom = getKeysByValues(ch_id,['STCM'])
speed = getKeysByValues(ch_id,[i+'.* SPEED' for i in motors])
print volt
print svc
print speed
for ch in chNum:
    if ch not in speed:
        speed.append(ch)
print speed
print statcom
for ch in statcom:
    svc.append(ch)
print svc

# Without Gen
channels.txtout(channels=volt,txtfile='Channels/voltages.txt')
channels.txtout(channels=speed,txtfile='Channels/speeds.txt')
channels.txtout(channels=svc,txtfile='Channels/svc.txt')

channels.xlsout(channels=volt,xlsfile='Channels/voltages.xls')
channels.xlsout(channels=speed,xlsfile='Channels/speeds.xls')
channels.xlsout(channels=svc,xlsfile='Channels/svc.xls')