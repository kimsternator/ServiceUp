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
cursor.execute("drop table if exists Users;")
cursor.execute("drop table if exists Images;")
cursor.execute("drop table if exists Chats;")
cursor.execute("drop table if exists Messages;")
# cursor.execute("drop table if exists Messages;")

# Create a TStudents table (wrapping it in a try-except is good practice)
try:
  print("Creating Posts Table")
  cursor.execute("""
    CREATE TABLE Posts (
    id              int AUTO_INCREMENT PRIMARY KEY,
    userID          INT NOT NULL, 
    title           VARCHAR (50) NOT NULL,
    description     TINYTEXT NOT NULL,
    price           VARCHAR (50) NOT NULL,
    tag             VARCHAR (50) NOT NULL,
    city            VARCHAR (50) NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  """)
except Exception as e:
  print(e)
  print("Posts table already exists. Not recreating it.")

try:
  print("Creating Users Table")
  cursor.execute("""
    CREATE TABLE Users ( 
      id                int AUTO_INCREMENT PRIMARY KEY,
      email             VARCHAR (50) NOT NULL,
      firstName         VARCHAR (50) NOT NULL,
      lastName          VARCHAR (50) NOT NULL,
      urlToProfilePic   TINYTEXT NOT NULL
   );
  """)
except Exception as e:
  print(e)
  print("Users table already exists. Not recreating it.")


try:
  print("Creating Images Table")
  cursor.execute("""
    CREATE TABLE Images ( 
      id                int AUTO_INCREMENT PRIMARY KEY,
      postID            INT NOT NULL,
      url_link          TINYTEXT NOT NULL
   );
  """)
except Exception as e:
  print(e)
  print("Images table already exists. Not recreating it.")

try:
  print("Creating Chats Table")
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Chats (
     id                 int AUTO_INCREMENT PRIMARY KEY,
     receiverID         int NOT NULL,
     senderID           int NOT NULL
    );   
  """)
except Exception as e:
  print(e)
  print("Chats table already exists. Not recreating it.")

try:
  print("Creating Messages Table")
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Messages (
     id                 int AUTO_INCREMENT PRIMARY KEY,
     chatID             int NOT NULL,
     message            VARCHAR (100) NOT NULL,
     receiverID         int NOT NULL,
     senderID           int NOT NULL,
     created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );   
  """)
except Exception as e:
  print(e)
  print("Messages table already exists. Not recreating it.")

db.close()
