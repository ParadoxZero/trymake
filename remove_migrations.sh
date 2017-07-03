#!/usr/bin/env bash
find . -path */migrations/* -name "*.p"y -not -path "*__init__*"
echo "Continue?(y/n)"
read n
case $n in
y)
find . -path */migrations/* -name "*.p"y -not -path "*__init__*" -exec rm {} \;
rm db.sqlite3
    ;;
*) echo "Exiting....";;
esac