from nutikacompile import compile_with_nuitka
import shutil
wholecommand = compile_with_nuitka(
    # Let's create the exe file that parses multiple file selection
    pyfile=r"C:\ProgramData\anaconda3\envs\nu\Lib\site-packages\shellextools\loggax3.py",
    # Other file types are also supported (PIL)
    icon=r"C:\ProgramData\anaconda3\envs\nu\iconapp.ico",
    # If the console is disabled, we can't capture stdout,
    # We use the following flags to avoid a console window:
    # startupinfo = subprocess.STARTUPINFO()
    # creationflags = 0 | subprocess.CREATE_NO_WINDOW
    # startupinfo.wShowWindow = subprocess.SW_HIDE
    disable_console=False,
    file_version="1.0.0.1",
    onefile=True,
    outputdir="c:\\nuitkafdflogga",
    addfiles=[
r"C:\ProgramData\anaconda3\envs\nu\iconapp.ico"
    ],
    # creates a permanent cache folder, this is very important!
    # If you want/need to recompile the app, make sure to delete
    # the cache folder first. In this example, the cache folders are: C:\Users\hansc\AppData\Local\loggax3\1.0.0.1 and
    # C:\Users\hansc\AppData\Local\cv2collage\1.0.0.1
    delete_onefile_temp=False,

    needs_admin=True,
    arguments2add="--msvc=14.3 --noinclude-numba-mode=nofollow --jobs=3 --clean-cache=all",
)

# wait until the first file is compiled, and press ENTER
input('Press ENTER when the process has been finished!')

# copy the icon file to the output folder of the first compilation
# That way, both files will be in the root folder of the cache folder: C:\Users\hansc\AppData\Local\cv2collage\1.0.0.1
shutil.copy(r"C:\ProgramData\anaconda3\envs\nu\iconapp.ico",r'c:\nuitkafdflogga\iconapp.ico')

wholecommand2 = compile_with_nuitka(
    pyfile=r"C:\ProgramData\anaconda3\envs\nu\cv2collage.py",
    icon=r"C:\ProgramData\anaconda3\envs\nu\iconapp.ico",
    # Console disabled
    disable_console=True,
    file_version="1.0.0.1",
    onefile=True,
    outputdir="c:\\nuitkafdfcv2",
    addfiles=[
"c:\\nuitkafdflogga\\loggax3.exe", # We include the file from the first compilation to parse multiple selections
        "c:\\nuitkafdflogga\\iconapp.ico",
    ],
    delete_onefile_temp=False,  # creates a permanent cache folder, important!
    needs_admin=True,
    arguments2add="--msvc=14.3 --noinclude-numba-mode=nofollow --plugin-enable=tk-inter --jobs=3 --clean-cache=all"
)
