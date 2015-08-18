The Cambridge Audio Azur series HDMI receivers (it seems pre HDMI receivers do
not have them) have RS232 serial ports that can be used to control most if not
all of the functionality. After doing the work on Azur receivers, I started
working on controlling my LG TV and later a Pioneer TV that was lying around at
work. If interested in doing some coding, read HACKING

### COMPATIBILITY

rs232server splits hardware support into loadable modules. I've listed the
hardware I've used the modules on and hardware I believe they should work on:

Azur Service:
All CA receivers should work apart from the 540R v1-2 (v3 should work) as they
do not have an rs232 port.
Azur 340R (tested on SW version 1.3, protocol version 1.1)
Azur 640R (tested on SW version 1.5, protocol version 1.0)

Lgtv Service:
LG M2762DP (UK model)

Pioneer Service:
KRL-32V

Arcam Service:
AVR300

Personally I use the 340R (upstairs) and 640R (downstairs). The 340R uses
miniclient with a bash script and the HTPC with the 640R uses the xbmc plugin.
Both systems are fairly reliable, and I run git HEAD. Please send me any
issues/improvements/comments you may have! I'd love to hear if you are using
the SW even if you disliked it ;-)

### PROGRAM

The program runs in two parts. A python daemon runs in the background and
responds to queries from the cli using dbus.  The hope is to decouple the two
sufficiently so that other clients can be written. The hope is to eventually
have the script listening to the users media player in order to switch on when
neccessary, replace alsa as the volume controller, etc...

### INSTALL

Just like a standard python module use:
```{sh}
sudo ./setup.py install
```
or to install it locally, use:
```{sh}
./setup.py install --user
```
The miniclient uses autotools (urgh) so just use
```{sh}
cd miniclient
./autogen.sh
./configure --prefix=/usr
make
sudo make install
```

### GETTING SERVICE READY

Modify rs232.conf.example with your favourite text editor to map to your serial devices.

```{sh}
sudo cp rs232.conf.example /etc/rs232.conf
sudo cp uk.co.madeo.rs232server.conf /etc/dbus-1/system.d/
sudo cp rs232server.service /usr/lib/systemd/system/
sudo systemctl start rs232server
```

The script requires python2, python-pyserial and dbus

To connect the Amplifier (Azur 340R), use a null modem cable to a serial port
or USB->serial controller

### USE
The rs232server can be started like any python program just run
./rs232server.  Run ./rs232server --help for further info. A tty can be set if
ttyUSB0 is not what your amplifier is connected to.

You will need to place rs232.conf in /etc and configure the correct ttys for
the services. To disable a service simply comment out the service in the .conf

Also provided is an xbmc (eden/11.x) service addon (see
https://github.com/arfoll/service.madeo.rs232server)

### THANKS
Tom Carlson - original creator of the python script to control Azur 340R
Jon Smith - blog post on lgtv serial communication
Suan-Aik Yeo - developer of libLGTV_serial
Sander Jongeleen - Initial arcam service work
Rob Sharp - For testing & mapping out features on arcam service
