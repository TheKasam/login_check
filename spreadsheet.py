#Description: Reads members sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time


def main():
    print("starting")
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    members = client.open("MISA Membership 2017-2018").sheet1
    members_list_of_lists = members.get_all_values()


    members_uteid = []
    members_names = []
    for x in members_list_of_lists:
         members_uteid.append(x[2])
    for x in members_list_of_lists:
        full_name = x[0].strip().lower() + x[1].strip().lower()
        members_names.append(full_name)

    responders_uteid = []
    responders_names = []

    responders = client.open("General Meeting 4 (Responses)").sheet1
    responders_list_of_list = responders.get_all_values()
    currentEventResp = len(responders_list_of_list[:])
    prevEventResp = 0

    while True:
        print("start while loop")
        startTime = time.time()
        responders = client.open("General Meeting 4 (Responses)").sheet1


        #contains all the files values
        responders_list_of_list = responders.get_all_values()


        #making a bunch of lists
        for x in range(-(currentEventResp - prevEventResp),0,1) :
            print(x)
            responders_uteid.append(responders_list_of_list[x][1])
            print("test",x)

            full_name = responders_list_of_list[x][2].strip().lower() + responders_list_of_list[x][3].strip().lower()
            responders_names.append(full_name)


        for x in range(currentEventResp-(currentEventResp - prevEventResp),currentEventResp) :
        #logic to check if member by ut_eid and Name
            if responders_uteid[x] in members_uteid and responders_uteid[x] != "":
                responders.update_cell(x+1,6, "Member - uteid found")
            elif responders_names[x] in members_names:
                responders.update_cell(x+1,6, "Member - Name found")
            else:
                responders.update_cell(x+1,6, "uteid nor name found")
            print(x)
        print("Dones")
        #check if responders changedi
        prevEventResp = currentEventResp
        while currentEventResp <= prevEventResp:
          currentEventResp = len(responders.get_all_values()[:])
        #   print(prevEventResp)
        #   print(currentEventResp)
        endTime = time.time()
        print(endTime)


main()
