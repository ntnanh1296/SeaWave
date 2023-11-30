curl -X POST http://localhost:8000/api/users -H "Content-Type: application/json" -d '{
  "email": "user1@gmail.com",
  "username": "user1",
  "password": "user1",
  "gender": "Male",
  "birthday": "1996-01-01"
}'



curl -X GET http://127.0.0.1:8000/api/users/1 



curl -X POST -H "Content-Type: application/json" -d '{"email": "user2@gmail.com", "password": "user2"}' http://127.0.0.1:8000/api/users/login/