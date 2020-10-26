# AutomazioneTende
this app automates the roof and curtains opening and closing on telescope pointing base

## Prerequisite on linux
sudo apt-get install python3-tk python3-pip

## First time configuration and install dependency:

```
pip3 install pipenv
pipenv install --dev
```

## Enter in the CRaC environment

```
pipenv shell
```

## Exit from the CRaC environment

```
exit
```

## Update dependency:

```
pipenv update --dev
```

# Run the unit test:

```
python -m unittest discover -v
```

## Run unit test with coverage:

```
coverage run -m unittest discover -v
coverage html
```

## Run a single unit test:

```
python -m unittest unit_test/roof_control_test.py
```

## Run a single unit test with coverage:

```
coverage run -m unittest unit_test/test_curtains.py
coverage html
```

# Check the coverage
Open up the file manager and navigate to  ./htmlcov
Double click on the html file relative to the class you want to check coverage

## Run the static type checker 

```
mypy *.py
```

## Run the static type checker on a specific file

```
mypy gui.py
```

## Run the linter

```
pycodestyle *.py
```

# Run the app

## Run the server with the hardware mocked

```
python server.py -m
```

## Run the server with coords looking up on theSkyX

```
python server.py -s
```

## Of course you can use both hardware mock and theSkyX

```
python server.py -m -s
```

## Run the client

```
python client.py
```

# TheSkyX Api Documentation

```
https://wwww.bisque.com/wp-content/scripttheskyx/functions_l.html
```

For enable/disable debugger on theSkyX: open menu via Tools | Run Java Script. This brings up a window with a buffer into which you can paste the script and a checkbox to "Enable Debugger" so you can run the script and get execution feedback. Keep it disabled on production!

# Port forwarding

```
ssh -L 59000:localhost:5901 -L 3030:localhost:3030 -C -N remoteIP
```

this way you can connect to the server via both vnc (5901) and CRaC server (3030). Or you can decide to run CRaC client/server locally and connect remotely to theSkyX (3040)


# Use crac client in a docker container on Mac (Draft)
https://sourabhbajaj.com/blog/2017/02/07/gui-applications-docker-mac/
https://medium.com/@SaravSun/running-gui-applications-inside-docker-containers-83d65c0db110

just once
```
brew cask install xquartz
brew cask install docker
```

right before starting the docker image
```
IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
export DISPLAY=$IP:0
xhost +
```
