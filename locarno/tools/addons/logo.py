# Import modules
from colorama import Fore
from colorama import init
from termcolor import cprint 
from pyfiglet import figlet_format

# Logo
cprint('--------------------------------------------', 'red')
cprint(figlet_format('Локарно', font='standard'), 'red', attrs=['bold'])
cprint('--------------------------------------------', 'red')
cprint('ZARMAZD представляет: М.К.Т. АС-4 "Локарно".', 'red')
cprint('Это бета-версия. Обо всех ошибках сообщайте автору.', 'red')
