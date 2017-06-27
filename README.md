# dcs5020l
Python module for controlling the dcs5020l PTZ camera

Introduction
============
I had this DCS5020L PTZ camera laying about and I was annoyed by the
web interface.  So I started looking into how to automate it via HTTP
requests in python.

Finding endpoints
-----------------
I went from various sites such as: [Dlink forums](http://forums.dlink.com/index.php?topic=57131.0) for solutions but was stumped when trying to find out camera positions and other controls for the IR emitters.

[binwalk](https://github.com/devttys0/binwalk) is your friend.

I went to DLINK's site, downloaded the firmware upgrade image and ran binwalk over it.  Sure enough, I exposed some additional endpoints that I could reach but it wasn't until I ran strings on the alphapd binary that exposed even more.

Found endpoints (that are used now)
-----------------------------------
* POST url+/pantiltcontrol.cgi
* GET  url+/image.jpg
* GET  url+/config/ptz_pos.cgi
* POST url+/nightmodecontrol.cgi

Methods
-------
* connect
* disconnect
* down
* up
* left
* right
* home
* getImage
* getPosition
* daynight
