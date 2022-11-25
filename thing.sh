#!/bin/bash

rm chats/*
bash run.sh $1 0 $2
python3 script.py
bash test.sh
