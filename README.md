# Bounsic-dev
Development repository for a musical-web-app that uses scrapping as its core. 
All services are found here.

# Bounsic

**Bounsic** is a modern, interactive platform for music playback and analysis, built with new technologies. The project follows a modular architecture to support scalable development, testing, and deployment.

---

## Authors

- **Juan David Patiño Parra** - juandavidp1127@gmail.com  
- **Juan David Carvajal Rondón** - juandacr25@gmail.com  
- **Christian Mauricio Rodriguez Curubo** - cmrcurubo@gmail.com  
- **Jose Daniel Montero Gutierrez** - jmontero.gutierrez2002@gmail.com  

---

## Project Structure

```
bounsic/
├── bounsic-front/       # Frontend (React + Bun)
├── bounsic-back/        # Backend (FastAPI + Python)
├── streaming/           # Streaming (FastAPI + Python)
├── package.json         # Global scripts and dependencies
└── README.md            # Project documentation
```

---
## Tech

![Bun](https://img.shields.io/badge/Bun-%23000000.svg?style=for-the-badge&logo=bun&logoColor=white)
![Angular](https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-00758F?style=for-the-badge&logo=mysql&logoColor=white)
![Azure](https://img.shields.io/badge/Microsoft%20Azure-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwind-css&logoColor=white)
---
## Installation

### Requirements

- [Bun](https://bun.sh/)
- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/) (For Angular)
- [TypeScript](https://www.typescriptlang.org/)
- [PowerShell](https://learn.microsoft.com/en-us/powershell/) (Windows) or [Bash](https://www.gnu.org/software/bash/) (Linux/Mac)
- [Git](https://git-scm.com/)

### Full Installation (Frontend + Backend + Streaming)

#### On Windows

```bash
bun run install
```

#### On Linux (Ubuntu)

Due to the cmd commands this is neccesary.
```bash
bun run install_linux
```
This will run the same commands as Windows with linux cmd

---

## Running the Project

### On Windows

```bash
bun run start
```

This will launch both the **frontend** , **backend** and **streaming** simultaneously using `concurrently`.

### On Linux (Ubuntu)

```bash
bun run start_linux
```

## All Scripts

| Script                             | Description                                                                                      |
|------------------------------------|--------------------------------------------------------------------------------------------------|
| `bun run install:frontend`         | Installs frontend dependencies                                                                   |
| `bun run install:backend`          | Sets up a Python virtual environment and installs backend dependencies (Windows)                 |
| `bun run install:streaming`        | Sets up a Python virtual environment and installs streaming dependencies (Windows)               |
| `bun run install:backend_linux`    | Same as above but for Linux (Ubuntu)                                                                 |
| `bun run install:streaming_linux`  | Same as above but for Linux (Ubuntu)                                                                 |
| `bun run install`                  | Installs all dependencies: frontend, backend, and streaming                                      |
| `bun run install_linux`            | Installs all dependencies for Linux: frontend, backend, and streaming                      |
| `bun run start:frontend`           | Starts the frontend app                                                                          |
| `bun run start:backend`            | Starts the backend server (Windows)                                                              |
| `bun run start:streaming`          | Starts the streaming service (Windows)                                                           |
| `bun run start:backend_linux`      | Starts the backend server (Linux)                                                          |
| `bun run start:streaming_linux`    | Starts the streaming service (Linux)                                                       |
| `bun run start`                    | Starts all services (frontend, backend, and streaming) concurrently                             |
| `bun run start_linux`              | Starts all services for Linux (frontend, backend, and streaming) concurrently              |
| `bun run test:frontend`            | Runs frontend tests                                                                               |
| `bun run test:frontend_linux`      | Runs frontend tests on Linux (with Chromium configured for headless testing)               |
| `bun run test:backend`             | Runs backend tests (Windows)                                                                     |
| `bun run test`                     | Runs all tests for frontend and backend concurrently                                            |

---

## License

This is a private project developed for academic and experimental purposes.

Anyways, authors ask for respect by **not using, copying, or distributing this code without explicit permission**.
