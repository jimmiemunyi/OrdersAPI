# Orders API Documentation
Deployed on Heroku - [link](https://jimmie-orders-api-e6327f2ac0f9.herokuapp.com/)


# Postgres

```bash
sudo su - postgres
psql
```

```
CREATE testuser WITH PASSWORD testpass;
CREATE DATABASE orders_db WITH OWNER testuser ENCODING='UTF8';
CREATE DATABASE orders_api_db_test WITH OWNER testuser ENCODING='UTF8';
```