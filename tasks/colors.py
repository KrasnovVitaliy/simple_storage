class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_green(value):
    print(f"{Colors.OKGREEN}{value}{Colors.ENDC}")


def print_cyan(value):
    print(f"{Colors.OKCYAN}{value}{Colors.ENDC}")


def print_blue(value):
    print(f"{Colors.OKBLUE}{value}{Colors.ENDC}")


def print_yellow(value):
    print(f"{Colors.WARNING}{value}{Colors.ENDC}")


def print_red(value):
    print(f"{Colors.FAIL}{value}{Colors.ENDC}")
