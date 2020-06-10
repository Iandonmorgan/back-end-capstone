![SONGWRYTR](./songwrytr_logo.png)

A back-end capstone project from [Landon Morgan](https://github.com/iandonmorgan) for [Nashville Software School Web Development Cohort 38](https://github.com/nss-day-cohort-38)

## Brief Proposal

Songwriters create intellectual property in the form of songs. This app will solve the problem of tracking information associated with creating this IP, including co-writer(s), percentage split(s), publisher(s), performance rights organization(s), and licensing contact information, specific to each user (songwriter).

## Project Definition

* FULL STACK application written in PYTHON using DJANGO framework
* Ability to create, read, update, and delete user-specific data

## Setup

Steps to get started:
1. `git clone git@github.com:iandonmorgan/back-end-capstone.git`
1. `cd` into directory created and `cd` into `songwrytrapp` directory where the `manage.py` file is; set up your virtual environment:

#### Mac users, run the following:
```sh
python -m venv songwrytrenv
source ./songwrytrenv/bin/activate
pip install django
pip freeze > requirements.txt
```
#### Windows users, run the following:
```sh
python -m venv songwrytrenv
source ./songwrytrenv/Scripts/activate
pip install django
pip freeze > requirements.txt
```
> Note the separate formats for the `source` command between Windows and Mac users. You will use this command each time you activate your virtual environment for this project.

1. Run a database migration using the `migrate` command, below, to create a set of tables that Django maintains for user management.

```sh
python manage.py makemigrations songwrytrapp
python manage.py migrate
```

1. Start application using command, `python manage.py runserver`
1. Navigate browser to [http://localhost:8000](http://localhost:8000)

## Entity Relationship Diagram

![SONGWRYTR ERD](./SONGWRYTR_ERD.png)