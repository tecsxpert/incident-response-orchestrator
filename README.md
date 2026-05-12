# 🛡️ Incident Response Orchestrator

## 📖 Overview
A Spring Boot backend system for tracking, scoring, and managing security incidents. It features JWT authentication, 
automated risk scoring, and multi-part file attachment support.

## 🏗️ Architecture Diagram
```text
       [ USER ] <--- JWT ---> [ SWAGGER / API ]
                                  |
                                  v
    +-------------------------------------------------------+
    |                SPRING BOOT APPLICATION                |
    |  +------------+      +-------------+      +---------+ |
    |  | Security   | ---> | Controllers | ---> | Service | |
    |  +------------+      +-------------+      +----+----+ |
    +------------------------------------------------|------+
                                                     v
                 +-----------------+        +-----------------+
                 |   POSTGRESQL    |        |  LOCAL STORAGE  |
                 |  (Incidents)    |        |   (/uploads)    |
                 +-----------------+        +-----------------+

🛠️ Prerequisites
JDK 17
Maven 3.8+
PostgreSQL 15+
Redis (Optional for caching)

🚀 Setup Steps
Clone the Repo: git clone <your-repo-link>
Database: Create a DB named incident_db in PostgreSQL.
Environment: Create your environment variables or update application.yml.
Run: Execute mvn spring-boot:run in the terminal.
Access: Open http://localhost:8080/swagger-ui.html.

---

### 🔑 .env.example Reference Table

| Variable | Description | Example Value |
| :--- | :--- | :--- |
| `DB_URL` | JDBC URL for Postgres | `jdbc:postgresql://localhost:5432/incident_db` |
| `DB_USER` | Database Username | `postgres` |
| `DB_PASS` | Database Password | `your_password` |
| `JWT_SECRET` | Secret Key (Base64) | `dGhpcy1pcy1zZWNyZXQtMjg0OTI=` |
| `MAIL_PASS` | SMTP Password | `ffbc50a7bda518` |

---