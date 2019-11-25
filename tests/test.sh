#!/bin/bash
echo "Time : $(date)" >> logs.txt
python3 tests.py -c ../scripts/configs.json -t frrouting_cfg >> logs.txt
