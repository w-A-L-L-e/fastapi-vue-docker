# fastapi-vue-docker
Small application skeleton providing backend with fast-api and aerich for migrations and tortoise as orm.
Frontend is with Vue.js and also adds translations/i18n.

# Running
To start up on local machine use the start.sh script that does a docker-compose up
```
./start.sh
```

Then upgrade the database which creates tables and inserts some test users and demo data.
```
./db_upgrade.sh
```

The backend api is documented with swagger. Visit http://localhost:5000 to see the api calls available.

Now visit http://localhost:8080 to see the website


