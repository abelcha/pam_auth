sudo apt-get update;
sudo apt-get install -y python python-pam libpam-python cryptsetup;
echo "auth sufficient pam_python.so /Pamela/pamela.py" >> /etc/pam.d/login;