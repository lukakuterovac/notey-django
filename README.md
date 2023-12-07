# Notey

Notey is a Django web application for writing notes and managing tasks on projects.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Tests](#tests)

## Prerequisites

Tools and packages required to successfully install this project:

- Python 3 [Install](https://www.python.org/)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages required for running Notey.

1. Clone the repository:

```bash
git clone https://github.com/lukakuterovac/notey-django.git
cd notey-django
```

2. Create a virtual environment:

For Linux or macOS:

```bash
python3 -m venv env
source env/bin/activate
```

For Windows:

```bash
python -m venv env
source env/Scripts/activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

4. Apply database migrations:

```bash
cd notey
python manage.py migrate
```

## Usage

1. Start the development server:

```bash
python manage.py runserver
```

2. Access the application in a web browser by navigating to http://localhost:8000/.

## Tests

Run tests using the following command:

```bash
pytest .\app\tests.py --html=reports/pytest-report.html
coverage run -m pytest .\app\tests.py
coverage html -d reports\coverage
```

Reports can be found in reports directory inside the project folder.
