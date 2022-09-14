#coding: utf-8

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os
import requests


scopes = "https://www.googleapis.com/auth/spreadsheets"

def main():

	row = 2

	
	accounts = []

	accountDict = {}

	for i in accounts:

		names = "Unranked"
		soloQ = "Unranked"
		flexTT = "Unranked"
		flexSR = "Unranked"
		

		getId = requests.get("https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/"+i+"?api_key=RGAPI-de5105bf-2740-4b2f-bbb8-5667fb30b0fb")
		accountId = str(getId.json()["id"])
		r = requests.get("https://euw1.api.riotgames.com/lol/league/v3/positions/by-summoner/"+accountId+"?api_key=RGAPI-de5105bf-2740-4b2f-bbb8-5667fb30b0fb")
		leagues = r.json()

			
		names = getId.json()["name"]

		
	
		for l in leagues:
			if l["queueType"] == "RANKED_SOLO_5x5":
				soloQ = str(l["tier"]+" "+l["rank"])
			elif l["queueType"] == "RANKED_FLEX_TT":
				flexTT = str(l["tier"]+" "+l["rank"])
			elif l["queueType"] == "RANKED_FLEX_SR":
				flexSR = str(l["tier"]+" "+l["rank"])
				#file.write(getId.json()["name"]+"\n")
				#file.write(l["queueType"]+": "+l["tier"]+"\n")
		
		accountDict = {
			"name"	:	getId.json()["name"],
			"soloQ"	:	soloQ,
			"flexTT":	flexTT,
			"flexSR":	flexSR
		}



		printer(accountDict, row)

		row += 1

def printer(accDict, row):

	print(accDict)

	store = file.Storage("token.json")
	creds = store.get()

    
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets("credentials.json", scopes)
		creds = tools.run_flow(flow, store)
	service = build("sheets", "v4", http=creds.authorize(Http()))


	data = [
   		{
   			"range": "Sheet1!A%s:D%s" % (row, row),
   			"majorDimension": "ROWS",
   			"values": [
   						[accDict["name"], accDict["soloQ"], accDict["flexTT"], accDict["flexSR"]
   					]
   			]
   					
   		},

   	]
	
	body = {
		"valueInputOption": "USER_ENTERED",
    	"data": data
	}
	
	result = service.spreadsheets().values().batchUpdate(
    spreadsheetId="1U428igWOgCWm_AfNLimqpul_VFa2z167Nm6FgFh3pmU", body=body).execute()
	print("{0} cells updated.".format(result.get("updatedCells")));



if __name__ == "__main__":
	main()

#os.remove("token.json")