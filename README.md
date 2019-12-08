# AutomazioneTende
this app automates the roof and curtains opening and closing on telescope pointing base

# prerequisite on linux
sudo apt-get install python3-tk python3-pip

# freeze local dependency:
pip3 freeze -l > requirements.txt

# update pip dependency:
pip3 install -U $(pip3 freeze -l | awk '{split($0, a, "=="); print a[1]}')
