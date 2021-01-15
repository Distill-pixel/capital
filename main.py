"""
[0] Information
‣	Capital is an Shirt/Pant/Face/Audio downloader. You may skid off the code or resell it (I wouldn't recommend doing this).
‣ Capital is completely proxyless as there is no imposed ratelimit over any of the endpoints used.
‣ Capital is completely free to use and is open sourced.
‣ Below this comment, you can find the metadata for this project.
‣ Capital is not meant for production use but is still capable for it.
‣ Please don't complain about the shit code, I didn't spend a lot of time making this.
‣ Set _stream to False if you do not want any output from workers, this might speed up the =process.
‣ You may modify the code so it's usable as a module.
"""

__todo__ = ["Push new option handler"]
__author__ = "Stellaris#0001"
__version__ = "1.0.1"
__maintainer__ = "Stellaris#0001"
__license__ = "MIT"
_final = None

"""
[1] Imports
"""

import requests
import xmltodict
import itertools
import util
import threading
import sys
import imghdr
import time
import colorama
from bs4 import BeautifulSoup
import io
import os

"""
[2] Setup
"""

if os.path.exists('output') == False:
	os.mkdir('output')
if os.path.exists('ids.txt') == False:
	with open("ids.txt", "w") as f:
		f.write(" ")

_stream = True
_final = []
_thread_list = []

try:
	_id_list = open("ids.txt", "r").read().splitlines()
	#_id_list.pop()
except FileNotFoundError:
	util.warning("ID's file not found. Aborting!")
	util.throw_error("ID's file not found!")
	sys.exit()

_choice = util.ask("Would you like to check Shirts/Pants/Faces [1], Animations/Models [2] or Audios [3]. [1/2/3] ")
if _choice != "1" and _choice != "2" and _choice != "3":
	util.warning("Invalid choice. Aborting!")
	util.throw_error("Invalid choice, aborted program.")
	sys.exit()

try:
	_thread_count = int(util.ask(f"How many threads do you wish to use? Recommended: 30 threads. [0-100] "))
except:
	util.warning("Error! You specified an invalid amount of threads (not an integer).")
	util.throw_error("Invalid thread amount specified, abort program.")
	sys.exit()

""" 
[3] Main
"""

def worker(thread):
	if _choice == "1":
		for _id in _id_list:
			_id_list.remove(_id)
			util.info(f"[T{thread}] Processing ID: {_id}.")
			_xml = requests.get(f"https://assetdelivery.roblox.com/v1/asset?id={_id}", headers = {"Requester": "Client"}).text
			if _xml == '{"errors":[{"code":404,"message":"Request asset was not found"}]}' or _xml == '{"errors":[{"code":409,"message":"User is not authorized to access Asset."}]}':
				util.throw_error(f"Error in fetching asset ID {_id}. Response: {_xml}")
				util.warning(f"[T{thread}] An error has occured: AssetID not found")
			else:
				print(_xml)
				_new_id = xmltodict.parse(_xml)["roblox"]["Item"]["Properties"]["Content"]["url"].replace("http://www.roblox.com/asset/?id=", "")
				_output = requests.get(f"https://assetdelivery.roblox.com/v1/asset?id={_new_id}", headers = {"Requester" : "Client"}).content
				_output_ramdisk = imghdr.what(io.BytesIO(_output))
				with open(f"output/{_new_id}.{_output_ramdisk}", "wb") as f:
					f.write(_output)
				util.info(f"[T{thread}] Done downloading asset ID: {_id}.")
		return False
	elif _choice == "2":
		for _id in _id_list:
			_id_list.remove(_id)
			util.info(f"[T{thread}] Processing ID: {_id}.")
			_output = requests.get(f"https://assetdelivery.roblox.com/v1/asset?id={_id}", headers = {"Requester" : "Client"})
			if _output.text == '{"errors":[{"code":404,"message":"Request asset was not found"}]}' or '{"errors":[{"code":409,"message":"User is not authorized to access Asset."}]}':
				util.throw_error(f"Error in fetching asset ID {_id}. Response: {_output}")
				util.warning(f"[T{thread}] An error has occured: AssetID not found")
			elif str(type(_output)) == "<class 'str'>":
				util.throw_error(f"Error in fetching asset ID {_id}.")
				util.warning(f"[T{thread}] An error has occured: Invalid choice for specified asset.")
			else:
				with open(f"output/{_id}.rbxm", "wb") as f:
					f.write(_output.content)
				util.info(f"[T{thread}] Done downloading asset ID: {_id}.")
	elif _choice == "3":
		for _id in _id_list:
			_id_list.remove(_id)
			soup = BeautifulSoup(requests.get("https://www.roblox.com/library/{_id}?Category=Audio").text, "html.parser")
			util.info(f"[T{thread}] Processing ID: {_id}.")
			success = False
			
			for link in soup.find_all('a'):
				url = link.get("data-mediathumb-url")
				if url != None:
					success = True
					_final_song = url
				else:
					pass

			if success == False:
				util.throw_error(f"Error in fetching ID: {_id}.")
				util.warning(f"[T{thread}] An error has occured: AssetID not found")
			else:
				audio = requests.get(_final_song).text
				ramfile = io.BytesIO(audio)
				with open(f"output/{_id}.{imghdr.what(audio)}", "wb") as f:
					f.write(audio)
				util.info(f"[T{thread}] Done downloading asset ID: {_id}.")	
				
for tnum in range(1, _thread_count + 1):
	try:
		_at = threading.Thread(target = worker, args = [tnum], daemon = True)
		_at.start()
		_thread_list.append(_at)
	except:
		util.warning("Thread overflow! Cannot create more workers.")
		util.throw_error("Thread overflow! Cannot create more workers.")

while len(_id_list) != 0:
	pass

time.sleep(1) # Giving the thread some time to process as the ID is removed before the worker is done with the task.
for _c_thread in _thread_list:
	_c_thread.join()
