# Tia 

### Overview

Timecamp is pretty bad at the best of the time, this tries to make it a bit more
bearable...

## Run as systemd service

It's better to run it this way as it means that you do not have to start the
program manually every time the pi is switched on. Before doing this, ensure that
tia can run properly without any errors.

First, make a new tia service by running: 

    sudo systemctl --force --full edit tia.service

Add the following:

    Description=Start Tia program on boot
    After=multi-user.target
    
    [Service]
    User=pi
    WorkingDirectory=/home/pi/tia/
    ExecStart=python3 main.py
    
    [Install]
    WantedBy=multi-user.target

Enable and monitor the service with:    
    
    systemctl status myscript.service
    sudo systemctl enable --now myscript.service

The output of the print() statements you will find in the journal:

    journalctl -b -e

## Development

### Project Tracking and repo

https://gitlab.com/tia-tracker/tia

There is a kanban board here too:
https://gitlab.com/tia-tracker/tia/-/issues

### Script to start the project

    rm -rf /home/vivi/pimount/tia/.idea;
    rmdir /home/vivi/pimount/tia;
    #mkdir /home/vivi/pimount;
    sshfs pi@192.168.1.29:/home/pi /home/vivi/pimount;
    ssh 192.168.1.29 -l pi;

