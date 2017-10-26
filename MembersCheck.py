#Description: Check if user is Member (or RSVPed) to an event when they sign in though a google form.
#The results are then posted in a column of the respective form's google sheet.
#Keep python script running till all members sign in. Can restart script at any time.
#To quit script press control - c or quit terminal / command promt

#modules needed
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time


def main():
    print("starting")
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

 ###edit these according to your sheet.###
    #from rsvp / members sheet
    #Make sure you use the right name here.
    member_sheet_name = "MISA Membership 2017-2018"
    member_email_column = 3
    member_first_name_column = 1
    member_last_name_column = 2
    #from responsers of sign in sheet
    responsers_sheet_name = "MISA GM 5 (Responses)"
    respondent_email_column = 2
    respondent_first_name_column = 3
    respondent_last_name_column = 4
    #shows the result of if the respondant was in the member/rsvp list
    respondent_result_column = 6

    #This is your member sheet or rsvp sheet
    #Finding a workbook by name and open the first sheet.
    members = client.open(member_sheet_name).sheet1
    #creates a 2d list with all rows from the sheet
    members_list_of_lists = members.get_all_values()

    members_email = []
    members_names = []
    for x in members_list_of_lists:
         members_email.append(x[member_email_column - 1])

    for x in members_list_of_lists:
        full_name = x[member_first_name_column - 1].strip().lower() + x[member_last_name_column -1].strip().lower()
        members_names.append(full_name)

    #opening responders sheet
    responders = client.open(responsers_sheet_name).sheet1
    #creates a 2d list with all rows from the sheet
    responders_list_of_list = responders.get_all_values()
    responders_email = []
    responders_names = []

    currentEventResp = len(responders_list_of_list[:])
    prevEventResp = 0
    print(responders_list_of_list)

    while True:
        print("New Round")
        startTime = time.time()

        #reopening sheet to get latest values
        responders = client.open(responsers_sheet_name).sheet1
        responders_list_of_list = responders.get_all_values()

        #filling responders lists
        for x in range(-(currentEventResp - prevEventResp),0,1) :
            responders_email.append(responders_list_of_list[x][respondent_email_column-1])
            full_name = responders_list_of_list[x][respondent_first_name_column-1].strip().lower() + responders_list_of_list[x][respondent_last_name_column-1].strip().lower()
            responders_names.append(full_name)


        for x in range(currentEventResp-(currentEventResp - prevEventResp),currentEventResp) :
        #logic to check if member by Email and Name
            if responders_email[x] in members_email and responders_email[x] != "":
                responders.update_cell(x+1,respondent_result_column, "Member - Email found")
            elif responders_names[x] in members_names:
                responders.update_cell(x+1,respondent_result_column, "Member - Name found")
            else:
                responders.update_cell(x+1,respondent_result_column, "Email nor Name found")
            print(x)
        print("Done with round")
        endTime = time.time()
        print("round time",endTime - startTime)

        #check if responders changed
        prevEventResp = currentEventResp
        while currentEventResp <= prevEventResp:
          currentEventResp = len(responders.get_all_values()[:])
    


main()
