#!/bin/python
input("Press enter to start.")

# recommendation: %run -i <file>


from selenium import webdriver                                                  # type: ignore
from selenium.webdriver.common.by import By                                     # type: ignore
from selenium.webdriver.common.action_chains import ActionChains                # type: ignore
from selenium.webdriver.support import expected_conditions                      # type: ignore
from selenium.webdriver.support.wait import WebDriverWait                       # type: ignore
from selenium.webdriver.common.keys import Keys                                 # type: ignore
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities  # type: ignore
from selenium.common.exceptions import NoSuchElementException                   # type: ignore

from typing import Callable, Any
import time
import traceback
import shutil
from pathlib import Path
import sys
import pickle


profileStoragePath = Path(sys.argv[0]).parent / "terminal-profile"
profileBackupPath = Path(sys.argv[0]).parent / "terminal-profile-backup"
#cookiesFilename = Path(sys.argv[0]).parent / "terminal-cookies.pkl"
cookiesFilename: Any = None

try:
	driver  # type: ignore
except NameError:
	driver=webdriver.Firefox(executable_path="geckodriver-v0.28.0-linux64")
	driver = webdriver.Firefox(executable_path="geckodriver-v0.28.0-linux64",
					 firefox_profile=webdriver.FirefoxProfile(profileStoragePath)
					)



bug_workaround_cookie_expiry_integer=False #only for chrome

def loadCookies___()->None:
    driver.delete_all_cookies()  # sometimes required for Firefox
    import pickle

    try:
        for cookie in pickle.load(open(cookiesFilename, "rb")):
            #if bug_workaround_cookie_expiry_integer and "expiry" in cookie:
            #    cookie["expiry"]=int(cookie["expiry"]*1000)
            driver.add_cookie(cookie)
    except FileNotFoundError:
        print("Cookie not found")
    
def closeAndDumpProfile()->None:
	print("======== start dump")
	try:
		driver.execute_script("window.close()")
	except:  # might be already closed or something
		import traceback
		print("======== while closing window :")
		traceback.print_exc()
		print("======== (end)")

	time.sleep(0.5)
	currentProfilePath = driver.capabilities["moz:profile"]

	try: shutil.rmtree(profileBackupPath)
	except FileNotFoundError: pass

	try: profileStoragePath.rename(profileBackupPath)
	except FileNotFoundError: pass

	shutil.copytree(currentProfilePath, profileStoragePath,
					ignore_dangling_symlinks=True
					)
	print("Dump successful")




def do_with_retry(f: Callable)->None:
	for i in range(20-1, -1, -1):
		try:
			f()
			# done
			break

		except:
			print("Something is wrong:")
			traceback.print_exc()
			print("======== waiting", i, "more seconds")

		time.sleep(1)
		

try:

	while True:
		driver.get("https://terminal.c1games.com/playground")

		#loadCookies()

		#driver.get("https://terminal.c1games.com/playground")

		# actually this is quite inefficient...

		try:
			login=driver.find_element(By.ID, "login")

			# there is login button
			do_with_retry(lambda: login.click())

			while driver.current_url != "https://terminal.c1games.com/home":
				print("Waiting for login...")
				time.sleep(1)
			print("Okay, logged in")
			#closeAndDumpProfile()

			driver.get("https://terminal.c1games.com/playground")

		except NoSuchElementException:
			# okay already logged in
			pass

		#closeAndDumpProfile()
		#print("**TEMPORARY**")

		#advanced option button
		do_with_retry(lambda: driver.find_element(By.CSS_SELECTOR, ".btn-disclaim").click())


		replay_folder=Path("/tmp/")

		most_recent_file: Path=max(
				replay_folder.glob("*.replay"),
				key=lambda path: path.stat().st_mtime)

		driver.find_element(By.NAME, "replayFiles").send_keys(
				str(most_recent_file)
				)

		#play button
		time.sleep(1)
		do_with_retry(lambda: driver.find_element(By.CSS_SELECTOR, ".mdi-play").click())

		#obvious
		do_with_retry(lambda: driver.find_element(By.ID, "banner-startgame").click())

		#open the "change speed" collapsible
		do_with_retry(lambda: driver.find_element(By.CSS_SELECTOR, ".magnifier.s3_btn").click())

		##set speed to 4X.
		#do_with_retry(lambda: driver.find_element(By.CSS_SELECTOR, ".\\_mag_item:nth-child(5) > .s3_btn").click())
		#set speed to 8X.
		do_with_retry(lambda: driver.find_element(By.CSS_SELECTOR, ".\\_mag_item:nth-child(6) > .s3_btn").click())

		try:
			input("Press enter to reload ========")
		except KeyboardInterrupt:
			print("==interrupted? break")
			raise

finally:
	try:
		print("======== dump profile")
		closeAndDumpProfile()
	finally:
		driver.quit()
