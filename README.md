# AutomazioneTende
this app automates the roof and curtains opening and closing on telescope pointing base

## Prerequisite on linux
sudo apt-get install python3-tk python3-pip

## Install dependency:

```
pip3 install pipenv
pipenv install --dev
```

## Update pip dependency:

```
pipenv update --dev
```

## Run the unit test:

```
python -m unittest discover -v
```

## Run unit test with coverage:

```
coverage run -m unittest discover -v
coverage html
```

## Run a single unit test:
python -m unittest unit_test/roof_control_test.py

## Run a single unit test with coverage:

```
coverage run -m unittest unit_test/test_curtains.py
coverage html
```

## Check the coverage
Open up the file manager and navigate to  ./htmlcov
Double click on the html file relative to the class you want to check coverage

## Run the server with the hardware mocked
python server.py -m

## Run the server with coords looking up on theSkyX
python server.py -s

## Of course you can use both hardware mock and theSkyX
python server.py -m -s

## Run the client ##
python client.py

**flag -t is to be deprecated**
