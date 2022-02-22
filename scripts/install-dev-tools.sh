#!/bin/bash
container install
wget -O - https://raw.githubusercontent.com/nektos/act/master/install.sh | bash
pwd
pip3 install -r requirements_test.txt
pip3 install -r requirements_dev.txt