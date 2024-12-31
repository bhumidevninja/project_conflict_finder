
# Projects API - README

## Overview

The Projects API provides functionality to manage projects while handling conflict detection and suggestions for project descriptions. It includes user-specific data and ensures dynamic inclusion of user information.

---

## Features

- **Dynamic User Inclusion**: Includes the `user` field in GET requests while excluding it in non-GET requests (e.g., POST, PUT).
- **Conflict Detection**: Validates new project descriptions against existing ones for potential conflicts.
- **Suggestions Generation**: Provides unique suggestions for improving project descriptions.
- **Keyword Generation**: Automatically generates keywords for projects based on their descriptions.

---

## Setup Instructions

### Prerequisites

1. Ensure you have **Python 3.8+** installed.
2. Install **pipenv** or **virtualenv** to manage your environment.

### Setup Steps

#### 1. Clone the repository

```bash
git clone https://github.com/your-repository-url.git
cd your-repository
```

#### 2. Create a Virtual Environment

Using `pipenv`:

```bash
pipenv install
pipenv shell
```

Or using `virtualenv`:

```bash
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scriptsctivate  # For Windows
pip install -r requirements.txt
```

#### 3. Configure Environment Variables

Create a `.env` file in the root of the project and add the following environment variables:

```
# .env file

# Django settings
SECRET_KEY=your_django_secret_key
DEBUG=True
HUGGING_FACE_TOKEN= hugging face api token
GROQ_API_KEY = suggestion api key


#### 4. Apply Migrations

Run the following command to apply database migrations:

```bash
python manage.py migrate
```

#### 5. Start the Development Server

Now you can run the Django development server:

```bash
python manage.py runserver
```

This will start the server at `http://127.0.0.1:8000`.

---

## Notes

- Ensure the `Projects` model has fields matching the serializer.
- Use appropriate authentication and permissions for user-specific data.