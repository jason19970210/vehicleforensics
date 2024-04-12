# .venv
a simple project which performs the vehicle data logging for digital forensics usage as PoC

tags: `Raspberry Pi`, `Vehicle`, `CAN Bus`, `OBD-II`, `Bluetooth`, `Message Queue`, `RabbitMQ`  

![https://img.shields.io/badge/python-3.9-blue](https://img.shields.io/badge/python-3.9-blue)

## ToC
- [Todo](#todo)
    - [client side](#client-side)
    - [server side](#server-side)
- [execution](#execution)
    - [clone project](#clone-project)
    - [virtual environment](#virtual-environment)
    - [server side setup](#server-side-setup)
    - [client side setup](#client-side-setup)

## ToDo
### Client Side
- [ ] ~~NTRU Implementation~~ (Deprecated, due to unselected from NIST PQC in Round 4)
- [ ] Falcon Implementation
- [ ] Kyber Implementation
- [ ] RabbitMQ Implementation
### Server Side
- [ ] ~~NTRU Implementation~~ (Deprecated, due to unselected from NIST PQC in Round 4)
- [ ] Falcon Implementation
- [ ] Kyber Implementation
- [ ] RabbitMQ Implementation
- [ ] MongoDB Implementation

## execution
### clone project

```shell=
$ git clone --recurse-submodules git@github.com:jason19970210/.venv.git
```

### virtual environment
for both `server-side` & `client-side`

#### pre-requirements

```shell=
$ python3 --version
```

#### create

```shell=
$ python3 -m venv .venv

$ cd .venv
$ sudo chmod +x ./bin/activate
```

#### enter virtual environment

```shell=
$ source ./bin/activate
(.venv) $
```

#### install dependencies

```shell=
## for main service
(.venv) $ pip3 install -r requirements.txt

## for kyber
(.venv) $ pip3 install -r ./utils/kyber_utils/requirements.txt
```

#### exit

```shell=
(.venv) $ deactivate
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
(.venv) $ python3 server_main.py
```

### client side setup
#### pre-requirements

```shell=
$ sudo apt update
$ sudo apt install -y bluetooth libbluetooth-dev libatlas-base-dev
```

#### start main script

```
(.venv)$ python3 client_main.py
```


## FAQ
### 1. Error when `pip install pybluez`
    > env: Windows 10
```
> pip install pybluez

Collecting pybluez>=0.23
  Using cached PyBluez-0.23.tar.gz (97 kB)
  error: subprocess-exited-with-error

  × python setup.py egg_info did not run successfully.
  │ exit code: 1
  ╰─> [1 lines of output]
      error in PyBluez setup command: use_2to3 is invalid.

  note: This error originates from a subprocess, and is likely not a problem with pip.
error: metadata-generation-failed

× Encountered error while generating package metadata.
╰─> See above for output.

hint: See above for details.
```
Solution:
> with `Microsoft Visual C++ 14.0 or greater is required`, link: https://my.visualstudio.com/Downloads?q=Visual%20C++%20Build%20Tools, download with `DVD (ISO)` format as offline installation  

> ref: https://benjenq.pixnet.net/blog/post/47913350-%E3%80%90%E7%A2%BC%E8%BE%B2%E3%80%91%E5%9C%A8-windows-%E5%B9%B3%E5%8F%B0%E4%B8%8A%E8%A7%A3%E6%B1%BA-pip-%E5%AE%89%E8%A3%9D%E5%A5%97%E4%BB%B6%E5%87%BA  
> ref: https://github.com/pybluez/pybluez/issues/431#issuecomment-1107884273
```
> pip install git+https://github.com/pybluez/pybluez.git#egg=pybluez
```