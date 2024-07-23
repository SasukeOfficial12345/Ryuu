import curses
import pyfiglet
import subprocess
import requests
import os
import sys

VERSION = "1.1"
UPDATE_URL = "https://raw.githubusercontent.com/SasukeOfficial12345/Ryuu/main/RyuuFilesMLBB.py"
VERSION_URL = "https://raw.githubusercontent.com/SasukeOfficial12345/Ryuu/main/version.txt"

def check_for_update():
    try:
        response = requests.get(VERSION_URL)
        response.raise_for_status()
        latest_version = response.text.strip()
        if latest_version > VERSION:
            return True, latest_version
        return False, None
    except Exception as e:
        return False, None

def update_script():
    try:
        response = requests.get(UPDATE_URL)
        response.raise_for_status()
        script_path = os.path.realpath(__file__)
        with open(script_path, 'w') as file:
            file.write(response.text)
        return True
    except Exception as e:
        return False

def print_header(stdscr):
    figlet_text = pyfiglet.figlet_format("RYUUFILESMLBB")
    stdscr.addstr(0, 0, figlet_text, curses.color_pair(1))
    stdscr.addstr(6, 0, f"VERSION {VERSION}", curses.color_pair(1))
    stdscr.refresh()

def print_menu(stdscr, selected_row_idx, menu):
    stdscr.clear()
    print_header(stdscr)
    
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) // 2 + idx + 8  # Offset to leave space for header and version
        if idx == selected_row_idx:
            stdscr.addstr(y, x, row, curses.color_pair(2))
        else:
            stdscr.addstr(y, x, row, curses.color_pair(1))
    
    stdscr.refresh()

def perform_action(stdscr, action):
    stdscr.clear()
    print_header(stdscr)

    if action == 'MLBBCONFIG.zip':
        stdscr.addstr(10, 0, "You selected MLBBCONFIG.zip", curses.color_pair(1))
        stdscr.refresh()
        
        # Update and upgrade packages
        subprocess.run(["pkg", "update"], capture_output=True, text=True)
        stdscr.addstr(12, 0, "Update complete. Upgrading packages...", curses.color_pair(1))
        stdscr.refresh()
        subprocess.run(["pkg", "upgrade", "-y"], capture_output=True, text=True)
        stdscr.addstr(14, 0, "Upgrade complete.", curses.color_pair(1))
        stdscr.refresh()
        
        # Install Git
        subprocess.run(["pkg", "install", "git", "-y"], capture_output=True, text=True)
        stdscr.addstr(16, 0, "Git installation complete.", curses.color_pair(1))
        stdscr.refresh()
        
        # Check for wget and install if not present
        result = subprocess.run("command -v wget", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            stdscr.addstr(18, 0, "wget not found. Installing wget...", curses.color_pair(1))
            subprocess.run(["pkg", "install", "wget", "-y"], capture_output=True, text=True)
            stdscr.addstr(20, 0, "wget installation complete.", curses.color_pair(1))
        else:
            stdscr.addstr(18, 0, "wget is already installed.", curses.color_pair(1))
        stdscr.refresh()
        
        # Download the file using wget
        subprocess.run(["wget", "https://github.com/SasukeOfficial12345/NormalCon/raw/main/NormalConfiguration-BRONLY.zip"], capture_output=True, text=True)
        stdscr.addstr(22, 0, "File downloaded.", curses.color_pair(1))
        stdscr.refresh()

    elif action == 'MLBBFIXDELAY.zip':
        stdscr.addstr(10, 0, "You selected MLBBFIXDELAY.zip", curses.color_pair(1))
        # Add specific code for MLBBFIXDELAY.zip here

    elif action == 'MLBBSDOWNLOADFILES.zip':
        stdscr.addstr(10, 0, "You selected MLBBSDOWNLOADFILES.zip", curses.color_pair(1))
        # Add specific code for MLBBSDOWNLOADFILES.zip here

    elif action == 'SUBSCRIBED':
        stdscr.addstr(10, 0, "You selected SUBSCRIBED", curses.color_pair(1))
        # Add specific code for SUBSCRIBED here

    elif action == 'Exit':
        stdscr.addstr(10, 0, "Exiting...", curses.color_pair(1))
        stdscr.refresh()
        stdscr.getch()
        return  # Exit the function

    stdscr.refresh()
    stdscr.getch()

def main(stdscr):
    # Check for updates
    update_available, latest_version = check_for_update()
    if update_available:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Update available: {latest_version}. Updating...", curses.color_pair(1))
        stdscr.refresh()
        if update_script():
            stdscr.addstr(2, 0, "Update successful. Restarting...", curses.color_pair(1))
            stdscr.refresh()
            stdscr.getch()
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            stdscr.addstr(2, 0, "Update failed. Continuing with current version...", curses.color_pair(1))
            stdscr.refresh()
            stdscr.getch()

    # Turn off cursor blinking
    curses.curs_set(0)

    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Regular text
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Selected text

    # Menu items
    menu = ['MLBBCONFIG.zip', 'MLBBFIXDELAY.zip', 'MLBBSDOWNLOADFILES.zip', 'SUBSCRIBED', 'Exit']

    # Specify the current selected row
    current_row = 0

    # Print the menu
    print_menu(stdscr, current_row, menu)

    while True:
        key = stdscr.getch()
        
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == ord('\n'):
            if current_row == len(menu) - 1:
                perform_action(stdscr, 'Exit')
                break
            perform_action(stdscr, menu[current_row])
        
        print_menu(stdscr, current_row, menu)

if __name__ == "__main__":
    curses.wrapper(main)
