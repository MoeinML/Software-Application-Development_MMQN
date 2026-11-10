# Train Booking Project
## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Team Members](#team-members)
- [Weekly Progress & Milestones](#weekly-progress--milestones)
  - [Week 1: Project Scope, Requirement Analysis & Agile Setup](#week-1-project-scope-requirement-analysis--agile-setup)
  - [Week 2: Database Connectivity & Python Environment Setup](#week-2-database-connectivity--python-environment-setup)
  - [Week 3: Modular Architecture & Basic Data Logic](#week-3-modular-architecture--basic-data-logic)
  - [Week 4: Full Scope CRUD Implementation](#week-4-full-scope-crud-implementation)
  - [Week 5: Streamlit Multi-Page UI Design](#week-5-streamlit-multi-page-ui-design)
  - [Week 6: Input Validation & Automated Testing (pytest)](#week-6-input-validation--automated-testing-pytest)
  - [Week 7: Code Refactoring, Integration & Documentation](#week-7-code-refactoring-integration--documentation)
  - [Week 8: Final Presentation & Live Demo](#week-8-final-presentation--live-demo)
- [Installation & Setup Guide](#installation--setup-guide)

---

## 📖 Project Overview
Managing train schedules, seat allocations, station connections, passenger information, and ticket bookings manually or through raw SQL queries is complex and prone to errors. This application addresses these challenges by delivering an intuitive Graphical User Interface (GUI) built with **Streamlit**, connected directly to a **MySQL** database backend.

---

## 👥 Team Members
- **Moein Lahashinejad**
- **Bach Quyen**
- **Le Minh**
- **Navid Behazin**

---

## 🗓️ Weekly Progress & Milestones

### Week 1: Project Scope, Requirement Analysis & Agile Setup

#### 1. Group Discussion (Lecture 1)
* **Who would use the application?**
  * Train station operators, booking administrators, and passengers who need to view, book, and manage train tickets seamlessly.
* **Which ONE main entity would you manage?**
  * **BOOKING** (as the core transaction entity linking passengers, schedules, and specific seats).
* **What are the essential features?**
  * Registering passengers and viewing active itineraries.
  * Searching train schedules between specific stations and dates.
  * Reserving seats and updating booking statuses (e.g., Pending to Confirmed).
  * Canceling ticket reservations and removing logs safely.
* **What could go wrong if you start coding immediately?**
  * Lack of clear architecture leads to tight coupling between UI and SQL logic.
  * Risk of security flaws, such as hardcoding database credentials.
  * Misaligned database schemas and unhandled constraint violations during CRUD operations.
  * Wasted effort rebuilding features due to unverified user requirements.

---

#### 2. Group Activity & Project Setup (Lecture 2)
* **Selected Project:** End-to-End Train Booking Management System (reusing the normalized 3NF MySQL schema `trainbookingsystem`).
* **Main Entity & User:** `BOOKING` entity managed by Passengers and Booking Administrators.
* **Requirements:**
  * **Functional Requirement 1:** Passengers must be able to search for available train schedules by specifying departure station, arrival station, and date.
  * **Functional Requirement 2:** The system must allow users to reserve available seats and generate a unique booking record linked to the passenger ID.
  * **Functional Requirement 3:** Booking administrators must be able to update booking statuses (e.g., Pending to Confirmed).
  * **Functional Requirement 4:** Passengers must be able to cancel an active booking and free up the allocated seat.
  * **Non-Functional Requirement (Security & Performance):** Database connection credentials must be securely stored in environment variables (`.env`), and search queries must return within 2 seconds under standard load.
* **Kanban Board Initial Tasks:**
  1. Setup repository structure and `.gitignore` file.
  2. Configure Python virtual environment (`.venv`) and `.env` file.
  3. Write modular MySQL database connection module (`db.py`).
  4. Develop data operation module (`train_operations.py`).
  5. Build entry point application file (`main.py`).
  6. Design multi-page Streamlit dashboard interface.
  7. Implement input validation and `pytest` automated test suite.
* **Initial Responsibilities:** Collaborative development model — all team members co-develop and contribute across database connectivity, logic partitioning, UI development, and GitHub workflow.

---

### Week 2: Database Connectivity & Python Environment Setup

#### 1. Objectives & Learning Outcomes
* Created a dedicated Python project workspace and configured a virtual environment (`.venv`) for dependency isolation[cite: 80].
* Installed the `mysql-connector-python` package via pip to bridge Python application logic with the MySQL database server[cite: 80, 89].
* Implemented secure database connectivity parameters and tested successful data retrieval.

#### 2. Technical Implementation Steps
* **Virtual Environment & Dependencies:** Set up `.venv` to manage required libraries cleanly and documented dependencies in `requirements.txt`.
* **Database Connection Module (`db.py`):** 
  * Established secure communication with the local MySQL server using `mysql.connector`.
  * Utilized `python-dotenv` to load sensitive database credentials (`root` password) safely from an ignored `.env` file, preventing credentials exposure in version control.
* **Data Operations & Testing (`train_operations.py` & `main.py`):**
  * Created database cursors (`connection.cursor()`) to execute SQL statements[cite: 94].
  * Executed `SELECT` queries and processed query results using `fetchall()` to fetch and display train and booking records[cite: 80, 95].
  * Verified end-to-end execution flow from entry point `main.py` through modular operations.

#### 3. Verification & Deliverables
* Successfully executed test connections and verified live data retrieval from the `trainbookingsystem` database.
* Committed and synchronized all modular code files and configuration templates to the shared GitHub repository.







































## 1. Project Overview

This project aims to develop a Python-based application for managing and interacting with a MySQL database.

The main objective is to build basic database operations and gradually expand the system with additional features.

## 2. Current Progress

The MySQL database structure has been successfully implemented.

Basic Python scripts for interacting with MySQL have also been developed using the `getpass` and `mysql` modules.

The current implementation includes:

- Database connection.
- Password input using `getpass`.
- Data retrieval (SELECT).
- Data insertion (INSERT).
- Data deletion (DELETE).

## 3. Sample Code

The file `test_connection.py` contains sample Python code demonstrating database connection and basic data operations.

It serves as the starting point for further development.

## 4. Next Steps

The project is still under development. The next steps include:

- Improving and organizing the Python code.
- Developing reusable database modules.
- Implementing data update (UPDATE) functionality.
- Improving error handling and database connection management.
- Expanding database operations and application features.

## 5. Project Status

Status: IN PROGRESS

Further development is ongoing.

---

More updates and features will be added as the project progresses.
