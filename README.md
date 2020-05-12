<h1 align="center">Welcome to DockerfileClazz 👋</h1>
<p>
  <a href="https://opensource.org/licenses/MIT" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <a href="https://twitter.com/LouisPerdereau" target="_blank">
    <img alt="Twitter: LouisPerdereau" src="https://img.shields.io/twitter/follow/LouisPerdereau.svg?style=social" />
  </a>
</p>

> This project aims to help you to write good Dockerfile

## General presentation

The goal of this project is to help you to follow my advises to write Dockerfile and possibly some good ones. You will follow step by step a sequence of questions who refer to official documentation and you will build docker image at the end. 🚀

## Description of the project structure

In this project you will find:
* A frontend application VueJS in the directory `./frontend`
* A backend application Django in the directory `./backend`
* And this README

I invite you to fork this project for working on it

## Requierements to start this project

First of all you will need to install [Docker 🐳](https://docs.docker.com/get-docker/) (If install on your laptop is boring you could install it on virtual machine or a Cloud Provider just think you will need this project to code).

Now you would need to clone this project to start to work.

## 📚 Steps

The VueJS and Django applications in the project are minimalist. The goal is not to dwell on the code of the applications but to focus on the following aspects :

- Understand docker image build
- Use docker cli, Dockerfile
- Use CI to build and store your image

### 🐳 1. Create Dockerfile for VueJS

Now you could create a file named `Dockerfile` in the directory `./frontend`.
Frontend app is a VueJS app, to build a VueJS app you will need to:

- Use a base image named `node:lts-slim`
- Create a workspace directory named `/app`
- Copy package.json and package-lock.json (here the doc of [package-lock.json](https://docs.npmjs.com/configuring-npm/package-lock-json.html) and [package.json](https://docs.npmjs.com/configuring-npm/package-json.html))
- Run `$ npm ci` to install dependancies (here the doc for [npm-ci](https://docs.npmjs.com/cli/ci.html))
- Copy the whole content in frontend directory into the docker image
- Run `$ npm run build` to build the project (this command is defined into `package.json` file as `vue-cli-service build`, I let you checkout the documentation about [npm-run](https://docs.npmjs.com/cli/run-script) to understand the principe of npm scripts)

To use a base image you should use annotation [FROM](https://docs.docker.com/engine/reference/builder/#from)

To create a workspace you should use annotation [WORKDIR](https://docs.docker.com/engine/reference/builder/#workdir)

To copy a file from the project into the image you should use annotation [ADD](https://docs.docker.com/engine/reference/builder/#add) or [COPY](https://docs.docker.com/engine/reference/builder/#copy)

To run a command into docker image you should use annotation [RUN](https://docs.docker.com/engine/reference/builder/#run)

Now you have an image with all copied files before. But you will just need the content of the static build directory named `dist` into `/app` who resulting of the command `$ npm run build`.

To keep the only important content `/app/dist` you should do a [multi stage](https://docs.docker.com/develop/develop-images/multistage-build/#name-your-build-stages) `Dockerfile` with name. Moreover you should render this static files with a proxy, I advise you to use this docker image `nginx:1.17-alpine` as base.

I advise you to named your different stage. Actually you can copy the content of a build in a previous stage into another like this `COPY --from=stage-build` only if you named a previous stage like this `FROM node:lts-slim AS stage-build`. Now you could copy the content of `/app/dist` into `/usr/share/nginx/html/`.

>I created for you a file named `.dockerignore` who allow, like gitignore, to omit or no, copy of file or directory into an image. You should notice tha we have use a white-list system, allow only what you need.
> _TIPS: if we add `!/app/dist` in `.dockerignore` it' cause of a  multi-stage_

Now you could build the image with [docker build](https://docs.docker.com/engine/reference/commandline/build/) from the root of this project. You can use this option:

- Named or tagged the image
- Specify a Dockerfile
- Specify the path of the build

<details><summary><i>SPOILER ALERT</i>: Response to build</summary>

```bash
docker build -t dockerclazz-frontend:v0.1 -f frontend/Dockerfile frontend
```
</details>

Now you could run the image with [docker run](https://docs.docker.com/engine/reference/commandline/run/). You can use this option:

- interactive
- tty
- detach
- port (on 8080:80)
- Remove automatically if it's stoped
- Name

<details><summary><i>SPOILER ALERT</i>: Response to run</summary>

```bash
docker run -it -d -p 8080:80 --rm --name dockerize-vuejs dockerclazz-frontend
```
</details>

Now visit http://localhost:8080 (if you run on a distant server `http://<YOUR_IP>:8080`)

If you finished execute :
```bash
docker ps -a
docker stop <CONTAINER_NAME_OR_ID>
```

### 🐍 2. Create Dockerfile for Django

Now you could create a file named `Dockerfile` in the directory `./backend`.
Frontend app is a Django app, to build a Django app you will need to:

- Use a base image named `python:3`
- Create a workspace directory named `/app`
- Copy `requirements.txt`
- Run `$ pip install -r requirements.txt` to install dependancies
- Copy the whole content in brackend directory into the docker image
- Add an environement variable named `PORT` with default value `9090`
- Then execute the commande `sh -c "/app/manage.py runserver 0.0.0.0:$PORT"` to run the web server at startup, `sh -c` allow you to add environement variable in commande

>I created for you a file named `.dockerignore` who allow, like gitignore, to omit or no, copy of file or directory into an image. You should notice tha we have use a white-list system, allow only what you need.

Now you could build the image with [docker build](https://docs.docker.com/engine/reference/commandline/build/) from the root of this project. You can use this option:

- Named or tagged the image
- Specify a Dockerfile
- Specify the path of the build

<details><summary><i>SPOILER ALERT</i>: Response to build</summary>

```bash
docker build -t dockerclazz-backend:v0.1 -f backend/Dockerfile backend
```
</details>

Now you could run the image with [docker run](https://docs.docker.com/engine/reference/commandline/run/). You can use this option:

- interactive
- tty
- detach
- environement variable with a PORT
- port (on 9090:`<PORT previously precise>`)
- Remove automatically if it's stoped
- Name

<details><summary><i>SPOILER ALERT</i>: Response to run</summary>

```bash
docker run -it -d -e PORT=9091 -p 9090:9091 --rm --name dockerize-django dockerclazz-backend
```
</details>

Then you can visit this url: http://localhost:9090/api/

If you finished execute :
```bash
docker ps -a
docker stop <CONTAINER_NAME_OR_ID>
```

## Author

👤 **Louis Perdereau**

* Twitter: [@LouisPerdereau](https://twitter.com/LouisPerdereau)
* Github: [@lperdereau](https://github.com/lperdereau)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/LouisClazz/DockerfileClazz/issues). You can also take a look at the [contributing guide](https://github.com/LouisClazz/DockerfileClazz/pulls).

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2020 [@lperdereau](https://github.com/lperdereau).<br />
This project is [MIT](https://opensource.org/licenses/MIT) licensed.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_