#!/usr/bin/env bash
find . -path */migrations/* -name "*.p"y -not -path "*__init__*"

if [ $1 == 'y' ]; then
    n='y'
else
    echo "Continue?(y/n)"
    read n
fi

case $n in
y)
find . -path */migrations/* -name "*.p"y -not -path "*__init__*" -exec rm {} \;
rm db.sqlite3
    ;;
*) echo "Exiting....";;
esac
