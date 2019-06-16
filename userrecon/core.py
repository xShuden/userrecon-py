#!/usr/bin/env python3

from time import time

import pkg_resources
import asyncio
import json
import sys

try:
    from userrecon.version import __version__, __author__
    import aiohttp

except ModuleNotFoundError as error:
    print("[-] error: {}".format(error))
    sys.exit(1)


def print_sexy_banner():
    print(
        """                                                                    
  __  __________  _____________  _________  ____        ____  __  __
 / / / / ___/ _ \\/ ___/ ___/ _ \\/ ___/ __ \\/ __ \\______/ __ \\/ / / /
/ /_/ (__  )  __/ /  / /  /  __/ /__/ /_/ / / / /_____/ /_/ / /_/ / 
\\__,_/____/\\___/_/  /_/   \\___/\\___/\\____/_/ /_/     / .___/\\__, /  
       {}Version: {} | Author: {}{}           /_/    /____/   
""".format(
            "\033[32m", __version__, __author__, "\033[0m"
        )
    )


async def check_status(session, social_network, username):

    global results
    results = {}

    account_missing_string = social_network["account_missing_string"]
    url = social_network["check_uri"].format(account=username)
    name = social_network["name"]

    try:
        async with session.get(url) as resp:
            print("\033[33m[!] {:10}: {}\033[0m\033[J".format(name, url), end="\r")

            text = await resp.text()
            if resp.status == 200 and not account_missing_string in text:
                print(
                    "\033[32m[+] {} : {}\033[0m\033[J".format(
                        social_network["name"], url
                    )
                )
                results[social_network["name"]] = url

        return resp.release()
    except:
        pass


async def verify_username(username):
    
    filepath = pkg_resources.resource_filename("userrecon", "web_accounts_list.json")
    with open(filepath, "r") as data_file:
        web_accounts_list = json.load(data_file)
        social_networks = web_accounts_list["sites"]

    print(
        "[*] checking username {}{}{} in {} social networks".format(
            "\033[1m", username, "\033[0m", len(social_networks)
        )
    )
    start = time()
    async with aiohttp.ClientSession() as session:
        tasks = [
            check_status(session, social_network, username)
            for social_network in social_networks
        ]
        await asyncio.gather(*tasks)
        print(
            "[*] {}{}{} results found in: {:.2f} segs.\033[J".format(
                "\033[1m", len(results.keys()), "\033[0m", time() - start
            )
        )


def generate_json_file(filename):

    output = json.dumps(results, indent=2)
    with open("{}.json".format(filename), "w") as f:
        f.write(output)
        print("[*] file {}.json was created".format(filename))
