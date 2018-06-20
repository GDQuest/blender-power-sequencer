## Version 1.1

### FFmpeg build proxies

Big thanks to @sudopluto for his work on the proxy generation script. He added % based-reporting and rewrote the code to make it easier to extend in the future, and to eventually make the script accessible from Blender.

### Multithreaded rendering

Use all your CPU power to render videos! Running multiple instances of Blender in the background, this script will smartly distribute rendering across your CPU cores. You can limit the number of cores and keep working while renders happen in the background.

Thanks to Justin Warren for the original [pulverize](https://github.com/sciactive/pulverize/blob/master/pulverize.py) script. We've fixed some of its bugs and we're looking to add new features to it.
