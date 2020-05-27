# Team: 39
# Chuxin Zou 1061714 China
# Dongnan Cao 970205 China
# Fuyao Zhang 813023 Austalia
# Liqin Zhang 890054 China
# Zhiqian Chen 1068712 Australia

# Author: Chuxin Zou (1061714)

## In this folder, we prepare the environment for our system and start it.

## First download the code for building the system from git
bash play.sh ubuntu file-transfer.yaml < openstacksdk-key

## Then install the requiring packages
bash play.sh ubuntu preparation.yaml < openstacksdk-key

## Finally we can start our system
bash start-system.sh ubuntu start.yaml < openstacksdk-key

## Go to http://172.26.133.0:5000 to check the web interface

## Stop the system
bash start-system.sh ubuntu stop.yaml < openstacksdk-key
