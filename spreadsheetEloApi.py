#coding: utf-8

from __future__ import print_function

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import requests
import secrets


SCOPES = "https://www.googleapis.com/auth/spreadsheets"


def main():

	row = 2

	
	accounts = ["Toxillo", "Sir Meldor", "Sir Synthoras", "xZylote", "Aphadon", "Sir Veredir"]

	accountDict = {}

	for i in accounts:

		names = "Unranked"
		soloQ = "Unranked"
		flexSR = "Unranked"
		tft = "Unranked"
		

		getId = requests.get("https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + i + "?api_key="  +  secrets.riot_key)
		accountId = str(getId.json()["id"])
		lolRequest = requests.get("https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + accountId + "?api_key=" + secrets.riot_key)
		lolLeagues = lolRequest.json()
		tftLeagues = requests.get("https://euw1.api.riotgames.com/tft/league/v1/entries/by-summoner/" + accountId + "?api_key=" + secrets.riot_key).json()
		print(tftLeagues)
			
		names = getId.json()["name"]
		level = getId.json()["summonerLevel"]
		
	
		for l in lolLeagues:
			if l["queueType"] == "RANKED_SOLO_5x5":
				soloQ = str(l["tier"] + " " + l["rank"])
			elif l["queueType"] == "RANKED_FLEX_SR":
				flexSR = str(l["tier"] + " " + l["rank"])
				#file.write(getId.json()["name"] + "\n")
				#file.write(l["queueType"] + ": " + l["tier"] + "\n")

		for l in tftLeagues:
			if l["queueType"] == "RANKED_TFT":
				tft = str(l["tier"] + " " + l["rank"])

		
		accountDict = {
			"name"	:	getId.json()["name"],
			"soloQ"	:	soloQ,
			"flexSR":	flexSR,
			"tft"	:	tft,
			"level" :	level
		}



		printer(accountDict, row)

		row  += 1

def printer(accDict, row):
	creds = None

	if os.path.exists('token.json'):
		creds = Credentials.from_authorized_user_file('token.json', SCOPES)

	
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('token.json', 'w') as token:
			token.write(creds.to_json())

	try:
		print(accDict)
		service = build("sheets", "v4", credentials=creds)


		data = [
			{
				"range": "Sheet1!A%s:E%s" % (row, row),
				"majorDimension": "ROWS",
				"values": [
					[ accDict["name"], accDict["soloQ"], accDict["flexSR"], accDict["tft"], accDict["level"] ]
				]
						
			},
		]

		body = {
			"valueInputOption": "USER_ENTERED",
			"data": data
		}
		
		result = service.spreadsheets().values().batchUpdate(spreadsheetId="1U428igWOgCWm_AfNLimqpul_VFa2z167Nm6FgFh3pmU", body=body).execute()

	except HttpError as err:
		print(err)

if __name__ == "__main__":
	main()

#os.remove("token.json")