from scripts.step_one import execute_step_1
from scripts.step_two import execute_step_2
from scripts.constants import INIT_MSG
from scripts.functions import get_user_date

if __name__ == "__main__":

    valid_options = ['1', '2', '3', '4']
    user_opt = None

    while user_opt not in valid_options:        
        user_date = get_user_date()
        user_opt = str(input(INIT_MSG))

        if user_opt == '1':
            execute_step_1(user_date)
        elif user_opt == '2':
            execute_step_2(user_date)
        elif user_opt == '3':
            execute_step_1(user_date)
            execute_step_2(user_date)
        elif user_opt == '4':
            print("Bye!")
            break
        else:
            print("Select a valid option!")
