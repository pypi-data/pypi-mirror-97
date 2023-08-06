# CoopStarter Application data repository

This project is a Python module, compatible with Django REST Framework and DjangoLDP additional module, describing the models and the API needed and available on the future coopstarter application.

## Installation

Here is the detailed explaination of the preferred installation process.
Depending on your OS and your python installation, commands could have to be run using either `python` or `python3`.

##### Manage many projects at the same time
If you'll have to work on many projects at the same time, we recommande to use virtualenvwrapper.
https://virtualenvwrapper.readthedocs.io/en/latest/

If you're not using virtualenvwrapper, create the python virtual environnement dedicated to the project


```shell
mkdir coopstarter
cd coopstarter
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

```shell
# Install sib-manager
pip install sib-manager
# Create your server folder
sib startproject coopstarter
# Enter in your project
cd coopstarter
```

Open the file "packages.yml", and replace the content of 'ldppackages :' by : 
```
oidc_provider: 'git+https://github.com/jblemee/django-oidc-provider.git@develop'
django_countries: django_countries
djangoldp_account: djangoldp_account
djangoldp_circle: djangoldp_circle
djangoldp_conversation: djangoldp_conversation
coopstarter_data: coopstarter_data
djangoldp_like: djangoldp_like
djangoldp_uploader: djangoldp_uploader
```

```shell
#Create your project
sib install coopstarter
```

## Running the project

```shell
python manage.py createsuperuser
python manage.py creatersakey
```

```shell
python manage.py runserver
```

If successful, this command will make available on `127.0.0.1:8000/admin/` the administrator backend. You will then be able to log-in with 'admin' as identifier and as password.

## Initialising the database

Warning! At this step, you should can Balessan or Alice

Nota Bene : If you using virtualenvwrapper, replace "../venv" by "path/to/your/virtualenv"


As some fixtures are provided to enrich the application database easily, the following command will allow you to properly load them.

```
python manage.py loaddata ../venv/lib/python3.6/site-packages/coopstarter_data/fixtures/*.json
```

If you load the coopstarter_data package locally through a symlink for development purpose, you should use the following command:

```
python manage.py loaddata coopstarter_data/fixtures/*.json
```

If you have some issues with the previous command, such as `Field table does not exist` or equivalent, please run:

```
python manage.py makemigrations
python manage.py migrate
```

And run the loaddata command once more.

If you get a error message like : `django.db.utils.OperationalError: no such table: coopstarter_data_mymissingtable, please run : 

```
python3 manage.py migrate --run-syncdb
```

## Funding

![EULOGO](documentation/EU_logos.png)

This software has been co-funded by the European Union.
The contents of this software are the sole responsibility of Cooperatives Europe and can in no way be taken to reflect the views of the European Union.
