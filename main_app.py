import utils.terminal_utils as tUtils
import utils.setup_utils as sUtils
import utils.user_action_utils as usrActUtils

import const.time_const as time
import const.messages as messages
import const.exceptions as exceptions



def main() -> None:
    """ Main Function that begins app execution """

    sUtils.init()
    cli_loop()

def cli_loop() -> None:
    """ Loop that runs until user quits- displays main menu and gets user actions """

    while True:
        try:
            tUtils.flush_terminal()
            print(messages.DEBUG_MESSAGE)
            print(f"It is currently {time.cur_month}/{time.cur_day}/{time.cur_year}")
            action = usrActUtils.get_action()
            usrActUtils.validate_action(action)
            usrActUtils.execute_action(action)
        except exceptions.BreakLoop:
            pass
