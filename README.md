# Surgin - DRF

[![Python Version](https://img.shields.io/badge/python-3.9+-yellow.svg)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/django-4.2+-green.svg)](https://www.djangoproject.com/)
[![Django Version](https://img.shields.io/badge/drf-3.15+-blue.svg)](https://www.djangoproject.com/)

## Table of Contents
- [Description](#description)
- [Getting Started](#getting-started)
- [Dependencies](#dependencies)
- [Installation](#installing)
- [Executing program](#executing-program)
- [Help](#help)
- [Version History](#version-history)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Description

A powerful web-based music streaming platform featuring OpenAPI documentation and developed using DRF and JWT authentication

## Getting Started

### Dependencies

* Python 3.9+
* Docker (coming soon...)
* Git

### Installing

1. **Clone the repository:**

```bash
   git clone https://github.com/2yt-code/Surgin.git
   cd Surgin
```

2. **Create a Virtual Environment:**

```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux:
   source venv/bin/activate
```

3. **Install dependencies:**

```bash
   pip install -r requirements/development.txt
```

### Executing program


1. **Basic commands for creating a database:**

```bash
   python manage.py makemigrations
   python manage.py migrate
```

2. **Run Server asgi:**

```bash
   daphne config.asgi:application
```
For more information, visit the Daphne [GitHub repository](https://github.com/django/daphne)

## Help

To read the project documentation, go to the [docs](docs) folder or start the server and visit the `schema/swagger-ui` address

## Version History

* 0.1
    * Initial Release

## License

Released under the **MIT** license, See the [LICENSE](LICENSE) file