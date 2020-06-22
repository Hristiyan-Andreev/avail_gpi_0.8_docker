import os
import sys
import subprocess as subp
import glob as gb
import re
import time
from os.path import getmtime
import PyInquirer as pyq
import docker as dock

import loggers as lg
import cli


# AVAIL_MAIN_FILE = 'main.py'
AVAIL_CONTAINER_NAME = "avail_gpi"
# import PyInquirer as pyq

# TODO: Master script to
# 4) monitor (health check) the main script
# 5) Menu

# Create a docker client, connected to the docker socket (server)
# Used for finding and stopping containers
dock_client = dock.from_env()

# Dicts of menu options - to avoid using strings in the whole program
mm_choices = {
    'ss_script': 'Start/Stop/Restart main avail script',
    'en_dis_auto': 'Enable/Disable autostart',
    'show_log': 'Show current log',
    'config': 'Configure paramaters',
    'back': 'Exit the program'
}

ss_options = {
    'start': 'Start the main avail script',
    'stop': 'Stop the main avail script',
    'restart': 'Restart the script',
    'back': 'Back to main menu'
}

autostart_options = {
    'enable': 'Enable main script autostart',
    'disable': 'Disable main scritp autostart',
    'back': 'Back to main menu'
}

control_log = lg.setup_logger('control_log', 'controller')


def is_container_running(name):

    try:
        dock_client.containers.get(name)
    except dock.errors.NotFound:
        return False
    except dock.errors.APIError:
        control_log.exception('Docker client-socket connection not working')
    
    return True


def start_avail_script():
    #Start the main avail script
    # is_running = is_avail_main_running()
    
    # # if is_running is True:
    #     control_log.info('Ad avail script {} is already running'.format(AVAIL_MAIN_FILE))
    #     return 1
    if is_container_running(AVAIL_CONTAINER_NAME) is False:
        os.system('docker container run --rm --privileged --name "avail_gpi" -v /Projects/avail_gpi_0.8_docker/avail_gpi:/app -v /var/log/:/app/logs avail_gpi_0.8:v1.1 &')
        control_log.info('Avail container started')
    else:
        control_log.info('Main container is already running')

    return 0
    

def stop_avail_script():
    is_running = is_container_running(AVAIL_CONTAINER_NAME)

    if is_running is False:
        control_log.info('Ad avail script {} is not running'.format(AVAIL_CONTAINER_NAME))
        return 1

    avail_container = dock_client.containers.get(AVAIL_CONTAINER_NAME)
    avail_cntr_id = avail_container.id
    try:
        avail_container.kill()
    except dock.errors.APIError:
        control_log.exception('Docker client-socket connection not working')
        return 1
    
    control_log.info('Avail container with ID:{} was terminated and deleted'.format(avail_cntr_id))
    return 0


def restart_avail_script():
    stop_avail_script()
    start_avail_script()

    return 0

def find_latest_log():
    all_log_files = []
    for log_file in gb.glob("/app/logs/*.log"):
        all_log_files.append(log_file)

    latest_log_file = max(all_log_files, key=os.path.getctime)
    return(latest_log_file)


def read_main_log():
    find_latest_log()
    main_log_file = lg.get_logger_fname('main')
    last_save_time = getmtime(main_log_file)
    print('\nPress CTRL+C to Exit')
    time.sleep(3)
    with open(main_log_file, 'r') as log_file:
        lines = log_file.readlines()
        for line in lines:
            print(line, end=" ")
        line_count = len(lines)


    while(True):
        try:
            save_time = getmtime(main_log_file)

            if last_save_time != save_time:
                with open(main_log_file) as log_file:
                    lines = log_file.readlines()
                new_lines = lines[line_count:]
                for line in new_lines:
                    print(line, end=" ")

                line_count = len(lines)
                last_save_time = save_time
            time.sleep(1)
        except KeyboardInterrupt as e:
            break
    
    return 0


def enable_avaiL_startup():
    with open('autostart.sh', 'w') as bash_file:
        bash_file.seek(0)
        bash_file.truncate()
        bash_file.write('#!/bin/sh\n')
        bash_file.write('cd /Projects/gpi_0.7_hw_reworked/\n')
        bash_file.write('python3 {} &'.format(AVAIL_MAIN_FILE))

    control_log.info('Main avail script autostart enabled')

    return 0


def disable_avail_startup():
    with open('autostart.sh', 'w') as bash_file:
        bash_file.seek(0)
        bash_file.truncate()

    control_log.info('Main avail script autostart disabled')
    return 0

# ------ Menu functions --------------------------------
def main_menu():
    main_menu_promt = {
        'type': 'list',
        'name': 'main_choice',
        'message': 'Choose an option\n',
        'choices': [v for k,v in mm_choices.items()]
    }


    while(True):
        print('\n')
        mm_answers = pyq.prompt(main_menu_promt)

        if mm_answers['main_choice'] is mm_choices['back']:
            break
        
        elif mm_answers['main_choice'] is mm_choices['ss_script']:
            ss_menu()

        elif mm_answers['main_choice'] is mm_choices['en_dis_auto']:
            autostart_menu()

        elif mm_answers['main_choice'] is mm_choices['show_log']:
            read_main_log()

        elif mm_answers['main_choice'] is mm_choices['config']:
            cli.config_menu()


def ss_menu():
    ss_menu_promt = {
        'type': 'list',
        'name': 'start_stop',
        'message': '\nChoose an option\n',
        'choices': [v for k,v in ss_options.items()]
    }

    while (True):
        print('\n')
        ss_answers = pyq.prompt(ss_menu_promt)

        if ss_answers['start_stop'] is ss_options['back']:
            break

        elif ss_answers['start_stop'] is ss_options['start']:
            start_avail_script()

        elif ss_answers['start_stop'] is ss_options['stop']:
            stop_avail_script()

        elif ss_answers['start_stop'] is ss_options['restart']:
            restart_avail_script()


def autostart_menu():
    autostart_menu_promt = {
        'type': 'list',
        'name': 'enable_disable',
        'message': '\nChoose an option\n',
        'choices': [v for k,v in autostart_options.items()]
    }

    while (True):
        print('\n')
        autostart_answers = pyq.prompt(autostart_menu_promt)

        if autostart_answers['enable_disable'] is autostart_options['back']:
            break

        elif autostart_answers['enable_disable'] is autostart_options['enable']:
            enable_avaiL_startup()

        elif autostart_answers['enable_disable'] is autostart_options['disable']:
            disable_avail_startup()


# inp = input("Start the bloody program!")
# start_avail_script()

# inp = input("Stop the bloody program!")
# stop_avail_script()

# inp = input("Read logging file")
# read_main_log()

# inp = input("Enable autostart")
# enable_avaiL_startup()

# inp = input("Disable autostart")
# disable_avail_startup()

try:
    main_menu()
except KeyboardInterrupt:
    print('Will miss you')
finally:
    print('We are done!')

