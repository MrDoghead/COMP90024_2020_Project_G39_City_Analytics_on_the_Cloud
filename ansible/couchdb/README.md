# Team: 39
# Chuxin Zou 1061714 China
# Dongnan Cao 970205 China
# Fuyao Zhang 813023 Austalia
# Liqin Zhang 890054 China
# Zhiqian Chen 1068712 Australia

# Author: Chuxin Zou (1061714)


## This folder contains the playbook for install couchdb and its configuration.

## Run the environment.yaml to prepare for installing couchdb by
bash play.sh ubuntu environment.yamal < openstacksdk-key

## Then log in to the instance using key2.pem and install couchdb manually on each instance 

## Then run the couchdb.yaml to configure it by
bash play.sh ubuntu couchdb.yamal < openstacksdk-key