##### Create new user ######
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


##### Login User #####
curl -X POST -H "Content-Type: application/json" -d '{"username": "user3", "password": "user3"}' http://localhost:8000/api/users/login/

### Get a detail user ######
curl -X GET http://127.0.0.1:8000/api/users/1 

### Edit a detail user ######
curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAxNDMxMTczLCJpYXQiOjE3MDE0MDIzNzMsImp0aSI6IjEwMTlhZDg0NzY0NDRmZmI5NDVhNzMzNDE0NGZlYTEwIiwidXNlcl9pZCI6MX0.X4mzKD0ie6ojAAuyh9lrDgOV_G26EcC3a4q0_qF_tkk" -d '{"username": "new_username", "email": "new_email@example.com", "gender": "new_gender", "birthday": "new_birthday"}' http://localhost:8000/api/users/2/


### Delete a detail user ######
curl -X DELETE -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAxNDMxMTczLCJpYXQiOjE3MDE0MDIzNzMsImp0aSI6IjEwMTlhZDg0NzY0NDRmZmI5NDVhNzMzNDE0NGZlYTEwIiwidXNlcl9pZCI6MX0.X4mzKD0ie6ojAAuyh9lrDgOV_G26EcC3a4q0_qF_tkk" http://localhost:8000/api/users/3/




##### Create new post ####
curl --location 'http://localhost:8000/api/posts/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAxNTAyNDc1LCJpYXQiOjE3MDE0NzM2NzUsImp0aSI6ImJiMzEzZTM2MjFiNjQyZGQ5NDk2ZmExNzllYjc5MGRjIiwidXNlcl9pZCI6MX0.9qK05LuiYlV24XuOQ9YTW1QvYSlti2wXhloYBxZ_0XE' \
--form 'text="dasdfafdaf"' \
--form 'photo=@"/home/ntnanh/Pictures/Screenshot from 2023-11-23 15-39-39.png"'

#### Update the post #### 

curl --location --request PUT 'http://localhost:8000/api/posts/1/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAxNDQ4MDE1LCJpYXQiOjE3MDE0MTkyMTUsImp0aSI6ImUyYTU1OWRiOTQxYzRlNWJhYTE1ZThlZTUwYzdiZjI3IiwidXNlcl9pZCI6M30.vyg0fRPEi25auE6S5az3zhc3w8kXW8P3_4luqXtdOF0' \
--form 'text="dasdfafdaf"' \
--form 'photo=@"/home/ntnanh/Pictures/Screenshot from 2023-11-23 15-39-39.png"'

##### Get the post ####
curl --location 'http://localhost:8000/api/posts/1/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAxNTMxOTUyLCJpYXQiOjE3MDE1MDMxNTIsImp0aSI6IjI4YmMzMDBmOGExMTQ0M2M4ODhkM2NmYzk5NDEzOTk5IiwidXNlcl9pZCI6MX0.dw10y0R8Az2YCJbvaPGySycAsgqEiNi09BLQG1O1ra8'

##### Get all post ####
curl --location 'http://localhost:8000/api/posts/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAxNzAxOTM3LCJpYXQiOjE3MDE2NzMxMzcsImp0aSI6ImU2NjY3NjNmOWUxODQ5NzViMjcxYWIyMWU3MmNkNjc5IiwidXNlcl9pZCI6M30.S5qBPeSxob3FOK479xzPaXmNn6hWgPhhUVv2AAfQVFI'

##### Delete the post ####
curl --location --request DELETE 'http://localhost:8000/api/posts/1/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAxNDQ4MDE1LCJpYXQiOjE3MDE0MTkyMTUsImp0aSI6ImUyYTU1OWRiOTQxYzRlNWJhYTE1ZThlZTUwYzdiZjI3IiwidXNlcl9pZCI6M30.vyg0fRPEi25auE6S5az3zhc3w8kXW8P3_4luqXtdOF0'

##### Like a post ####
curl -X POST -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAxNTMxOTUyLCJpYXQiOjE3MDE1MDMxNTIsImp0aSI6IjI4YmMzMDBmOGExMTQ0M2M4ODhkM2NmYzk5NDEzOTk5IiwidXNlcl9pZCI6MX0.dw10y0R8Az2YCJbvaPGySycAsgqEiNi09BLQG1O1ra8" http://localhost:8000/api/posts/1/likes/



###### Create new comment ######

curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAxNTMxOTUyLCJpYXQiOjE3MDE1MDMxNTIsImp0aSI6IjI4YmMzMDBmOGExMTQ0M2M4ODhkM2NmYzk5NDEzOTk5IiwidXNlcl9pZCI6MX0.dw10y0R8Az2YCJbvaPGySycAsgqEiNi09BLQG1O1ra8" \
-d '{"text": "This is a new comment on the post."}' \
http://localhost:8000/api/posts/1/comments/



