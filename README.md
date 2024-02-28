# Library service

Simple Library api ,
structured by books , borrowings , payments,  etc.

## installation

Python3 must be already installed

```shell
git clone https://github.com/M4Xpy/library_service
cd library_service
python3 -m venv venv
source venv/bin/activate
pip install requirements.txt
python manage.py runserver # starts Django project
```

## Run  with  docker

Docker  should  be  installed
```shell
sudo docker-compose build
sudo docker-compose up
```

## Features

* Authentication functionality for Customer/User
* Managing by books , borrowings , payments,  etc. directly from api interface
* Admin panel for advanced managing



![Api Logo](./media/img.png)

