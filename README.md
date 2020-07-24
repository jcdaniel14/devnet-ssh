<h1 align="center">Devnet-SSH</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0.5-blue.svg?cacheSeconds=2592000" />
  <a href="#" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
</p>

> Fast and simple SSH library for interactive sessions based on Paramiko.

## Supported Platforms
Currently tested on:
- Cisco switches (IOS,IOS-XE,Nexus)
- Cisco routers (IOS,IOS-XR,IOS-XE)
- HP (Model 5920AF)
- Huawei (Model NE40)
- Linux Servers

## Install

```sh
pip install devnet-ssh
```

## Getting started
### Establishing connection
```
from devnet_ssh import ssh_connect

session = SSHConnect(host="192.168.213.230",user="cisco",pwd="cisco") 
```
### Executing commands
```
console = session.send_command("show ip int brief")
for line in console:
    print(line)
```
```
Interface                  IP-Address      OK? Method Status                Protocol
Embedded-Service-Engine0/0 unassigned      YES NVRAM  administratively down down
GigabitEthernet0/0         192.168.213.230 YES NVRAM  up                    up
GigabitEthernet0/1         unassigned      YES NVRAM  administratively down down
GigabitEthernet0/1.1       unassigned      YES unset  administratively down down
GigabitEthernet0/1.75      10.71.89.1      YES NVRAM  administratively down down
GigabitEthernet0/1.626     10.33.62.121    YES NVRAM  administratively down down
GigabitEthernet0/1.777     192.168.1.1     YES NVRAM  administratively down down
GigabitEthernet0/1.918     10.30.83.161    YES manual administratively down down
GigabitEthernet0/1.990     10.13.87.1      YES NVRAM  administratively down down
```

### Connecting to a different vendor
#### You can choose between supported vendors: 
- SSHConnect.CISCO
- SSHConnect.HP
- SSHConnect.HUAWEI

>os_type is associated with device prompt (# for Cisco, > for HP/Huawei) and it sends the appropiate commands for disable scrolling after establishing connection.
```
from devnet_ssh import SSHConnect

session = SSHConnect(host="192.168.213.231",user="huawei",pwd="huawei",os_type=SSHConnect.HUAWEI)
```
```
console = session.send_command("display ip routing-table")
for line in console:
    print(line)
```
```
Route Flags: R - relay, D - download to fib, T - to vpn-instance, B - black hole route
------------------------------------------------------------------------------
Routing Table : _public_
Destinations : 8        Routes : 8
Destination/Mask    Proto   Pre  Cost        Flags NextHop         Interface
0.0.0.0/0   Static  1    0             RD  192.168.213.225 GigabitEthernet0/3/23
127.0.0.0/8   Direct  0    0             D   127.0.0.1       InLoopBack0
127.0.0.1/32  Direct  0    0             D   127.0.0.1       InLoopBack0
127.255.255.255/32  Direct  0    0             D   127.0.0.1       InLoopBack0
192.168.213.224/27  Direct  0    0             D   192.168.213.231 GigabitEthernet0/3/23
192.168.213.231/32  Direct  0    0             D   127.0.0.1       GigabitEthernet0/3/23
192.168.213.255/32  Direct  0    0             D   127.0.0.1       GigabitEthernet0/3/23
255.255.255.255/32  Direct  0    0             D   127.0.0.1       InLoopBack0
```

## Author

👤 **Gustavo Santiago**

* Github: [@jcdaniel14](https://github.com/jcdaniel14)
