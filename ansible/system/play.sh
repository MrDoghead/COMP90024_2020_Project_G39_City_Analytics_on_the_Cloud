# Team: 39
# Chuxin Zou 1061714 China
# Dongnan Cao 970205 China
# Fuyao Zhang 813023 Austalia
# Liqin Zhang 890054 China
# Zhiqian Chen 1068712 Australia

# Author: Chuxin Zou (1061714)


#!/bin/bash

. ./unimelb-comp90024-2020-grp-39-openrc.sh; ansible-playbook -i hosts.ini -u $1 -k -b --become-method=sudo -K $2
