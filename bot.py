import requests
import json
import urllib.parse
import os
from datetime import datetime
from core.helper import get_headers, countdown_timer, extract_user_data, config
from colorama import *
import random



class Drops:
    def __init__(self) -> None:
        self.session = requests.Session()


    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        banner = f"""{Fore.GREEN}
                 ██████  ██    ██   ██████  ██    ██  ███    ███  ██████   ███████  ██████  
                ██       ██    ██  ██       ██    ██  ████  ████  ██   ██  ██       ██   ██ 
                ██       ██    ██  ██       ██    ██  ██ ████ ██  ██████   █████    ██████  
                ██       ██    ██  ██       ██    ██  ██  ██  ██  ██   ██  ██       ██   ██ 
                 ██████   ██████    ██████   ██████   ██      ██  ██████   ███████  ██   ██     
                    """
        print(Fore.GREEN + Style.BRIGHT + banner + Style.RESET_ALL)
        print(Fore.GREEN + f" Drops coin Bot")
        print(Fore.RED + f" FREE TO USE = Join us on {Fore.GREEN}t.me/cucumber_scripts")
        print(Fore.YELLOW + f" before start please '{Fore.GREEN}git pull{Fore.YELLOW}' to update bot")
        print(f"{Fore.WHITE}~" * 60)

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def load_data(self, query: str):
        query_params = urllib.parse.parse_qs(query)
        query = query_params.get('user', [None])[0]

        if query:
            user_data_json = urllib.parse.unquote(query)
            user_data = json.loads(user_data_json)
            first_name = user_data['first_name']
            return first_name
        else:
            raise ValueError("User data not found in query.")
        
    def sessions(self, query: str):
        url = "https://api.drops-tgcoin.com/sessions"
        data = json.dumps({'encodedMessage':query})
        self.headers.update({ 
            'Content-Type': 'application/json'
        })

        response = self.session.post(url,headers=self.headers, data=data)
        if response.status_code == 200:
            return response.json()['token']
        else:
            return None
        
    def sign_up(self, token: str):
        url = "https://api.drops-tgcoin.com/users/sign-up-rewards"
        self.headers.update({ 
            'Content-Type': 'application/json',
            'X-Auth-Token': token
        })

        response = self.session.post(url,headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def rewards(self, token: str):
        url = "https://api.drops-tgcoin.com/drops/claim/rewards"
        self.headers.update({ 
            'Content-Type': 'application/json',
            'X-Auth-Token': token
        })

        response = self.session.get(url,headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def claim_farming(self, token: str):
        url = "https://api.drops-tgcoin.com/drops/claim/rewards"
        self.headers.update({ 
            'Content-Type': 'application/json',
            'X-Auth-Token': token
        })

        response = self.session.post(url,headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def tasks(self, token: str):
        url = "https://api.drops-tgcoin.com/tasks"
        self.headers.update({ 
            'Content-Type': 'application/json',
            'X-Auth-Token': token
        })

        response = self.session.get(url,headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def verify_tasks(self, token: str, task_id: int):
        url = f"https://api.drops-tgcoin.com/tasks/{task_id}/verify"
        self.headers.update({ 
            'Content-Type': 'application/json',
            'Content-length': '0',
            'X-Auth-Token': token
        })

        response = self.session.post(url,headers=self.headers)
        if response.status_code == 201:
            return True
        else:
            return False
        
    def process_query(self, query: str):

        account = self.load_data(query)

        token = self.sessions(query)
        if not token:
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}[ Query Account{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {account}  {Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT}Isn't Valid{Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
            )
            return
        
        user = self.rewards(token)
        if not user:
            signup = self.sign_up(token)
            if signup:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {signup['user']['firstName']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {signup['user']['dropsAmount']:.2f} $DROPS {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
            return

        if user:
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {account} {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {user['dropsAmount']:.2f} $DROPS {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
            )
        else:
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT}  {Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT}Is None{Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
            )

        claim_farm = self.claim_farming(token)
        if claim_farm:
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {claim_farm['changeAmount']:.2f} $DROPS {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
            )
        else:
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                f"{Fore.YELLOW+Style.BRIGHT} Is Already Claimed {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
            )

        tasks = self.tasks(token)
        if tasks:
            for task in tasks:
                task_id = task['id']

                if task and task['active']:
                    verify = self.verify_tasks(token, task_id)
                    if verify:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {task['title']} {Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {task['rewardDrops']} $DROPS {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {task['title']} {Style.RESET_ALL}"
                            f"{Fore.RED+Style.BRIGHT}Isn't Completed{Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                        )
        else:
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                f"{Fore.YELLOW+Style.BRIGHT} Is None {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
            )

    def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            with open('proxies.txt', 'r') as file:
                proxies = [line.strip() for line in file if line.strip()]

            while True:
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Proxy's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(proxies)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-------------------------------------------------------------------{Style.RESET_ALL}")
                
                for i, query in enumerate(queries):
                    query = query.strip()
                    if query:
                        self.log(
                            f"{Fore.GREEN + Style.BRIGHT}Account: {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{i + 1} / {len(queries)}{Style.RESET_ALL}"
                        )
                        if len(proxies) >= len(queries):
                            proxy = self.set_proxy(proxies[i])# Set proxy for each account
                            self.log(
                                f"{Fore.GREEN + Style.BRIGHT}Use proxy: {Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
                            )
                        else:
                            self.log(Fore.RED + "Number of proxies is less than the number of accounts. Proxies are not used!")
                        user_info = extract_user_data(query)
                        user_id = str(user_info.get('id'))
                        self.headers = get_headers(user_id)

                        self.process_query(query)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-------------------------------------------------------------------{Style.RESET_ALL}")
                        account_delay = config['account_delay']
                        countdown_timer(random.randint(min(account_delay), max(account_delay)))

                cycle_delay = config['cycle_delay']
                countdown_timer(random.randint(min(cycle_delay), max(cycle_delay)))

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Drops - BOT.{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":

    bot = Drops()
    bot.clear_terminal()
    bot.welcome()
    bot.main()


