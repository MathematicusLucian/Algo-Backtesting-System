# Algo-Trading-System

Work-in-progress: An algorithmic trading system consisting of 8 repos:
- [algo_system_deployment](https://github.com/MathematicusLucian/algo_system_deployment)
- [backtesting_ms](https://github.com/MathematicusLucian/backtesting_ms)
- [stonk-value-forecasting-model](https://github.com/MathematicusLucian/stonk-value-forecasting-model)
- [market_sentiment_ms](https://github.com/MathematicusLucian/market_sentiment_ms)
- [market_data_ms](https://github.com/MathematicusLucian/market_data_ms)
- [LiveCoinWatch](https://github.com/MathematicusLucian/LiveCoinWatch)
- [algo-trader-ms](https://github.com/MathematicusLucian/algo-trader-ms)
- [algo_trading_ui](https://github.com/MathematicusLucian/algo_trading_ui)

![Candlesticks chart](./assets/candlesticks.png)

*Flask, SciKit, Backtesting.py, TA, TA-Lib, Angular, SQLite3, and Docker*:
- ``ui``: Angular UI presents performance of cryptocurrencies
- ``backtesting_microservice``: Flask API to run backtesting of strategy - libraries/dependencies: ``backtesting.py``, and technical analysis: ``TA``/``TA-Lib``.
- ``mdi_microservice``: MDI (Market data and indicators) Microservice - Flask API to fetch market data from OKX, CoinGecko, and my LiveCoinWatch library which is an interface to the [LiveCoinWatch API](https://www.livecoinwatch.com/), deployed to [PyPi](https://pypi.org/project/LiveCoinWatch/1.0.0/).
- ``sentiment_microservice``: Flask API to scrape X/Twitter and determine sentiment.

## Architecture

### Docker
There are 4 Docker containers:
- 3 x Flask/Uwsgi - Flask web application with _uwsgi_ 
- 1 x Angular/Nginx - Angular web client

These containers built by separate Dockerfiles, created and connected with Docker Compose, and expand upon the respective official images from Docker Hub.
- The Docker Compose file is used to build and host app: ```docker-compose.yml``` to create containers and run the app. Several versions, i.e. for different environments.
- External requests hit the _nginx_ web server's port 80, and the response is by Angular or Flask depending on the URL. Reverse proxy (`nginx`) - web server, and reverse proxy. External user hits the nginx - distributes request to UI or a microservice.
- _/api_ is sent to Flask docker container (port 5000; as per the _nginx.conf_ file. nginx is aware of both the Angular and Flask services.) 
- Flask container connects via port 1234 to the database.

**NB. Setup the UI before Docker Compose**: [Angular Prerequisites] (https://github.com/angular/angular-cli#prerequisites) - that being, Docker, node, npm and angular-cli.
- Navigate to the `ui` directory. 
- Execute `ng build`; and with `--prod` to create a production build for Angular.

***Execute following commands:***
  - Run with (watch): ``docker compose up --build --wait && docker compose alpha watch``
  - ``docker compose watch docker-compose.yml && docker compose up``
  - ``docker-compose -f docker-compose.yml up --build``
  - Without cache ``docker-compose build --no-cache``

***Open Browser and type following URLs:***
  - `localhost` - the welcome message from Angular and a backend default message.
  - `localhost/api` - the welcome message from Flask.
  - `localhost/api/ping` - sample `json` from Flask.

***Cleaning Docker:*** Prune Docker regularly:
- ``docker system prune``
- ``docker rmi $(docker images | awk '/^<none>/ {print $3}')``

### Microservices (Python)
Seperated to improve load time (thus if changes are made, not always need to reload whole back-end, or install to container dependencies of other microservices.) WIP: Sentiment scraping, sentiment analysis, LLM, etc..

There are 3 ***Flask*** apps, each of which includes tests setup, configs and settings files, Dockerfile for running the Flask container, etc..
  - Flask - Back-End Python framework.
  - ```.env``` variable: Environment variables for Flask and SQLite3. Several versions, i.e. for different environments.
  - Optimised for large scale app structure, with `Blueprints`, `application factory` and several configs that can be extended from this seed project to any Prod-ready app.
  - uwsgi - WSGI server - direct support for popular NGINX web 
  - Flask code Testing.

***Dependencies Setup (Mac)***

TA-LIB:

    brew install ta-lib
    export TA_INCLUDE_PATH="$(brew --prefix ta-lib)/include"
    export TA_LIBRARY_PATH="$(brew --prefix ta-lib)/lib"
    pip install ta-lib