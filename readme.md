# Quizzy Backend

[![Django CI](https://github.com/carinaesoft/quizyBackend/actions/workflows/django.yml/badge.svg?branch=master)](https://github.com/carinaesoft/quizyBackend/actions/workflows/django.yml)

A robust Django REST Framework backend for the Quizzy quiz application, providing comprehensive APIs for managing quizzes, questions, results, and game logic.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Database](#database)
- [Docker](#docker)
- [Contributing](#contributing)
- [License](#license)

## Overview

Quizzy Backend is a Django-based REST API server designed to power the Quizzy quiz application. It handles quiz management, question administration, user results tracking, and game logic implementation with support for multiple locales.

## Features

- 📝 **Quiz Management**: Create, read, update, and delete quizzes
- ❓ **Question Management**: Manage questions with hierarchical structure (using django-mptt)
- 📊 **Results Tracking**: Store and retrieve user quiz results
- 🎮 **Game Logic**: Custom game logic implementation
- 🌍 **Multi-Language Support**: Locale/internationalization support
- 🔐 **CORS Support**: Cross-Origin Resource Sharing enabled
- 📦 **Admin Interface**: Enhanced admin with Grappelli UI
- 🖼️ **Image Processing**: Built-in image handling with ImageKit
- ⚡ **Production Ready**: Configured with Gunicorn and WhiteNoise

## Tech Stack

- **Framework**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Database**: PostgreSQL (via psycopg2)
- **Web Server**: Gunicorn 21.2.0
- **Image Processing**: Pillow 9.0.1, django-imagekit 5.0.0
- **Admin UI**: Grappelli 3.0.8
- **Static Files**: WhiteNoise 5.2.0
- **Utilities**: django-mptt, django-cors-headers, django-extensions, django-environ

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL (or SQLite for development)
- pip

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/carinaesoft/quizyBackend.git
   cd quizyBackend
