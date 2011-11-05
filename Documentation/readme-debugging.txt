When you suspect a problem with the way power management is reflecting on your machine
please enable the following laptop-mode-tools options to extract more information as to
what might be causing the problem


VERBOSE_OUTPUT=1
#
# Set this to 1 if you want to see a lot of information when you start/stop 
# laptop_mode.
#

LOG_TO_SYSLOG=1
# Set this to 1 if you want to log messages to syslog. All of laptop-mode-tools messages
get logged into syslog. This helps further in debugging the problem.



DEBUG=1
# Run in shell debug mode
# Enable this if you would like to execute the entire laptop-mode-tools program
# in shell debug mode. Warning: This will create a lot of text output.
#
# This shell debug mode output will be listed on the terminal where laptop-mode-tools'
# init script it called.

# If you are debugging an individual module, perhaps you would want to enable
# each module specific debug mode (available in module conf files)

# Further details and documentation about more of the options of laptop-mode-tools is 
#  available in the man page
