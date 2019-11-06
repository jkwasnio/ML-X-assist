# SGE COMMANDS

# Determine the queues you want your job to run on.
# You can name multiple queues by separating them with comma (no spaces!).
# It is possible to address individual nodes
# GPUs are available in graphix.q only!
#$ -q {SGE_JOB_QUEUE}

# Determines were to store the default command line and potential error output of your application as a text file.
# If no path is given your current working directory is used as default
# The option -j y joins default and error output to a singe file.
#$ -j y

# Determines an e-mail address to send job informations to.
# The options control the cases in which to send a e-mail (b=begin, e=end, a=abort, s=suspend)
#$ -M {SGE_JOB_MAIL_ADDRESS} -m {SGE_JOB_MAIL_OPTIONS}

# Influences Job priority. Users can only decrease their job priority by setting a value between 0 and -1023.
# not used
    # -p 0

# Request exclusive memory for your job. This value is automatically multiplied by the number of requested CPU slots.
# If not explicitly requested default value is 1 GB. If your job exceeds the memory request it will be aborted.
#$ -l h_vmem={SGE_JOB_MEM_LIMIT_GB}G

# Request a maximum CPU time limit for your job. Note that the requested CPU time must be less than 1 hour in order to successfully submit to short.q.
# If not explicitly requested default value is 14 days. If your job exceeds the CPU time request it will be aborted.
#$ -l h_cpu={SGE_JOB_TIME_LIMIT_H}:00:00

# Selects your current directory as working directory for your job.
#$ -cwd

# Requests the user commands to be interpreted as bash commands
#$ -S /bin/bash

# Name job
#$ -N {SGE_JOB_NAME}

# Job Order
{SGE_JOB_ORDER_COMMAND}

# USER COMMANDS IN BASH
#!/bin/bash

# preamble
{SGE_JOB_PREAMBLE}

# run job
bash job.sh
