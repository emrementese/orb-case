# ORB CASE

## Setup and Installation Instructions

### With Docker

1. clone project

2. create .env file on root dir & copy .env.examples to .env

3. install [docker & docker-compose plugin](https://docs.docker.com/compose/)

4. Run docker compose

on root directory run command on terminal;

    docker compose build

after build run;

(-d flag is not following the compose)
alternatif command: docker-compose

    docker compose up -d

if all containers will be started successfully visit api root:

[http://localhost:8080/api/](http://localhost:8080/api/)

### With out Docker

1. clone project

2. install python version 12

3. install [poetry](https://python-poetry.org/) with pip

4. install postgresql end setup with .env variables

5. create .env file on root dir & copy .env.examples to .env

Run commands

    poetry shell

    poetry install

    cd src

    python manage.py makemigrations

    python manage.py migrate

    python manage.py runserver

[http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

## Notes

- .env dosyasını oluşturmayı ve değişkenleri example dosyadan almayı unutmayın
- projeye auth eklediğim için bir süper user oluşturun
- Swagger UI 'dan token vererek end-pointleri kullanabilirsiniz aksi takdirde 401 dönecektir.
- category end-pointine alternatif olarak list end-pointi için bir filtre yazdım.
- Ayrıca CRUD end-pointlerinin testlerinide events/tests içerisinde yazdım.
- Projeyi docker compose ile ayağa kaldırmanızı tavsiye ediyorum

Teşekkürler iyi çalışmalar ...

Mid. Software Dev.
Emre Menteşe
