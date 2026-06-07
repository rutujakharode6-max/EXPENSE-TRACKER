from colorama import init, Fore, Style
import sys

# Initialize Colorama (converts ANSI escape sequences to Windows API calls if needed)
init(autoreset=True)

def pastel_color(hex_str):
    """
    Generate an ANSI escape sequence for a truecolor (24-bit) foreground color.
    """
    hex_str = hex_str.lstrip('#')
    r, g, b = tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{r};{g};{b}m"

# Required Colors
PINK = pastel_color("#FFB6C1")
BLUE = pastel_color("#B0E0E6")
GREEN = pastel_color("#98FB98")

ASCII_HEADER = f"""
{PINK}   ____        __     __   ____               __          
{PINK}  / __ \____ _/ /____/ /  /_  /________ _____/ /_____  ___ 
{BLUE} / /_/ / __ `/ __/ _ \ /   / / / ___/ __ `/ __/ //_/ _ \/ ___/
{BLUE}/ ____/ /_/ / /_/  __/ /  / / / /  / /_/ / /_/ ,< /  __/ /    
{GREEN}\/    \__,_/\__/\___/_/  /_/ /_/   \__,_/\__/_/|_|\___/_/     
{Style.RESET_ALL}
"""

def show_startup_message():
    print(ASCII_HEADER)
    print(f"{BLUE}Starting the Pastel Expense Tracker...{Style.RESET_ALL}")
    print(f"{PINK}Loading your expenses...{Style.RESET_ALL}")
    print(f"{GREEN}Ready! Please refer to the GUI window.{Style.RESET_ALL}\n")
