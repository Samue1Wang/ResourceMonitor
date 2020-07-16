from enum import Enum
import os
import sys
import math
import time
import logging
import optparse

FABRIC_TARGET_PATH = ''
IOTA_TARGET_PATHS = ['./hornet/comnetdb', './hornet/snapshots/comnet/export.bin']


class Mode(Enum):
	FABRIC = 'fabric'
	IOTA = 'iota'


def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-f", "--fabric", dest="fabric", action="store_true", default=False, help="Hyperledger Fabric channel block size.")
	parser.add_option("-i", "--iota", dest="iota", action="store_true", default=False, help="IOTA Hornet ledger size, including 'DB' and 'Snapshots' Folder.")
	(options, arguments) = parser.parse_args()

	if options.fabric and options.iota:
		print('[X] Options Error: Only 1 option is required, not 2')
		
		sys.exit(1)


	if not options.fabric and not options.iota:
		print('[X] Options Error: At least 1 option is needed')
		
		sys.exit(1)

	return Mode.FABRIC if options.fabric else Mode.IOTA


def convert_bytes_to_human_readable(size_bytes):
	unit = ['B', 'KB', 'MB', 'GB']

	if size_bytes == 0:
		return '0 B'

	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes/p, 2)

	human_size = f'{s} {unit[i]}'

	return human_size


def get_size(path: str, convert: bool = False):
	try:
		size = None

		if os.path.isdir(path):
			print('[+] The path is pointed to a directory')

			size = sum(d.stat().st_size for d in os.scandir(path) if d.is_file())
		
		else:
			print('[+] The path is pointed to a file')

			size = os.path.getsize(path)

		if convert:
			return convert_bytes_to_human_readable(size)

		return size	
	except Exception as e:	
		print('[X] Error: Can not located file path')
		print(f'  -- {path}')
		print(e)

		sys.exit(1)

def start_fabric_tracker():
	print('[+] Start Hyperledger Fabric Tracker Process')

	logging.basicConfig(level=logging.INFO, format="%(asctime)s\t[+] %(message)s", filename="fabric_ledger_tracker_log.txt")


def start_iota_tracker():
	print('[+] Start IOTA Hornet Tracker Process')

	logging.basicConfig(level=logging.INFO, format="%(asctime)s\t[+] %(message)s", filename="iota_ledger_tracker_log.txt")


def main():
	mode = get_arguments()

	if mode is Mode.FABRIC:
		start_fabric_tracker()

	elif mode is Mode.IOTA:
		start_iota_tracker()

if __name__ == '__main__':
	# main()

	size = get_size('.', True)

	print(size)
	print(type(size))

	sys.exit(0)