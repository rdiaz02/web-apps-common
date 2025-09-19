#!/bin/bash

##  I doubt it is necessary anymore or will even work, as I don't think Cox is run that way now 2025-09.
## Cox also runs as
## /home2/ramon/web-apps/R-4.5.1-patched-config-as-mine/bin/R --no-restore --no-readline --no-save --slave <f1-pomelo.R >>f1-pomelo.Rout 2> error.msg
## so no trace of Cox in there

## Yes, ugly as hell

find /proc -maxdepth 1 -user www-data -type d -mmin +240 -exec basename {} \; | xargs ps | grep "pomelo2" | awk '{print $1}' | sudo xargs kill
find /proc -maxdepth 1 -user www-data -type d -mmin +240 -exec basename {} \; | xargs ps | grep "Cox 1" | awk '{print $1}' | sudo xargs kill
find /proc -maxdepth 1 -user www-data -type d -mmin +240 -exec basename {} \; | xargs ps | grep "R-4.5.1" | awk '{print $1}' | sudo xargs kill
