sudo apt-get install virtualenv
virtualenv venv -p /usr/bin/python3

https://docs.mongodb.org/manual/tutorial/install-mongodb-on-linux/
curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.2.4.tgz
tar -zxvf mongodb-linux-x86_64-3.2.4.tgz
mkdir -p mongodb
cp -R -n mongodb-linux-x86_64-3.2.4/ mongodb
export PATH=<mongodb-install-directory>/bin:$PATH

sudo mkdir -p /data/db
Before running mongod for the first time, ensure that the user account running mongod has read and write permissions for the directory.Before running mongod for the first time, ensure that the user account running mongod has read and write permissions for the directory.
