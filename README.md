# 🚀 DevOps Note-Taking App (CI/CD Pipeline)

A modern, containerized web application built with Python (Flask) and SQLite, designed specifically to demonstrate a complete Continuous Integration (CI) workflow using Jenkins and Docker.

## 🛠️ Technologies & Tools Used
* **Application:** Python, Flask, HTML/CSS (Glassmorphism UI)
* **Database:** SQLite
* **Containerization:** Docker
* **CI/CD:** Jenkins (Declarative Pipeline)
* **Version Control:** Git & GitHub

## 🔄 Pipeline Architecture (CI)
This project includes a `Jenkinsfile` that automates the following stages:
1. **Checkout Code:** Pulls the latest source code from the `main` branch.
2. **Build Docker Image:** Builds a lightweight, optimized container image for the Flask app.
3. **Push to DockerHub:** Authenticates and pushes the tagged image (using Jenkins Build ID) to the DockerHub registry.
4. **Clean up:** Removes local images and clears the workspace to save server storage.

## 💻 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/NotesApp.git](https://github.com/your-username/NotesApp.git)
   cd NotesApp