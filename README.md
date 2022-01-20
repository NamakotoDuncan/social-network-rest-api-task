## Description
Create a simple REST API based social network in Django
where Users can sign up and create text posts, as well as view, like, and unlike other
Users’ posts.

## General Notes
- Used Celery and Redis for background tasks
- user password stored as plaintext
- No pagination of api response
- Use of sqlite as datastore 
- No api versioning
- No data caching
- No exception handling in views

## Basic models:
- User
- Post (CRUD by a user)
- PostLikes - Track Post Likes

## Basic Features:
- user signup
- user login
- get user information
- post creation
- post like
- post unlike
- post update
- post delete


## Requirements:
- Implement token authentication using JWT

## API Endpoints:
- [POST] /api/signup - User signup endpoint
- [POST] /api/login - Login endpoint
- [GET]  /api/user/<USER-ID> Get user information
- [POST] /api/post-create/ (POST) - create new post
- [GET]  /api/post - List all Posts
- [GET]  /api/post/<post-id> - get Post by id
- [POST]  /api/post/<POST-ID> like or unlike a Post
- [PUT]  /api/post/<POST-ID> - Update post with Id
- [DELETE]  /api/post/<POST-ID> - delete post with Id


## Setup
### Environment variables
#### check .env.example file

### Run application without docker
set up virtualenv 
- https://gist.github.com/Geoyi/f55ed54d24cc9ff1c14bd95fac21c042

### Install dependencies
pip install -r requirements.txt
### Migrations
python manage.py makemigrations

### Run Unit Tests
python manage.py test

### Run application
python manage.py runserver

## Docker Commands
- Build: docker-compose up --build
- Run: docker-compose up
- Remove: docker-compose down -v
- docker system prune (-f)

## Sample Api Calls
### Login
curl -X POST -H 'Content-Type: application/json' -i http://localhost:8000/api/login --data '{
    "email": "newuser@test2.com",
    "password": "1234563"
}








