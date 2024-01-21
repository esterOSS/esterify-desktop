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
desktop_distros = ["Ubuntu", "Debian", "Arch Linux", "Fedora", "Gentoo", "Alpine", "Nix OS", "openSUSE"]
desktop_de = ["GNOME Vanilla", "Plasma"]
enterprise_distros = ["CentOS", "Red Hat"]
enterprise_de = ["GNOME Vanilla", "Plasma"]

def standard_gnome_installation():
    print("This operation will install the icons, font, and edit the application shortcuts (potentially dangerous). \nIf you don't want to do this, press Ctrl+C. \nStarting operation in 5 seconds!")
    for i in [5, 4, 3, 2, 1]:
        print(i)
        time.sleep(1)
    # Copy the `estericons` folder to `/usr/share/icons/`.
    shutil.copytree(os.path.join(os.path.dirname(__file__), "estericons"), "/usr/share/icons/estericons/")
    print("The icons have been copied to `/usr/share/icons/`.")

    # Copy the `Gilroy` file to `/usr/share/fonts/`.
    for fontfile in os.listdir(os.path.join(os.path.dirname(__file__), "fonts")):
        shutil.copy(os.path.join(os.path.dirname(__file__), "fonts") + "/" + fontfile, "/usr/share/fonts/")
    print("The font has been copied to `/usr/share/fonts/`.")

    # Copy the `adw-gtk3` themes to `/usr/share/themes`.
    shutil.copytree(os.path.join(os.path.dirname(__file__), "adw-gtk3"), "/usr/share/themes/adw-gtk3")
    shutil.copytree(os.path.join(os.path.dirname(__file__), "adw-gtk3") + "-dark", "/usr/share/themes/adw-gtk3" + "-dark")
    print("The themes have been copied to `/usr/share/themes/`.")

    # Execute the gsettings commands
    myuser = os.getlogin()
    os.system(f"sudo -Hu {myuser} dbus-launch gsettings set org.gnome.desktop.interface icon-theme \'estericons\'")
    os.system(f"sudo -Hu {myuser} dbus-launch gsettings set org.gnome.desktop.interface gtk-theme \'adw-gtk3\'")
    os.system(f"sudo -Hu {myuser} dbus-launch gsettings set org.gnome.desktop.interface document-font-name \'Sans 11\'")
    os.system(f"sudo -Hu {myuser} dbus-launch gsettings set org.gnome.desktop.interface font-antialiasing \'rgba\'")
    os.system(f"sudo -Hu {myuser} dbus-launch gsettings set org.gnome.desktop.interface font-hinting \'slight\'")
    os.system(f"sudo -Hu {myuser} dbus-launch gsettings set org.gnome.desktop.interface font-name \'Gilroy-Medium 11\'")
    os.system(f"sudo -Hu {myuser} dbus-launch gsettings set org.gnome.desktop.interface font-rgba-order \'rgb\'")
    os.system(f"sudo -Hu {myuser} dbus-launch gsettings set org.gnome.desktop.interface monospace-font-name \'Monospace 13\'")
    os.system(f"sudo -Hu {myuser} dbus-launch gsettings set org.gnome.desktop.wm.preferences titlebar-font \'Gilroy-Medium 11\'")
    os.system(f"sudo -Hu {myuser} dbus-launch gsettings set org.gnome.desktop.wm.preferences titlebar-uses-system-font true")

    print("The settings are set! Now reboot your system")
    input("Press Enter to exit!")
    exit(1)

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
        exit(1)
    elif choice == 1:
        display_menu(desktop_distros)
        choice = get_selection(desktop_distros)
        display_menu(desktop_de)
        choice = get_selection(desktop_de)
        if choice == 1:
            standard_gnome_installation()
        elif choice != 0 :
            print("This desktop isn't supported yet!")
        else:
            print("Goodbye!")
            exit(1)
    elif choice == 2:
        display_menu(mobile_distros)
        choice = get_selection(mobile_distros)
        if choice == 1: 
            display_menu(mobile_de)
            choice = get_selection(mobile_de)
            if choice == 2:
                standard_gnome_installation()
            elif choice != 0 :
                print("This desktop isn't supported yet!")
            else:
                print("Goodbye!")
                exit(1)
        elif choice != 0:
            print("This distro isn't supported yet!")
        else:
            print("Goodbye!")
            exit(1)
    elif choice == 3:
        display_menu(enterprise_distros)
        choice = get_selection(enterprise_distros)
        display_menu(enterprise_de)
        choice = get_selection(enterprise_de)
        if choice == 1:
            standard_gnome_installation()
        elif choice != 0 :
            print("This desktop isn't supported yet!")
        else:
            print("Goodbye!")
            exit(1)
    #elif 1 <= choice < len(devices):
    #    selected_device = devices[choice - 1]
    #    if choice == 1:
    #        print("At this point in time, desktop and enterprise Linux distros aren't supported yet! Sorry, I'm working on that right now!")
