from enum import Enum


class ColorEnum(Enum):
    BG_BLACK = "\u001b[40;1m"
    BG_RED = "\u001b[41;1m"
    BG_GREEN = "\u001b[42;1m"
    BG_YELLOW = "\u001b[43;1m"
    BG_BLUE = "\u001b[44;1m"
    BG_MAGENTA = "\u001b[45;1m"
    BG_CYAN = "\u001b[46;1m"
    BG_WHITE = "\u001b[47;1m"
    GREY = "\x1b[38;21m"
    BLUE = "\x1b[38;5;39m"
    YELLOW = "\x1b[38;5;226m"
    RED = "\x1b[38;5;196m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"


def set_color_text_console(text: str, color: ColorEnum) -> str:
    return color.value + text + ColorEnum.RESET.value
