# Remember the set up: There is a ROOT_APPS_DIR, and from that, the rest
# of things hang. That is not a relative path, because that ends up being
# a PITA.  Most of the rest of the programs can change directories,
# etc. But one thing that is hardwired in the paths is a web-apps-common
# directory. Of course, you can change this, but then you will need to use
# sed (or whatever else you fancy) on the files, and modify it. In
# particular, some common python modules and files live there.

# So even if these two lines are here, messing with them will get you
# nowhere. You also need to change the paths in the individual .cgi and
# .py files. Those that say "sys.path.append".
ROOT_APPS_DIR = "/home2/ramon/web-apps"
web_apps_common_dir = ROOT_APPS_DIR + '/web-apps-common'


## R_bin = ROOT_APPS_DIR + '/R-3.1.1-patched-2014-08-21/bin/R'
R_bin = ROOT_APPS_DIR + '/R-4.5.1-patched-config-as-mine/bin/R'
## R_bin2 = ROOT_APPS_DIR + '/R-3.4.1-72824/bin/R'
R_bin2 = R_bin
w3mPath = '/usr/bin/w3m'
python_path = "/usr/bin/python"




web_apps_mpi_error_log = web_apps_common_dir + "/log"
web_apps_counter_log = web_apps_common_dir + "/log" + "/ApplicationCounter"
web_apps_app_caught_error = web_apps_common_dir + "/log" + \
                            "/app_caught_error"

## next unlikely to require changing, unless you want, of course


MAX_MPI_CRASHES = 2 ## note we loop also in runAndCheck.py
## MAX_NUM_RELAUNCHES = 1
## zz-new-checks-runs 2025-09
MAX_NUM_RELAUNCHES = 0
TIME_BETWEEN_CHECKS = 0.5


MAX_time = 3600 * 24 * 15 ## 5 is days until deletion of a tmp directory
MAX_covariate_size = 363948523L ## a 500 * 40000 array of floats
MAX_time_size = 61897L ## time to survival, class, etc size
MAX_class_size = MAX_time_size
MAX_PERMUT = 90000000  ## maximum number of permutations


num_procs_mpi = 4     ### Used to be 63 ## For mpi
## I used to use that, but seems not to work with newer versions
## hostfile_mpi = web_apps_common_dir + "/hostfile_Gallotia_4"
hostfile_mpi = web_apps_common_dir + "/hostfile_Gallotia_64"
hostfile_mpi_R = web_apps_common_dir + "/hostfile_Gallotia_64"

# I disable openib, even if it works, as I was seeing it slower than tcp
# and I am using a single node
mpirun_command = "mpirun -np " + str(num_procs_mpi)

# mpirun_command = "mpirun --mca btl ^openib -hostfile " + hostfile_mpi +\
#               " -np " + str(num_procs_mpi)

## Using MPI is a real PITA. Try to avoid it.
## Only genesrf was using it. Trying newer R with forking (no snow)
# R_mpi_run = "mpirun --mca btl ^openib -np 1 --hostfile " + hostfile_mpi_R + \
#              " " + R_bin + " --no-restore --no-readline --slave --no-save "

R_no_mpi_run = R_bin2 + " --no-restore --no-readline --slave --no-save "


##########################################################
##########################################################
#########  Application specific paths and limits
##########################################################
##########################################################

# These are really not max, but max + 1.
MAX_poms = 3 ## Max number of pomelo2 running
MAX_tnasas = 3
MAX_genesrf = 1 ## uses MPI and is slow. No point in having more.
MAX_adacgh = 3 ## maybe this are R procs, not server procs?
MAX_signs = 3
MAX_DURATION_TRY_Signs = 5 * 3600
MAX_DURATION_TRY_ADaCGH = 5 * 3600
## the file f1-pomelo.R contains also a number, numcores, for cores for Cox

ROOT_POMELO_DIR = ROOT_APPS_DIR + "/pomelo2"
R_pomelo_bin = R_bin
Pomelo_MAX_time = 3 * 3600 ## 3 hours is max duration allowd for any process
pomelo_url = "http://pomelo2.iib.uam.es"
R_MAX_time = 3600 * 4
MAX_DURATION_genesrf =  R_MAX_time
Pomelo_MAX_for_clean = 240 ## 4 * 60 minutes

R_tnasas_bin = R_bin



##########################################################
##########################################################
#########  None of the ones below should need to change
##########################################################
##########################################################

ROOT_POMELO_TMP_DIR = ROOT_POMELO_DIR + "/www/tmp"
Pomelo_runningProcs= ROOT_POMELO_DIR + "/www/Pom.running.procs"
Pomelo_cgi_dir      = ROOT_POMELO_DIR + "/cgi"
pomelo_templates_dir = ROOT_POMELO_DIR + "/www/Pomelo2_html_templates"
pomelo_running_procs_file_expression = Pomelo_runningProcs + "/Pom.*@*"
buryPomCall = Pomelo_cgi_dir + "/buryPom.py"

#************  SELENIUM STUFF **************

Pomelo_covariate_sel_file = ROOT_POMELO_DIR + "/www/selenium-core-0.7.1/TEST_DATA/EXPRESSION_Anova-limma"
Pomelo_class_lab_sel_file = ROOT_POMELO_DIR + "/www/selenium-core-0.7.1/TEST_DATA/CLASS_LABELS_Anova-limma"
Pomelo_covariable_sel_file = ROOT_POMELO_DIR + "/www/selenium-core-0.7.1/TEST_DATA/covariables.anova"
Pomelo_examples_data_dir  = ROOT_POMELO_DIR + "/www/Examples/Data"
