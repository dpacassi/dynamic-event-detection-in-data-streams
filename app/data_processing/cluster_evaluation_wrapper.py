import subprocess
import sys

script_names = ['cluster_evaluation_wrapper.py', 'cluster_evaluation.py']


######################################################################################
# Step 1: Check if the script is already running.
######################################################################################

for script_name in script_names:
    status = subprocess.getstatusoutput(
        "ps aux | grep -e '%s' | grep -v grep | awk '{print $2}'| awk '{print $2}'" % script_name
    )
    if status[1]:
        sys.exit(0)

######################################################################################
# Step 2: Retrieve open evaluations from the database.
######################################################################################


######################################################################################
# Step 3: Run cluster_evaluation.py with the defined arguments in the database.
######################################################################################

# p = subprocess.Popen(['python', 'script.py', 'arg1', 'arg2'])
# p.terminate()
