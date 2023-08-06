"""Collection of tools for changing the text of your terminal."""
import os, platform, secrets
from PIL import ImageColor

if platform.system().lower() == 'windows':
    os.system("color")

colors = {
    "0": "#000000",
    "1": "#800000",
    "2": "#008000",
    "3": "#808000",
    "4": "#000080",
    "5": "#800080",
    "6": "#008080",
    "7": "#c0c0c0",
    "8": "#808080",
    "9": "#ff0000",
    "10": "#00ff00",
    "11": "#ffff00",
    "12": "#0000ff",
    "13": "#ff00ff",
    "14": "#00ffff",
    "15": "#ffffff",
    "16": "#000000",
    "17": "#00005f",
    "18": "#000087",
    "19": "#0000af",
    "20": "#0000d7",
    "21": "#0000ff",
    "22": "#005f00",
    "23": "#005f5f",
    "24": "#005f87",
    "25": "#005faf",
    "26": "#005fd7",
    "27": "#005fff",
    "28": "#008700",
    "29": "#00875f",
    "30": "#008787",
    "31": "#0087af",
    "32": "#0087d7",
    "33": "#0087ff",
    "34": "#00af00",
    "35": "#00af5f",
    "36": "#00af87",
    "37": "#00afaf",
    "38": "#00afd7",
    "39": "#00afff",
    "40": "#00d700",
    "41": "#00d75f",
    "42": "#00d787",
    "43": "#00d7af",
    "44": "#00d7d7",
    "45": "#00d7ff",
    "46": "#00ff00",
    "47": "#00ff5f",
    "48": "#00ff87",
    "49": "#00ffaf",
    "50": "#00ffd7",
    "51": "#00ffff",
    "52": "#5f0000",
    "53": "#5f005f",
    "54": "#5f0087",
    "55": "#5f00af",
    "56": "#5f00d7",
    "57": "#5f00ff",
    "58": "#5f5f00",
    "59": "#5f5f5f",
    "60": "#5f5f87",
    "61": "#5f5faf",
    "62": "#5f5fd7",
    "63": "#5f5fff",
    "64": "#5f8700",
    "65": "#5f875f",
    "66": "#5f8787",
    "67": "#5f87af",
    "68": "#5f87d7",
    "69": "#5f87ff",
    "70": "#5faf00",
    "71": "#5faf5f",
    "72": "#5faf87",
    "73": "#5fafaf",
    "74": "#5fafd7",
    "75": "#5fafff",
    "76": "#5fd700",
    "77": "#5fd75f",
    "78": "#5fd787",
    "79": "#5fd7af",
    "80": "#5fd7d7",
    "81": "#5fd7ff",
    "82": "#5fff00",
    "83": "#5fff5f",
    "84": "#5fff87",
    "85": "#5fffaf",
    "86": "#5fffd7",
    "87": "#5fffff",
    "88": "#870000",
    "89": "#87005f",
    "90": "#870087",
    "91": "#8700af",
    "92": "#8700d7",
    "93": "#8700ff",
    "94": "#875f00",
    "95": "#875f5f",
    "96": "#875f87",
    "97": "#875faf",
    "98": "#875fd7",
    "99": "#875fff",
    "100": "#878700",
    "101": "#87875f",
    "102": "#878787",
    "103": "#8787af",
    "104": "#8787d7",
    "105": "#8787ff",
    "106": "#87af00",
    "107": "#87af5f",
    "108": "#87af87",
    "109": "#87afaf",
    "110": "#87afd7",
    "111": "#87afff",
    "112": "#87d700",
    "113": "#87d75f",
    "114": "#87d787",
    "115": "#87d7af",
    "116": "#87d7d7",
    "117": "#87d7ff",
    "118": "#87ff00",
    "119": "#87ff5f",
    "120": "#87ff87",
    "121": "#87ffaf",
    "122": "#87ffd7",
    "123": "#87ffff",
    "124": "#af0000",
    "125": "#af005f",
    "126": "#af0087",
    "127": "#af00af",
    "128": "#af00d7",
    "129": "#af00ff",
    "130": "#af5f00",
    "131": "#af5f5f",
    "132": "#af5f87",
    "133": "#af5faf",
    "134": "#af5fd7",
    "135": "#af5fff",
    "136": "#af8700",
    "137": "#af875f",
    "138": "#af8787",
    "139": "#af87af",
    "140": "#af87d7",
    "141": "#af87ff",
    "142": "#afaf00",
    "143": "#afaf5f",
    "144": "#afaf87",
    "145": "#afafaf",
    "146": "#afafd7",
    "147": "#afafff",
    "148": "#afd700",
    "149": "#afd75f",
    "150": "#afd787",
    "151": "#afd7af",
    "152": "#afd7d7",
    "153": "#afd7ff",
    "154": "#afff00",
    "155": "#afff5f",
    "156": "#afff87",
    "157": "#afffaf",
    "158": "#afffd7",
    "159": "#afffff",
    "160": "#d70000",
    "161": "#d7005f",
    "162": "#d70087",
    "163": "#d700af",
    "164": "#d700d7",
    "165": "#d700ff",
    "166": "#d75f00",
    "167": "#d75f5f",
    "168": "#d75f87",
    "169": "#d75faf",
    "170": "#d75fd7",
    "171": "#d75fff",
    "172": "#d78700",
    "173": "#d7875f",
    "174": "#d78787",
    "175": "#d787af",
    "176": "#d787d7",
    "177": "#d787ff",
    "178": "#d7af00",
    "179": "#d7af5f",
    "180": "#d7af87",
    "181": "#d7afaf",
    "182": "#d7afd7",
    "183": "#d7afff",
    "184": "#d7d700",
    "185": "#d7d75f",
    "186": "#d7d787",
    "187": "#d7d7af",
    "188": "#d7d7d7",
    "189": "#d7d7ff",
    "190": "#d7ff00",
    "191": "#d7ff5f",
    "192": "#d7ff87",
    "193": "#d7ffaf",
    "194": "#d7ffd7",
    "195": "#d7ffff",
    "196": "#ff0000",
    "197": "#ff005f",
    "198": "#ff0087",
    "199": "#ff00af",
    "200": "#ff00d7",
    "201": "#ff00ff",
    "202": "#ff5f00",
    "203": "#ff5f5f",
    "204": "#ff5f87",
    "205": "#ff5faf",
    "206": "#ff5fd7",
    "207": "#ff5fff",
    "208": "#ff8700",
    "209": "#ff875f",
    "210": "#ff8787",
    "211": "#ff87af",
    "212": "#ff87d7",
    "213": "#ff87ff",
    "214": "#ffaf00",
    "215": "#ffaf5f",
    "216": "#ffaf87",
    "217": "#ffafaf",
    "218": "#ffafd7",
    "219": "#ffafff",
    "220": "#ffd700",
    "221": "#ffd75f",
    "222": "#ffd787",
    "223": "#ffd7af",
    "224": "#ffd7d7",
    "225": "#ffd7ff",
    "226": "#ffff00",
    "227": "#ffff5f",
    "228": "#ffff87",
    "229": "#ffffaf",
    "230": "#ffffd7",
    "231": "#ffffff",
    "232": "#080808",
    "233": "#121212",
    "234": "#1c1c1c",
    "235": "#262626",
    "236": "#303030",
    "237": "#3a3a3a",
    "238": "#444444",
    "239": "#4e4e4e",
    "240": "#585858",
    "241": "#626262",
    "242": "#6c6c6c",
    "243": "#767676",
    "244": "#808080",
    "245": "#8a8a8a",
    "246": "#949494",
    "247": "#9e9e9e",
    "248": "#a8a8a8",
    "249": "#b2b2b2",
    "250": "#bcbcbc",
    "251": "#c6c6c6",
    "252": "#d0d0d0",
    "253": "#dadada",
    "254": "#e4e4e4",
    "255": "#eeeeee"
}

names = {
    "30": "BLACK",
    "31": "RED",
    "32": "GREEN",
    "33": "YELLOW",
    "34": "BLUE",
    "35": "PURPLE",
    "36": "CYAN",
    "37": "WHITE",
    "90": "LIGHTBLACK_EX",
    "91": "LIGHTRED_EX",
    "92": "LIGHTGREEN_EX",
    "93": "LIGHTYELLOW_EX",
    "94": "LIGHTBLUE_EX",
    "95": "LIGHTMAGENTA_EX",
    "96": "LIGHTCYAN_EX",
    "97": "LIGHTWHITE_EX"
}


def HEX(color: str) -> str:
    """
    Convert hex code to the closest ansi escape code.

    Parameters
    ----------
    color : str
        Hex color to convert to ansi.

    Returns
    -------
    str
        color parameter as ansi escape code.
    """
    for ansicolor, hexcolor in colors.items():
        if hexcolor == color:
            return ansicolor

    r,g,b = ImageColor.getcolor(color, "RGB")

    cube = lambda x : x*x
    f = lambda hex_val,ref : cube(int(hex_val,16) - ref)

    min_cube_d=cube(0xFFFFFF)
    nearest = '15'

    for k,h in colors.items():
        cube_d = f(h[1:3],r) + f(h[3:5],g) + f(h[5:7],b)
        if cube_d < min_cube_d:
            min_cube_d = cube_d
            nearest = k

    return nearest

def RGB(r: int, g: int, b:int) -> str:
    """
    Convert r, g and b values to ansi escape code.

    Parameters
    ----------
    r : int
        r value of RGB
    g : int
        g value of RGB
    b : int
        b value of RGB

    Returns
    -------
    str
        r, g and b parameters as ansi escape code.
    """
    color = r, g, b
    for ansicolor, hexcolor in colors.items():
        if hexcolor == '#%02x%02x%02x' % color:
            return ansicolor

    cube = lambda x : x*x
    f = lambda hex_val,ref : cube(int(hex_val,16) - ref)

    min_cube_d=cube(0xFFFFFF)
    nearest = '15'

    for k,h in colors.items():
        cube_d = f(h[1:3],r) + f(h[3:5],g) + f(h[5:7],b)
        if cube_d < min_cube_d:
            min_cube_d = cube_d
            nearest = k

    return nearest


def fg(color) -> str:
    """
    Change the foreground of your terminal.

    Parameters
    ----------
    color : tuple, str, int
        Color to print in terminal. tuple being RGB values, str being a HEX value and int being a ansi escape code.

    Returns
    -------
    str
        color parameter as terminal color. It will change the terminal text when printed.

    Raises
    ------
    Exception
        color parameter is not a tuple, str or int.
    """
    if isinstance(color, tuple):
        color = RGB(color[0], color[1], color[2])
        return "\u001b[38;5;{0}m".format(color)
    elif isinstance(color, str):
        color = HEX(color)
        return "\u001b[38;5;{0}m".format(color)
    elif isinstance(color, int):
        return "\u001b[38;5;{0}m".format(color)
    else:
        raise Exception("Invalid color")

def bg(color) -> str:
    """
    Change the background of your terminal.

    Parameters
    ----------
    color : tuple, str, int
        Color to print in terminal. tuple being RGB values, str being a HEX value and int being a ansi escape code.

    Returns
    -------
    str
        color parameter as terminal color. It will change the terminal background when printed.

    Raises
    ------
    Exception
        color parameter is not a tuple, str or int.
    """
    if isinstance(color, tuple):
        color = RGB(color[0], color[1], color[2])
        return "\u001b[48;5;{0}m".format(color)
    elif isinstance(color, str):
        color = HEX(color)
        return "\u001b[48;5;{0}m".format(color)
    elif isinstance(color, int):
        return "\u001b[48;5;{0}m".format(color)
    else:
        raise Exception("Invalid color")

class Style:
    """Styles for the terminal."""

    BOLD = "\x1b[1m"
    DIM = "\x1b[2m"
    UNDERLINE = "\x1b[4m"
    BLINK = "\x1b[5m"
    REVERSE = "\x1b[7m"
    HIDDEN = "\x1b[8m"
    RESET = "\x1b[0m"

class Fore:
    """Foregrounds for the terminal."""

    BLACK = "\x1b[30m"
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    BLUE = "\x1b[34m"
    PURPLE = "\x1b[35m"
    CYAN = "\x1b[36m"
    WHITE = "\x1b[37m"
    LIGHTBLACK_EX = "\x1b[90m"
    LIGHTRED_EX = "\x1b[91m"
    LIGHTGREEN_EX = "\x1b[92m"
    LIGHTYELLOW_EX = "\x1b[93m"
    LIGHTBLUE_EX = "\x1b[94m"
    LIGHTMAGENTA_EX = "\x1b[95m"
    LIGHTCYAN_EX = "\x1b[96m"
    LIGHTWHITE_EX = "\x1b[97m"
    RESET = "\x1b[0m"

class Back:
    """Backgrounds for the terminal."""

    BLACK = "\x1b[40m"
    RED = "\x1b[41m"
    GREEN = "\x1b[42m"
    YELLOW = "\x1b[43m"
    BLUE = "\x1b[44m"
    PURPLE = "\x1b[45m"
    CYAN = "\x1b[46m"
    WHITE = "\x1b[47m"
    LIGHTBLACK_EX = "\x1b[100m"
    LIGHTRED_EX = "\x1b[101m"
    LIGHTGREEN_EX = "\x1b[102m"
    LIGHTYELLOW_EX = "\x1b[103m"
    LIGHTBLUE_EX = "\x1b[104m"
    LIGHTMAGENTA_EX = "\x1b[105m"
    LIGHTCYAN_EX = "\x1b[106m"
    LIGHTWHITE_EX = "\x1b[107m"
    RESET = "\x1b[0m"

def colored(text, color=None, on_color=None, style=None):
    """
    Change the color of the terminal for one piece of text.

    Parameters
    ----------
    text : str
        text to be colored.
    color : str, optional
        color to change the text to, by default None
    on_color : str, optional
        color to change the background to, by default None
    style : str, optional
        style to change terminal style to, by default None

    Returns
    -------
    str
        your text with a text color/background color or style.
    """
    if style == None:
        style = "RESET"
    else:
        style = style.upper()
    if color == None and on_color == None:
        return f"{getattr(Style, style)}{text}{Style.RESET}"
    elif on_color == None:
        return f"{getattr(Style, style)}{getattr(Fore, color.upper())}{text}{Style.RESET}"
    elif color == None:
        return f"{getattr(Style, style)}{getattr(Back, on_color.upper())}{text}{Style.RESET}"
    else:
        return f"{getattr(Style, style)}{getattr(Back, on_color.upper())}{getattr(Fore, color.upper())}{text}{Style.RESET}"
def cprint(text, color=None, on_color=None, style=None, end=None):
    """
    colored function but it auto prints.

    Parameters
    ----------
    text : str
        text to be colored.
    color : str, optional
        color to change the text to, by default None
    on_color : str, optional
        color to change the background to, by default None
    style : str, optional
        style to change terminal style to, by default None
    end : str, optional
        what ends the print statement, by default None
    """
    print(colored(text, color, on_color, style), end=end)

class Pattern_Print:
    def pattern_print(self, text: str, pattern=["reset"], end=None):
        """
        Print text in a pattern of colors

        Parameters
        ----------
        text : str
            Text to be printed
        pattern : list, optional
            Pattern to follow, by default ["reset"]
        end : str, optional
            What to print at the end, by default None
        """
        try:
            if pattern == ["reset"]:
                pattern = self.pat
            if pattern != self.pat:
                self.pat = pattern
        except AttributeError:
            self.pat = pattern
        try:
            self.next_in_pattern
        except AttributeError:
            self.next_in_pattern = 0
        try:
            print(colored(text, pattern[self.next_in_pattern]), end=end)
        except IndexError:
            self.next_in_pattern = 0
            print(colored(text, pattern[self.next_in_pattern]), end=end)
        self.next_in_pattern += 1

pattern_print = Pattern_Print().pattern_print

def pattern_input(text, pattern=["reset"]):
    """
    input the next thing in a pattern of colors.

    Parameters
    ----------
    text : str
        text to show in the input statement
    pattern : list, optional
        color pattern. saved every statement, by default ["reset"]

    Returns
    -------
    str
        Text entered.
    """
    pattern_print(text, pattern, end="")
    return input()

def rand(text):
    """
    Randomly pick a color and make your text that color.

    Parameters
    ----------
    text : str
        text to have a random color.

    Returns
    -------
    str
        text parameter as random terminal color
    """
    return colored(text, secrets.choice(list(names.values())))
