from flask import Flask
from flask_socketio import SocketIO

# bi-directional communications between the clients and the server.

#MESSAGING DATABASE 
#**CRUD operations organize by id/sender from login 


#MESSAGING TEMPLATE
#*display id 
# request when div is pulled into view
#*block date/timestamp message sender recipient

#MESSAGE DELIVERY
#sumbition sent update message status.notification

#SECURITY CHECKS
#json request id match senderid
#make sure sender/receiver exists 


db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("""SELECT googleID, userID, receiverID, senderID,
    FROM Users, Posts, Messages,
    Where Users.googleID = Messages.senderID, LIMIT 0,30
    );
    """ )

# cursor = db.cursor()
  cursor.execute(f"""INSERT into Messages (date, message, senderUserID, recieverUserID)
    VALUES ('Today', 'Hello World', 'Alice','Bob');""")
