## stun service test python client
### 1. Install pystun
`sudo pip install pystun`
### 2. Test
`pystun -H stun.ekiga.net`
### 3. Public stun server
>stun.ideasip.com
>stun.voipbuster.com

## what is linux sound server (relationship between alsa, jack, pulseaudio, gstreamer and so on)
### 1. Recommended refer
[how-it-works-linux-audio-explained](http://tuxradar.com/content/how-it-works-linux-audio-explained)
### 2. Some tips
if you need connect program on jack, it must be use jack api.

##  stop sound server pulseaudio
refer from [debian pulseaudio wiki](https://wiki.debian.org/PulseAudio)
###1. Disabling deamon autospawn
`sudo vi /etc/pulse/client.conf`
uncomment autospawn line and set value no
```
autospawn = no
```
###2. Stop the service
`pulseaudio --kill`

## snd-aloop
### 1. Check all sound cards
`cat /proc/asound/cards`

### 2. Check snd-aloop module
`modinfo snd-aloop`

### 3. Set module options
`sudo vi /etc/modprobe.d/sound.conf`
```options snd slots=snd-aloop,snd-hda-intel```

### 4. Install module
`sudo modprobe snd-aloop`

### 5. Check sound cards if success
`cat /proc/asound/cards`

## rebuild kernel module alsa-driver
### 1. Install the package alsa-source
`apt-get install alsa-source`
`cd /usr/src`
`tar xvfj alsa-driver.tar.bz2 `

### 2. Install the linux headers
`apt-get install linux-headers-$(uname -r) `
`cd /usr/src/modules/alsa-driver`

### 3. Configure alsa-source to build all or if you know what you want, selet only what you need. (all is the default so you can skip this step.
`dpkg-reconfigure alsa-source`

### 4. Produce the new alsa package
`fakeroot debian/rules binary_modules KSRC=/usr/src/linux-headers-$(uname -r) KVERS=$(uname -r)`

### 5. Install the new alsa package
`dpkg --install /usr/src/modules/alsa-modules-$(uname -r)_1.0.23+dfsg-2_i386.deb`

