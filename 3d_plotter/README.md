# Overview
3D Plotter is a library that repurposes a 3D printer using the DRV-8823 stepper motor drivers. It gives low-level hardware control of individual motors whlie also providing high level plotting using Numpy arrays. Currently, a RPi utilizes those stepper motor drivers with the GPIO library and is sent movements for higher level plotting with the use of a Flask webserver ran locally on the RPi.


# Installation
All software is stored server-side with clients just accessing the webpage over a local network.
TODO: Add a requirements.txt for package dependcies on new installs

# Deployment
Most deployments would benefit from running this as a Linux systemd process for long-term use. In any case, the deployment will always require the following command to be run:
```
python server.py
```
From here, the webpage is accessed over a local network at: **deployed machine's IP:65432**
