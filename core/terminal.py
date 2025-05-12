from colorama import Fore, Style

def log(msg: str, color: str = Fore.RESET) -> None:
    print(color + msg + Style.RESET_ALL)
