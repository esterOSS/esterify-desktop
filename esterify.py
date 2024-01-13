import sys
import time
import os
import shutil
import subprocess  # Import the subprocess module for running shell commands

if os.geteuid() != 0:
    print("This script must be run with superuser rights.")
    sys.exit(1)

devices = ["Desktop", "Mobile", "Enterprise"]
mobile_distros = ["postmarketOS", "Mobian"]
mobile_de = ["Phosh", "GNOME Vanilla/Mobile", "Plasma Mobile"]
desktop_distros = ["Ubuntu", "Debian", "Arch Linux", "Fedora", "Gentoo", "Alpine", "Nix OS"]
desktop_de = ["GNOME Vanilla", "Plasma"]
enterprise_distros = ["CentOS", "Red Hat"]
enterprise_de = ["GNOME Vanilla", "Plasma"]

def display_menu(array):
    print("Choose an option:")
    for i in range(len(array)):
        print(f"{i + 1}. {array[i]}")
    print("0. Exit")

def get_selection(array):
    choice = input("Enter your choice (0-%d): " % (len(array)))
    if not choice.isdigit():
        print("Invalid choice. Please enter a number.")
        return get_selection(array)
    choice = int(choice)
    if choice < 0 or choice > len(array):
        print("Invalid choice. Please select a valid option.")
        return get_selection(array)
    return choice

while True:
    display_menu(devices)
    choice = get_selection(devices)

    if choice == 0:
        print("Goodbye!")
        sys.exit(0)
    elif choice == 2:
        display_menu(mobile_distros)
        choice = get_selection(mobile_distros)
        if choice == 1: 
            print("This operation will install the icons, font, and edit the application shortcuts (potentially dangerous). \nIf you don't want to do this, press Ctrl+C. \nStarting operation in 5 seconds!")
            for i in [5, 4, 3, 2, 1]:
                print(i)
                time.sleep(1)

            # Copy the `estericons` folder to `/usr/share/icons/`.
            estericons_folder = os.path.join(os.path.dirname(__file__), "estericons")
            destination_folder = "/usr/share/icons/"
            shutil.copytree(estericons_folder, destination_folder)

            print("The icons have been copied to `/usr/share/icons/`.")

            # Copy the `Gilroy` file to `/usr/share/fonts/`.
            for fontfile in os.listdir(os.path.join(os.path.dirname(__file__), "fonts")):
                gilroy_font = fontfile
                destination_folder = "/usr/share/fonts/"
                shutil.copy(gilroy_font, destination_folder)

            print("The font has been copied to `/usr/share/fonts/`.")
            
            # Copy the `adw-gtk3` themes to `/usr/share/themes`.
            adw_gtk3 = os.path.join(os.path.dirname(__file__), "adw-gtk3")
            adw_gtk3_dark = os.path.join(os.path.dirname(__file__), "adw-gtk3-dark")
            destination_folder = "/usr/share/themes/"

            shutil.copytree(adw_gtk3, destination_folder)
            shutil.copytree(adw_gtk3_dark, destination_folder)

            print("The themes have been copied to `/usr/share/themes/`.")

            # Execute the gsettings command
            iconsset_command = "gsettings set org.gnome.desktop.interface icon-theme 'estericons'"
            subprocess.call(iconsset_command, shell=True)
            themeset_command = "gsettings set org.gnome.desktop.interface gtk-theme 'adw-gtk3'"
            subprocess.call(themeset_command, shell=True)
            iconsset_command = "gsettings set org.gnome.desktop.interface font-name ''"

            print("The settings are set! Now reboot your system")
            input("Press Enter to exit!")
            os.exit(1)

        else:
            print("This distro isn't supported yet!")
    elif 1 <= choice < len(devices):
        selected_device = devices[choice - 1]
        if choice == 1:
            print("At this point in time, desktop and enterprise Linux distros aren't supported yet! Sorry, I'm working on that right now!")
