# Student management system
This is a student management system that allows you to:
- Crud operations on students
- **Upload and image for a student (AWS S3)**
- **Email students (in microservice manner)**
- View a student grade and average
- Filter students
- etc..

## Tech Stack
* **Backend**: FastApi (python)
* **Database**: Postgres
* **Containerization**: Docker
* **Cloud**: AWS (EC2, S3)
* **Security**: JWT 
* _microservices: email service_

## Includes: 
    1. Pagination and sorting
    2. JWT authentication
    3. Database connectivity via Postgres
    4. Email service (**microservice**)
    5. AWS integration (S3)
    6. Dockerized and  deployed to AWS



## Run Locally (Docker)
* note: you need to have docker installed

Clone the project 

```bash
  git clone git@github.com:NatanGer97/StudentManagementPy.git
```

Go to the project directory

```bash
  cd my-project
```

run docker-compose 
```bash
  docker-compose docker-compose up -d
```

## Run Locally with docker image only

