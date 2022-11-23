# FastChat
## Basic Plan
A multi-server, multi-client system to allow chats between various clients. The basic model for the project will be as follows:
We create a program that controls a client. This program starts by calling a function called log-in. The login process contains 2 options:
1. Sign Up
2. Sign In

If the user chooses to sign up, they will face one of two scenarios, either the username they choose will be unique, in which case the sign up is successful, or the username will already be taken by a different user. In this case, an error message is displayed and the user is asked to try again.

If the uesr chooses to sign in, they will enter the username and password and then face the following scenarios:
1. Successful Log In - if the credentials match and the user is not already logged in
2. Already Logged In - if the credentials match but the user is logged in elsewhere
3. Incorrect Password - if the username exists but the password is incorrect
4. No such User - if the username is not a valid one

After a succesful sign up or sign in, the user will be taken to an infinite menu.

This menu will allow users to message a single other user, message a group or create/join groups. The user can also quit the program whenever required. Now, we wait for user input to carry out specific instructions.

Depending on the users input, we need to send certain messages to the server to process the request. Based on what the server receives, it carries out some checks and if everything seems alright, it returns a corresponding message to the client (usually to determine the outcome of the request). In this way, we handle various kinds of client requests.

As for sending messages between clients, we send a special message which contains information about the sender and the desired receiver. The server then uses this to ensure that the message is only sent to the desired receiver.

## What we've done so far:
1. Implemented basic functionalities of the client and created a menu system for a user
2. Integrated servers that work with a number of clients to efficiently receive and transmit messages
3. Created a special server to which each client connects at first and which routes clients to other servers
4. Created load balancing functionalities to ensure even distribution across servers
5. Created a database that works by storing user information, encryption keys and messages
6. Added the functionality of creating groups and joining them
7. Created specialised messages for groups
8. Worked on rsa encryption of messages 

## Pending Work/Problems
1. Integrating the database fully to store all the information
2. Storing pending messages on the database
3. Processing of images using B64
4. Improving encryption-decryption

## Future Plans
1. Add digital signatures for message credibility and verification

## Team Members
1. Aadish Sethiya
2. Chaitanya Aggarwal
3. Premankur Chakraborty 
