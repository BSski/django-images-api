<p align="center">
  <h2 align="center">DjangoImagesAPI</h2>
</p>


<div markdown="1" align="center">


[![Build Status](https://bsski.semaphoreci.com/badges/DjangoImagesAPI/branches/main.svg?style=shields&key=0adba4be-b67c-416d-802b-90f43f19ff0f)](https://bsski.semaphoreci.com/projects/DjangoImagesAPI)
[![Demo Uptime](https://img.shields.io/uptimerobot/ratio/7/m792080634-601b784c89ee78a144c83275)](https://django-music-bsski.herokuapp.com/)
[![Heroku](https://pyheroku-badge.herokuapp.com/?app=django-images-api-bsski&style=flat)](https://django-images-api-bsski.herokuapp.com/)
[![Maintainability](https://api.codeclimate.com/v1/badges/a84055e6e49ddb02653e/maintainability)](https://codeclimate.com/github/BSski/DjangoImagesAPI/maintainability)
[![CodeFactor](https://www.codefactor.io/repository/github/bsski/djangoimagesapi/badge)](https://www.codefactor.io/repository/github/bsski/djangoimagesapi)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
</div>


<h3 align="center">
  :fireworks: Live demo :fireworks:
</h3>

<p align="center">
  https://django-music-bsski.herokuapp.com/
</p>

<p align="center">
Live demo's admin credentials are available upon request.
</p>




## Table of contents
* [Project description](#scroll-project-description)
* [Technologies used](#hammer-technologies-used)
* [Deployment](#hammer_and_wrench-deployment)
* [Environment variables](#closed_lock_with_key-environment-variables)
* [Features](#rocket-features)
* [Room for improvement](#arrow_up-room-for-improvement)
* [Author](#construction_worker-author)


## :scroll: Project description
This is a recruitment task for a Junior Python Developer position. The task was simple:
to create a Django admin-panel-only website, with two models (Author, Song) with a
many-to-many relationship between them, along with viewing and creating instances of
those models in the admin panel.

The database choice was arbitrary, but with a recommendation of an in-memory version.
While I believe it would make the task easier in for example Java's Spring, in Django it
doesn't. I decided to take the challenge and try to run Django with an in-memory database
only, and I succeeded. Every time the server is shut down, created model instances are
wiped. Every time the server is started, migrations are run and the admin account is
created automatically. I do realise that it is a nonstandard solution, but I still wanted
to try that, since the rest of the task was straightforward.

Besides that, I implemented automated testing in a CI/CD pipeline on SemaphoreCI, along
with dockerization and deployment from a container to Heroku.


## :hammer: Technologies used
- Python 3.7 & 3.8
- Django 3.2
- Django REST Framework 3.13.1
- PostgreSQL 14.2
- AWS S3
- AWS Lambda
- Gunicorn 20.1.0
- Docker
- SemaphoreCI
- Heroku
- dj-rest-auth with JWT Token


## :hammer_and_wrench: Deployment

A) through Docker:
1. Create an `.env` file basing on `.env_sample_file` from the repository.
2. Run `docker run --env-file .env -p 8020:8020 bsski/django-music:latest` in the `.env` file directory.
3. Access `localhost:8020`. 

B) without Docker:
1. Download the repository.
2. Create a virtual environment.
3. Run `pip install -r requirements.txt` in the directory of `requirements.txt`.
4. Create an `.env` file basing on `.env_sample_file` from the repository in the directory of `.env_sample_file`.
5. Run `python manage.py runserver --noreload` in the directory of `manage.py`.
6. Access `127.0.0.1:8000`.

The admin panel can be found under your chosen URL or, if you didn't set it in the .env file, the default `/hidden_admin_url`.
Security through obscurity is not enough of course, but I find it a nice complementary solution.


## :closed_lock_with_key: Environment variables

To run this project, you have to set up the following environment variables in the `.env` file (**the values below are exemplary**):
```
SECRET_KEY=TestSecretKey
AWS_S3_REGION_NAME=eu-central-1
AWS_S3_ADDRESSING_STYLE=virtal
AWS_S3_SIGNATURE_VERSION=s3v4
AWS_ACCESS_KEY_ID=MFAA21AFHG9AFKA2AEY
AWS_SECRET_ACCESS_KEY=13Fjm32eam23k23Qf432fDFda9saf
AWS_STORAGE_BUCKET_NAME=main-bucket
AWS_THUMBNAILS_STORAGE_BUCKET_NAME=thumbnails-bucket
DEFAULT_FILE_STORAGE=storages.backends.s3boto3.S3Boto3Storage
PORT=8020
ADMIN_LOGIN_URL=test_admin_login_url
DJANGO_SUPERUSER_PASSWORD=TestAdminPassword
DJANGO_SUPERUSER_USERNAME=TestAdminName
DJANGO_SUPERUSER_EMAIL=TestAdmin@email.com
```


## :rocket: Features
- two models in a many-to-many relationship (Author, Song),
- django admin panel which enables creating instances of models and viewing them,
- purely in-memory database.

Furthermore, the website is deployed on Heroku from a Docker image using a CI/CD SemaphoreCI pipeline:

![CI/CD screenshot](https://i.imgur.com/0NfYohr.png)


## :arrow_up: Room for improvement

Due to time limitation there are very important things left to add:
- Localstack to test and run app locally,
- tests,
- CI/CD: working dockerization and deployment to heroku,
- typehints,
- the code would also benefit from some cleaning.


## :construction_worker: Author

- [@BSski](https://www.github.com/BSski)
