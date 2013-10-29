"""
A basic outline for the healthcare project. Uses easyGUI (tested on Linux
in the labs), and currently has pass functions for Oracle implementation.
The first five functions below need to be implemented.
"""


def createPrescription(pnum, tname, enum):
    """
    Yet to be implemented function to create a perscription using patient number
    pnum, test name tname, and employee number enum. Currently unimplemented
    because the lab tutorials have yet to cover Python connection to Oracle.
    We should probably learn that ourselves.
    """
    return "createPrescription not yet implemented"

def checkTest(pnum, tname):
    """
    Also unimplemented, checks if patient is allowed to take test. Returns bool.
    """
    if pnum == '1':
        return True
    else:
        return False

def performTest(pnum, tname, lname, tdate, tresult):
    """
    Also unimplemented, inserts test record into database. Shoudld only be
    called after checkTest returns True.
    """
    return "performTest not yet implemented"

def performSearch(stype, pnum = None, enum = None, sdate = None, edate = None,
                  ttype = None):
    """
    Also unimplemented, performs one of three search types and returns
    the result.
    """
    return "performSearch not yet implemented"

def informationUpdate(pnum, name, address, birthday, phone):
    """
    Also unimplemented, updates a patient record or creates if pnum does not
    exist. Returns "Patient created" or "Patient updated" if successful.
    """
    return "informationUpdate not yet implemented"

import easygui as eg
import sys

# Declare string names for application programs / modules
p = "Create Prescription"
t = "Administer Test"
i = "Update / Create Patient Information"
s = "Search"
# Declare string names for search types
ptr = "Patient Test Records"
dpr = "Doctor Prescription Record"
aa = "Alarming Age"

# GUI input functions for the four basic application processes.
def guiPrescription():
    """
    Interface for creating a new prescription.
    """
    msg = "Please enter the prescription information."
    title = "Prescription Info"
    fieldNames = ["Patient Healthcare #", "Test Name", "Doctor Employee #"]
    fieldValues = []
    fieldValues = eg.multenterbox(msg, title, fieldNames)
    msg = createPrescription(fieldValues[0], fieldValues[1], fieldValues[2])
    title = "Result"
    eg.msgbox(msg, title)

def guiTest():
    """
    Interface for performing a test.
    """
    msg = "Enter test information to confirm patient eligibility. Enter 1 as patient number to test successful patient eligibility."
    title = "Test Details"
    fieldNames = ["Patient Healthcare #", "Test Name"]
    fieldValues = []
    fieldValues = eg.multenterbox(msg, title, fieldNames)
    pnum, tname = fieldValues
    msg = checkTest(pnum, tname)
    if msg:
        msg = "Patient eligibility confirmed. Enter test result."
        title = "Test Results"
        fieldNames = ["Lab Name", "Test Date (mm/dd/yyyy)", "Test Result"]
        fieldValues = []
        fieldValues = eg.multenterbox(msg, title, fieldNames)
        lname, tdate, tresult = fieldValues
        msg = performTest(pnum, tname, lname, tdate, tresult)
        title = "Result"
        eg.msgbox(msg, title)
    else:
        eg.msgbox("Patient is not eligible to receive this test.", "Error!")

def guiUpdateInformation():
    """
    Interface for updating or creating a patient.
    """
    msg = "Please enter the patient information."
    title = "Patient Info"
    fieldNames = ["Patient Healthcare #", "Name", "Address",
                  "Birth Day (mm/dd/yyyy)", "Phone Number"]
    fieldValues = []
    fieldValues = eg.multenterbox(msg, title, fieldNames)
    pnum, name, address, birthday, phone = fieldValues
    msg = informationUpdate(pnum, name, address, birthday, phone)
    title = "Result"
    eg.msgbox(msg, title)

def guiSearch():
    """
    Interface for performing a search
    """
    msg = "Select the type of search to perform"
    title = "Search Type Selection"
    choices = [ptr, dpr, aa]
    choice = eg.choicebox(msg, title, choices)
    if choice == ptr:
        msg = "Please enter the patient healthcare number."
        title = "Patient Test Record Search"
        fieldNames = ["Patient Healthcare #"]
        fieldValues = []
        # Should later be changed to enterbox if only needs one entry
        fieldValues = eg.multenterbox(msg, title, fieldNames)
        msg = performSearch(ptr, pnum = fieldValues[0])
        title = "Result"
        eg.msgbox(msg, title)
    elif choice == dpr:
        msg = "Please enter the employee number and date range for your search."
        title = "Doctor Prescription Record Search"
        fieldNames = ["Doctor Employee #", "Start Date (mm/dd/yyyy)",
                      "End Date   (mm/dd/yyyy)"]
        fieldValues = []
        fieldValues = eg.multenterbox(msg, title, fieldNames)
        enum, startdate, enddate = fieldValues
        msg = performSearch(dpr, enum = enum, sdate = startdate,
                            edate = enddate)
        title = "Result"
        eg.msgbox(msg, title)
    elif choice == aa:
        msg = "Please enter the test type you would like to search for"
        title = "Alarming Age Search"
        # Should later be changed to enterbox if only needs one entry
        fieldNames = ["Test Name"]
        fieldValues = []
        fieldValues = eg.multenterbox(msg, title, fieldNames)
        msg = performSearch(aa, ttype = fieldValues[0])
        title = "Result"
        eg.msgbox(msg, title)


while 1:
    msg ="Welcome to ABHealthCare, please select an option."
    title = "ABHealthCare Control Panel"
    choices = [p, t, i, s]
    choice = eg.choicebox(msg, title, choices)

    # note that we convert choice to string, in case
    # the user cancelled the choice, and we got None.
    if choice == p:
        guiPrescription()
    elif choice == t:
        guiTest()
    elif choice == i:
        guiUpdateInformation()
    elif choice == s:
        guiSearch()

    msg = "Do you want to continue using ABHealthCare?"
    title = "Continue?"
    if eg.ccbox(msg, title, ('Continue', 'Exit')):     # show a Continue/Cancel dialog
        pass  # user chose Continue
    else:
        sys.exit(0)           # user chose Cancelimport curses