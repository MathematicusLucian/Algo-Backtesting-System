# CryptoTracker App

Angular UI presents performance of cryptocurrencies, and Flask API to fetch the data (*Flask, Docker, Angular, and SQLite3*.)

This service imports my LiveCoinWatch library, which is an interface to the [LiveCoinWatch API](https://www.livecoinwatch.com/). It is available at:
- GitHub: [github.com/MathematicusLucian/LiveCoinWatch](https://github.com/MathematicusLucian/LiveCoinWatch)
- PyPi: [pypi.org/project/LiveCoinWatch/1.0.0/](https://pypi.org/project/LiveCoinWatch/1.0.0/)

## Architecture

### Docker
  - Docker Compose to build and host app: ```docker-compose.yml``` to create containers and run the app. Several versions, i.e. for different environments.
  - Reverse proxy (`nginx`) - web server, and reverse proxy. External user hits the nginx - distributes request to UI or Server.

### Microservice (Python)
***Flask*** app: including tests setup, configs and settings files, Dockerfile for running the Flask container, etc..
  - Flask - Back-End Python framework.
  - ```.env``` variable: Environment variables for Flask and SQLite3. Several versions, i.e. for different environments.
  - Optimised for large scale app structure, with `Blueprints`, `application factory` and several configs that can be extended from this seed project to any Prod-ready app.
  - uwsgi - WSGI server - direct support for popular NGINX web server.
  - Flask code Testing.

### UI (TypeScript)
***Angular:*** Front-End JavaScript framework.

## Run
**NB. Setup the UI before Docker Compose**: 
[Angular Prerequisites] (https://github.com/angular/angular-cli#prerequisites) - that being, Docker, node, npm and angular-cli.
- Navigate to the `ui` directory. 
- Execute `ng build --prod` to create a production build for Angular.

**Running Docker Compose:**
There are two Docker containers:
- Flask/Uwsgi - Flask web application with _uwsgi_ server.
- Angular/Nginx - Angular web client

Both built using separate Dockerfiles, created and connected with Docker Compose, and which expand upon the respective official images from Docker Hub.

***Execute following commands:***
  - ``docker-compose -f docker-compose.yml up --build``
  - Without cache ``docker-compose build --no-cache``

***Open Browser and type following URLs:***
  - `localhost` - the welcome message from Angular and a backend default message.
  - `localhost/api` - the welcome message from Flask.
  - `localhost/api/ping` - sample `json` from Flask.

Details:
- External requests hit the _nginx_ web server's port 80, and the response is by Angular or Flask depending on the URL. 
- _/api_ is sent to Flask docker container (port 5000; as per the _nginx.conf_ file. nginx is aware of both the Angular and Flask services.) 
- Flask container connects via port 1234 to the database.

## Env
- Create: ``python3 -m venv venv``
- Active: ``source venv/bin/activate``
- ***Requirements:***``pip freeze -r requirements.txt | sed '/freeze/,$ d'``

## Tests

### Running the Python Tests
- Flask (Python) unit tests are in the `server/tests` directory and managed by `manage .py` Python file.
- Run with: ``docker-compose -f docker-compose.yml run --rm crypto_tracker_flask python manage.py test``

### Running UI unit tests
Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).