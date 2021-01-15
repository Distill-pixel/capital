# Capital
Capital is a completely proxyless Roblox asset downloader. You can download Decals/Models/Audios/Videos/Animations etc.
# Instructions [WINDOWS]
```
‣ Download the ZIP file, then extract it to a location you wish to.
‣ Edit the "ids.txt" file. Paste all your asset ID's here with a linebreak.
‣ Run the executable. You might have issues with your anti-virus, if so, please disable it or add an exclusion for the executable.
‣ Choose a mode.
‣ Choose the amount of threads.
‣ All done! It will now check all the ID's specified.
```
# Run from source on Linux
```bash
# You need to have python3 installed by default.
$ sudo apt install git # this is for Debian/Ubuntu or their forks. you may have to use pacman etc. for other distro's.
$ git clone https://github.com/distill-pixel/capital
$ cd capital
$ python3 -m ensurepip
$ python3 -m pip install -r requirements.min.txt
$ vim ids.txt
# Enter your ID's. You can use Nano etc. as well.
$ python3 main.py
```
# Run from source on Windows
```
‣ Install Python3 from https://python.org (>3.6)
‣ Download the repo with git or download the zip file and extract it in a folder.
‣ Install modules with pip3 install -r requirements.min.txt
‣ Edit the ids.txt file with notepad.
‣ Run python3 main.py
```
# Note
This project is poorly made as there was not a lot of time spent on it, but it works nevertheless. It should perform decently and finish checking ID's fast. It all depends on the amount though. Errors are written to errors.txt. All binaries are for the amd64 architecture, for running it on ARM64/PowerPC/x86/ARMHF etc. architectures, you will have to run it from source.
# Credits
Felix for helping me compile it for Windows (I don't have a Windows machine) and Shidposter for the idea.
