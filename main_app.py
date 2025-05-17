import utils.terminal as tUtils
import utils.setup as sUtils
import utils.user_action as usrActUtils
import src.views as views

import data.time_const as time
import data.messages as messages
import data.exceptions as exceptions



def main() -> None:
    """ Main Function that begins app execution """

    sUtils.init()
    cli_loop()

def cli_loop() -> None:
    """ Loop that runs until user quits- displays main menu and gets user actions """

    while True:
        try:
            tUtils.flush_terminal()
            print(messages.debug_message)
            print(f"It is currently {time.cur_month}/{time.cur_day}/{time.cur_year}")
            views.display_menu()

            action = usrActUtils.get_action()
            if usrActUtils.is_valid(action):
                usrActUtils.execute(action)

        except exceptions.BreakLoop:
            pass
