import os
import re
import psspy
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
target_folder=os.path.dirname(sys.argv[0])  # script directory
os.chdir(target_folder)
zone=110
fault=11925
psspy.dyre_new([1,1,1,1],r"""SEC-2019 _11Nov2015-newX.dyr""","","","")
psspy.dynamics_solution_param_2([100,_i,_i,_i,_i,_i,_i,_i],[ 0.4,_f, 0.0008333, _f,_f,_f,_f,_f])
psspy.set_netfrq(1)
psspy.set_relscn(1)
psspy.bsys(1,0,[0.0, 380.],0,[],0,[],0,[],1,[zone])
psspy.chsb(1,0,[-1,-1,-1,1,13,0])
dataextract(zone)
svcChannels(zone)
import varchannels
psspy.lines_per_page_one_device(1,10000000)
psspy.progress_output(2,'qassim2.log',[0,0])
psspy.strt(0,'8804to8846withSVC200-2025.out')
psspy.run(0, 0.1,600,0,51)
psspy.dist_scmu_fault([0,0,1,fault],[0.0,0.0,0.0,0.0])
psspy.run(0, 0.21667,600,0,11)
psspy.dist_clear_fault(1)
psspy.dist_branch_trip(fault,18846,r"""1""")
psspy.set_osscan(1,0)
psspy.set_vltscn(1, 1.15, 0.8)
psspy.run(0, 1.0,600,0,31)
psspy.run(0, 5.0,600,0,51)
psspy.close_report()
