#!/bin/bash

# mysql에 scrimdor Database를 먼저 만들 것
# CREATE DATABASE scrimdor;
sudo docker exec api1 "/bin/bash" -c "export FLASK_APP=scrimdor && flask db init"
sudo docker exec api1 "/bin/bash" -c "export FLASK_APP=scrimdor && flask db migrate"
sudo docker exec api1 "/bin/bash" -c "export FLASK_APP=scrimdor && flask db upgrade"