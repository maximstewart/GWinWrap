# GWinWrap
GWinWrap is a Gtk with Python gui to select videos for XWinWrap, images for Nitrogen Wallpaper Manager, and gifs for Gifsicle.
It includes the XWinWrap binary and source code for Shantanu Goel's version of XWinWrap.

# Notes
* Need python 2+
* Need PyGObject
* When you first run the application and save settings for a screen, you need to chmod 744 the new file(s) in your $HOME directory.
* A settings file per screen is generated.


# Images
![1 Default view starting out. ](images/pic1.png)
![2 Video thumbnails in image grid. Path to directory highlighted purple. ](images/pic2.png)
![3 Image thumbnails in image grid. ](images/pic3.png)
![4 Image in preview popup. ](images/pic4.png)
![5 Xscreensaver preview running. ](images/pic5.png)
![6 Settings window poped open. ](images/pic6.png)

# TODO
* Better/automatic screen detection.
* Run chmod against newly created launch scripts.


# Credit
GWinWrap python and glade by: Maxim Stewart  -- https://www.itdominator.com/
<br/>
XWinWrap binary by: Shantanu Goel -- http://tech.shantanugoel.com
