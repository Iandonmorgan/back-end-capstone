![SONGWRYTR](./songwrytr_logo.png)

A back-end capstone project from [Landon Morgan](https://github.com/iandonmorgan) for [Nashville Software School Web Development Cohort 38](https://github.com/nss-day-cohort-38)

![SONGWRYTR Compositions Macbook Air](./macbook_SONGWRYTR.png)

## Using SONGWRYTR

A user can create an account, log-in, and enter data for Writers, Publishing Companies, and Compositions. User-specific data can be created, read, updated, and deleted. Users are able to search compositions based on titles, lyrics, and notes entered.

<img align="left" src="./iPhone_SONGWRYTR.png" alt="SONGWRYTR Dashboard iPhone">

The first time a user logs in, their dashboard is empty, but for users with data entered, the dashboard will display the most recent 5 recordings recorded and most recent 5 compositions written. The dashboard can be accessed by clicking the SONGWRYTR logo in the top left corner, if navigating other parts of the app.

Inside a composition, a user can attach or remove Writers and Publishing Companies, designating a percentage split based on their writing arrangement, as well as CRUD functionality for information tied to a recording of that composition, including link to recording audio, artwork. Info can be entered for all recordings on a specific composition, as a way to track recorded versions of a song.

I built SONGWRYTR in a way that limits writer splits to 100%, and publishing splits to 100%, for a total of 200%. Performance Rights Organizations, like BMI and ASCAP will manage split information differently, but the logic is effectively the same and I followed something closer resembling BMI’s method in creating my app.

To create ‘SONGWRYTR’ I used the front end languages: [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5), [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS), and [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript). Those power a lot of what you’re seeing, along with [Bootstrap](https://getbootstrap.com/docs/3.4/javascript/) for styling. Behind the scenes, I used [Python](https://docs.python.org/3/) with [Django](https://docs.djangoproject.com/en/3.0/) framework as my backend languages. Additional technologies I used were [git](https://git-scm.com/doc), [GitHub](https://github.com/), [TablePlus](https://tableplus.com/) and [SQLite3](https://www.sqlite.org/docs.html) to manage my [SQL](https://www.w3schools.com/sql/) database, and [VSCode](https://code.visualstudio.com/) as my code editor.

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

3. Run a database migration using the `migrate` command, below, to create a set of tables that Django maintains for user management.

```sh
python manage.py makemigrations songwrytrapp
python manage.py migrate
```

4. Load Performance Rights Organization fixtures by using command, `python manage.py loaddata PROs`
4. Start application using command, `python manage.py runserver`
4. Navigate browser to [http://localhost:8000](http://localhost:8000)

## Entity Relationship Diagram

![SONGWRYTR ERD](./SONGWRYTR_ERD.png)