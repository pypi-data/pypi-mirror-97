from __future__ import unicode_literals
import os
import platform
import click
import six
import sys
import time
from halo import Halo
from PyInquirer import (
    Token,
    ValidationError,
    Validator,
    print_json,
    prompt,
    style_from_dict,
)
from pyfiglet import figlet_format
from git import Repo


try:
    import colorama

    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None

style = style_from_dict(
    {
        Token.QuestionMark: "#fac731 bold",
        Token.Answer: "#4688f1 bold",
        Token.Instruction: "",  # default
        Token.Separator: "#cc5454",
        Token.Selected: "#0abf5b",  # default
        Token.Pointer: "#673ab7 bold",
        Token.Question: "",
    }
)


def getContentType(answer, conttype):
    return answer.get("content_type").lower() == conttype.lower()


def spinning_cursor():
    while True:
        for cursor in "|/-\\":
            yield cursor


def spin_cursor():
    spinner = spinning_cursor()
    for _ in range(50):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write("\b")


class EmptyValidator(Validator):
    def validate(self, value):
        if len(value.text):
            return True
        else:
            raise ValidationError(
                message="You can't leave this blank", cursor_position=len(value.text)
            )


def log(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(string, font=font), color))
    else:
        six.print_(string)


def askQuestions():

    questions = [
        {
            "type": "input",
            "name": "project_name",
            "message": "Name of the Project",
            "default": "SQLI DETECTTION SYSTEM FLASK",
            "validate": EmptyValidator,
        },
        {
            "type": "input",
            "name": "env_name",
            "message": "Name for your environment",
            "default": "sqli_env",
            "validate": EmptyValidator,
        },
        {
            "type": "list",
            "name": "clone_type",
            "message": "How do you want the project type as ?",
            "choices": ["local development", "source code", "dockerized code"],
        },
        {
            "type": "confirm",
            "name": "create",
            "message": "Do you create the project now",
        },
    ]

    answers = prompt(questions, style=style)
    return answers


@Halo(text="Clonning Repository", spinner="dots")
def clone_repository(project_name):
    project_location = "./" + project_name
    Repo.clone_from(
        "https://github.com/jayvishaalj/fyp-2021-template.git", project_location
    )


@Halo(text="installing packages", spinner="dots")
def create_environment(environment_name, project_name):
    # my_cmd_linux = """
    # python3 -m venv .env
    # source .env/bin/activate
    # pip install -r requirements.txt
    # """
    # project_cd = os.getcwd() + project_name
    os.system("start")
    os.system("py -3 -m venv ." + environment_name)
    os.system("." + environment_name + "\\scripts\\activate")
    os.chdir(os.getcwd() + "/" + project_name)
    os.system("pip install -r requirements.txt")
    os.system(".env\\scripts\\deactivate")


@click.command()
def cli():
    """
    Simple CLI for Generating Flask SocketIO MYSQL CONNECTORS and SQL INJECTION DETECTION SYSTEM Code!
    """
    try:
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
        log("SCDLP CLI", color="blue", figlet=True)
        log("Welcome to SCDLP CLI", "green")
        answers = askQuestions()
        # print("\n answers : \n  ", answers)
        if answers["create"]:
            clone_repository(answers["project_name"])
            log(" Your Repository has been created!", "green")
            create_environment(answers["env_name"], answers["project_name"])
            log(" Your Project Has been created Successfully!", "green")
    except (KeyboardInterrupt):
        log("Keyboard Interrupt By User!", "red")
    except (KeyError):
        log("Key error By User!", "red")
    except (SystemExit):
        log("System Exited Exception!", "red")
    except:
        msg = "Unexpected error:" + sys.exc_info()[0]
        log(msg, "red")
    finally:
        log("Bye! Thank You :)", "cyan")