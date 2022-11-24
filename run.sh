#!/bin/bash

psql -U postgres -c "DROP TABLE IF EXISTS CREDS CASCADE"
psql -U postgres -c "DROP TABLE IF EXISTS MESSAGES"
psql -U postgres -c "DROP TABLE IF EXISTS SERVERS"
psql -U postgres -c "DROP TABLE IF EXISTS GPS"
psql -U postgres -c "DROP TABLE IF EXISTS CHATROOMS"

psql -U postgres -c "CREATE TABLE CREDS ( USERNAME TEXT NOT NULL PRIMARY KEY, PASSWORD TEXT NOT NULL, PUBLICKEY TEXT NOT NULL)"
psql -U postgres -c "CREATE TABLE MESSAGES (CONTENT TEXT NOT NULL, SENDER TEXT, RECEIVER TEXT REFERENCES CREDS(USERNAME) , TIME TIME NOT NULL )"
psql -U postgres -c "CREATE TABLE SERVERS (USERNAME TEXT NOT NULL REFERENCES CREDS(USERNAME), PORTS INT NOT NULL)"
psql -U postgres -c "CREATE TABLE GPS (GROUPNAME TEXT NOT NULL, USERNAME TEXT REFERENCES CREDS(USERNAME), PASSWORD TEXT NOT NULL, ISADMIN INT NOT NULL)"
psql -U postgres -c "CREATE TABLE CHATROOMS(USERNAME TEXT REFERENCES CREDS(USERNAME), BUDDY TEXT)"

rm dsPort.txt port.txt
rm pkeys/*

#launch the simple servers
#add number of servers as necessary
gnome-terminal -e "python3 server.py"

#launch the ds serer
gnome-terminal -e "python3 ds.py"

#launch the clients
#add number of clients as necessary with their own clien1 and client 2 files
gnome-terminal -- /bin/sh -c 'python3 client.py'
gnome-terminal -- /bin/sh -c 'python3 client.py'
