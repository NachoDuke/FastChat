#!/bin/bash

rm chats/*
bash run.sh 1 0 $1
python3 script.py
