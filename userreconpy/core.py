#!/usr/bin/env python3

try:
    from userreconpy.version import __version__, __author__
    from time import time

    import pkg_resources
    import asyncio
    import json
    import sys

    # requirements.txt
    from colorama import init, Fore, Style
    import aiohttp

except ModuleNotFoundError as e:
    print("[-] error: {}".format(e))
    sys.exit(1)

# colorama
init()

RESULTS = {}


def print_sexy_banner():
    print(
        """                                                                    
  __  __________  _____________  _________  ____        ____  __  __
 / / / / ___/ _ \\/ ___/ ___/ _ \\/ ___/ __ \\/ __ \\______/ __ \\/ / / /
/ /_/ (__  )  __/ /  / /  /  __/ /__/ /_/ / / / /_____/ /_/ / /_/ / 
\\__,_/____/\\___/_/  /_/   \\___/\\___/\\____/_/ /_/     / .___/\\__, /  
       {}Version: {} | Author: {}{}           /_/    /____/   
""".format(
            Fore.GREEN, __version__, __author__, Fore.RESET
        )
    )


def generate_json_file(filename):
    """ generate JSON file with output
    """

    output = json.dumps(RESULTS, indent=2)
    with open("{}.json".format(filename), "w") as f:
        f.write(output)

    print("[*] file {}.json was created".format(filename))


async def check_username_exists(session, social_network, username):
    """Check if the username exists
    """

    account_existence_string = social_network["account_existence_string"]
    url = social_network["check_uri"].format(account=username)
    name = social_network["name"]

    try:
        async with session.get(url) as resp:
            print(
                "{}[!] {:10}: {}{}\033[J".format(Fore.YELLOW, name, url, Fore.RESET),
                end="\r",
            )

            text = await resp.text()
            if resp.status == 200 and account_existence_string in text:
                print(
                    "{}[+] {} : {}{}\033[J".format(
                        Fore.GREEN, social_network["name"], url, Fore.RESET
                    )
                )

                RESULTS[social_network["name"]] = url

        return resp.release()

    except:
        pass


def get_social_networks_list():
    """ Get the social networks list
    """

    filepath = pkg_resources.resource_filename("userreconpy", "web_accounts_list.json")

    with open(filepath, "r") as data_file:
        web_accounts_list = json.load(data_file)
        social_networks = web_accounts_list["sites"]

    return social_networks


async def checking_username(username: str):
    """Check the username on all social networks
    """

    social_networks = get_social_networks_list()

    print(
        "[*] checking username {}{}{} in {} social networks".format(
            Style.BRIGHT, username, Style.RESET_ALL, len(social_networks)
        )
    )

    start = time()
    async with aiohttp.ClientSession() as session:
        tasks = [
            check_username_exists(session, social_network, username)
            for social_network in social_networks
        ]
        await asyncio.gather(*tasks)

        print(
            "[*] {}{}{} results found in: {:.2f}s.\033[J".format(
                Style.BRIGHT, len(RESULTS.keys()), Style.RESET_ALL, time() - start
            )
        )

