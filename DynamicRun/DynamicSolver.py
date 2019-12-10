import os, sys
import re
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

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
import dyntools

class DynamicSolver():
    def __init__(self,dirpath,dyrpath,dllpath,savfile, fault, zone,tripBuses,triptype,statusbar):
        self.dirpath = unicode(dirpath,encoding="UTF-8")
        self.dyrpath = unicode(dyrpath,encoding="UTF-8")
        self.dllpath = unicode(dllpath,encoding="UTF-8")
        self.savfile = unicode(savfile,encoding="UTF-8")
        self.fault = fault
        self.zone = [zone]
        self.triptype = triptype
        self.tripBuses = [unicode(elem, encoding="UTF-8") for elem in tripBuses]
        self.outfile = 'Output/fault '+str(fault)+'-'.join(self.tripBuses)+'Outage.out'
        self.statusbar = statusbar
        self.psseInit()


    def convert(self):
        psspy.cong(0)
        psspy.conl(0, 1, 1, [0, 0], [100.0, 0.0, 0.0, 100.0])
        psspy.conl(0, 1, 2, [0, 0], [100.0, 0.0, 0.0, 100.0])
        psspy.conl(0, 1, 3, [0, 0], [100.0, 0.0, 0.0, 100.0])
        psspy.ordr(0)
        psspy.fact()
        psspy.tysl(0)
        self.statusbar.showMessage('Case Converted')

    def dataextract(self,zone):
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
                    varNum = line.split(
                        'CIM5BL')  # Create a list of all the columns except the first 10 and the last 2.
                    varNum = varNum[1].split()
                    if re.search(r'(33.000|13.800|132.00|380.00)', line):
                        varName = re.split(r'(33.000|13.800|132.00|380.00)', line)  # Get the name
                        varName = varName[0].strip()  # Get the name
                    else:
                        varName = line.split()[:2]
                        varName = varName[0] + " " + varName[1]
                    var = varNum[5]
                    test = int(var[:-1]) + 3
                    channel = """psspy.var_channel([-1,""" + str(
                        test) + """], '""" + varName + """ SPEED')""" + "\n"
                    out.write(channel)
        out.close()
        psspy.close_report()

    def svcChannels(self,zone):
        out = open('varchannels.py', 'a')
        psspy.lines_per_page_one_device(1, 10000000)
        psspy.report_output(2, 'Logs/svcModels.log', [0, 0])
        psspy.bsys(0, 1, [0.0, 132.], 0, [], 0, [], 0, [], len(zone), zone)
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

    def statcomChannels(self,zone):
        out = open('varchannels.py', 'a')
        psspy.lines_per_page_one_device(1, 10000000)
        psspy.report_output(2, 'Logs/statcomModels.log', [0, 0])
        psspy.bsys(0, 1, [0.0, 132.], 0, [], 0, [], 0, [], len(zone), zone)
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
                    var = varNum[4].replace('-', '')
                    # print var
                    channel = """psspy.var_channel([-1,""" + var + """], '""" + varName + """ STCM I')""" + "\n"
                    out.write(channel)
                    # var = int(varNum[4].replace('-',''))+2
                    # channel = """psspy.var_channel([-1,""" + str(var) + """], '""" + varName + """ STCM VAR')""" + "\n"
                    # out.write(channel)
        out.close()
        psspy.close_report()

    def solve(self):
        psspy.case(self.savfile)
        self.convert()
        psspy.lines_per_page_one_device(1, 10000000)
        psspy.progress_output(2, 'Logs/' + self.outfile[6:-3] + '.log', [0, 0])
        psspy.addmodellibrary(self.dllpath)
        psspy.dyre_new([1, 1, 1, 1], self.dyrpath, "", "", "")
        psspy.dynamics_solution_param_2(intgar1=200, realar1=0.4, realar3=0.0008333, realar4=0.0033333)
        psspy.set_relang(1, 0, "")
        psspy.bsys(1, 0, [0.0, 380.], 0, [], 0, [], 0, [], len(self.zone), self.zone)
        psspy.chsb(1, 0, [-1, -1, -1, 1, 13, 0])
        self.dataextract(self.zone)
        self.svcChannels(self.zone)
        self.statcomChannels(self.zone)
        import varchannels
        psspy.bus_frequency_channel([-1, self.fault], r"""Frequency""")
        # psspy.chsb(0, 0, [-1, -1, -1, 1, 1, 0])
        ierr = psspy.strt(0, self.outfile)
        if ierr == 0:
            self.statusbar.showMessage('Case Initialized, Check Log file for details')
        psspy.run(0, 0.1, 600, 0, 51)
        psspy.dist_scmu_fault([0, 0, 1, self.fault], [0.0, 0.0, 0.0, 0.0])
        psspy.run(0, 0.21667, 600, 0, 11)
        psspy.dist_clear_fault(1)
        if self.triptype == 1:
            psspy.dist_3wind_trip(int(self.tripBuses[0]),int(self.tripBuses[1]),int(self.tripBuses[2]),r"""1""")
        elif self.triptype == 2:
            psspy.dist_machine_trip(int(self.tripBuses[0]),r"""1""")
        else:
            psspy.dist_branch_trip(int(self.tripBuses[0]), int(self.tripBuses[1]), r"""1""")
        psspy.set_osscan(1, 0)
        psspy.set_vltscn(1, 1.15, 0.8)
        psspy.run(0, 1.0, 600, 0, 31)
        psspy.run(0, 5.0, 600, 0, 51)
        psspy.close_report()
        self.solved = True
        self.statusbar.showMessage('Finished Solving, Check Log file for details')


    def checkmotorstalled(self,ch_id):
        # Get all speed channel numbers
        chNum = self.getKeysByValues(ch_id, ['.* SPEED'])
        self.channels.xlsout(channels=chNum, xlsfile='Channels/AllSpeeds.xls', show=False, overwritesheet=True,
                        sheet='Sheet1')
        data = pd.read_excel('Channels/AllSpeeds.xlsx', header=3, index_col=0)
        check = data.iloc[0] - data.iloc[-1]
        check = check.loc[check > 0.01]
        check = check.index.tolist()
        if not len(check) == 0:
            chNum = self.getKeysByValues(ch_id, check)
        else:
            chNum = []
        return chNum

    '''
    Get a list of keys from dictionary which has value that matches with any value in given list of values
    '''

    def getKeysByValues(self,dictOfElements, listOfValues):
        listOfKeys = list()
        listOfItems = dictOfElements.items()
        for item in listOfItems:
            try:
                if re.search('|'.join(listOfValues), item[1]):
                    listOfKeys.append(item[0])
            except:
                continue
        return listOfKeys

    def psseInit(self):
        ierr = psspy.psseinit(buses=150000)
        if ierr ==0:
            self.statusbar.showMessage('PSSE Initialized')
        os.chdir(self.dirpath)
        sys.path.insert(1, self.dirpath)
        try:
            os.makedirs('Output')
            os.makedirs('Channels')
            os.makedirs('Logs')
            os.makedirs('Figuers')
        except OSError:
            print'Error creating directory'
            pass
    def plot(self,title,motors,voltagesBuses,bFreq,bSvc,bStatcom):
        if not self.solved:
            pass
        self.channels = dyntools.CHNF(self.outfile)
        sh_ttl, ch_id, ch_data = self.channels.get_data()
        chNum = self.checkmotorstalled(ch_id)

        # motors = ['179031', '179111']
        # voltagesBuses = [str(fault), '18911', '179111']
        volt = self.getKeysByValues(ch_id, ['VOLT ' + i for i in voltagesBuses])
        svc = self.getKeysByValues(ch_id, ['SVC'])
        statcom = self.getKeysByValues(ch_id, ['STCM'])
        speed = self.getKeysByValues(ch_id, [i + '.* SPEED' for i in motors])
        freq = self.getKeysByValues(ch_id, ['FREQUENCY'])

        for ch in chNum:
            if ch not in speed:
                speed.append(ch)
        if bStatcom:
            for ch in statcom:
                svc.append(ch)

        self.channels.xlsout(channels=volt, xlsfile='Channels/voltages.xls', show=False, overwritesheet=True, sheet='Sheet1')
        self.channels.xlsout(channels=speed, xlsfile='Channels/speeds.xls', show=False, overwritesheet=True, sheet='Sheet1')
        if not len(svc) == 0: self.channels.xlsout(channels=svc, xlsfile='Channels/svc.xls', show=False, overwritesheet=True,
                                              sheet='Sheet1')
        self.channels.xlsout(channels=freq, xlsfile='Channels/freq.xls', show=False, overwritesheet=True, sheet='Sheet1')
        filename = 'Figuers/' + title
        with PdfPages(filename + '.pdf') as pdf:
            ######################
            # PLOT VOLTAGES      #
            ######################

            data = pd.read_excel('Channels/voltages.xlsx', header=3, index_col=0)
            data.rename(columns=lambda x: x.split('VOLT')[1][:7].strip(), inplace=True)
            fig_size = plt.rcParams["figure.figsize"]
            # Set figure width to 12 and height to 9
            fig_size[0] = 11.69
            fig_size[1] = 8.27
            plt.rcParams["figure.figsize"] = fig_size
            data.plot()
            plt.xlabel('Time (sec)')
            plt.ylabel('Voltage (pu)')
            plt.legend(loc='lower right')
            plt.xlim([0, 5])
            plt.suptitle(title+' - Voltages')
            plt.savefig(filename+ ' - Voltages' + '.png')
            pdf.savefig()

            plt.close()

            ######################
            # PLOT SPEEDS        #
            ######################

            data = pd.read_excel('Channels/speeds.xlsx', header=3, index_col=0)
            data.rename(columns=lambda x: x[:6].strip(), inplace=True)
            data.plot()
            plt.xlabel('Time (sec)')
            plt.ylabel('Speed')
            plt.legend(loc='lower right')
            plt.xlim([0, 5])
            # plt.ylim([-0.2,0.1])
            plt.suptitle(title+' - Motorspeeds')
            plt.savefig(filename+ ' - Motorspeeds' + '.png')
            pdf.savefig()
            plt.close()

            # ######################
            # # PLOT SVC & Statcoms       #
            # ######################

            if bSvc:
                data = pd.read_excel('Channels/svc.xlsx', header=3, index_col=0)
                # data.rename(columns=lambda x: x[:6].strip(), inplace=True)
                # df = pd.read_csv('Channels/svc.csv',index_col='Time')
                data.plot()

                plt.xlabel('Time (sec)')
                plt.ylabel('SVC Output')
                plt.legend(loc='lower right')
                plt.xlim([0, 5])
                plt.suptitle(title + ' - FACTS')
                plt.savefig(filename + ' - FACTS' + '.png')
                pdf.savefig()
                plt.close()
            ###################
            ## FREQUNCY PLOT ##
            ###################
            if bFreq:
                data = pd.read_excel('Channels/freq.xlsx', header=3, index_col=0)
                # data.rename(columns='FREQUENCY', inplace=True)
                # data = pd.read_csv('Channels/voltages.csv',index_col='Time')
                data = (1 + data) * 60
                fig_size = plt.rcParams["figure.figsize"]
                # Set figure width to 12 and height to 9
                fig_size[0] = 11.69
                fig_size[1] = 8.27
                plt.rcParams["figure.figsize"] = fig_size
                data.plot()
                plt.xlabel('Time (sec)')
                plt.ylabel('Frequency')
                plt.legend(loc='lower right')
                plt.xlim([0, 5])
                plt.suptitle(title + ' - Frequency')
                plt.savefig(filename + ' - Frequency' + '.png')
                pdf.savefig()

                plt.close()
