from __future__ import print_function
import pickle
import time
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
spreadsheet_id = '159nIWVZ0XX1B5ouzrCV5bPPqucObhjb9t_00fZXplQM'

# Test sheet
# spreadsheet_id = '1K_nswXmeeeQInfrM1zWQTHQ152zd1fs552DeCgKHsNo'

prev_values = ['C52:C52', 'C39:C39']

values = ['C26:C26', 'C39:C39', 'C52:C52'] #'C13:C13'

room_prio = ['C52:C52', 'D48:D48', 'D49:D49', 'D50:D50', 'C48:C48', 'C49:C49', 'C50:C50']


def prev_room_check(sheet):
    prev1 = sheet.values().get(spreadsheetId=spreadsheet_id, range=prev_values[0]).execute().get('values', [])
    time.sleep(0.2)
    prev2 = sheet.values().get(spreadsheetId=spreadsheet_id, range=prev_values[1]).execute().get('values', [])
    if prev1 and prev2 and (prev1[0][0] != '5. ABH' or prev2[0][0] != '5.ABH'):
        return True
    return False

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    prev1 = None
    prev2 = None
    if prev_room_check(sheet):
        room_to_get = 'C52'

    for i in range(18000):
        prev1 = sheet.values().get(spreadsheetId=spreadsheet_id, range=values[0]).execute().get('values', [])
        prev2 = sheet.values().get(spreadsheetId=spreadsheet_id, range=values[1]).execute().get('values', [])

        index = 0

        if prev1 and prev2 and prev1[0][0] == "5. ABH" and prev2[0][0] == "5. ABH":
            index = 1

        test_room = sheet.values().get(spreadsheetId=spreadsheet_id, range=room_prio[index]).execute().get('values', [])

        while test_room and index + 1 < len(room_prio):
            index += 1
            time.sleep(0.05)
            test_room = sheet.values().get(spreadsheetId=spreadsheet_id, range=room_prio[index]).execute().get('values', [])
            if test_room and test_room[0][0] == "5. ABH":
                print("Already eingetragen")
                quit(0)

        if not test_room:
            result = service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id, range=room_prio[index],
                valueInputOption="RAW", body={'values': [['5. ABH']]}).execute()
            print("Jetzt eingetragen")
            quit(0)

        '''for dach in values:
            result = sheet.values().get(spreadsheetId=spreadsheet_id, range=dach).execute()
            values_current = result.get('values', [])
            if not values_current:
                print('No data found.')
                result = service.spreadsheets().values().update(
                    spreadsheetId=spreadsheet_id, range=dach,
                    valueInputOption="RAW", body={'values': [['5. ABH']]}).execute()
            else:
                if values_current[0][0] == "":
                    result = service.spreadsheets().values().update(
                        spreadsheetId=spreadsheet_id, range=dach,
                        valueInputOption="RAW", body={'values': [['5. ABH']]}).execute()
            print(values_current[0][0])'''
        time.sleep(0.2)

    print("Alles Kaputt")


if __name__ == '__main__':
    main()
