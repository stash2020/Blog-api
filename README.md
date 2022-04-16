# Blog API

A REST API for blog built using Django Rest Framework

## Installation

### Requirements
- Python
- Django

    Complete list available in requirements.txt file

### Quickstart
- Clone the repo.  
    ```bash
    git clone https://github.com/stash2020/Blog-api.git
    ```

- Inside the blog folder, make a virtual environment and activate it 
    
    bash
    ```
    cd blog
    python -m venv env 
    source env/bin/activate
    ```
    windows
    ```
    cd blog
    virtualenv venv
    venv\Scripts\activate.bat
    ```

- Install requirements from requirements.txt
    ```
    pip install -r requirements.txt
    ```

- Makemigrations and migrate the project
    ```
    python manage.py makemigrations && python manage.py migrate
    ```

- Create a superuser
    ```
    python manage.py createsuperuser
    ```

- Runserver
    ```
    python manage.py runserver
    ```

**Note: After running the server, you can use the api inside browser or you can use Postman to make api calls. 
Make sure in each api call, you provide username, password by creating a user.**


## With Docker

- pull image
  ```
  docker pull stashxander/drf_blog
  ```
  
- run container
  ```
  docker run -d -p 8080:8000  --name drf_blog_app drf_blog
  ```
**Note: with docker Port is 8080**



# RESTAPI Docs
I have added `drf-yasg` for API documentation which can be accessed after running the backend server and going to following links:

Swagger UI docs:    http://127.0.0.1:8000/swagger/

Redoc UI docs:  http://127.0.0.1:8000/redoc/

While working with api in browser, you can login using `http://127.0.0.1:8000/api-auth/login` link.


## API
<details>
<summary> User model </summary> 

- User:
    - username: string(unique),
    - password: string(min 8 chars)

</details>

<details>
<summary> Post Model </summary>

- Post:
    - id: Post id(read only),
    - title: string,
    - author: user-id(read only),
    - body: string,
    - created_at: datetime(read only)
    - updated_at: datetime(read only)
</details>

<details>
<summary>Comment Model </summary>

- Comment:
    - parent: post id(read only),
    - author: user id(ready only),
    - body: string,
    - created_at: datetime(read only)
    - updated_at: datetime(read only)
</details>

<details>
<summary>Like Model </summary>

- Like:
    - parent: post id(read only),
    - author: user id(ready only),
    - created_at: datetime(read only)
    - updated_at: datetime(read only)
</details>



### Endpoints

| Function                                | REQUEST    | Endpoint                                                 | Authorization |
|-----------------------------------------|------------|----------------------------------------------------------|---------------|
| Create new user                         | POST       | http://127.0.0.1:8000/user/register/                     | Not Required  |
| Returns list of all existing users      | GET        | http://127.0.0.1:8000/user/                              | Basic Auth    |
| Details of an user instance             | GET        | http://127.0.0.1:8000/user/{int:id}/                     | Basic Auth    |
| Update the detail of an user instance   | PUT, PATCH | http://127.0.0.1:8000/user/{int:id}/                     | Basic Auth    |
| Delete an user instance                 | DELETE     | http://127.0.0.1:8000/user/{int:id}/                     | Basic Auth    |
|                                         |            |                                                          |               |
| List of all existing posts              | GET        | http://127.0.0.1:8000/posts/                             | Not Required  |
| Creates a new post instance             | POST       | http://127.0.0.1:8000/posts/create/                      | Basic Auth    |
| Details of a post instance              | PUT, PATCH | http://127.0.0.1:8000/posts/{int:id}/                    | Not Required  |
| Updates an existing post                | PUT, PATCH | http://127.0.0.1:8000/posts/{int:id}/                    | Basic Auth    |
| Deletes the existing post               | DELETE     | http://127.0.0.1:8000/posts/{int:id}/                    | Basic Auth    |
|                                                                                                                                 |
| List of comments on a particular post   | GET        | http://127.0.0.1:8000/posts/{int:id}/comment/            | Not Required  |
| Create a comment instnace               | POST       | http://127.0.0.1:8000/posts/{int:id}/comment/create/     | Basic Auth    |
| Details of a comment instance           | GET        | http://127.0.0.1:8000/posts/{int:id}/comment/{int:id_2}/ | Not Required  |
| Updates an existing comment             | PUT, PATCH | http://127.0.0.1:8000/posts/{int:id}/comment/{int:id_2}/ | Basic Auth    |
| Deletes an existing comment             | DELETE     | http://127.0.0.1:8000/posts/{int:id}/comment/{int:id_2}/ | Basic Auth    |
|                                                                                                                                 |
| List of likes on a particular post      | GET        | http://127.0.0.1:8000/posts/{int:id}/like/               | Not Required  |
| Create a like instnace                  | POST       | http://127.0.0.1:8000/posts/{int:id}/like/create/        | Basic Auth    |
| Details of a like instance              | GET        | http://127.0.0.1:8000/posts/{int:id}/like/{int:id_2}/    | Not Required  |
| Updates an existing like                | PUT, PATCH | http://127.0.0.1:8000/posts/{int:id}/like/{int:id_2}/    | Basic Auth    |
| Deletes an existing like                | DELETE     | http://127.0.0.1:8000/posts/{int:id}/like/{int:id_2}/    | Basic Auth    |

