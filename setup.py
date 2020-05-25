from setuptools import setup

setup(
	name="ResourceMonitor",
	version="0.0.1",
	description="Monitoring CPU/Memory usage percent for single process or all process",
	author="Samue1Wang@NTA-Lab",
	author_email="s60106m@gmail.com",
	packages=["ResourceMonitor"],
	install_requires=["psutil"]
)