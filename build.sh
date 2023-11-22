#!/usr/bin/env bash
alias python3="./venv/bin/python3"
python3 dataset/server.py
python3 dataset/application.py
python3 dataset/changes.py
python3 dataset/incidents.py
python3 dataset/dataCenter.py
mkdir -p CSV_TGT/
mv *.csv CSV_TGT
