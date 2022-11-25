#!/bin/bash
rm -rf out.txt outs.txt
touch out.txt
cat chats/* >> out.txt

python3 test.py
rm -rf out.txt outs.txt