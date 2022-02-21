#!/bin/bash

# mysql에 scrimdor Database를 먼저 만들 것
# CREATE DATABASE scrimdor;
sudo docker exec api1 "/bin/bash" -c "export FLASK_APP=hibike && flask db init"
sudo docker exec api1 "/bin/bash" -c "export FLASK_APP=hibike && flask db migrate"
sudo docker exec api1 "/bin/bash" -c "export FLASK_APP=hibike && flask db upgrade"