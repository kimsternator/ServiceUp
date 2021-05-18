# Import MySQL Connector Driver
import mysql.connector as mysql

# Load the credentials from the secured .env file
import os
from dotenv import load_dotenv
load_dotenv('credentials.env')

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST'] # must 'localhost' when running this script outside of Docker

# Connect to the database
db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

# # CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!!
# I'LL LEAVE THIS FOR NOW FOR TESTING PURPOSES, DELETE LATER!!
cursor.execute("drop table if exists Posts;")

# Create a TStudents table (wrapping it in a try-except is good practice)
try:
  cursor.execute("""
    CREATE TABLE Posts (
    id int AUTO_INCREMENT PRIMARY KEY,
    userID INT NOT NULL, 
    service_type VARCHAR (20) NOT NULL,
    who VARCHAR (20) NOT NULL,
    available VARCHAR (20) NOT NULL,
    compensation VARCHAR (20) NOT NULL,
    info TINYTEXT NOT NULL
  );
  """)
except Exception as e:
  print(e)
  print("Posts table already exists. Not recreating it.")

try: 
  cursor.execute("""
    CREATE TABLE Users( 
      userID int AUTO_INCREMENT PRIMARY KEY,
      googleID TEXT NOT NULL,
      email VARCHAR (20) NOT NULL,
      name  VARCHAR (20) NOT NULL,
      lastName VARCHAR (20) NOT NULL,
      urlToProfilePic TEXT NOT NULL
   );
  """)
except Exception as e:
  print(e)
  print("Users table already exists. Not recreating it.")

try: 
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Messages (
     index int AUTO_INCREMENT PRIMARY KEY,
     date TEXT NOT NULL,
     message TEXT NOT NULL,
     receiverUserID int NOT NULL,
     senderUserID int NOT NULL
    );   
  """)

except Exception as e:
  print(e)
  print("Messages table already exists. Not recreating it.")



db.close()
