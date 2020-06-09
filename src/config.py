import json
import os
import sys
import inspect

current_dir = os.path.dirname(os.path.abspath(__file__))
# print(current_dir)
parent_dir = os.path.dirname(current_dir)
cfg_dir = os.path.join(parent_dir, 'cfg')
# print(cfg_dir)
# sys.path.append(cfg_dir)
config_file = os.path.join(cfg_dir, 'config.json')
print(config_file)
# config_file = "config.json"

WATCHED_FILES = [config_file]
LAST_EXIT_FILE = 'last_exit.pkl'
STATE_FILE = 'gpi_pair_state.pkl'


# das_logger = setup_logger()
try:
	with open(config_file) as cf_file:
		config_dict = json.load(cf_file)
except FileExistsError or FileNotFoundError:
	# das_logger.error('Nema config.json file, losho.')
	print('Nema config deistvaite!')

elemental_ip = config_dict['elemental_ip']
gpi2stream = config_dict['gpi_to_event']
min_av_enbl = config_dict['min_avail_enabled']
min_av_dur = config_dict['min_avail_duration']
