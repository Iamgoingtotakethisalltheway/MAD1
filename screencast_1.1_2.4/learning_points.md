## Write a simple index.html file.

## Inspect webpage through browser tools.

## Host a simple python web server.
> Open terminal in the directory which contains the index.html file, type  
> 
    python -m http.server

## Connect to this new web page from same computer or through another computer on LAN.
> From same computer, type one of the following into the address bar  
> >
    0.0.0.0:8000
    127.0.0.1:8000
    localhost:8000
> To access this page from another computer in same LAN, find out the ip address of the host machine  
> In terminal, type  
> >
    ifconfig
> Note down the ip number and share it with a friend on LAN  
> 
    192.168.1.6:8000