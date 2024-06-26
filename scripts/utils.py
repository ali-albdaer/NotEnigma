from config import PRINT_COLOR


colors = {
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'reset': '\033[0m'
}

def color_text(color, text):
    if not PRINT_COLOR:
        return text
    
    color = colors.get(color.lower(), colors['reset'])
    return f'{color}{text}\033[0m'

def print_color(color, text):
    if not PRINT_COLOR:
        print(text)
        return
    
    color = colors.get(color.lower(), colors['reset'])
    print(f'{color}{text}\033[0m')
