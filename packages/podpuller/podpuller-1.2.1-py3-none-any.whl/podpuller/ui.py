import logging
import sys
import os

from bullet import Check, colors
from termcolor import cprint


def interrupt_dl():
    logging.info("Download aborted by Ctrl+c")
    try:
        return yesno("Do you like to mark item as played? (y/n) or quit? (Ctrl+c): ")
    except KeyboardInterrupt:
        print("\nQuitting")
        sys.exit()


def yesno(prompt):
    user_wish = input(prompt + " [y/n] ")
    return user_wish and "yes".startswith(user_wish.lower())


def mark_deletion(dir):
    if os.path.exists(dir):
        filenames = sorted(os.listdir(dir), reverse=True)
        if filenames:
            not_dotfiles = [f for f in filenames if not f.startswith(".")]
            cprint(f"Mark listened with [Space]. [Enter] to continue.", "red")
            cli = Check(
                choices=not_dotfiles, check="X ", check_color=colors.foreground["red"]
            )
            return cli.launch()
