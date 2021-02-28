
cd

cat .ssh/*.pub > ~/.ssh/authorized_keys
chmod 644 ~/.ssh/
chmod 600 ~/.ssh/*
chmod 644 ~/.ssh/authorized_keys ~/.ssh/*.pub

ssh-keygen -A
service ssh start

python3 bing.py
