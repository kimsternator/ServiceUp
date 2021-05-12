from flask import Flask
from flask_socketio import SocketIO

# flask_messenger 

#Service up private message system built with flask
# create a socket in Flask -> ‘flask-socketio’ extension enables us to do
# bi-directional communications between the clients and the server.

#MESSAGING DATABASE 
#**CRUD operations 
#organize by id/sender from login 
#deletes from one end?

#MESSAGING TEMPLATE
#*display
#id
#request when div is pulled into view
#*block
#date/timestamp
#message 
#sender 
#recipient

#MESSAGE DELIVERY
#sumbition
#sent update 
#message status
#notification

#SECURITY CHECKS
#json request id match senderid
#make sure sender/receiver exists 
