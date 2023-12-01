curl -X POST http://localhost:8000/api/users/ -H "Content-Type: application/json" -d '{
  "email": "user1@gmail.com",
  "username": "user1",
  "password": "user1",
  "gender": "Male",
  "birthday": "1996-01-01"
}'

curl -X POST http://localhost:8000/api/users/ -H "Content-Type: application/json" -d '{
  "email": "user3@gmail.com",
  "username": "user3",
  "password": "user3",
  "gender": "Male",
  "birthday": "1996-01-01"
}'



curl -X POST -H "Content-Type: application/json" -d '{"username": "user3", "password": "user3"}' http://localhost:8000/api/users/login/


curl -X GET http://127.0.0.1:8000/api/users/1 



curl -X POST -H "Content-Type: application/json" -d '{"email": "user2@gmail.com", "password": "user2"}' http://127.0.0.1:8000/api/users/login/


curl -X GET -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAxNDAyNTQ0LCJpYXQiOjE3MDEzOTg5NDQsImp0aSI6ImEwZWRlYTVjZjkwMTQwOGQ5ODk4YTIzMzQ3YTgwOWNjIiwidXNlcl9pZCI6MX0.UIEJUHNNxtI-h95644uclI46bpIEO60qdcLw0TuRKCk" http://localhost:8000/api/users/4/


curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAxNDAyNTQ0LCJpYXQiOjE3MDEzOTg5NDQsImp0aSI6ImEwZWRlYTVjZjkwMTQwOGQ5ODk4YTIzMzQ3YTgwOWNjIiwidXNlcl9pZCI6MX0.UIEJUHNNxtI-h95644uclI46bpIEO60qdcLw0TuRKCk" -d '{"username": "new_username", "email": "new_email@example.com", "gender": "new_gender", "birthday": "new_birthday"}' http://localhost:8000/api/users/2/
