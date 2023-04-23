# rc_collage

## What is it? 

[![](https://i.ytimg.com/vi/c9OouCauJ1Y/oar2.jpg?sqp=-oaymwEaCJUDENAFSFXyq4qpAwwIARUAAIhCcAHAAQY=&rs=AOn4CLBa8cG36u-xxiLEfehP5JcSw_a89g)](https://www.youtube.com/shorts/c9OouCauJ1Y)



## How to use the precompiled version

If you want to use it without compiling anything, download the 3 zip files and extract them. 
Click on cv2collage.exe - the app will copy itself to "C:\ProgramData\RCTools\cv2collage.exe" and create an uninstaller
"C:\ProgramData\RCTools\cv2collage_uninstall.cmd" - The whole process takes about 30 seconds, you won't see anything, there 
is no install screen. (You may need administrator rights to install the app.) After the app has been installed, you can access it 
via the Windows context menu (clicking on folders/images)


## How to compile the source code 

1) Create an env (I use Anaconda)
2) Install the requirements https://github.com/hansalemaos/rc_collage/raw/main/requirements.txt
3) Download the source code https://github.com/hansalemaos/rc_collage/raw/main/cv2collage.py
4) Compile it using this script https://github.com/hansalemaos/rc_collage/raw/main/cv2collagecm.py



## False Alarm

Unfortunately, a few Anti-Virus report the EXE file as malware (false positive).
Maybe because the file copies itself to the ProgramData folder, and changes entries in the Windows' Reg
![](https://github.com/hansalemaos/rc_collage/blob/main/falsepositives.png?raw=true)


## Uninstall 

Execute "C:\ProgramData\RCTools\cv2collage_uninstall.cmd"
Delete C:\Users\hansc\AppData\Local\loggax3\1.0.0.1 and C:\Users\hansc\AppData\Local\cv2collage\1.0.0.1


## Create your own Windows Context Menu tools 

https://github.com/hansalemaos/shellextools
