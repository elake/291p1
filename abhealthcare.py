"""
A basic outline for the healthcare project. Uses easyGUI (tested on Linux
in the labs), and currently has pass functions for Oracle implementation.
The first five functions below need to be implemented.
"""

# >>> INTS ARE MISSING <<<

import sys
import cx_Oracle
import time

def createPrescription(pnum, pname, tname, enum, ename):
    """ 
    - Create a new test_record with enum, tname, pnum, test_id (generated upon creation), and
    prescription_date (uses current date). Lab_name, test_date, result are all null.
    - Rejects: Prescriptions which conflict with not_allowed. Also fails if enum, tname or pnum
    do not exist.
    - Returns: Prescription creation success or failure message.
    """
    # Check that pnum or pname is supplied.
    if (pnum is '' and pname is ''):
        return "Prescription creation failed. Either a patient health care number or a patient name is required."

    # Check that tname is supplied.
    if tname is '':
        return "Prescription creation failed. Test name is required."

    # Check that enum or ename is supplied.
    if (enum is '' and ename is ''):
        return "Prescription creation failed. Either a doctor employee number or a doctor name is required."

    # If enum was provided, check it exists.
    if (enum != ''):
        queryStr='SELECT employee_no FROM doctor WHERE employee_no={}'.format(enum)
        cur.execute(queryStr)
        is_doctor = cur.fetchone()
        if is_doctor is None:
            return "Prescription creation failed. Doctor employee number  does not exist."
        # If enum and ename were both provided, check that enum matches corresponding ename.
        elif (ename != ''):
            queryStr='SELECT p.name FROM patient p, doctor d  WHERE (d.employee_no={} AND p.health_care_no=d.health_care_no)'.format(enum)
            cur.execute(queryStr)
            matching_name = cur.fetchone()
            matching_name = matching_name[0] 
            if (matching_name != ename):
                return "Prescription creation failed. Doctor employee number does not match doctor name provided."   
        # If enum was the only thing provided for doctor and matches a doctor in the database, no further work required.
        else:
            pass

    # If pnum was provided, check it exists.
    if (pnum != ''):
        queryStr='SELECT health_care_no FROM patient WHERE health_care_no={}'.format(pnum)
        cur.execute(queryStr)
        is_patient = cur.fetchone()
        if is_patient is None:
            return "Prescription creation failed. Patient number does not exist. Please add patient using Update/Create Patient Info."
        # If pnum and pname were both provided, check that pnum matches corresponding pname.
        elif (pname != ''):
            queryStr='SELECT name FROM patient WHERE health_care_no={}'.format(pnum)
            cur.execute(queryStr)
            pmatching_name = cur.fetchone()
            pmatching_name = pmatching_name[0]
            if (pmatching_name != pname):
                return "Prescription creation failed. Patient health care # does not match patient name provided."    
        # If pnum was the only thing provided for patient and matches a patient in the database, no further work required.
        else:
            pass

    # If only ename was provided for doctor information, check it exists.
    if (ename != ''):
        queryStr='SELECT p.name FROM patient p, doctor d  WHERE (p.name=\'{}\' AND p.health_care_no=d.health_care_no)'.format(ename)
        cur.execute(queryStr)
        is_ename=cur.fetchone()
        if is_ename is None:
            return "Prescription creation failed. Doctor name does not exists."
        # If there are multiple doctors: Print all doctor names found to gui, along with their doctor information. 
        queryStr='SELECT p.name, d.employee_no, d.clinic_address, d.office_phone FROM patient p, doctor d WHERE (p.name=\'{}\' AND p.health_care_no=d.health_care_no)'.format(ename)
        cur.execute(queryStr)
        doc_info=cur.fetchall()
        if len(doc_info) > 1:
            doc_list=[]
            for doc in doc_info:
                doc_list.append(doc)
            right_doc = eg.choicebox("Select the correct doctor information:", "Doctor Name Search Results", doc_list)   
            right_doc = right_doc.lstrip('(')
            right_doc = right_doc.rstrip(')')
            right_doc = right_doc.split(",")
            # Get the enum from selected doctor for new test_record
            enum = right_doc[1].strip("'")
        else:
            # If there is only 1 doctor with that name, enum is easy to get.
            enum = doc_info[0]
            enum = enum[1]
    
    # If only pname was provided for patient information, check it exists.
    if (pname != ''):
        queryStr='SELECT name FROM patient WHERE name=\'{}\''.format(pname)
        cur.execute(queryStr)
        is_pname=cur.fetchone()
        if is_pname is None:
            return "Prescription creation failed. Patient name does not exist."
        # If there are multiple patients: Print all patient names found to gui, along with their some of their information.
        queryStr='SELECT name, health_care_no, phone FROM patient WHERE name=\'{}\''.format(pname)
        cur.execute(queryStr)
        patient_info=cur.fetchall()
        if len(patient_info) > 1:
            patient_list=[]
            for patient in patient_info:
                patient_list.append(patient)
            right_patient = eg.choicebox("Select the correct patient information:", "Patient Name Search Results", patient_list)
            right_patient = right_patient.lstrip('(')
            right_patient = right_patient.rstrip(')')
            right_patient = right_patient.split(",")
            # Get pnum from selected patient for new test_record
            pnum = right_patient[1].strip("'")
        else:
            # If there is only 1 patient with that name, pnum is easy to get.
            pnum = patient_info[0]
            pnum = pnum[1]
 
    # Get type_id based off tname. Also check type_id exists.
    queryStr='SELECT type_id FROM test_type WHERE test_name=\'{}\''.format(tname)
    cur.execute(queryStr)
    type_id = cur.fetchone()
    if type_id is None:
        return "Prescription creation failed. Test type does not exist."
    type_id = type_id[0]

    # Check prescription does not conflict with not_allowed.
    queryStr='SELECT health_care_no FROM not_allowed WHERE type_id={}'.format(type_id)
    cur.execute(queryStr)
    not_allowed = cur.fetchall()
    for patient_num in not_allowed:
        # Cast to ints for comparison
        patient_num = int(patient_num[0])
        temp_pnum = int(pnum)
        if (patient_num == temp_pnum):
            return "Prescription creation failed. Patient is not allowed to take this test."

    # Generate a new test_id incrementing up from the last
    # Assumes all inserts have followed test_id incrementing procedure
    test_id = cur.execute('SELECT COUNT(test_id) FROM test_record').fetchone()[0]+1
    # Create a new test record (date, result, lab are all null)
    pdate = time.strftime('%d/%m/%y')
    pdate = 'TO_DATE(\'{}\', \'dd/mm/yy\')'.format(pdate)
    
    insertStr='INSERT into TEST_RECORD (test_id,type_id,patient_no,employee_no,medical_lab,result,prescribe_date,test_date) values ({}, {}, {}, {}, {}, {}, {}, {})'.format(test_id, type_id, pnum, enum, 'NULL', 'NULL', pdate, 'NULL')
    cur.execute(insertStr)
    con.commit()

    # Inform user prescription successfully created
    return "Prescription Created"
    
def performTest(test_id, lname, tresult):
    """ 
    - Enter results after a medical test is completed. Lab name, test date and
      result can be updated.
    - Cannot update any test_record that does not exist (implies
      createPrescription was successful)
    - Only called when checkTest has run successfully (patient has valid
      prescription)
    """
    
    return "performTest not yet implemented"

def checkTest(pnum, tname, enum):
    """
    Checks if patient has a valid prescription, and whether the prescription
    has already been used. Returns (test_id, result).
    """
    # Get type_id
    queryStr='SELECT type_id FROM test_type WHERE test_name=\'{}\''.format(tname)
    cur.execute(queryStr)
    type_id = cur.fetchone()
    if type_id is None:
        eg.msgbox("Test type does not exist.", "Error!")
        return None
    type_id = type_id[0]

    queryStr = 'SELECT test_id, result FROM test_record WHERE patient_no={} AND type_id={} AND employee_no={}'.format(pnum, type_id, enum)
    cur.execute(queryStr)
    return cur.fetchone()

def performSearch(stype, pnum = None, enum = None, sdate = None, edate = None,
                  ttype = None):
    """
    Also unimplemented, performs one of three search types and returns
    the result.
    """
    return "performSearch not yet implemented"

def informationUpdate(pnum, name, address, birthday, phone):
    """
    Updates a patient record or creates if pnum does not
    exist. Returns status.
    """
    # Check if patient exists
    queryStr = 'SELECT health_care_no from patient where health_care_no={}'.format(pnum)
    cur.execute(queryStr)
    if cur.fetchone() is None:
        cont = eg.ccbox("Patient does not exist. Create with supplied information?")
        if cont == 0: return "Entry cancelled."
        insertStr = 'INSERT INTO patient (health_care_no, name, address, birth_day, phone) VALUES ({},\'{}\',\'{}\',to_date(\'{}\', \'mm/dd/yyyy\'),{})'.format(pnum, name, address, birthday, phone)
        cur.execute(insertStr)
        con.commit()
        return "Patient created successfully"
    else:
        cont = eg.ccbox("Patient already exists. Update information?")
        if cont == 0: return "Entry cancelled."
        updateStr = 'UPDATE patient SET name={}, address={}, birth_day=to_date(\'{}\', \'mm/dd/yyyy\'), phone={} WHERE health_care_no={}'.format(name, address, birthday, phone, pnum)
        cur.execute(updateStr)
        con.commit()
        return "Patient updated successfully"

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

# GUI input functions for the basic application processes.

def guiPrescription():
    """
    Interface for creating a new prescription.
    """
    msg = "Please enter the prescription information."
    title = "Prescription Info"
    fieldNames = ["Patient Healthcare #", "Patient Name", "Test Name", "Doctor Employee #", "Doctor Name"]
    fieldValues = []
    fieldValues = eg.multenterbox(msg, title, fieldNames)
    if fieldValues == None:
        eg.msgbox('Operation cancelled')
        return
    msg = createPrescription((fieldValues[0]), fieldValues[1], fieldValues[2], (fieldValues[3]), fieldValues[4])
    title = "Result"
    eg.msgbox(msg, title)

def guiTest():
    """
    Interface for performing a test.
    """
    msg = "Enter test information to confirm patient eligibility. Enter 1 as patient number to test successful patient eligibility."
    title = "Test Details"
    fieldNames = ["Patient Healthcare #", "Test Name", "Employee #"]
    fieldValues = []
    fieldValues = eg.multenterbox(msg, title, fieldNames)
    if fieldValues == None:
        eg.msgbox('Operation cancelled')
        return
    pnum, tname, enum = fieldValues
    valid_prescription = checkTest(int(pnum), tname, int(enum))
    if valid_prescription:
        test_id = valid_prescription[0]
        result = valid_prescription[1]
        if result:
            eg.msgbox("Prescription already used!", "Error!")
            return
        msg = "Patient eligibility confirmed. Enter test result."
        title = "Test Results"
        fieldNames = ["Lab Name", "Test Result"]
        fieldValues = []
        fieldValues = eg.multenterbox(msg, title, fieldNames)
        if fieldValues == None:
            eg.msgbox('Operation cancelled')
            return
        lname, tresult = fieldValues
        msg = performTest(test_id, lname, tresult)
        title = "Result"
        eg.msgbox(msg, title)
    else:
        eg.msgbox("Prescription info invalid. Please check all fields. ", "Error!")

def guiUpdateInformation():
    """
    Interface for updating or creating a patient.
    """
    msg = "Please enter the patient information. Note that empty boxes will also update, allowing you to delete patient information."
    title = "Patient Info"
    fieldNames = ["Patient Healthcare #", "Name", "Address",
                  "Birth Day (mm/dd/yyyy)", "Phone Number"]
    fieldValues = []
    fieldValues = eg.multenterbox(msg, title, fieldNames)
    if fieldValues == None:
            eg.msgbox('Operation cancelled')
            return
    pnum, name, address, birthday, phone = fieldValues
    try: pnum = int(pnum)
    except ValueError: pnum = 'NULL'
    try: phone = int(phone)
    except ValueError: phone = 'NULL'
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
        if fieldValues == None:
            eg.msgbox('Operation cancelled')
            return
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
        if fieldValues == None:
            eg.msgbox('Operation cancelled')
            return
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
        if fieldValues == None:
            eg.msgbox('Operation cancelled')
            return
        msg = performSearch(aa, ttype = fieldValues[0])
        title = "Result"
        eg.msgbox(msg, title)

#Login process (Could be made into function, but I forget how scoping)
not_connected = True
while not_connected:
    msg = "Please enter login credentials for the Oracle database."
    title = "Oracle DB login"
    fieldNames = ["Username", "Host", "Port", "SID",  "Password"]
    fieldValues = eg.multpasswordbox(msg, title, fieldNames)
    if fieldValues == None:
        msg = "Do you want to continue using ABHealthCare?"
        title = "Continue?"
        if eg.ccbox(msg, title, ('Continue', 'Exit')):     # show a Continue/Cancel dialog
            pass  # user chose Continue
        else:
            sys.exit(0)           # user chose Cancelimport curses
    else:
        a, b, c, d, e = fieldValues
        constring = '{}/{}@{}:{}/{}'.format(a, e, b, c, d)
        try:
            not_connected = False
            con = cx_Oracle.connect(constring)
        except cx_Oracle.DatabaseError:
            eg.msgbox("Error! Database credentials invalid!")
            not_connected = True
cur = con.cursor()

#Main program body
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
        con.close()
        sys.exit(0)           # user chose Cancelimport curses
