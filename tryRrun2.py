#!/usr/bin/python
import os
import time
import signal
import shutil
import sys
import socket
import counterApplications
import random
import random
tmpDir = sys.argv[1]
numtries = sys.argv[2]
application = sys.argv[3]

## This uses MPI! It is called, at least, from genesrf.

sys.path.append("/asterias-web-apps/web-apps-common")
from web_apps_config import *

# numtries = 50 ## I redefine it here. for really stubborn cases


# MIN_LAM_NODES = 5 ## highly deployment dependant. But in our clusters
## less than 5 noes means something seriously wrong.
## Beware that a partially working cluster, if less than MIN_LAM_NODES, will
## behave weirdly, as tryRrun2.py will start, but then kill, lots of running jobs.


# def tryRrun(Rcommand, tmpDir, numtries = 10, application = "SignS")
#     """ Try to launch R via os.system, verifying MPI got initialized.
#     We try to initiate R up to numtries times; we verify MPI (or Snow)
#     got initialized correctly (that requires that R produces an mpiOK file).
#     If it doesn't, we call the mpi sanitization scripts to do their job
#     and try again.
#     """

def collectZombies(k = 10):
    """ Make sure there are no zombies in the process tables.
    This is probably an overkill, but works.
    """
    for nk in range(k):
        try:
            tmp = os.waitpid(-1, os.WNOHANG)
        except:
            None


## The following does not work. We would need to caputer the output
## from ps, and then get substring with -sessionsuffix and the number = lamSuffix.
## But killing lam kills all slaves and the main process
## lamdpid = os.popen('ps --ppid ' + str(lampid) + ' -o "%p" --no-headers').readline()
## time.sleep(0.5)


## general cleaning
# buried = os.system("/http/mpi.log/buryThem2.py")
# killedlamandr = os.system('/http/mpi.log/killOldLamAllMachines.py')
# cleaned_dirs = os.system('/http/mpi.log/delete_old_dirs.py')


try:
    counterApplications.add_to_counter_log(application, tmpDir, socket.gethostname())
except:
    None

startedOK = False
time.sleep(random.uniform(0, 1)) ## to prevent truly simultaneous from crashing MPI

for i in range(int(numtries)):
    os.system('touch ' + tmpDir + '/numtries_' + str(i)) ## debug
    # lamSuffix = str(int(time.time())) + str(os.getpid()) + \
    #             str(random.randint(10, 999999))
    # lamenvfile = open(tmpDir + '/lamSuffix', mode = 'w')
    # lamenvfile.write(lamSuffix)
    # lamenvfile.flush()
    # lamenvfile.close()
    # lamenv = os.putenv('LAM_MPI_SESSION_SUFFIX', lamSuffix)

    # fullRcommand = 'export LAM_MPI_SESSION_SUFFIX="' + lamSuffix + '";' + '/usr/bin/lamboot -b -H /http/mpi.defs/lamb-host.' + socket.gethostname() + '.def; cd ' + tmpDir + '; sleep 40;' + '/var/www/bin/R-local-7-LAM-MPI/bin/R  --no-restore --no-readline --no-save --slave <f1.R >>f1.Rout 2> error.msg &'

    fullRcommand = 'cd ' + tmpDir + '; ' + R_mpi_run +\
                   '<f1.R >>f1.Rout 2> error.msg &'

    # counterApplications.add_to_LAM_SUFFIX_LOG(lamSuffix, application, tmpDir,
    #                                           socket.gethostname())

    Rrun = os.system(fullRcommand)
    os.system('touch ' + tmpDir + '/first_Rrun') ## debug
    time.sleep(100 + random.uniform(1, 12))
    collectZombies()

    if os.path.exists(tmpDir + "/RterminatedOK"):
        startedOK = True
        break

    # if os.path.exists(tmpDir + "/mpiOK"):
    #     if int(os.popen('lamnodes | wc').readline().split()[0]) > MIN_LAM_NODES:
    #         ## debug
    #         os.system('echo "' + str(int(os.popen('lamnodes | wc').readline().split()[0])) + '" > ' + tmpDir + '/MIN_LAM_NODES_CHECK')
    #         startedOK = True
    #         break
    # try:
    #     lamkill = os.system('lamhalt; lamwipe')
    # except:
    #     None

    try:
        counterApplications.add_to_MPIErrorLog(application, tmpDir,
                                                socket.gethostname())
    except:
        None

        
#     if not os.path.exists('/http/mpi.log/' + application + 'ErrorLog'):
#         os.system('touch /http/mpi.log/' + application + 'ErrorLog')
#     outlog = open('/http/mpi.log/' + application + 'ErrorLog', mode = 'a')
#     outlog.write('MPI fails on ' + time.ctime(time.time()) +
#                  ' Directory: ' + tmpDir + '\n')
#     outlog.close()
   
   
if not startedOK:
    ## Logging
    try:
        counterApplications.add_to_MPIErrorLog(application, tmpDir,
                                                socket.gethostname(),
                                               'MPI max num crashes')
    except:
        None
    
#     if not os.path.exists('/http/mpi.log/' + application + 'ErrorLog'):
#         os.system('touch /http/mpi.log/' + application + 'ErrorLog')
#     outlog = open('/http/mpi.log/' + application + 'ErrorLog', mode = 'a')
#     outlog.write('MPI fails on ' + time.ctime(time.time()) +
#                  ' Directory: ' + tmpDir + '\n')
#     outlog.close()
    ## Make sure the checkdone.cgi will stop; we create the two files here
    ## either of which will lead to loading results.html
    out1 = open(tmpDir + "/natural.death.pid.txt", mode = "w")
    out2 = open(tmpDir + "/kill.pid.txt", mode = "w")
    out1.write('MPI initialization error!!')
    out2.write('MPI initialization error!!')
    out1.close()
    out2.close()
    outf = open(tmpDir + "/pre-results.html", mode = "w")
    outf.write("<html><head><title> MPI initialization problem.</title></head><body>\n")
    outf.write("<h1> MPI initialization problem.</h1>")
    outf.write("<p> After " + numtries + " attempts we have been unable to ")
    outf.write(" initialize MPI.</p>")
    outf.write("<p> We will be notified of this error, but we would also ")
    outf.write("appreciate if you can let us know of any circumstances or problems ")
    outf.write("so we can diagnose the error.</p>")
    outf.write("</body></html>")
    outf.close()
    shutil.copyfile(tmpDir + "/pre-results.html", tmpDir + "/results.html")


