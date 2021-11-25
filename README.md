# Tia 

### Overview

Timecamp is pretty bad at the best of the time, this tries to make it a bit more
bearable...

### Project Tracking and repo

https://gitlab.com/tia-tracker/tia

There is a kanban board here too:
https://gitlab.com/tia-tracker/tia/-/issues

### Script to start the project

    rm -rf /home/vivi/pimount/.idea;
    rmdir /home/vivi/pimount;
    mkdir /home/vivi/pimount;
    sshfs pi@192.168.1.29:/home/pi /home/vivi/pimount;
    ssh 192.168.1.29 -l pi;
