# vehicleforensics
a simple project which performs the vehicle data logging for digital forensics usage as PoC

tags: `Raspberry Pi`, `Vehicle`, `CAN Bus`, `OBD-II`, `Bluetooth`, `Message Queue`, `RabbitMQ`  

![https://img.shields.io/badge/python-3.9-blue](https://img.shields.io/badge/python-3.9-blue)

## ToDo
### Client Side
- [ ] NTRU Implementation
- [ ] Falcon Implementation
- [ ] RabbitMQ Implementation
### Server Side
- [ ] NTRU Implementation
- [ ] Falcon Implementation
- [ ] RabbitMQ Implementation
- [ ] MongoDB Implementation

## execution
### clone project

```shell=
$ git clone git@github.com:jason19970210/vehicleforensics.git
```

### virtual environment
#### pre-requirements

```shell=
$ python3 --version
```

#### create

```shell=
$ python3 -m venv vehicleforensics

$ cd vehicleforensics
$ sudo chmod +x ./bin/activate
```

#### enter virtual environment

```shell=
$ source ./bin/activate
(vehicleforensics) $
```

#### install dependencies

```shell=
(vehicleforensics) $ pip3 install -r requirements.txt
```

#### exit

```shell=
(vehicleforensics) $ deactivate
$ 
```

### server side setup
#### pre-requirements

```shell=
$ sudo apt update
$ sudo apt install -y python3-pip 
```

#### docker & docker compose installation

1. https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04
2. https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04

### start / stop rabbitmq container

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

#### start main script

```shell=
(vehicleforensics) $ python3 server_main.py
```

## client side
#### pre-requirements

```shell=
$ sudo apt update
$ sudo apt install -y bluetooth libbluetooth-dev libatlas-base-dev
```

#### start main script

```
(vehicleforensics)$ python3 client_main.py
```
