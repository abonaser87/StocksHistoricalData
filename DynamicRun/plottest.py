import os,sys
import re
# TODO: Update the file to work with version 33
def convert():
    psspy.cong(0)
    psspy.conl(0,1,1,[0,0],[ 100.0,0.0,0.0, 100.0])
    psspy.conl(0,1,2,[0,0],[ 100.0,0.0,0.0, 100.0])
    psspy.conl(0,1,3,[0,0],[ 100.0,0.0,0.0, 100.0])
    psspy.ordr(0)
    psspy.fact()
    psspy.tysl(0)
def dataextract(zone):
    target_folder=os.path.dirname(sys.argv[0])  # script directory
    os.chdir(target_folder)
    out=open('varchannels.py','w')
    out.write('import psspy\n')
    psspy.lines_per_page_one_device(1,10000000)
    psspy.report_output(2,'models.log',[0,0])
    psspy.bsys(0,0,[0.0, 380.],0,[],0,[],0,[],1,[zone])
    psspy.ldlist(0,0,[1,1])
    infile=open('models.log')
    for lines in infile:      # go through the input file, one line at a time
        lines = lines.split(None,0)
        for line in lines:
            varNum=[]
            varName=[]
            if line.startswith('1'):
                varNum=line.split('CIM5BL')  #Create a list of all the columns except the first 10 and the last 2.
                varNum=varNum[1].split()
                if re.search(r'(33.000|13.800|132.00|380.00)',line):
                    varName=re.split(r'(33.000|13.800|132.00|380.00)',line) #Get the name
                    varName = varName[0].strip() #Get the name
                else:
                    varName = line.split()[:2]
                    varName = varName[0]+" "+varName[1]
                var=varNum[5]
                test = int(var[:-1])+3
                channel = """psspy.var_channel([-1,"""+str(test)+"""], '"""+varName+""" SPEED')"""+"\n"
                out.write(channel)
    out.close()
    psspy.close_report()
def svcChannels(zone):
    target_folder=os.path.dirname(sys.argv[0])  # script directory
    os.chdir(target_folder)
    out=open('varchannels.py','a')
    psspy.lines_per_page_one_device(1,10000000)
    psspy.report_output(2,'svcModels.log',[0,0])
    psspy.bsys(0,0,[0.0, 380.],0,[],0,[],0,[],1,[zone])
    psspy.mlst(0, 0, [1,1,2])
    infile=open('svcModels.log')
    for lines in infile:      # go through the input file, one line at a time
        lines = lines.split(None,0)
        for line in lines:
            varNum=[]
            varName=[]
            if 'CSVGN1' in line:
                varNum=line.split('CSVGN1')  #Create a list of all the columns except the first 10 and the last 2.              
                varNum=varNum[1].split()
                if re.search(r'(33.000|13.800|132.00|380.00)',line):
                    varName=re.split(r'(33.000|13.800|132.00|380.00)',line) #Get the name
                    varName = varName[0].strip() #Get the name
                else:
                    varName = line.split()[:2]
                    varName = varName[0]+" "+varName[1]
                var=varNum[5]               
                channel = """psspy.var_channel([-1,"""+var+"""], '"""+varName+""" SVC')"""+"\n"
                out.write(channel)
    out.close()
    psspy.close_report()
def latest_psse_location():
    import _winreg
    ptiloc = r"SOFTWARE\PTI"
    ptikey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, ptiloc, 0, _winreg.KEY_READ)
    ptikeyinfo = _winreg.QueryInfoKey(ptikey)
    numptisubkeys = ptikeyinfo[0]
    vdict = {}
    for i in range(numptisubkeys):
        vernum = _winreg.EnumKey(ptikey, i)
        try:
            n = int(vernum[-2:])
            vdict[n]=vernum
        except:
            pass

    vers = vdict.keys()
    vers.sort()
    k = vers[-1]
    lver = vdict[k]
    lverloc = ptiloc + "\\" + lver + "\\" + "Product Paths"
    lverkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, lverloc, 0, _winreg.KEY_READ)
    lverdir, stype = _winreg.QueryValueEx(lverkey, 'PsseInstallPath')
    _winreg.CloseKey(ptikey)
    _winreg.CloseKey(lverkey)
    return lverdir
def solve(savfile,fault,zone,outfile):
    psspy.case(savfile)
    convert()
    psspy.dyre_new([1, 1, 1, 1], r"""Case/SEC-2022_8Feb2018.dyr""", "", "", "")
    psspy.dynamics_solution_param_2(intgar1=100,realar1=0.4,realar3=0.0008333)
    psspy.set_netfrq(1)
    psspy.set_relscn(1)
    psspy.bsys(1,0,[0.0, 380.],0,[],0,[],0,[],1,[zone])
    psspy.chsb(1,0,[-1,-1,-1,1,13,0])
    dataextract(zone)
    svcChannels(zone)
    import varchannels
    psspy.lines_per_page_one_device(1,10000000)
    psspy.progress_output(2,'qassim.log',[0,0])
    psspy.strt(0,outfile)
    psspy.run(0, 0.1,600,0,51)
    psspy.dist_scmu_fault([0,0,1,fault],[0.0,0.0,0.0,0.0])
    psspy.run(0, 0.21667,600,0,11)
    psspy.dist_clear_fault(1)
    psspy.dist_branch_trip(fault,18803,r"""1""")
    psspy.set_osscan(1,0)
    psspy.set_vltscn(1, 1.15, 0.8)
    psspy.run(0, 1.0,600,0,31)
    psspy.run(0, 5.0,600,0,51)
    psspy.close_report()


pssedir = 'C:\Program Files (x86)\PTI\PSSE32'
pssedir = str(pssedir)              # convert unicode to str

# =============================================================================================
# Files Used

pssbindir  = os.path.join(pssedir,'PSSBIN')
exampledir = os.path.join(pssedir,'EXAMPLE')
# =============================================================================================
# Check if running from Python Interpreter
exename = sys.executable
p, nx   = os.path.split(exename)
nx      = nx.lower()
if nx in ['python.exe', 'pythonw.exe']:
    os.environ['PATH'] = pssbindir + ';' + os.environ['PATH']
    sys.path.insert(0,pssbindir)
import redirect
redirect.psse2py()    
import psspy
ierr = psspy.psseinit(buses=150000)

import dyntools
target_folder=os.path.dirname(sys.argv[0])  # script directory
os.chdir(target_folder)

outfile = '8804SVC200-2020.out'
savfile = 'Case/SEC-2022_Peak Base Case_5Feb2018_511MW.sav'
zone=110
fault=11925

solve(savfile,fault,zone,outfile)

channels = dyntools.CHNF(outfile)
sh_ttl, ch_id, ch_data = channels.get_data()
print ch_id
print ch_data
channels.txtout(channels=[20,35,36],txtfile='voltages.txt')
channels.txtout(channels=[170,171],txtfile='speeds.txt')
channels.txtout(channels=[241],txtfile='svc.txt')