from stdiomask import getpass
import inquirer
from inquirer.themes import load_theme_from_dict
import click

theme = {
    "Question": {
        "mark_color": "cyan",
        "brackets_color": "magenta"
    },
    "List": {
        "selection_color": "black_on_yellow",
        "selection_cursor": "❯",
    },
    "Checkbox": {
        "selection_color": "black_on_yellow",
        "selected_color": "yellow",
        "selection_icon": '❯',
        "selected_icon": '✔︎',
        "unselected_icon": ' '
    }
}


def _clean_backspace(s):
    ns = []
    for c in s.split("\b"):
        if c == "":
            ns = ns[:-1]
        ns.append(c)
    return "".join(ns)


def option_selector(msg, options):
    options = [f'  {option} ' for option in options]
    answer = inquirer.prompt([
        inquirer.List('value', message=msg, choices=options)
    ], theme=load_theme_from_dict(theme))
    if answer is None:
        raise click.Abort()
    return answer.get("value").strip()


def checkboxes(msg, options):
    options = [f'{option} ' for option in options]
    msg += " (use space to check an option, enter to submit)"
    answer = inquirer.prompt([
        inquirer.Checkbox('value', message=msg, choices=options)
    ], theme=load_theme_from_dict(theme))

    if answer is None:
        raise click.Abort()
    return [a.strip() for a in answer.get("value", [])]


def text(msg, validate=None, default=""):
    if validate is not None:
        value = inquirer.Text('value', message=msg, validate=validate)
    else:
        value = inquirer.Text('value', message=msg)
    answer = inquirer.prompt([value], theme=load_theme_from_dict(theme))

    if answer is None:
        raise click.Abort()

    answer = _clean_backspace(answer.get("value").strip())
    return default if answer == "" else answer


def integer(msg, validate=None, default=None):
    return text(msg, validate, default)


def number(msg, validate=None, default=None):
    answer = text(msg, validate, default)
    return None if answer == "" else float(answer)


def long_text(msg):
    answer = inquirer.prompt([
        inquirer.Editor('value', message=msg)
    ], theme=load_theme_from_dict(theme))

    if answer is None:
        raise click.Abort()
    return _clean_backspace(answer.get("value").strip())


def path(msg, validator="directory", exists=True):
    if validator == "file":
        validator = inquirer.Path.FILE
    else:
        validator = inquirer.Path.DIRECTORY

    answer = inquirer.prompt([
        inquirer.Path('value', message=msg, path_type=validator, exists=exists)
    ], theme=load_theme_from_dict(theme))

    if answer is None:
        raise click.Abort()
    return answer.get("value")


def hidden(msg):
    click.echo(click.style(
        "[", fg=theme.get("Question", []).get("brackets_color")), nl=False)
    click.echo(click.style(
        "?", fg=theme.get("Question", []).get("mark_color")), nl=False)
    click.echo(click.style(
        "] ", fg=theme.get("Question", []).get("brackets_color")), nl=False)
    return getpass(msg+": ")


def confirm(msg, default=True):
    answer = inquirer.prompt({
        inquirer.Confirm('value', message=msg, default=default),
    }, theme=load_theme_from_dict(theme))

    if answer is None:
        raise click.Abort()
    return answer.get("value")
