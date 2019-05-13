"""
Functions for simplifying the creation of __main__.py application scripts.
"""


from argparse   import ArgumentParser
from logging    import (FileHandler, Formatter, StreamHandler, getLogger, 
                        DEBUG, INFO)


def create_logger(debug_set, log_filename):
    """
    Creates a logger for standard error and potentially file output.
    """
    LOG_FORMAT = "%(asctime)s::%(name)s::%(levelname)s::%(message)s"
    TIMESTAMP_FORMAT = "%H:%M:%S"

    debug_level = INFO
    if debug_set:
        debug_level = DEBUG

    logger = getLogger()
    logger.setLevel(debug_level)

    std_err = StreamHandler()
    std_err.setFormatter(Formatter(LOG_FORMAT, TIMESTAMP_FORMAT))

    file_handler = None
    if log_filename != "":
        file_handler = FileHandler(log_filename, mode = 'w')
        file_handler.setFormatter(Formatter(LOG_FORMAT, TIMESTAMP_FORMAT))

    logger.addHandler(std_err)
    if file_handler is not None:
        logger.addHandler(file_handler)

    return logger

def create_argument_parser(application_name, version, 
                            application_description = ""):
    """
    Create a parser that supports version, debug, and logfile arguments.  
    
    Can be extended by applications with their own specific options.
    """
    parser = ArgumentParser(prog = application_name, 
                            description = application_description)
    parser.add_argument("-V", "--version", action = "version", 
                        version = version)
    parser.add_argument("-d", "--debug", action = "store_true", 
                        help = "Output more messages that can be used to "
                                "help debug the application")
    parser.add_argument("-l", "--logfile", action = "store", default = "", 
                        help = "File to log to along with standard output")
    return parser

