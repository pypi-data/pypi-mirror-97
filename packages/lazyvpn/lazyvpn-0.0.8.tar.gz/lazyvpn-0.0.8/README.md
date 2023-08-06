# lazyvpn
https://zwiki.zillowgroup.net/display/AT/LazyVPN

##Prerequisites
Python 3.6+

Follow this [wiki](https://zwiki.zillowgroup.net/display/ZillowOps/Instructions+for+using+Okta+verify+to+connect+to+AnyConnect+VPN) to install **AnyConnect VPN** and 
this [wiki](https://zwiki.zillowgroup.net/display/ZGITArchive/Okta+-+Setting+Up+Two-factor+Authentication) to set up **Okta Verify**

##Installation
This is a Python 3 project.

Install/Upgrade from PyPi:
```
pip3 install --upgrade lazyvpn
```

##Configuration
To set up or update the configuration for a password change run:
```
lazyvpn -c
```
OR
```
lazyvpn --configure
```

##Connect to VPN
```
lazyvpn -u
```
OR
```
lazyvpn --up
```
##Disconnect from VPN
```
lazyvpn -d
```
OR
```
lazyvpn --down
```
##Reconnect to VPN
```
lazyvpn -ud
```