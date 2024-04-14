# DynamicElectricityPriceControl

The script is very basic right now, but will be more advanced in the future. 
Its a beta phase, the code is not very beautiful and not following basic coding conventions, but will be corrected. 

Download the files to a directory of your choice:



1. Start a docker container with postgre SQL.
   You need to adapt the volume to your needs. Please choose a safe password instead of secret123$%&.
   
docker run -d --name postgres-heatpump -e POSTGRES_PASSWORD=secret123$%& -e PGDATA=/var/lib/postgresql/data/pgdata -v /intenso/docker/volumes/postgre:/var/lib/postgresql/data --network nextcloudpi -p 8071:8080 -v /etc/timezone:/etc/timezone:ro -v /etc/localtime:/etc/localtime:ro -p 5432:5432 postgres

Also adapt the database.ini file with that password.

2.  Init the database with


3. Install requirements
   
python -m pip install -r requirements.txt

4. Adapt the .env file. Put in your data in the .env.example file and delete the ending .example. The file name should be .env

5. Test the script
python3 daily.py 
python3 minutely.py

This should not invoke any error

6. set cron jobs: 
00 16 * * * python3 /intenso/docker/volumes/postgre/python/daily.py
*/1 * * * *  python3 /intenso/docker/volumes/postgre/python/minutely.py 
