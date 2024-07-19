def colored(string, color):
    """
    Returns the given string wrapped with a ANSI escape code that gives it color when printed to a terminal.
    Args:
        string: String to be colored.
        color: Chosen color for the string. Can be 'r' for red, 'g' for green, 'y' for yellow, 'b' for blue, 'p' for
            pink, 't' for teal, or 'gray' for gray.

    Returns:

    """
    colors = {"r": 31, "g": 32, "y": 33, "b": 34, "p": 35, "t": 36, "gray": 37}
    return f"\x1b[{colors[color]}m{string}\x1b[0m"


# Example usage
if __name__ == "__main__":
    print(f"{colored('This', 't')} {colored('is', 'y')} {colored('RED', 'r')}.")
