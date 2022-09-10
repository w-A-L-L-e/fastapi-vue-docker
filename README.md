# fastapi-vue-docker
Small application skeleton providing backend with fast-api and aerich for migrations and tortoise as orm.
Frontend is with Vue.js and also adds translations/i18n.

This is a skeleton app that does not do much apart from show how vue, translations and a json api backend
with fast-api can work together nicely. There is also a roles system to give different roles to users and then
allow or deny access to certain pages or actions (both implemnted in frontend and backend).

Original inspiration was this, but here we solved some issues that it had and added the translations and roles
and other goodies.


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


