# How to deploy

1. git clone git@github.com:missterr/recommendations-test-task.git
2. cd recommendations-test-task/recommendations
3. docker-compose up -d --build (movies import can take up to 50 minutes)
4. Login in using any http client that can handle cookies:
```
POST /users/login/ HTTP/1.1
Host: localhost:8010
Content-Type: application/json

{"username": "user2@test.com", "password": "1Qwertyu"}
```

5. Recommendation request (sessionid received on the previous step):
```
GET /users/recommendations/ HTTP/1.1
Host: localhost:8010
Cookie: csrftoken=uG4hQLzJluxAcHSjwfjpLMDWV0h40uuSlSgY0J9IBeebxRbYYJ6eLjVuBZVOvSJx; sessionid=25r15oynxu5ebbrz01j6x4lq4zq41dl4
```

Admin panel is accessible http://localhost:8010/admin/
