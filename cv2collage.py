# If the user has selected several files, we get all paths of them and process them in one instance.
# If sys.argv contains "collagefolder", the user has selected a whole folder, and we skip this step.
# Attention: selecting individual files is expensive, but nothing else has worked so far.
# https://stackoverflow.com/a/1824064/15096247
# sleeptime is the time between each file scan, if no more files are added, the function returns the
# file list to process. If the sleep time is too short, not all selected files will be parsed.
from shellextools.getmultifiles import get_all_selected_files
import sys
if len(sys.argv) > 1:
    if 'collagefolder' not in sys.argv:
        allmyfiles = get_all_selected_files(sleeptime=4)

# parses sys.argv and changes the default arguments path/str in main(path: str = "", action: str = "")
from hackyargparser import add_sysargv

from PIL import Image
from cv2_collage_v2 import create_collage_v2
from tkinteruserinput import get_user_input
from a_cv_imwrite_imread_plus import open_image_in_cv
from shellextools import (
    format_folder_drive_path_backslash, add_multicommands_files, get_my_icon, add_multi_commands_to_drive_and_folder,
)
from shellextools import create_file_with_timestamp,show_notification,get_folder_file_complete_path
import os
import numpy as np


# icon for tkinter pop-ups
myicon = get_my_icon(iconfile="iconapp.ico")
@add_sysargv
def main(path: str = "", action: str = ""):
    """
    This function creates a collage of images from a given folder or a list of images.

    Args:
        path (str): The path of the folder containing the images or the list of images.
        action (str): The action to be performed. It can be either 'collagefolder' or 'collage'.

    Returns:
        int: Returns 0 if the function executes successfully.

    Raises:
        None

    """
    lst = []
    # if the user has clicked on a single folder, we get all files recursively, and check which can be opened by PIL
    if action == 'collagefolder':
        exts = Image.registered_extensions()
        supported_extensions = [ex[1:] for ex, f in exts.items() if f in Image.OPEN]
        supported_extensions = [x.lower().strip('. ') for x in supported_extensions]
        mypath=format_folder_drive_path_backslash(path)
        allfiles=get_folder_file_complete_path(mypath)
        for fia in allfiles:
            if fia.ext.lower().strip('. ') in supported_extensions:
                lst.append(format_folder_drive_path_backslash(fia.path))


    if action == "collage":
        # if the user has selected several files, we get the paths from the list of lists
        lst = [x[x.index('--path') + 1] for x in allmyfiles]
        lst = [format_folder_drive_path_backslash(pa) for pa in lst] # format_folder_drive_path_backslash strips quotes, spaces etc.

    imagewidth = get_user_input( # The width of the output image
        linesinputbox=1,
        size="800x250",
        title="Collage width",
        textabovebox="Enter the desired collage width:",
        submitbutton="Submit",
        regexcheck=r"\d+",
        showerror=("Error", "This is not a number! Try again!"),
        showinfo=None,
        showwarning=None,
        icon=myicon,
    )
    # a rough orientation for the number of elements in each row/column.
    # Result may vary due to different image sizes
    heightdiv = get_user_input(
        linesinputbox=1,
        size="800x250",
        title="Collage height divider",
        textabovebox="Enter the desired height divider:",
        submitbutton="Submit",
        regexcheck=r"\d+",
        showerror=("Error", "This is not a number! Try again!"),
        showinfo=None,
        showwarning=None,
        icon=myicon,
    )
    # a rough orientation for the number of elements in each row/column.
    # Result may vary due to different image sizes
    widthdiv = get_user_input(
        linesinputbox=1,
        size="800x250",
        title="Collage width divider",
        textabovebox="Enter the desired width divider:",
        submitbutton="Submit",
        regexcheck=r"\d+",
        showerror=("Error", "This is not a number! Try again!"),
        showinfo=None,
        showwarning=None,
        icon=myicon,
    )

    imagewidth=int(imagewidth)
    widthdiv=int(widthdiv)
    heightdiv=int(heightdiv)

    # the collage will be saved in the same dictionary as png with a time stamp
    newfi = create_file_with_timestamp(
        folder=os.sep.join(lst[0].split(os.sep)[:-1]), extension=".png", prefix="collage_", suffix="", sep="_",
        create_file=False
    )
    allpics = []
    for fi in lst:
        try:
            # OpenCV can't open as many formats as PIL, but we try it first, because it is faster
            allpics.append(open_image_in_cv(fi,channels_in_output=4))
        except Exception as fe:
            try:
                # If it fails, we try it with PIL, and convert the image to a numpy array
                allpics.append(open_image_in_cv(np.array(Image.open(fi)), channels_in_output=4))
            except Exception:
                continue

    # creates the collage, default background color is (0, 0, 0)
    _ = create_collage_v2(allpics, maxwidth=imagewidth, heightdiv=heightdiv, widthdiv=widthdiv, background=(0, 0, 0),
                                save_path=newfi, )

    # When the collage is done, a toast will be shown.
    # You should wait until you see the toast, and don't create collages simultaneously

    show_notification(
        title="Collage is ready!",
        msg=newfi,
        icon_path=None,
        repeat=2,
        sleeptime=1,
    )

    return 0

if __name__ == "__main__":
    # when we click on the app the first time, it installs itself, and adds the file extensions to the Windows' reg.
    # Probably you need admin rights to do that. This step might trigger your Anti-Virus
    if len(sys.argv) == 1:
        exts = Image.registered_extensions()
        supported_extensions = [ex[1:] for ex, f in exts.items() if f in Image.OPEN]
        # just change the .py ending to .exe - don't name it differently
        # it must be hard coded! There is no way of using sys.argv[0] or __file__
        futurnameofcompiledexe = "cv2collage.exe"
        multicommands = [
            {
                "mainmenuitem": "CVTools",
                "submenu": "Collage",
                "folderinprogramdata": "RCTools",
                "filetypes": exts, # all extensions that PIL can read
                "additional_arguments": "--action collage",  # action will be automatically updated by hackyargparser
            }
        ]
        # Adds everything to the Windows' reg, copies the file to "C:\ProgramData\RCTools"
        # and creates an uninstaller cv2collage_uninstall.cmd - This step might trigger your Anti-Virus
        add_multicommands_files(multicommands, futurnameofcompiledexe)

        multicommands = [
            {
                "mainmenuitem": "CVTools",
                "submenu": "Collage",
                "folderinprogramdata": "RCTools",
                "add2drive": True, # will be available in the context menu of a drive
                "add2folder": True, # will be available in the context menu of any folder
                "additional_arguments": "--action collagefolder",
            },

        ]
        add_multi_commands_to_drive_and_folder(
            futurnameofcompiledexe,
            multicommands,
        )


    else:
        # if there is more than one item in sys.argv, we create the collage
        # The first time you run it, it might fail, because the temp folder for
        # loggax3.exe (takes care of multiple file selection)
        # has not been created yet.
        main()
