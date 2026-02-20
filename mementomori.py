#!/usr/bin/env python3

from pathlib import Path
from datetime import *
import configparser
import argparse
import shutil
import random
import sys
import time

from dateutil.relativedelta import *
from dateutil.parser import *
import yaml



def parseargs():
    parser = argparse.ArgumentParser(
        description="memento mori (latin. 'Remember about mortality') Command-line life counter. "
    )
    parser.add_argument(
        "-m", "--mode",
        choices=["date", "timer", "timer-extended"],
        help="select the output mode"
    )
    args = parser.parse_args()

    return {
        "mode": args.mode
    }

def defaultconfig(conffile: Path):
    try:
        conffile.parent.mkdir(parents=True, exist_ok=True)
        config = configparser.ConfigParser()

        config["general"] = {
            "mode": "timer-extended"
        }

        with conffile.open("w") as f:
            f.write(
            "# memento-mori configuration file\n"
            "# See https://github.com/naujan/memento-mori#configuration \n\n"
            )
            config.write(f)

    except OSError as e:
        print(f"Error: Error while creating the config: {e}")
        sys.exit(1)

def gendatafile(datafile: Path, exp): 
    try:
        datafile.parent.mkdir(parents=True, exist_ok=True)
        user_data = {
            "expected_date": exp
        }
        with datafile.open("w") as f:
            f.write("""# memento mori user data
# You can modify it as you want 
\n""")
            yaml.dump(user_data, f)
            
    except OSError as e:
        print(f"Error: Error while creating the date file: {e}")
        sys.exit(1)

def load_user_data(datafile: Path):
    try:
        with datafile.open("r") as f:
            return yaml.safe_load(f) or {}

    except FileNotFoundError:
        print("Data file not found.")
        return {}

def userask(prompt, anwser_type=str, choices=None, default=None):
    try:
        default_suffix = f"[default={default}]" if default is not None else ""
        user_input  = anwser_type(input(f"{prompt} : ").strip())

        if not user_input and default is not None:
            user_input = str(default)

        if choices:
            if user_input.lower() not in [c.lower() for c in choices]:
                print(f"Invalid choice. Avaiable: {','.join(choices)}")

            
        return user_input
    except KeyboardInterrupt:
        print(f"\nProgram exited by user")
        sys.exit(0)
    
def userask_yn(prompt, default=None):
    ans =  userask(prompt, str, choices=["y","n","yes", "no"], default=default)
    return ans.lower() in ["y", "yes"]


# The calculator
# Values are randomized, same inputs does not guarantee identical outputs.
# Values based on web statistic articles, and my imagination :P

def calculate(birthdate, sex, smoking, drinking, diet, bmi):
    expectancy = 110
    if sex == "male":
        expectancy -= random.uniform(3,6)
    if smoking:
        expectancy -= random.uniform(8,12)
    expectancy -= drinking * (0.2 if drinking < 5 else 1)
    if bmi < 18.5:
        expectancy -= random.uniform(1, 3) 
    elif 18.5 <= bmi < 25:
        pass
    elif 25 <= bmi < 30:
        expectancy -= random.uniform(3, 7) 
    else:
        expectancy -= random.uniform(7,10) 
    if diet > 7:
        expectancy += random.uniform(1, 3)
    elif diet > 5:
        expectancy += 1
    elif diet > 3:
        expectancy -= random.uniform(3,5)
    else:
        expectancy -= random.uniform(5,8)

    exp_years = int(expectancy)
    years_frac = expectancy - exp_years
    exp_months = int(years_frac * 12)
    exp_days = int(((years_frac * 12) - exp_months) * 30.44) # avg days in a month

    exp_date = birthdate + relativedelta(
        years = exp_years,
        months = exp_months,
        days = exp_days
    )

    return exp_date

def translate_date(date): 
    try: 
        return datetime.strptime(date, "%d-%m-%Y").date() 
    except ValueError: 
        print("Invalid date format. Please use (DD-MM-YYYY)")

def run_timer(date):
    print("\033[2J\033[H", end="")
    try:
        print("\033[?25l",end="")
        while True:
            now = datetime.now()

            if now >= date:
                print("\nTime's up...")
                break
                
            diff = int((date - now).total_seconds())
            hours = diff // 3600
            minutes = (diff % 3600)  // 60
            seconds = diff % 60
            timer = f"{hours:02}:{minutes:02}:{seconds:02}"
            
            col, row = shutil.get_terminal_size()
            hpad = (col - len(timer)) // 2
            vpad = row // 2

            print("\033[2J\033[H", end="")
            
            print("\n"*vpad)

            print(timer.center(col))

            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting")
        print("\033[2J\033[H", end="")

    finally:
        print("\033[?25h",end="")

def run_timer_extened(date):
    print("\033[2J\033[H", end="")
    try:
        print("\033[?25l",end="")
        while True:
            now = datetime.now()

            if now >= date:
                print("\nTime's up...")
                break
                
            diff = relativedelta(date, now)
            timer = f"{diff.years} years, {diff.months} months,\
 {diff.days} days, {diff.hours} hours, {diff.minutes} minutes and {diff.seconds} seconds left."
            
            col, row = shutil.get_terminal_size()
            hpad = (col - len(timer)) // 2
            vpad = row // 2

            print("\033[2J\033[H", end="")
            
            print("\n"*vpad)

            print(timer.center(col))

            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting")
        print("\033[2J\033[H", end="")

    finally:
        print("\033[?25h",end="")

def main():
    cli_args = parseargs()
    
    conffile = Path("~/.config/memento-mori/config.conf").expanduser()
    datafile = Path("~/.config/memento-mori/data.yaml").expanduser()

    if not conffile.exists():
        print("Could not find the config file:", conffile)

        if userask_yn("Do you want to generate the default config? (Y/n)", default="y"):
            print("Generating the config file")
            defaultconfig(conffile)
            print("No errors while generating")

        else:
            sys.exit(1)

    if not datafile.exists():
        print("\033[2J\033[H", end="") # CLEAR
        print(f"""
Welcome to the memento mori setup
Could not find a valid datafile ({datafile})
Before you can see your fate, let me ask you some questions...
        """)


        while True:
            birthdate = translate_date(
                userask("What year were you born? (DD-MM-YYYY)",str)
            )
            if birthdate is not None:
                break
        
        print(birthdate)
    
        sex = userask("What is you gender? (Male/Female)",str,["Male", "Female"]).lower()
        
        smoking = userask_yn("Are you smoking? (y/N)","n")

        drinking = userask("What is your drinking efficiency? (0-10)",int)

        diet = userask("How would you rank your diet? (0-10)", int)

        bmi = userask("What is your BMI?", float)

        print("Calculating...")
        expected_date = calculate(birthdate, sex, smoking, drinking, diet, bmi)
        print(f"Generating data file... ({datafile})")
        gendatafile(datafile, expected_date)

    config = configparser.ConfigParser()
    config.read(conffile)

    user_data = load_user_data(datafile)
    final_date = datetime.combine(user_data.get("expected_date"), datetime.min.time())

    if not config.has_section("general"):
        print("Config file missing [general] section")
        sys.exit(1)

    
    mode = cli_args["mode"] or config.get("general", "mode", fallback="date")
    
    if mode == "date":
        print(final_date.date())
    elif mode == "timer":
        run_timer(final_date)
    elif mode == "timer-extended":
        run_timer_extened(final_date)
    else:
        print(f"Error: Invalid option '{mode}' in config. Must be one of 'date', 'timer' or 'timer-extended'.")

if __name__ == "__main__":
    main()