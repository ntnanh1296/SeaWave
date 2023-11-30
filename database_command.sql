# Login

psql -h localhost -p 5432 -d seawave_db -U sqladm

# list all table

\dt

python3 manage.py migrate user_service zero
python3 manage.py makemigrations user_service
python3 manage.py migrate