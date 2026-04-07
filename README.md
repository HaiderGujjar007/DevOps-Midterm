# Student Information Portal - Docker Web Application

**Student:** Haider Rasheed  
**Registration No:** FA23-BCS-058  
**Assignment:** Setting Up and Running a Web Application with Docker

---

## Project Structure

```
docker-webapp/
├── app/
│   ├── app.py            # Flask web application
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile        # Container config for web app
├── mysql-init/
│   └── init.sql          # Database schema + student data
├── docker-compose.yml    # Orchestrates both services
└── README.md
```

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- No additional software needed

---

## How to Run

### Step 1 — Open a terminal in the project folder

```bash
cd docker-webapp
```

### Step 2 — Build and start the containers

```bash
docker-compose up --build
```

Wait until you see:
```
student_web | * Running on http://0.0.0.0:5000
```

### Step 3 — Open the web application

Go to your browser and visit:

```
http://localhost:5000
```

### Step 4 — Search for a student

In the search box, type:

```
FA23-BCS-058
```

Press **Search** or hit **Enter** — the student's full profile will appear.

---

## How to Stop

```bash
docker-compose down
```

To also delete the database volume:
```bash
docker-compose down -v
```

---

## How It Works

| Component | Technology | Role |
|-----------|------------|------|
| Web App | Python Flask | Serves the UI and handles search requests |
| Database | MySQL 8.0 | Stores student records, subjects, transcripts |
| Containerization | Docker | Packages each service into isolated containers |
| Orchestration | Docker Compose | Runs both containers together with networking |

### Data Flow
1. User enters registration number in browser
2. Flask app queries MySQL database
3. Student info (name, subjects, CGPA) is returned
4. Results are displayed on the web page

---

## Database Schema

```sql
students         -- First name, last name, registration number
subjects         -- Subject names and grades per student
transcripts      -- CGPA and semester info per student
```

---

## Pre-loaded Student Data

| Field | Value |
|-------|-------|
| Name | Haider Rasheed |
| Registration No | FA23-BCS-058 |
| CGPA | 3.72 |
| Semester | Fall 2024 |
| Subjects | DBMS, OS, Web Tech, DSA, Software Engineering |
.......