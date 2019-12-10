# AutomazioneTende
this app automates the roof and curtains opening and closing on telescope pointing base

## Prerequisite on linux
sudo apt-get install python3-tk python3-pip

## Freeze local dependency:
pip3 freeze -l > requirements.txt

## Update pip dependency:
pip3 install -U $(pip3 freeze -l | awk '{split($0, a, "=="); print a[1]}')

## Run the unit test:
python -m unittest discover -v

## Run a single unit test:
python -m unittest unit_test/roof_control_test.py

## Run the server with the hardware mocked
python server.py -m

## Run the server with coords looking up on theSkyX
python server.py -s

## Of course you can use both hardware mock and theSkyX
python server.py -m -s

**flag -t is to be deprecated**
