# AutomazioneTende
this app automates the roof and curtains opening and closing on telescope pointing base

## Prerequisite on ubuntu linux using default python

```shell
sudo apt-get install python3-tk python3-pip
```

## Prerequisite on linux using pydev

```shell
sudo apt-get install tk-dev openssl-dev libffi-dev
https://pyenv.run | bash
```

open ~/.bashrc and copy these 3 lines at the bottom of the file

```shell
export PATH="/home/alessio/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

## First time configuration and install dependency:

```shell
pip3 install pipenv
pipenv install --dev
```

--dev is needed only for development purpose

## Enter in the CRaC environment

```shell
pipenv shell
```

## Exit from the CRaC environment

```shell
exit
```

## Update dependency:

```shell
pipenv update --dev
```

# Run the unit test:

```shell
python -m unittest discover -v
```

## Run unit test with coverage:

```shell
coverage run -m unittest discover -v
coverage html
```

## Run a single unit test:

```shell
python -m unittest unit_test/roof_control_test.py
```

## Run a single unit test with coverage:

```shell
coverage run -m unittest unit_test/test_curtains.py
coverage html
```

# Check the coverage
Open up the file manager and navigate to  ./htmlcov
Double click on the html file relative to the class you want to check coverage

## Run the static type checker 

```shell
mypy *.py
```

## Run the static type checker on a specific file

```shell
mypy gui.py
```

## Run the linter

```shell
pycodestyle *.py
```

# Run the app

## run indipendently

### Run the server with the hardware mocked

```shell
python server.py -m
```

### Run the server with coords looking up on theSkyX

```shell
python server.py -s
```

### Of course you can use both hardware mock and theSkyX

```shell
python server.py -m -s
```

### Run the client

```shell
python client.py
```

### Run via crac.sh both client and server

```shell
./crac.sh -s start
```

### Stop via crac.sh the server (client can be stopped closing its window)

```shell
./crac.sh -s stop
```

### Print logs

```shell
./crac.sh -s logs
```

### Pick only an instance

```shell
./crac.sh -s start -a client
```

### Pass one or more arguments

```shell
./crac.sh -s start -a server -p "-m -s"
```

if you pass just an argument, quotes are not mandatory
```shell
./crac.sh -s start -a server -p -m
```

```shell
./crac.sh -s logs -a server
```

```shell
./crac.sh -s logs -a client
```

obviously, only the server use arguments

# TheSkyX Api Documentation

```
https://wwww.bisque.com/wp-content/scripttheskyx/functions_l.html
```

For enable/disable debugger on theSkyX: open menu via Tools | Run Java Script. This brings up a window with a buffer into which you can paste the script and a checkbox to "Enable Debugger" so you can run the script and get execution feedback. Keep it disabled on production!

# Port forwarding

```shell
ssh -L 59000:localhost:5901 -L 3030:localhost:3030 -C -N remoteIP
```

this way you can connect to the server via both vnc (5901) and CRaC server (3030). Or you can decide to run CRaC client/server locally and connect remotely to theSkyX (3040)

# Use docker and docker-compose

## Use crac server in a docker container
Install docker

compile the docker image
```shell
docker build -t crac_server . -f Dockerfile.server
```

run the docker image
```shell
docker run --net=host crac_server
```

you can also pass the arguments:
```shell
docker run --net=host crac_server -m -s
```

## Use crac client in a docker container
Install docker

https://sourabhbajaj.com/blog/2017/02/07/gui-applications-docker-mac/
https://medium.com/@SaravSun/running-gui-applications-inside-docker-containers-83d65c0db110

just once in a Mac environment
```shell
brew cask install xquartz
brew cask install docker
```

compile the docker image
```shell
docker build -t crac_client . -f Dockerfile.client
```

Right before starting the docker image
```shell
IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
export DISPLAY=$IP:0
xhost +
```

run the docker image
```shell
docker run -e DISPLAY=$IP:0 --net=host crac_client
```

## Use crac in a docker-composer for development purpose with composer.sh

Install docker and docker-compose

start the service on a Mac OSX
```shell
./composer.sh -o mac -s start
```

start the service on linux
```shell
./composer.sh -s start
```

stop the service on a Mac OSX
```shell
./composer.sh -o mac -s stop
```

stop the service on linux
```shell
./composer.sh -s stop
```

Flag used by composer.sh:
-o mac if it's running on a mac OSX
-s start/stop/restart/build/logs
-a crac_client/crac_server

It is possibile to change the arguments passed to the crac server in the command section of crac_server in docker-compose.yml