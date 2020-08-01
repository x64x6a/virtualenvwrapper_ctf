#!/bin/bash

if [ ! -z "$PROJECT_HOME" ]
then
    if [ -s "$PROJECT_HOME/.active_ctf" ]
    then 
        workon `cat $PROJECT_HOME/.active_ctf`
    fi
fi
