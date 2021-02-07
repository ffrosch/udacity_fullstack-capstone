#!/bin/bash
# Set heroku environment variables based on a local environment file
# Environment files MUST NOT be committed to source control.
#
# AUTHOR: Florian Frosch
# USAGE: bash setup.sh [filename]

# DEFINE VARIABLES______________________________________________________________
vars=""
input=".env.prod"

# USE OPTIONAL USER-ARG OR FALLBACK ON STANDARD NAME____________________________
if [ "$1" == "" ]; then
    echo "Opening $input"; else
    if [ -f "$1" ]; then
        input=$1; else
        echo "'$1' does not exist, trying '$input' instead"
    fi
fi

# EXIT IF INPUT ENV-FILE DOES NOT EXIST_________________________________________
if ! test -f "$input"; then
    echo "'$input' does not exist. Exiting..."; exit 1
fi

# TEMPORARILY STORE VARIABLES AS A STRING_______________________________________
while read -r line; do
    export vars="$vars $line"
done < "$input"

# SET VARIABLES IN HEROKU_______________________________________________________
eval "heroku config:set $vars"

# DELETE THE TEMPORARY VARIABLE STORE___________________________________________
unset vars