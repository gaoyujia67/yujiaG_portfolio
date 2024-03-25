import datetime
from lighting import lighting 
import select
import sys

def is_thanksgiving(date):
    """
    Determines if the provided date corresponds to Thanksgiving.

    Args:
        date (datetime.date): The date to check.

    Returns:
        bool: True if the date is Thanksgiving, False otherwise.
    """
    november_first = datetime.date(date.year, 11, 1)
    november_first_weekday = november_first.weekday()
    if november_first_weekday>3:
        thanksgiving_date = november_first + datetime.timedelta\
            (days=(3 - november_first_weekday) + 4*7)
    else:
        thanksgiving_date = november_first + datetime.timedelta\
            (days=(3 - november_first_weekday) + 3*7)
    return date == thanksgiving_date

def play(date):
    """
    Returns a lighting pattern based on the specific holiday corresponding to the provided date.

    Args:
        date (datetime.date): The date to check for corresponding holidays.

    Returns:
        list: A list of integers representing the lighting pattern for the holiday.
    """
    pattern=[77, 77, 77, 77]
    if date.month == 2 and date.day == 14:
        print("Happy Valentine's Day!")
        pattern=[150, 0, 0, 100] #pink
    if date.month == 3 and date.day == 17:
        print("Happy St. Patrick's Day!")
        pattern=[0, 255, 0, 0] #green
    if date.month == 7 and date.day == 4:
        print("Happy Independence Day!")
        pattern=[0, 0, 255, 0, 255, 0, 0, 0, 0, 0, 0, 255] #blue, red, white
    if date.month == 10 and date.day == 31:
        print("Happy Halloween!")
        pattern=[77, 0, 99, 0, 255, 130, 0, 0] #black, orange
    if is_thanksgiving(date):
        print("Happy Thanksgiving Day!")
        pattern=[255, 130, 0, 0, 33, 22, 22, 0] #orange, brown
    if date.month == 12 and date.day == 25:
        print("Happy Christmas!")
        pattern=[0, 200, 0, 33, 0,0,0,220, 244, 0,0,0] #green, white, red
    return pattern


def stop_lights(lit):
    """
    Stops the lighting effects and turns off the lights.

    Args:
        lit (lighting): The lighting system instance to control.
    """
    lit.shut_off()
    print("Lights have been turned off.")
    exit()

def input_date():
    """
    Prompts the user to input a valid date and returns a datetime.date object for it.

    Returns:
        datetime.date: The date input by the user after validation.
    """
    while(1):
        while(1):
            year = input("Please type in the year: ")
            try:
                year = int(year)
            except ValueError:
                print("year is not an int")
                continue
            break

        while(1):
            month = input("Please type in the month: ")
            try:
                month = int(month)
            except ValueError:
                print("month is not an int")
                continue
            break
        
        while(1):
            day = input("Please type in the day: ")
            try:
                day = int(day)
            except ValueError:
                print("Day is not an int.")
                continue
            break
        
        try:
            date = datetime.date(int(year), int(month), int(day))
        except ValueError:
            print('not a valid date')
            continue
        break
    return datetime.date(int(year), int(month), int(day))


if __name__ == "__main__":
    date = input_date()
    pattern_date = play(date)
    lit = lighting()
    flag = True

    try:
        while True:
            lit.general_pattern(pattern_date)
            lit.breath(flag, 0.9)
            flag = not flag
            lit.breath(flag, 0.9)
            flag = not flag

    # Type "Ctrl+C" to turn off the light
    except KeyboardInterrupt:
        stop_lights(lit)

    except Exception as e:
        print(f"An error occurred: {e}")
        stop_lights(lit)