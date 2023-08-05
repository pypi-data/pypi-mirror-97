Thalamus: The GNU Health Message and Authentication Server
==========================================================

The Thalamus project provides a RESTful API hub to all the GNU Health 
Federation nodes. The main functions are:

#. **Message server**: A concentrator and message relay from and to  
   the participating nodes in the GNU Health Federation and the GNU Health
   Information System (PgSQL). Some of the participating nodes include 
   the GNU Health HMIS, MyGNUHealth mobile PHR application,
   laboratories, research institutions and civil offices.

#. **Authentication Server**: Thalamus also serves as an authentication and
   authorization server to interact with the GNUHealth Information System


Thalamus is part of the GNU Health project, but it is a self contained, 
independent server that can be used in different health related scenarios.

Installation
------------
Thalamus is pip-installable::

  $ pip3 install --upgrade --user thalamus 
 
Technology
----------
RESTful API: Thalamus uses a REST (Representional State Transfer) 
architectural style, powered by 
`Flask <https://en.wikipedia.org/wiki/Flask_(web_framework)>`_ technology

Thalamus will perform CRUD (Create, Read, Update, Delete) operations. They
will be achived via the following methods upon resources and their instances.

* **GET** : Read
 
* **POST** : Create
 
* **PATCH** : Update
 
* **DELETE** : Delete.

The DELETE operations will be minimal.
  

JSON: The information will be encoded in `JSON <https://en.wikipedia.org/wiki/JSON>`_ format.

Resources
---------

Some resources and end-points are:

* People (/people)

* Pages of Life (/pols)

* DomiciliaryUnits (/domiciliary-units)

* PersonalDocs (/personal_docs)


Running Thalamus from a WSGI Container
--------------------------------------
In production settings, for performance reasons you should use a HTTP server.
We have chosen `uWSGI <http://projects.unbit.it/uwsgi>`_ , but you can use any WSGI server. We have
also included the configuration file for Gunicorn if you prefer it instead of uWSGI.

For example, you can run the Thalamus application from uWSGI as follows.
The default configuration file uses secure (SSL) connections::

  $ uwsgi --ini etc/thalamus_uwsgi.ini


For development, ff you want to run it directly from the Flask Werkzeug server,::

  $ python3 ./thalamus.py


Examples
--------
**Command-line, using httpie**

Retrieve the demographic information of person::

  $ http --verify no --auth ITAPYT999HON:gnusolidario https://localhost:8443/people/ESPGNU777ORG

Yields to::

    HTTP/1.1 200 OK
    Connection: close
    Content-Length: 411
    Content-Type: application/json
    Date: Fri, 21 Apr 2017 16:22:38 GMT
    Server: gunicorn/19.7.1

    {
        "_id": "ESPGNU777ORG",
        "active": true,
        "biological_sex": "female",
        "dob": "Fri, 04 Oct 1985 13:05:00 GMT",
        "education": "tertiary",
        "ethnicity": "latino",
        "gender": "female",
        "lastname": "Betz",
        "marital_status": "married",
        "name": "Ana",
        "password": "$2b$12$cjrKVGYEKUwCmVDCtEnwcegcrmECTmeBz526AAD/ZqMGPWFpHJ4FW",
        "profession": "teacher",
        "roles": [
        "end_user"
        ]
        
    }

**Retrieve the demographics information globally**::

  $ http --verify no --auth ITAPYT999HON:gnusolidario https://localhost:8443/people

Yields to::

    HTTP/1.1 200 OK
    Connection: close
    Content-Length: 933
    Content-Type: application/json
    Date: Fri, 21 Apr 2017 16:31:23 GMT
    Server: gunicorn/19.7.1

    [
        {
            "_id": "ITAPYT999HON",
            "active": true,
            "biological_sex": "female",
            "dob": "Fri, 05 Oct 1984 09:00:00 GMT",
            "education": "tertiary",
            "ethnicity": "latino",
            "gender": "female",
            "lastname": "Cordara",
            "marital_status": "married",
            "name": "Cameron",
            "password": "$2b$12$Y9rX7PoTHRXhTO1H78Tan.8mVmyayGAUIveiYxu2Qeo0ZDRvJQ8/2",
            "profession": "teacher",
            "roles": [
            "end_user",
            "health_professional"
            ]
            
        },
        
        {
            "_id": "ESPGNU777ORG",
            "active": true,
            "biological_sex": "female",
            "dob": "Fri, 04 Oct 1985 13:05:00 GMT",
            "education": "tertiary",
            "ethnicity": "latino",
            "gender": "female",
            "lastname": "Betz",
            "marital_status": "married",
            "name": "Ana",
            "password": "$2b$12$cjrKVGYEKUwCmVDCtEnwcegcrmECTmeBz526AAD/ZqMGPWFpHJ4FW",
            "profession": "teacher",
            "roles": [
            "end_user"
            ]
            
        }
        
    ]
    

**Using Python requests**::

  >>> import requests
  >>> person = requests.get('https://localhost:8443/people/ESPGNU777ORG', auth=('ITAPYT999HON', 'gnusolidario'), verify=False)
  >>> person.json()
    {'_id': 'ESPGNU777ORG', 'active': True, 'biological_sex': 'female','dob': 'Fri, 04 Oct 1985 13:05:00 GMT',
    'education': 'tertiary', 'ethnicity': 'latino', 'gender': 'female', 'lastname': 'Betz', 'marital_status': 'married',
    'name': 'Ana', 'password': '$2b$12$cjrKVGYEKUwCmVDCtEnwcegcrmECTmeBz526AAD/ZqMGPWFpHJ4FW', 'profession': 'teacher',
    'roles': ['end_user']}

**Note on roles**
The demo user "ITAPYT999HON" is a health professional (health_professional role),
so she has global access to demographic information. 

The user "ARGBUE111FAV", password "freedom". This is the "root" user for the demo database. 

Check the ``roles.cfg`` file for examples information about roles and ACLs.


Development
-----------
Thalamus is part of the GNU Health project.

The development will be done on GNU Savannah, using the Mercurial repository.

Tasks, bugs and mailing lists will be on health-dev@gnu.org , for development.

General questions can be done on health@gnu.org mailing list.

Homepage
--------
https://www.gnuhealth.org


Release Cycle
-------------
Thalamus, as other GNU Health components, will follow its own release process.


Documentation
-------------
The Thalamus documentation will be at the corresponding
chapter in the GNU Health Wikibook

https://en.wikibooks.org/wiki/GNU_Health

:Author: Luis Falcon <falcon@gnuhealth.org>
