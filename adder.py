from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, FloodWaitError, PhoneNumberBannedError
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser
import os
import sys
import csv
import traceback
import time
import random

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"
def banner():
	os.system('clear')
	print(f"""***PUPLEBELLY***""")

cpass = configparser.RawConfigParser()
cpass.read('config.data')


numbers = []

for section in cpass.sections():
	person = []	   
	for key in cpass[section]:
		person.append(cpass[section][key])
	numbers.append(person)



try:

	#n = 2800
	n = int(input("Starting index to add members from: "))
	for person in numbers:
		api_id = person[0]
		api_hash = person[1]
		phone = person[2]
		client = TelegramClient(phone, api_id, api_hash)


		try:
			client.connect()

			if not client.is_user_authorized():
				client.send_code_request(phone)
				os.system('clear')
				banner()
				client.sign_in(phone, input(gr+'[+] Enter the code for ' + phone + ': '+re))

			users = []
			with open(r"members.csv", encoding='UTF-8') as f:  #Enter your file name
				rows = csv.reader(f,delimiter=",",lineterminator="\n")
				next(rows, None)
				for row in rows:
					user = {}
					user['username'] = row[0]
					user['id'] = int(row[1])
					user['access_hash'] = int(row[2])
					user['name'] = row[3]
					users.append(user)

			chats = []
			last_date = None
			chunk_size = 200 	
			groups = []
			result = client(GetDialogsRequest(
				offset_date=last_date,
				offset_id=0,
				offset_peer=InputPeerEmpty(),
				limit=chunk_size,
				hash=0
			))
			chats.extend(result.chats)

			for chat in chats:
				try:
					if chat.megagroup == True:
						groups.append(chat)

				except:
					continue

			print(gr+'Choose a group to add members:'+cy)
			i = 0
			for group in groups:
				print(str(i) + '- ' + group.title)
				i += 1

			g_index = input(gr+"Enter a Number: "+re)
			target_group = groups[int(g_index)]

			target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

			mode = 1

			users = users[n:]

			for user in users:
				n += 1
	#		   if n % 70 == 0:
	#				break
				try:
					print("Adding {}".format(user['id']))
					if mode == 1:
						if user['username'] == "":
							continue
						user_to_add = client.get_input_entity(user['username'])
					elif mode == 2:
						user_to_add = InputPeerUser(user['id'], user['access_hash'])
					else:
						sys.exit("Invalid Mode Selected. Please Try Again.")
					client(InviteToChannelRequest(target_group_entity, [user_to_add]))
					print("Waiting for 60-180 Seconds...")
					time.sleep(random.randrange(60, 180))
				except PeerFloodError:
					print("Getting Flood Error from telegram. Moving to the next number")
					break
				except UserPrivacyRestrictedError:
					print("The user's privacy settings do not allow you to do this. Skipping.")
					print("Waiting for 5 Seconds...")
					time.sleep(random.randrange(60, 180))
				except FloodWaitError:
					print("Getting Flood Error for a while. Wait for a few hours. Moving to the next number")
					break
				except Exception as e:
					traceback.print_exc()
					try:
						print("Unexpected Error: " + e.message)
					except:
						pass
					
					continue

		except PhoneNumberBannedError:
			print("Phone:" + phone + " Has Been Banned. Please remove from list")
			continue




except KeyError:
	os.system('clear')
	banner()
	print(re+"[!] run python setup.py first !!\n")
	sys.exit(1)
