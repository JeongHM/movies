## Movies API
영화 정보 API 로써 아래와 같은 API 와 API 문서 (swagger) 를 제공합니다.

1. [GET] http://127.0.0.1:5050/api/v1/movies
    - 전체 영화 정보를 조회합니다.
2. [POST] http://127.0.0.1:5050/api/v1/movies
    - 영화 정보를 저장합니다.
3. [PUT] http://127.0.0.1:5050/api/v1/movies
    - 전체 영화 정보를 업데이트 합니다.
4. [DELETE] http://127.0.0.1:5050/api/v1/movies
    - 전체 영화 정보를 삭제합니다.
5. [GET] http://127.0.0.1:5050/api/v1/movies/{movie_id}
    - 특정 영화 정보를 조회합니다.
6. [Swagger] http://127.0.0.1:3030/docs


### 1. Technology Stack

| Component         | Technology           |
| ----------------- | -------------------- |
| API Documentation | Swagger-UI (Node.js) |
| Backend           | Python 3.7 (Flask)   |
| Container         | Docker-compose       |
| Database          | Sqlite3              |

### 2. File Structure

```markdown

├── dockerfiles             # dockerfile 정보
├── swagger                 # swagger docs
│   └── ...                 
├── src
│   └── api
│       ├── common          # API 내 공용 모듈
│       └── v1
│           ├── controllers # 컨트롤러 
│           ├── services    # 비지니스 로직
│           ├── model       # 모델 로직 
│           ├── testcases   # 테스트 케이스
│           └── validators  # 검증 
├── .gitignore
├── application.py
├── docker-compose.yaml
├── README.md
├── start.sh                # 시작 스크립
└── requirements.txt
```

### 3. How to Start
1. Clone Repository

    원격 저장소의 코드를 가져옵니다. 
    ```shell script
    $ git clone https://github.com/JeongHM/movies.git 
    ```
   
2. Start Application, Swagger
    1. Docker-compose 로 실행하지 않는 경우
        ```shell script
        # application 실행 [path: <your_path>/movies] 
        $ FLASK_APP=src/application.py port=5050 flask run --port 5050
       
        # swagger 실행 [path: <your_path>/movies/swagger]
        $ npm install
        $ node index.js
        ```
       
    2. Docker-compose 로 실행하는 경우 
        - docker, docker-compose 가 설치되어있는 경우에 사용이 가능합니다.
        - 쉘 스크립트 사용 시 포트, 컨테이너를 확인합니다.
        - 확인 후 컨테이너를 실행합니다.
        
        ```shell script
        # path: <your_path>/movies
        
        $ sh start.sh
        ```
       
3. Check API, Swagger
    1. application
        
        http://127.0.0.1:5050/api/v1/movies
        
    2. swagger
     
        http://127.0.0.1:3030/docs
        
4. How to Test API
    1. Swagger
        1. http://127.0.0.1:3030/docs 접속
        2. 위 문서로 테스트를 진행합니다. 
        
    2. Test 
        1. 어플리케이션을 실행시켜줍니다. (3번 참고)
        2. 아래 명령어를 실행시켜줍니다.
        ```shell script
        $ python3 -m unittest src/api/v1/testcases/movies.py
        
        ..........
        ----------------------------------------------------------------------
        Ran 10 tests in 0.226s

        OK  
        ```
        
