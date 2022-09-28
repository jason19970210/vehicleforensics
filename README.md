# vehicleforensics
a simple project which performs the vehicle data logging for digital forensics usage as PoC

tags: `Raspberry Pi`, `Vehicle`, `CAN Bus`, `OBD-II`, `Bluetooth`, `Message Queue`, `RabbitMQ`  

![https://img.shields.io/badge/python-3.9-blue](https://img.shields.io/badge/python-3.9-blue)

## execution
### pre-requirements
```shell=
$ sudo apt update
$ sudo apt install -y bluetooth libbluetooth-dev libatlas-base-dev
```
```
docker & docker compose installation

1. https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04
2. https://docs.docker.com/compose/install/linux/
```

### clone project
```shell=
$ git clone git@github.com:jason19970210/vehicleforensics.git
```
### create a virtual environment
```shell=
$ python3 -m venv vehicleforensics

$ cd vehicleforensics
$ sudo chmod +x ./bin/activate
```
### enter virtual environment
```shell=
$ source ./bin/activate
(vehicleforensics) $
```
### exit virtual environment
```shell=
(vehicleforensics) $ deactivate
$ 
```

### setup virtual environment dependencies
```shell=
(vehicleforensics) $ pip3 install -r requirements.txt
```

### start / stop rabbitmq
```shell=
$ docker-compose up -d
```
```shell=
$ docker-compose down
```

#### check docker-compose container status
```shell=
$ docker-compose ps
```