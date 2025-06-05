# slovak_accounting
📘 Slovak Accounting System (SaaS-Ready)
This project is a modular accounting system designed for small and medium-sized businesses in Slovakia. Built with Django and Django REST Framework, it aims to provide full transparency and automation for bookkeeping tasks — with the potential to evolve into a SaaS product.

🔧 Key Features
Modular Architecture – Separate Django apps for:

Accounting (accounts, journal entries)

Orders and Sales

Document Management (incoming/outgoing, file uploads)

Custom User Authentication (with JWT)

RESTful API – All features are exposed via a clean and secure API, tested using pytest and APIClient.

JWT Authentication – Secure access for all endpoints using djangorestframework-simplejwt.

Test-Driven Development (TDD) – All backend logic is written through strict TDD practices.

Dockerized Environment – Easily deployable using Docker and Docker Compose.

📂 Technologies
Python 3.12+

Django 5.2

Django REST Framework

PostgreSQL (via Docker)

Pytest

SimpleJWT

Docker + Docker Compose

📁 Modules Overview
App	Description
accounting	Core accounting logic: chart of accounts, journal entries
orders	Order creation and confirmation with line items
documents	Upload and classify financial documents (invoices, etc.)
custom_user	Email-based authentication and user management

🚀 Roadmap
 Secure user authentication with JWT

 Basic accounting and journal logic

 Document upload and classification

 Suggest typical journal entries based on document type

 Admin interface for accountants and business users

 Monthly SaaS subscription support

📦 How to Run
bash
Копировать
Редактировать
docker compose up --build
docker compose run backend pytest
📜 License
This project is licensed under the MIT License.

