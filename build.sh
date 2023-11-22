#!/usr/bin/env bash
# if venv is present use it
if [ -f ".venv/bin/python3" ];
then
    echo "venv present"
    alias python3="./venv/bin/python3"
fi
echo "Starting Dataset Generation, it may take some time"
python3 dataset/server.py
python3 dataset/application.py
python3 dataset/changes.py
python3 dataset/incidents.py
python3 dataset/dataCenter.py
echo "exporting dataste to CSV_TGT"
mkdir -p CSV_TGT/
mv *.csv CSV_TGT
