class Colors:
    """ Class that contains styling and color coding for strings inside the Python Console
        To be used in a f string, as follows:

        f"{Colors.STYLE}{Colors.COLOR}some string example {Colors.NORMAL}"

        Styling is optional; but NORMAL has to be used to reset after the desired string formatting
    """

    # TEXT STYLES
    NORMAL = '\033[0m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'

    # TEXT COLORS
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
