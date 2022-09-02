"""Log
As absurd as it sounds, this is the Pignus Log handler, which attempts to make logging more
approachable for the many different interfaces of Pignus.

"""
import inspect
import sys

from rich import print as pprint

from pignus_api.utils import glow
from pignus_shared.utils import xlate


def debug(message: str, **kwargs):
    """Method to handle DEBUG level logs.
    :unit-test: test__debug
    """
    _handle_log("DEBUG", message, **kwargs)
    return True


def info(message: str, **kwargs):
    """Method to handle INFO level logs.
    :unit-test: test__info
    """
    _handle_log("INFO", message, **kwargs)
    return True


def warning(message: str, **kwargs):
    """Method to handle WARNING level logs.
    :unit-test: test__warning
    """
    _handle_log("WARNING", message, **kwargs)
    return True


def error(message: str, **kwargs):
    """Method to handle ERROR level logs.
    :unit-test: test__error
    """
    _handle_log("ERROR", message, **kwargs)
    return True


def critical(message: str, **kwargs):
    """Method to handle CRITICAL level logs.
    :unit-test: test__critical
    """
    _handle_log("CRITICAL", message, **kwargs)
    return True


# Internal log methods
def _handle_log(level, message: str, **kwargs):
    """Routing point for all log lines, for any interpreter. Organizes details for all levels all
    log log levels.
    """
    the_log = _get_base_log(message, **kwargs)
    the_log["level"] = level
    the_log["level_int"] = _eval_log_numeral(level)
    _handle_dipslay(the_log)
    return True


def _get_base_log(message: str, **kwargs) -> dict:
    """Get the primary logging details. """
    the_log = {
        # "filename": _get_filename(),
        "message": message
    }
    for arg_name, arg_value in kwargs.items():
        if arg_name == "image":
            the_log["image"] = kwargs["image"]
        elif arg_name == "build":
            the_log["build"] = kwargs["build"]
        elif arg_name == "stacktrace" and arg_value:
            the_log["stacktrace"] = _get_stacktrace()
        else:
            the_log[arg_name] = arg_value

    return the_log


def _get_stacktrace() -> str:
    """Gets all the files called to get to the log line. """
    steps_to_this_func = 4
    file_calls = []
    for trace in inspect.stack()[steps_to_this_func:]:
        file_calls.append(trace.filename)

    return ", ".join(file_calls)


def _get_api_request_log() -> dict:
    """Get the api gateway request details.
    :unit-test: test___get_api_request_log
    """
    if not glow.content["path"]:
        return False
    content = glow.content
    if "api-key" in content:
        content.pop("api-key")
    return content


def _get_filename() -> str:
    """Get the file that called the logging module as relative to Pignus."""
    steps_to_this_func = 4
    filename = inspect.stack()[steps_to_this_func].filename
    return filename[filename.find("pignus"):]


def _handle_dipslay(the_log: dict) -> bool:
    """Handle displaying the log, either to a console or headless TTY."""
    display_log = _diplay_log(the_log)
    if not display_log:
        return False

    # If the execution is a users terminal
    if sys.stdin and sys.stdin.isatty():
        _handle_stdout_display(the_log)
    else:
        the_log_json = xlate.json_dump(the_log)
        print(the_log_json)
    return True


def _diplay_log(the_log) -> bool:
    """Print the log to the console or log collector."""
    config_level = _eval_log_numeral(glow.general["LOG_LEVEL"])
    log_level = _eval_log_numeral(the_log["level"])
    if log_level >= config_level:
        return True
    else:
        False


def _handle_stdout_display(the_log: dict) -> bool:
    """Handle the log display if the script is being run manually."""
    # log_keys = ["filename", "image"]
    log_keys = ["image/build"]

    level = _get_level_color(the_log["level"])
    if the_log["level"] == "WARNING":
        pprint("[%s]\t%s" % (level, the_log["message"]))
    else:
        pprint("[%s]\t\t%s" % (level, the_log["message"]))

    # Display the image/build
    if "image/build" in log_keys and "image" in the_log and "build" in the_log:
        pprint("\t\tImage:\t%s" % the_log["image"])
        pprint("\t\tBuild:\t%s" % (the_log["build"]))
    elif "image/build" in log_keys and "image" in the_log:
        pprint("\t\tImage:\t%s" % the_log["image"])
    elif "image_build" in log_keys and "image_build" in the_log:
        pprint("\t\tImageBuild:\t%s" % the_log["image_build"])
    elif "image/build" in log_keys and "build" in the_log:
        pprint("\t\tBuild:\t%s" % (the_log["build"]))

    # if "stage" in the_log:
    #     pprint("\t\tStage:\t%s" % the_log["stage"])
    if "scan" in the_log:
        pprint("\t\tScan:\t%s" % the_log["scan"])

    for log_key, log_data in the_log.items():
        if log_key in log_keys:
            pprint("\t%s:\t%s" % (log_key.title(), log_data))
    if "exception" in the_log:
        pprint("\t\tException:\t%s" % the_log["exception"])
    if "error" in the_log:
        pprint("\tError:\t%s" % the_log["error"])
    return True


def _get_level_color(level):
    """ Get the syntax to color the log level for the CLI interface.
    :unit-test: test___get_level_color
    """
    if level == "ERROR":
        return "[red]%s[/red]" % level
    elif level == "WARNING":
        return "[yellow]%s[/yellow]" % level
    elif level == "DEBUG":
        return "[plum3]%s[/plum3]" % level
    elif level == "INFO":
        return "[green]%s[/green]" % level
    return level


def _eval_log_numeral(level: str) -> int:
    """Get the numerical value of a log level string as python logging understands them.
    :unit-test: test___eval_log_numeral
    """
    if type(level) == str:
        level = level.upper()
        if level == "DEBUG":
            level = 10
        elif level == "INFO":
            level = 20
        elif level == "WARNING":
            level = 30
        elif level == "ERROR":
            level = 40
        elif level == "CRITICAL":
            level = 50
    return level


# End File: pignus/src/pignus_shared/utils/log.py
