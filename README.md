NEW DOCKER RUNNING INSTRUCTIONS
1. [docker-compose up --build]
2. if running first time open second terminal after this ^ command
   and run [docker exec -it agile-web bash]
   then inside the new bash that comes up run [python init_db.py]
3. go to [http://localhost:5000/]

OLD VIRTUAL_ENV Running Instructions

1. clone repository and cd into the directory
2. create a virtual environment with [python3 -m venv my_venv]
3. activate the virtual environment with [source my_venv/bin/activate]
4. install requirements [pip3 install -r requirements.txt]
5. run [python3 app.py]
6. go to http://localhost:5000/ in browser
7. deactivate the virtual env with [deactivate]
