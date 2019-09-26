#!/usr/bin/env python3


try:
    from colorama import init, Fore, Style

except ModuleNotFoundError as e:
    print(f"[-] error: {e}")
    print(
        "[!] please install the requirements: $ sudo -H pip3 install -r requirements.txt"
    )
    sys.exit(1)


def print_banner(version):

    print(
        f"""
  __  __________  _____________  _________  ____        ____  __  __
 / / / / ___/ _ \\/ ___/ ___/ _ \\/ ___/ __ \\/ __ \\______/ __ \\/ / / /
/ /_/ (__  )  __/ /  / /  /  __/ /__/ /_/ / / / /_____/ /_/ / /_/ /
\\__,_/____/\\___/_/  /_/   \\___/\\___/\\____/_/ /_/     / .___/\\__, /
       {Fore.GREEN}Version: {version} | Author: decoxviii{Fore.RESET}           /_/    /____/\n\n"""
    )
