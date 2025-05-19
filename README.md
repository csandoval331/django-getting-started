# Following djangoProject tutorial: https://docs.djangoproject.com/en/5.1/intro/tutorial01/
- first, create your virtual environment and install django
```bash
:: this command lets you choose which python version to use and the destination folder name
python3 -m virtualenv -p /usr/bin/python3.10 ./venv

:: this command for default settings. Note, default system python will be used. In my case, it is python3.12.3.final.0-64
virtualenv venv

:: Now, we initialize virtual environment.
source venv/bin/activate

:: install django
pip install django

:: check django version
python -m django --version
```

- create working dir for your project and generate a new django project
```sh
mkdir getting-started
django-admin startproject mysite getting-started
```

- analyze the django framework file structure `tree -L 2`
```bash
(env):$ tree -L 2 getting-started/
getting-started/
├── manage.py
└── mysite
    ├── asgi.py
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```
- `mysite/` - project directory
-  `mysite/__init__.py` - an empty file that tells python that this project should be considered as a python package
    - __myinit__.py can be an empty file or could contain init code for package
    - [More about python packages](https://docs.python.org/3/tutorial/modules.html#tut-packages)
    - Dotted Module Name -  
- `mysite/settings.py` - will have config settings for webapp
- `mysite/urls.py` - here you can define your urls declarations. **Note from site:** Good URL should not change
- `mysite/asgi.py` - an entry point for asgi-compatible web servers to server your project 
    - **ASGI webserver:** Asynchronous Server Gateway Interface - an asynchronous webserver that can efficiently handle multiple concurent request, especially with features such as websockets and long-polling
- `mysite/wsgi.py`: Web Server Gateway Interface - It is a standard that defines how web servers (nginx, apache) and web frameworks (djang and flask) can work indepently from each other 

# Projects vs App
- A project is a collection of configurations and apps for a particular webapp
- An app is a web application that does something

# creating the app `polls` for your project and adding it to mysite/settins.py: INSTALLED_APPS: ["polls.apps.Polls"]
```sh
python manage.py startapp polls

## once app polls is created, we add it to mysite/settings.py: INSTALLED_APPS
INSTALLED_APPS = [
    "polls.apps.PollsConfig",
    "django.contrib.admin",
    ...
]
```

## Creating the 'polls/urls.py' file
- we will need to create urls.py file in polls
```py
    from django.urls import path
    from . import views


    urlpatterns = [
        path("", views.index, name="index")
    ]
```


# Once polls is created and added to myiste/settings.py, we run makemigration polls
- `python manage.py makemigrations polls`

# update your database schema
- django will allow you to track changes made to your database. When adding new models, deleting them, or adding more fields to the model will require an update
- `python manage.py migrate`

# How to update your models in django
- make changes to your `models.py`
    ```py
    class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    ```
- `python manage.py makemigrations` - to create migrations files for when changes are made to database models. For example, if we had a class named cars with the elements make, model. But then if we needed to add total-mileage as an element, the migrate files would be created to help update the object cars in the database
    - python will generate files in migrations. Note, each new change to model will generate files [0001_init.py, 0002_model_change.py, ...]
- `python manage.py migrate` - python will co`mmit those changes to database
    - in my case, changes will be commited to the default database liteSQL

# Interacting with the database using django shell and using timezone
- `python manage.py shell`
```py
## import timezone library in order to create question with timezone
from django.utils import timezone

## import models
from polls.models import Choice, Question

import datetime
from django.utils import timezone

q = Question(question_text="Hello world", pub_date=timezone.now() )
q.save()
print(q , q.question_text )

q.was_published_recently()

q.choice_set.all()
q.choice_set.count()

## here we can find all the queries that are stored in Question
Question.objects.all()

## we use the question object to create the choice 
c1 = q.choice_set.create(choice_text="Not much", votes=0)
c = q.choice_set.get(pk=1)


print(timezone.now())
## output: 2025-02-26 22:55:04.055820+00:00
print(datetime.timedelta(days=1))
## output: 1 day, 0:00:00 
```

# GettingStarted - part 3 : creating views with functionality
- Views are the functions that take in a request and return a response
- "Your view can read records from a database, or not. It can use a template system such as Django’s – or a third-party Python template system – or not. It can generate a PDF file, output XML, create a ZIP file on the fly, anything you want, using whatever Python libraries you want." - django tutorial
- 

## Template namespacing
- we created the path ./templates/polls/index.html . This is to avoid differrent modules with the same template name from conflicting.
- ./templates/polls/index.html and ./templates/results/index.html can exist even if they have the name 'index.html'
- we could also save the files as ./templates/polls-index.html and ./templates/result-index.html. But this would be difficult to update if we need to move the templates or something. And it would be difficult to update the module name. If we wanted to change poll to polls. Then we would need to edit the file names one by one.
- Now we might be able to get away with putting our templates directly in polls/templates (rather than creating another polls subdirectory), but it would actually be a bad idea. Django will choose the first template it finds whose name matches, and if you had a template with the same name in a different application, Django would be unable to distinguish between them. We need to be able to point Django at the right one, and the best way to ensure this is by namespacing them. That is, by putting those templates inside another directory name.
- 

##############################################################################

# Django csrf_token
- django protects agains csrf by using `{% csrf_token %}`, which gets added to the html form
- the csrf_token will generate a new token each time a user logs in
- [link](https://docs.djangoproject.com/en/5.2/ref/csrf/)
```

# How to setup django for production
- [how to setup django with apache and mod_wsgi](https://docs.djangoproject.com/en/5.1/topics/install/#installing-official-release)
- apache is a production web server and can be configured with mod_wsgi
- mod_wsgi allows you to load your webapp into memory for faster response times - this is so cool!

# Programming syntax
- In python, programmers can import modules from packages by doing this,
    ```py
    ## long way of import specific sub-module
    import sound.effects.echo
    sound.effects.echo.echofilter(input, output, delay=0.7, atten=4)

    ## alternative - this seems easier to use and remember, rather than having to import complete
    from sound.effect import echo
    echo.echofilter(input, output, delay=0.7, atten=4)

    ## this also works
    from sound.effet.echo import echofilter
    echofilter(input, output, delay=0.7, atten=4)
    ```
- python lambda functions - allows you to write functions in one line
    ```python
    # lamda function
    sum = lambda x, y : x+y
    print(sum(2,3) ) ## will return 5
    ```
    ```python
    # equivalent function
    function sum(x, y):
        return x + y
    ```