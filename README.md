# FastChat

## List of features  implemented:
1. Encryption and decryption of messages
2. Creating and maintaining database
3. Storage of encrypted passwords
4. Sending and receiving images
5. Implementation of personal and group chats
6. Implementation of special admin features
7. Load balancing leading to low latency and high throughput
8. Implemented pending messages feature

## Basic Plan
A multi-server, multi-client system to allow chats between various clients. The basic model for the project will be as follows:
We create a program that controls a client. This program starts by calling a function called log-in. The login process contains 2 options:
1. Sign Up
2. Sign In

If the user chooses to sign up, they will face one of two scenarios, either the username they choose will be unique, in which case the sign up is successful, or the username will already be taken by a different user. In this case, an error message is displayed and the user is asked to try again. When the user succesfully signs up, the username and password of the user is stored in the database. The password is encrypted using a fernet key hence securing the password.

If the uesr chooses to sign in, they will enter the username and password and then face the following scenarios:
1. Successful Log In - if the credentials match and the user is not already logged in
2. Already Logged In - if the credentials match but the user is logged in elsewhere
3. Incorrect Password - if the username exists but the password is incorrect
4. No such User - if the username is not a valid one

After a succesful sign up or sign in, the user will be taken to an infinite menu.

This menu will allow users to message a single other user, message a group or create/join groups. The user can also quit the program whenever required. Now, we wait for user input to carry out specific instructions.

Depending on the users input, we need to send certain messages to the server to process the request. Based on what the server receives, it carries out some checks and if everything seems alright, it returns a corresponding message to the client (usually to determine the outcome of the request). In this way, we handle various kinds of client requests.  

### Personal chatrooms:

As for sending messages between clients, we send a special message encrypted with the help of RSA private key of the user. This encrypted message contains information about the sender and the desired receiver. The server then uses this to ensure that the message is only sent to the desired receiver. After sending the encrypted messsage to the server, the receiver decrypts the message using the public key of sender and gets the message. This ensures end-to-end encryption of messages so that no one else is able to fetch these messages. The user can also send specified images to the receiver which when fetched by the receiver gets stored on their device.

When the receiver is not present in the same chatroom as that of sender or when the receiver is offline, the encrypted message sent by the sender gets stored the database. The receiver can access these messages either by checking the pending messages from the menu or by entering the chatroom again.

### Group chatrooms:

A user can select the option to create a group. This group is secured by a password hence only someone with the password will be able to join it. This user becomes the admin of the group and experiences additional powers to remove participants from the group. A normal user can join any group by selecting the join group option from the menu given the user knows the name of the group and the password of the group.

All the participants of the group can enter the group's chatroom by selecting the respective option from the menu. This allows users to send end-to-end encrypted messages to pther participants of the group.

## Execution:
### run.sh 'number of servers' 'number of clients' 'type of distribution server':
This script takes three command line arguments to specify the number of servers to be produced, number of clients present and the type for distribution server to be implemented for load  balancing. The script then generates the desired numbers of servers and clients.

### things.sh 'type of distribution server':
This script is used to run the python scrypt file to check latency and throughput.

<!-- ## What we've done so far:
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
 -->
## Team Members
1. Aadish Sethiya
2. Chaitanya Aggarwal
3. Premankur Chakraborty 
