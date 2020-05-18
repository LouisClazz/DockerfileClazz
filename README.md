<h1 align="center">Welcome to DockerfileClazz 👋</h1>
<p>
  <a href="https://opensource.org/licenses/MIT" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <a href="https://twitter.com/LouisPerdereau" target="_blank">
    <img alt="Twitter: LouisPerdereau" src="https://img.shields.io/twitter/follow/LouisPerdereau.svg?style=social" />
  </a>
</p>

> This project aims to introduce you into writing clean Dockerfiles to lightweight your Docker images.

## General presentation

The goal of this project is to dive my advises to write Dockerfile and introduce you to Docker best practises. You will follow a sequence of steps which will guide you throught the journey of building Dockerfiles. You will also need to refer to the official [Docker documentation](https://docs.docker.com/).

## Description of the project structure

In this project, you will find:
* A frontend application VueJS in the directory `./frontend`.
* A backend application Django in the directory `./backend`.
* And this README.

I invite you to fork this project to work directly on it.

## Requierements to start this project

First of all, you need to install [Docker 🐳](https://docs.docker.com/get-docker/) (If you don't want to install it locally on your computer, you can install it on virtual machine or a Cloud Provider, just keep in mind you will need this project to code).

You also need to fork/clone this project to start working.

## 📚 Steps

The VueJS and Django applications in the project are minimalist. As said previously, the goal is not to dwell on the code of the applications but to focus on the following aspects :

- Understanding docker image build
- Use docker CLI, and write Dockerfiles
- Use CI to build and store your docker image

### 🐳 1. Creating the Dockerfile for the VueJS app

Now that you filled all the requirements, you can start creating a file named `Dockerfile` in the directory `./frontend`.

#### 🐳 1.1 Writing the Dockerfile.

This file is the file that will be used by docker to build the image which will then be used by docker to spawn 1 or more containers.
As the frontend app is a VueJS app, to build the image you need to :

- Use a base image named `node:lts-slim`.
- Create a workspace directory named `/app`.
- Copy package.json and package-lock.json (Check the official documentation of [package-lock.json](https://docs.npmjs.com/configuring-npm/package-lock-json.html) and [package.json](https://docs.npmjs.com/configuring-npm/package-json.html))
- Run `$ npm ci` to install dependancies (Check the official documentation for [npm-ci](https://docs.npmjs.com/cli/ci.html))
>__Note:__ We first copy the `package.json` and `package-lock.json` files into the image and download dependencies so docker keep these layers in its cache so we don't have to download it again everytime we build the image.
- Copy the whole content of the frontend directory into the docker image.
- Run `$ npm run build` to build the project as a static html/css/js app.
>__Note:__ When using VueJS, this command is defined into `package.json` file as `vue-cli-service build`. As a result behind the scenes, this is the command that will be used to build the app. You can checkout the documentation about [npm-run](https://docs.npmjs.com/cli/run-script) to understand how of npm scripts works)

To use a base image, you should use annotation [FROM](https://docs.docker.com/engine/reference/builder/#from)

To create a workspace, you should use annotation [WORKDIR](https://docs.docker.com/engine/reference/builder/#workdir)

To copy a file from the project into the image, you should use annotation [ADD](https://docs.docker.com/engine/reference/builder/#add) or [COPY](https://docs.docker.com/engine/reference/builder/#copy)

To run a command into docker image you should use annotation [RUN](https://docs.docker.com/engine/reference/builder/#run)

#### 🐳 1.2 Building the docker image.

Now that you wrote the Dockerfile for the frontend app, you can build the image using [docker build](https://docs.docker.com/engine/reference/commandline/build/) from the root of this project. 
Here's a list of usefull options:

- Name or tag the image
- Specify a Dockerfile
- Specify the path of the build

<details><summary><i>SPOILER ALERT</i>: Response to build</summary>

```bash
docker build -t dockerclazz-frontend:v0.1 -f frontend/Dockerfile frontend
```
</details>

#### 🐳 1.3 Creating a container from our image and testing.

Now that you successfully built your image, you can spawn a container from this image and test it, using [docker run](https://docs.docker.com/engine/reference/commandline/run/). 
Here's a list of usefull options :

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

If you finished the execution :
```bash
docker ps -a
docker stop <CONTAINER_NAME_OR_ID>
```

Voila ! Congratulations, you just built your VueJS frontend app into a docker image ! You can now use it to spawn any number of your application instances.

#### 🐳 1.4 Enhancing the Dockerfile

One thing remains : your docker image is still pretty heavy for only a sample project, and the more dependencies you'll add, the more it will grow.

Currently, have an image with all the copied files before. But the only thing your app needs to run is the result of the `$ npm run build` command. This static result is located in the directory named `dist` into `/app`.

To keep only the important content `/app/dist`, do a [multi stage](https://docs.docker.com/develop/develop-images/multistage-build/#name-your-build-stages) `Dockerfile`. Multi-stage will help us build the app in a temporary image and then copy the result of the build into a definitive image. To render static HTML/CSS and JS you should use a proxy, I advise you to use this docker image `nginx:1.17-alpine` as base.

I recommend that you name your different stages.
You can copy the content of a build in a previous stage into another like this `COPY --from=stage-build` only if you named a previous stage like this `FROM node:lts-slim AS stage-build`. Now you can copy the content of `/app/dist` into `/usr/share/nginx/html/`.

>I created for you a file named .dockerignore whose job is similar to a .gitignore file, It can allow or ignore files during the build of the docker image. The best practises in a .dockerignore are the same as a .gitignore, so by default you should always ignore everything and then white-list the things you need.
>__WARNING:__ when using Kaniko to build the images the .dockerignore behavior is slightly different than when using Docker. As a result white-listing /app/dist is mandatory when using Kaniko and a multi-stage image building.

If you now build your image again, the image should be much more of a lighter weight.

### 🐍 2. Create Dockerfile for Django

In this second part we'll be writing a new `Dockerfile`for a backend app in the `./backend` directory.
The objective here is the same but with less help.

#### 🐍 2.1 Writing the Dockerfile.

As the backend app is a Django app, to build the image you need to :

- Use a base image named `python:3`
- Create a workspace directory named `/app`
- Copy `requirements.txt`
- Run `$ pip install -r requirements.txt` to install dependencies
- Copy the whole content in brackend directory into the docker image
- Add an environement variable named `PORT` with default value `9090`
- Then execute the commande `sh -c "/app/manage.py runserver 0.0.0.0:$PORT"` to run the web server at startup, `sh -c` allow you to add environement variable in commande

#### 🐍 2.2 Building the docker image.

Now that you wrote your dockerfile, you can build the image using [docker build](https://docs.docker.com/engine/reference/commandline/build/) from the root of this project.
Here's a list of usefull options :

- Name or tag the image
- Specify a Dockerfile
- Specify the path of the build

<details><summary><i>SPOILER ALERT</i>: Response to build</summary>

```bash
docker build -t dockerclazz-backend:v0.1 -f backend/Dockerfile backend
```
</details>

#### 🐍 2.3 Creating a container from our image and testing.

Now that you successfully built your image, you can spawn a container from this image and test it, using [docker run](https://docs.docker.com/engine/reference/commandline/run/). 
Here's a list of usefull options :

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

If you finished the execution :
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