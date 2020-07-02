import optparse
import time
import logging
import os
try:
	import psutil
except:
	os.system("python -m pip install psutil")
import psutil


RUN = True
# RUN = False
OVERRIDE_LOG = True
MONITOR_PROCESS = True
# MONITOR_PROCESS = False
INTERVAL = 0.5

def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-p", "--pid", dest="pid", help="The process ID which you want to observe.")
	(options, arguments) = parser.parse_args()
	
	return options.pid if options.pid else False



def setting_logging():
	print("[+] Setting logging config...")
	logging.basicConfig(level=logging.INFO, format="%(asctime)s\t[+] %(message)s", filename="resource_usage_log.txt")


def check_log_file_exists():
	if OVERRIDE_LOG and os.path.exists("./resource_usage_log.txt"):
		print("[+] Log file already exists !")
		print("[+] Delete the log file: resource_usage_log.txt ...")
		os.remove("./resource_usage_log.txt")
		print("[+] Delete successed !")

def get_process_list():
	process = [p.name() for p in psutil.process_iter()]
	for p in psutil.process_iter():
		print(p)

def start_monitor_loop(pid):
	proc = None
	if MONITOR_PROCESS and pid:
		pid = int(pid)
		print("\n[+] Start Resource Monitor with PID {pid}:" .format(pid=pid))
		proc = psutil.Process(pid)
		print(" - Name: {} | Status: {}" .format(proc.name(), proc.status))
	else:
		print("\n[+] Start Resource Monitor:")

	while RUN:
		if MONITOR_PROCESS and pid:
			if not proc.is_running():
				print("[+] Process not exists, monitor exit !")
				return

		cpu = psutil.cpu_percent() if not proc else proc.cpu_percent()
		mem = psutil.virtual_memory().percent if not proc else proc.memory_percent()

		print(f"  - CPU Usage: {cpu:>5.2f}% | Memory Usage: {mem:>5.2f}%\t\t\r", end="")
		logging.info(f"CPU Usage: {cpu:>5.2f}% | Memory Usage: {mem:>5.2f}%")

		time.sleep(INTERVAL)


def main():
	pid = get_arguments()
	check_log_file_exists()
	setting_logging()
	# get_process_list()
	start_monitor_loop(pid)


if __name__ == "__main__":
	main()
