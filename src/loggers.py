from datetime import datetime as dt
import logging as log
import os

this_path = os.path.abspath(os.path.dirname(__file__))
PATH = os.path.join(this_path, "../logs")

def get_datestamp():
    now = dt.now()
    dt_string = now.strftime("%d-%m-%Y")
    return dt_string

def get_formatted_f_handler(filename):

    file_format = log.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
    file_handler = log.FileHandler(filename)
    
    # try:
    #     file_handler = log.FileHandler(filename)
    # except FileNotFoundError or FileExistsError as error:
    #     with open(filename, 'w') as logfile:
    #         logfile.write('Logfile created')

    file_handler.setLevel(log.DEBUG)
    file_handler.setFormatter(file_format)
    
    return file_handler

def get_formatted_s_handler():

    console_format = log.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
    console_handler = log.StreamHandler()
    console_handler.setLevel(log.DEBUG)
    console_handler.setFormatter(console_format)

    return console_handler


def get_logger_fname(filename):
    dt_string = get_datestamp()
    path = path = PATH
    full_filename = '{}/{}'.format(path,'{}_{}.log'.format(filename,dt_string))
    return full_filename


def setup_logger(name, filename = None):
    logger = log.getLogger(name)

    if filename:
        full_filename = get_logger_fname(filename)
        file_handler = get_formatted_f_handler(full_filename)
        logger.addHandler(file_handler)
   

    console_handler = get_formatted_s_handler()

    logger.addHandler(console_handler)
    logger.setLevel(log.DEBUG)

    return logger

def get_main_logger():
    # return setup_logger('main_log', 'main')
    return setup_logger('main_log', 'main')

def get_reload_logger():
    return setup_logger('reload_log', 'main')
