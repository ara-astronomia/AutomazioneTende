# AutomazioneTende
codice per automatizzare il movimento delle tende in relazione alla posizione del telescopio

# freeze local dependency:
pip3 freeze -l > requirements.txt

# prerequisite
sudo apt-get install python3-tk

# update pip dependency:
pip3 install -U $(pip3 freeze -l | awk '{split($0, a, "=="); print a[1]}')
