## Movies API


### Technology Stack

| Component         | Technology           |
| ----------------- | -------------------- |
| API Documentation | Swagger-UI (Node.js) |
| Backend           | Python 3.7 (Flask)   |
| Container         | Docker-compose       |
| Database          | Mysql                |
| Middleware        | Nginx                |

### File Structure

```markdown

├── dockerfiles             # dockerfile 정보
├── src
│   └── api
│       ├── common          # API 내 공용 모듈
│       └── v1
│           ├── controllers # 컨트롤러 
│           ├── services    # 비지니스 로직 
│           └── testcases   # 테스트 케이스
├── .gitignore
├── application.py
├── docker-compose.yaml
├── README.md
└── requirements.txt
```

### How to Start
1. Clone Repository
2. Start Shell
3. Check API, Swagger