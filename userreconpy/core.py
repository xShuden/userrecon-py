#!/usr/bin/env python3

import sys
import json
import asyncio
import pkg_resources
import time

try:
    import aiohttp
    from colorama import init, Fore, Style

except ModuleNotFoundError as e:
    print(f"[-] error: {e}")
    print(
        "[!] please install the requirements: $ sudo -H pip3 install -r requirements.txt"
    )
    sys.exit(1)


class Userreconpy:
    def __init__(self, args):
        self.args = args
        self.username = self.args["USERNAME"]
        self.websites = self.get_websites()
        self.results = {}

    def generate_json_file(self):

        filename = f"{self.username}-{time.strftime('%y-%m-%d-%H-%M-%S')}"
        output = json.dumps(self.results, indent=2)
        with open(f"{filename}.json", "w") as f:
            f.write(output)

        print(f"[*] file {filename}.json was created\033[J")

    def get_websites(self) -> list:

        filepath = pkg_resources.resource_filename(
            "userreconpy", "web_accounts_list.json"
        )
        with open(filepath, encoding="utf8") as website_list:
            return json.load(website_list)["sites"]

    async def check_response(self, response, web: dict):

        url = web["check_uri"].format(account=self.username)
        account_existence_string = web["account_existence_string"]
        name = web["name"]

        content = await response.content.read()
        content = str(content)

        def print_positive_results():
            if response.status == 200 and account_existence_string in content:
                print(f"{Fore.GREEN}[+] {name}: {url}{Fore.RESET}\033[J")
                self.results[name] = {"status":"positive", "url":url}
            else:
                print(f"[-] {name}: {url}\033[J", end="\r")

        def print_negative_results():
            if not response.status == 200 or not account_existence_string in content:
                print(f"{Fore.YELLOW}[-] {name}: {url}{Fore.RESET}\033[J")
                self.results[name] = {"status":"negative", "url":url}
            else:
                print(f"[+] {name}: {url}\033[J", end="\r")

        def print_all_results():
            if response.status == 200 and account_existence_string in content:
                print(f"{Fore.GREEN}[+] {name}: {url}{Fore.RESET}")
                self.results[name] = {"status":"positive", "url":url}
            else:
                print(f"{Fore.YELLOW}[-] {name}: {url}{Fore.RESET}")
                self.results[name] = {"status":"negative", "url":url}

        switch = {
            "--all": print_all_results,
            "--positive": print_positive_results,
            "--negative": print_negative_results,
        }

        for key, value in self.args.items():
            if value and key in switch:
                switch[key]()

    async def fetch(self, session, web: dict):

        url = web["check_uri"].format(account=self.username)
        try:
            async with session.get(url, timeout=120) as response:
                await self.check_response(response, web)
        except Exception as e:
            print(f"{Fore.RED}[x] {url}{Fore.RESET}\033[J")
            pass

    async def run(self):

        connector = aiohttp.TCPConnector()
        async with aiohttp.ClientSession(connector=connector) as session:
            await asyncio.gather(*[self.fetch(session, web) for web in self.websites])

    def main(self):

        username = Style.BRIGHT + self.username + Style.RESET_ALL

        start_time = time.time()
        print(
            f"[*] checking username: {username} in {len(self.websites)} websites\033[J"
        )
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run())
        loop.close()
        print(f"[*] results found in: {time.time() - start_time:0.2f}s\033[J")

        if self.args["--output"]:
            self.generate_json_file()
