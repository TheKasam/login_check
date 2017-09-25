#Description: Reads members sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def main():
    while True:
        # use creds to create a client to interact with the Google Drive API
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        members = client.open("MISA Membership 2017-2018").sheet1
        responders = client.open("MISA General Meeting 2 Sign In (Responses)").sheet1

        #contains all the files values
        members_list_of_lists = members.get_all_values()
        responders_list_of_lists = responders.get_all_values()

        #making a bunch of lists
        members_uteid = []
        responders_uteid = []
        members_names = []
        responders_names = []

        for x in members_list_of_lists:
             members_uteid.append(x[2])

        for x in responders_list_of_lists:
            responders_uteid.append(x[3])

        for x in members_list_of_lists:
            full_name = x[0].strip().lower() + x[1].strip().lower()
            members_names.append(full_name)

        for x in responders_list_of_lists:
            full_name = x[0].strip().lower() + x[1].strip().lower()
            responders_names.append(full_name)


        #logic to check if member by ut_eid
        for x in range(len(responders_uteid)):
            if responders_uteid[x] not in members_uteid:
                responders.update_cell(x+1,5, "nani!!")
                print(responders_uteid[x])

        #checking with first and last name
        for x in range(len(responders_names)):
            if responders_names[x] not in members_names:
                responders.update_cell(x+1,5,"nani!?!")




main()
