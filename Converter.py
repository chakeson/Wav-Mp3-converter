import ffmpeg
import os, sys, logging, re, urllib, webbrowser, threading, configparser
from tkinter import * # pylint: disable=unused-wildcard-import 
from tkinter import messagebox, filedialog




## LOGGER FOR THE CODE BECAUSE tkinter and pyinstaller break in new ways and to ease that debugging.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_format = " %(asctime)s: %(Levelname)s - %(message)s"
file_handler = logging.FileHandler("log.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(log_format)

#logger.level("Message here")
#logger.exception("Message here") #For try except


# Capture stdout
sys.stdout = open('stdout.txt', 'w')  # Redirect all the prints when we run the program. Relevant when the program runs with no console. This happens when program is built with pyinstaller -windowed tag




def resource_path(relative_path): #for pyinstaller to work with extra files
    logger.debug("Called function resource_path with: "+ str(relative_path))
    try: 
        base_path = sys._MEIPASS    # pylint: disable=no-member
    except Exception:
        logger.exception("ResourcePathing error")
        base_path = os.path.abspath(".")
    logger.info("Resource path"  + str(os.path.join(base_path, relative_path)))
    return os.path.join(base_path, relative_path)


## CONSTANTS
config_file="settings.ini"
__version__ = 1.0
#URL vars
github_url = "https://github.com/chakeson/Wav-Mp3-converter"
license_url = "https://github.com/chakeson/Wav-Mp3-converter/blob/main/LICENSE"
version_url = "https://github.com/chakeson/Wav-Mp3-converter/blob/main/version"

def custom_popup(title_bar, text_to_show):
    logger.debug("Called function custom_popup")
    messagebox.showinfo(title_bar, text_to_show)
    return



def check_license():
    logger.debug("Called function check_license")
    webbrowser.open_new(license_url)
    return

def program_not_working():
    logger.debug("Called function program_not_working")
    custom_popup(u"Sorry", "Most likely YouTube has changed something and thus the program needs to be updated with the latest version of one of it's dependencies YouTube-dl. Find out if it's this click \"check for updates\" button. If not this you are probably not putting in correct links to videos.\n If not any of this please report it on GitHub, click the \"GitHub\" button")
    return

def github_open():
    logger.debug("Called function github_open")
    webbrowser.open_new(github_url)
    return


def check_update_starter():
    check_update_thread = threading.Thread(target=check_update)
    check_update_thread.start()
    return

## UI help functions
def check_update(): #TODO
    logger.debug("Called function check_update")
    #custom_popup("Not impmented", "Not impmented yet.")
    try:
        logger.debug("Version urllib launched.")
        urlib_request = urllib.request.Request( version_url, headers={'User-Agent': 'Mozilla/5.0'} )
        version_website_text_uft8 = urllib.request.urlopen(urlib_request).read()
        version_website_text_uft8 = version_website_text_uft8.decode("utf-8")
    except Exception as E:
        logger.exception("Urllib request failed.")
        custom_popup("Failed to fetch version.", str(E))
        return
    try:
        website_version_regex = re.compile(r'\"__version__ = [0-9+.]*\<')   #(r'(\"productNameBold\":\")([a-zA-Z\s])*(",")')
        version_from_url = website_version_regex.findall(str(version_website_text_uft8))
        version_from_url = float(version_from_url[14:-1])
    except Exception as E:
        logger.exception("Regex on website text failed.")
        custom_popup("Version checkers regex failed.", str(E))
        return
        
    logger.debug("Version checker, url version is: " + version_from_url)

    if version_from_url > __version__:
        logger.debug("Newer version, avaliable.")
        custom_popup("New version out", "Latest version is: "+ str(version_from_url))
        github_open() #Open the github in browerser if newer version is out.

    elif version_from_url <= __version__:
        logger.debug("No new version.")
        custom_popup("No new update released", "Currently running: "+str(__version__) + ". Latest published version: " + str(version_from_url))
    else:
        logger.debug("Version checking failed.")
        custom_popup("Version checking failed", "Version checking failed. Suggest manual look up, on github.")


    return


## Chooses the directory to download too, with youtube-dl
def open_dir():
    global directory_name
    user_input = filedialog.askdirectory(initialdir = "/")
    
    #Check if the user choose nothing, and if so does not update.
    if user_input != '' or None:
        directory_name = user_input
    else:
        return

    #Write to config in memory the saved location
    config['download_settings']['file_path'] = directory_name
    #Write config in memeory to the file.
    try:
        with open(config_file, "w") as tobewritten:
            #config.write(filename)
            config.write(tobewritten)
    except Exception as E:
        logger.exception("Resolution error open dir")
        custom_popup("Config file Error open dir", Exception)


    return

##THEME functions

def get_theme_color(theme_choice):
    # Function that contains themes colors.
    # Takes in lowercase string with the themes name, then matched and the right colors are returned
    # Function call looks like  main_color, second_color, third_color, fourth_color, text_color = get_theme_color("dark")
    # Grey, Dark and Black theme colors are based on https://uxdesign.cc/dark-mode-ui-design-the-definitive-guide-part-1-color-53dcfaea5129

    global main_color
    global second_color
    global third_color
    global fourth_color
    global text_color

    if theme_choice == "light":
        main_color = "SystemButtonFace"
        second_color = "SystemButtonFace"
        third_color = "SystemButtonFace"
        fourth_color = "#ffffff"
        text_color = "#000000"
    
    elif theme_choice == "grey":   
        main_color = "#7e7e7e"
        second_color = "#626262"
        third_color = "#515151"
        fourth_color = "#626262"
        text_color = "#F7F7F7"

    elif theme_choice == "dark":   
        main_color = "#121212"
        second_color = "#212121"
        third_color = "#424242"
        fourth_color = "#212121"
        text_color = "#BDBDBD"

    elif theme_choice == "black":
        main_color = "#000000"
        second_color = "#212121"
        third_color = "#424242"
        fourth_color = "#212121"
        text_color = "#9E9E9E"
    
    else:
        raise Exception("Missing theme option"+str(theme_choice))
    
    return main_color, second_color, third_color, fourth_color, text_color



def set_theme(theme_choice):
    #Fetch theme color
    global main_color
    global second_color
    global third_color
    global fourth_color
    global text_color
    #Fetch colors
    main_color, second_color, third_color, fourth_color, text_color = get_theme_color(theme_choice)

    #Save changes
    config['GUI']['theme'] = str(theme_choice)
    try:
        with open(config_file, "w") as tobewritten:
            #config.write(filename)
            config.write(tobewritten)
    except Exception as E:
        logger.exception("Resolution error open dir")
        custom_popup("Config file Error theme select: "+str(theme_choice), Exception)

    return



## Builds the config file with the settings the first time the code is run.
def build_config_file( config, filename):

    
    config['GUI'] = {'theme': 'light'}
    config['download_settings'] = {'standard_resolution': 'Highest resolution',
                                    'file_path': 'False',
                                    'audio_only': 'False',
                                    "finished_notification": "False"}
    try:
        with open(filename, "w") as configfile:
            #config.write(filename)
            config.write(configfile)
    except Exception as E:
        logger.exception("Resolution error")
        custom_popup("Config file Error", Exception)

    return

## Load in config file and validate input 
def load_config_file():


    write_changes = 0

    #Check the filepath
    #directory_name = config.get('download_settings','file_path')
    if config.get('download_settings','file_path') == "" or None:
        config['download_settings']['file_path'] = "False"
        write_changes = 1

    #Theme set up
    
    global main_color
    global second_color
    global third_color
    global fourth_color
    global text_color

    theme_choice = config.get('GUI','theme') 
    try:
        main_color, second_color, third_color, fourth_color, text_color = get_theme_color(theme_choice)
    except Exception as E:
        logger.exception("Theme color fetching failed")
        main_color, second_color, third_color, fourth_color, text_color = get_theme_color("light")
        config['GUI']['theme'] = "light"
        write_changes = 1


    if write_changes == 1:
        try:
            with open(config_file, "w") as tobewritten:
                config.write(tobewritten)
        except Exception as E:
            logger.exception("Resolution error open dir")
            custom_popup("Config file Error open dir", Exception)




    return

def main():
    #Check for settings
    ## CONFIG
    global config
    config = configparser.ConfigParser()
    config.read(config_file)
    
    if config.sections() == []: # if it's an empty list. Checks if empty config and if yes then builds it with standard settings.
        #Make the settings file.
        build_config_file(config, config_file)
    
    load_config_file() #Load into variables the config values and values associated with them.

    

    return

if __name__ == "__main__":
    main()




##GUI Code bellow

#TK set up
root = Tk()
root.title("YouTube-DL GUI") #Title/Name of program in top bar
#path_icon = resource_path('icon.ico') #Program icon path #TODO
#root.iconbitmap(path_icon) #Icon of the program #TODO

root.minsize( 520, 270) #minimum window size
root.geometry("600x300") #Window start up size

## UI scaling with window resizing
#Grid.rowconfigure(root, 0, weight=0)
#Grid.rowconfigure(root, 1, weight=1)
#Grid.columnconfigure(root, 0, weight=0)
#Grid.columnconfigure(root, 1, weight=1)
#Scales the grid with window size/resolution

#Main UI

download_dir_button = Button( root, text="Download file directory", command=open_dir)
download_dir_button.grid(row=1, column=0, sticky="new")


## TOP bar
menu_bar = Menu(root)
root.config(menu=menu_bar)   #Add menu to root

# tearoff=0 remove line in menu which opens up the menu in a separate window.
#Menu Items:
#File
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_separator()
file_menu.add_command(label="Close program", command=root.quit)

#Settings
setting_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Settings", menu=setting_menu)

#Theme submenu
setting_menu_sub_menu = Menu(setting_menu, tearoff=0)
setting_menu_sub_menu.add_command(label="Light", command=lambda: set_theme("light"))
setting_menu_sub_menu.add_command(label="Grey", command=lambda: set_theme("grey"))
setting_menu_sub_menu.add_command(label="Dark", command=lambda: set_theme("dark"))
setting_menu_sub_menu.add_command(label="Black", command=lambda: set_theme("black"))
setting_menu.add_cascade(label="Theme", menu=setting_menu_sub_menu)


#Help/About
help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Check for updates", command=check_update_starter)
help_menu.add_command(label="License", command=check_license)
help_menu.add_command(label="Program not working", command=program_not_working)
help_menu.add_command(label="Github", command=github_open)




root.mainloop()
