#!/usr/bin/env bash

echo "***********************************************"
echo "---apt update e upgrade---"
echo "***********************************************"

apt-get -y update

echo "***********************************************"
echo "---OS dependencies---"
echo "***********************************************"

apt-get -y install python3-pip
apt-get -y install python3-dev python3-setuptools