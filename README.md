# Django Survey Web App

A Django survey web app that you can customize per your requirements.
This Django survey system can be used to build a questionnaire with software code.
It includes code highlighter and the flexibility to have multiple choices, dropdowns or opinions.
Participants can be assigned to multiple groups (i.e., control vs treatment) or any other design.
In future, the plan is to add more features and make it more flexible.

## Requirements

 * Python 2.7
 * pip
 * virtualenv

All the dependencies are wrapped into virtualenv and written into `requiremnts.txt`.

## Installation instructions

The first step is to create a directory which will include two directories after all the installations are done

```
mkdir survey
cd survey
```

First, you will need to create a virtual environment for our dependencies and activate it.

```
virtualenv envi
source envi/bin/activate
```


Second, you will then need to clone this repo

```
mkdir djsurvey
cd djsurvey
git clone
```

Now, we need to move to the repo directory we cloned and install all dependacies and run the website.

```
cd djsurvey
pip install -r requirements.txt
python manage.py runserver
```

now go to your browser and enter this URL `127.0.0.1:8000`

You can now run the survey :)


## Enjoy & Play :)

## Developer

* **Abdullah Alsharif** - *Initial work and main developer* - [aalshrif90](http://aalshrif90.github.io/)
