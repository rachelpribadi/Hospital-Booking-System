#Assignment 2 -- (Group project)
#Group member : Jordy Awangsaputra, Rachel Roselynn Pribadi, Brandon Wong Baldwin

from abc import ABC, abstractmethod

class BookingSystem:
    '''
    Class: Booking System
    Purpose: This booking system is the main controller for the entire clinic system.
    Student Name: Rachel Roselynn Pribadi, Jordy Awangsaputra, Brandon Wong Baldwin
    Student ID: 36677183, 35999225, 36680559

    Attributes:
    - staff_list (lst): This list contains all of the MedicalStaff Objects
    - client_list (lst): This list contains all of the Client objects
    - appointments_list (lst): This list contains all of the Appointment objects
    '''

    def __init__(self):
        '''
        This initialises an empty booking system.
        Input: None
        Output: None
        '''
        self.staff_list = [] 
        self.client_list = [] 
        self.appointments_list = []  

    def find_staff(self, name: str):  
        '''
        Finds staff by their name.
        Input: name(str) = Name of the staff member.
        Output: Staff object, None if not found.
        '''
        for staff in self.staff_list:
            if staff.staff_name == name:
                return staff
        return None


    def find_available_staff(self, role, date):
        '''
        Find an available staff by role on a given date
        Input: role(str) = The role of the staff (GP, Nurse, Psychologist)
               date(str) = The date of the appointment (YYYY-MM-DD)
        Output: Staff object available, None if not found
        '''
        candidates = []
        for s in self.staff_list:
            if s.role == role and not s.check_max(date):
                candidates.append(s)

        if not candidates:   # none available
            return None

        chosen = candidates[0]
        for s in candidates:
            if len(s.booking_list) < len(chosen.booking_list):
                chosen = s
        return chosen

    def find_client(self, name, number):
        '''
        Find client by name and contact number match with client list
        Input: name(str) = Client name
               number(str) = Client contact number
        Output: Matching client object, None if not found
        '''
        for i in self.client_list:
            if i.client_name == name and i.contact_number == number:
                return i
        return None
    
    #Managing of staffs
    def add_staff (self):
        '''
        Add a staff to the staff list.
        Input: None
        Output: None
        '''
        while True:
            name = input("Enter staff name: ").strip()
            if not name:   # blank
                print("You cannot leave this empty")
            elif name.isdigit():   # concept has not been taught in class, learned it from https://www.w3schools.com/python/ref_string_isdigit.asp and is used to check if all characters are digits.
                print("A name cannot be only numbers")
            else:
                break

            

        while True:
            role = input("Enter role (GP/Nurse/Psychologist): ").strip().lower()
            if role == "gp":
                staff = GP(name)
                break
            elif role == "nurse":
                staff = Nurse(name)
                break
            elif role == "psychologist":
                staff = Psychologist(name)
                break
            else:
                print("Invalid role, try again.")


        self.staff_list.append(staff)
        print("Staff member added")
    
    def edit_staff (self):
        '''
        Edits the current details of the staff.
        Input: None
        Output: None
        '''
        
        if not self.staff_list:
            print("No staff available yet")
            return
        print('List of staff: ')
        self.display_staff()
        name = input("Enter name of the staff you want to edit: ").strip()
        edit_staff = self.find_staff(name)
        if not edit_staff:
            print('Staff is not found')
            return
        new_name = input("Enter new name, but just press enter to leave it unchanged: ").strip()
        if not new_name:
            new_name = name
        edit_staff.set_name(new_name)
        new_role = input(f"Enter new role (GP/Nurse/Psychologist), but just press enter to leave it unchanged: ").strip().lower()
        if not new_role:  
            print(f"There are no changes on the role of {new_name}")  
            return
        
        staff_appt = edit_staff.booking_list[:]

        if new_role == "gp":
            new_staff = GP(new_name)
            print(f"{new_name}'s role is now a GP")
        elif new_role == "nurse":
            new_staff = Nurse(new_name)
            print(f"{new_name}'s role is now a Nurse")
        elif new_role == "psychologist":
            new_staff = Psychologist(new_name)
            print(f"{new_name}'s role is now a Psychologist")
        else:
            print("Invalid role. No changes have been made.")
            return

        self.staff_list.remove(edit_staff)
        new_staff.booking_list = staff_appt
        for appt in new_staff.booking_list:
            appt.assigned_staff = new_staff
        self.staff_list.append(new_staff)

    def delete_staff (self):
        '''
        Delete a staff member.
        Input: None
        Output: None
        '''
        if not self.staff_list:
            print("No staff available yet")
            return
        print("List of staffs available: ")
        self.display_staff()
        name = input("Enter staff name to be removed: ")
        deleteStaff = self.find_staff(name)
        if not deleteStaff:
            print("Staff not found")
            return
        if deleteStaff.booking_list:
            print("Staff cannot be deleted as he/she got an appointment")
            return
        self.staff_list.remove(deleteStaff)
        print(name + " has been deleted ")

    
    def display_staff (self):
        '''
        Display all the staff list grouped by role.
        Input: None
        Output: None
        '''
        if not self.staff_list:
            print("No staff available yet")
            return
        print('Staff list: ')
        roles = ["GP", "Nurse", "Psychologist"]
        for role in roles:
            print("===" + role.capitalize() + "===")
            available = False
            for i in self.staff_list:
                if i.role == role.lower():
                    name = i.staff_name
                    appointment = len(i.booking_list)
                    print(f"Name: {name}, Number of Appointments: {appointment}")
                    available = True
                    print()
            if available == False:
                print("No " + role + " available yet")
                print("")

    #Managing of appointments
    def add_appointment(self):
        '''
        This adds an appointment to the appointment list
        Input: None
        Output: None
        '''
        print("---- Book an Appointment ----")
        if len(self.staff_list) == 0:
            print("No staff available.")
            return

        while True:
            name = input("Enter client name: ").strip()
            if not name:   
                print("You cannot leave this empty")
            elif name.isdigit():   
                print("A name cannot be only numbers")
            else:
                break

        while True:
            number = input("Enter contact number: ").strip()
            if not number:
                print("You cannot leave this empty")
            elif not number.isdigit():
                print("Contact number must only be numbers")
            else:
                break

        client = self.find_client(name, number)
        if not client:
            client = Client(name, number)
            self.client_list.append(client)

        while True:
            appt_type = input("Enter appointment type (GP/Nurse/Psychologist): ").strip().lower()
            if appt_type in ["gp", "nurse", "psychologist"]:
                break  
            print("Invalid appointment type, choose either GP, Nurse, or Psychologist")


        # to input and check validity of date
        while True:
            date = input("Enter appointment date (2025-MM-DD): ").strip()
            if len(date) == 10 and date[4] == "-" and date[7] == "-":
                y, m , d = date.split("-")
                if y == "2025" and m.isdigit() and d.isdigit():
                    m = int(m)
                    d = int(d)
                    if 1 <= int(m) <= 12 and 1 <= int(d) <= 31 and y == "2025":
                        break
            print("Invalid date, try again")

        # to input and check validity of the time
        while True:
            time = input("Enter appointment time (HH:MM): ").strip()
            if len(time) == 5 and time[2] == ":":
                hour, minute = time.split(":")
                if hour.isdigit() and minute.isdigit():
                    if len(hour) == 2 and len(minute) == 2:
                        hour = int(hour)
                        minute = int(minute)
                        if 0 <= hour <= 23 and 0 <= minute <= 59:
                            break
            print("Invalid time, try again")
            

        if appt_type.lower() == "gp":
            while True:
                reason = input("Reason for visit: ")
                if reason == "":
                    print("You cannot leave this empty")
                elif reason.isdigit():
                    print ("Reason cannot only be numbers")
                else: 
                    break
            while True:
                consult = input("Enter consultation type (Telehealth/Standard/Long): ").strip().lower()
                if consult in ["telehealth", "standard", "long"]:
                    break
                print("Invalid type of consultation, try again.")
            appt = GPAppointment(client, date, time, reason, consult)

        elif appt_type.lower() == "nurse":
            while True: 
                vaccine = input("Vaccine name: ")
                if vaccine == "":
                    print ("You cannot leave this empty")
                elif vaccine.isdigit():
                    print ("Vaccine cannot only be numbers")
                else: 
                    break
            appt = NurseAppointment(client, date, time, vaccine)

        elif appt_type.lower() == "psychologist":
            while True: 
                session = input("Session length (30/60): ").strip()
                if session == "":
                    print ("You cannot leave this empty")  
                elif session != "30" and session != "60":
                    print ("Session length can only be 30 or 60 minutes, answer (30/60)")
                else:
                    break                  
            appt = PsychologistAppointment(client, date, time, session)

        chosen = self.find_available_staff(appt_type, date)
        if not chosen:
            print(f"No {appt_type.capitalize()} are available on {date}")
            return

        # This checks if the staff already has appointment at the same date & time
        for current in chosen.booking_list:
            if current.appointment_time == time and current.appointment_date == date:
                print(f"{chosen.staff_name} already has an appointment at {date} {time}.")
                return


        chosen.add_appointment(appt)        #staffs 
        appt.assigned_staff = chosen       
        self.appointments_list.append(appt) #system
        client.booking_list.append(appt)    #client

        print(f"Appointment with {chosen.staff_name} ({chosen.role.lower()}) has been booked.")

        self.save_to_txt(display_message = False) #so that it autosaves to the text file and does not print any messages

    def edit_appointment(self):
        '''
        Edits the current appointment details in the list.
        Input: None
        None: None
        '''
        print("---- Edit Appointment ----")
        if len(self.appointments_list) == 0:
            print("No appointments to edit.")
            return

        name = input("Enter name registered for the appointment: ").strip()
        found = False
        for appt in self.appointments_list:
            if appt.client.get_name() == name:
                found = True

                while True:
                    new_type = input(f"Enter new appointment type (GP/Nurse/Psychologist), press enter to keep it as ({appt.appointment_type}): ").strip().lower()
                    if new_type == "":
                        new_type = appt.appointment_type.lower()
                        break
                    if new_type in ["gp", "nurse", "psychologist"]:
                        break
                    print("Invalid appointment type, try again.")

                while True:
                    new_date = input(f"Enter new date (YYYY-MM-DD), press enter to keep it as ({appt.appointment_date}): ")
                    if new_date == "":
                        new_date = appt.appointment_date
                        break
                    if len(new_date) == 10 and new_date[4] == "-" and new_date[7] == "-":
                        y, m, d = new_date.split("-")
                        if y == "2025" and m.isdigit() and d.isdigit():
                            if len(m) == 2 and len(d) == 2 and len(y) == 4:
                                m = int(m)
                                d = int(d)
                                if 1 <= m <= 12 and 1 <= d <= 31 and y == "2025":
                                    break
                    print("Invalid date, try again")

                while True:
                    new_time = input(f"Enter new time (use 24 hour format HH:MM) or press enter to keep it as ({appt.appointment_time}): ")
                    if not new_time:
                        new_time = appt.appointment_time
                        break
                    if len(new_time) == 5 and new_time[2] == ":":
                        hour, minute = new_time.split(":")
                        if hour.isdigit() and minute.isdigit():
                            if len(hour) == 2 and len(minute) == 2:
                                hour = int(hour)
                                minute = int(minute)
                                if 0 <= hour <= 23 and 0 <= minute <= 59:
                                    break
                    print("Invalid time, try again")
                

                # This is IF SAME APPOINTMENT TYPE 
                if new_type == appt.appointment_type.lower():
                    if new_type == "gp":
                        new_reason = input(f"Enter a new reason (press enter to keep it as '{appt.reason_for_visit}'): ")
                        if new_reason != "":
                            appt.reason_for_visit = new_reason
                        while True:
                            new_consult = input(f"Enter new consultation type (Telehealth/Standard/Long) or press Enter to keep ({appt.consultation_type}): ").strip().lower() 
                            if new_consult == "":
                                break
                            elif new_consult in ["telehealth", "standard", "long"]:
                                appt.consultation_type = new_consult
                                break
                            print("Invalid, choose either TeleHealth, Standard or Long. Try again.")                    
                    
                    elif new_type == "nurse":
                        while True:
                            vaccine = input(f"Enter new vaccine name (press enter to keep it as '{appt.vaccine_name}'): ") 
                            if vaccine == "":
                                break
                            elif vaccine.isdigit():
                                print ("Vaccine cannot only be numbers")
                            else: 
                                appt.vaccine_name = vaccine
                                break

                    elif new_type == "psychologist":
                        while True: 
                            session = input(f"Enter new session length (30/60) (press Enter to keep it as '{appt.session_length}': ").strip()
                            if session == "":
                                break
                            elif session != "30" and session != "60":
                                print ("Session length can only be 30 or 60 minutes, answer (30/60)")
                            else:
                                appt.session_length = session
                                break  
                        
                    appt.set_appt_date(new_date)
                    appt.set_appt_time(new_time)
                    print ("Appointment has been updated")

                    self.save_to_txt(display_message = False) #so that it autosaves to the text file and does not print any messages
                    return

                # If appointment type is changed, have to recreate the appointment
                if appt in self.appointments_list:
                    self.appointments_list.remove(appt)

                if appt in appt.assigned_staff.booking_list:
                    appt.assigned_staff.remove_appointment(appt)

                if appt in appt.client.booking_list:
                    appt.client.booking_list.remove(appt)

                if new_type == "gp":
                    while True:
                        reason = input("Reason for visit: ")
                        if reason == "":
                            print("You cannot leave this empty")
                        elif reason.isdigit():
                            print ("Reason cannot only be numbers")
                        else: 
                            break
                    while True:
                        consult = input("Enter consultation type (Telehealth/Standard/Long): ").strip().lower()
                        if consult in ["telehealth", "standard", "long"]:
                            break
                        print("Invalid type of consultation, try again.")
                    new_appt = GPAppointment(appt.client, new_date, new_time, reason, consult)
                    staff = self.find_available_staff("gp", new_date)

                elif new_type == "nurse":
                    while True: 
                        vaccine = input("Vaccine name: ")
                        if vaccine == "":
                            print ("You cannot leave this empty")
                        elif vaccine.isdigit():
                            print ("Vaccine cannot only be numbers")
                        else: 
                            break
                    new_appt = NurseAppointment(appt.client, new_date, new_time, vaccine)
                    staff = self.find_available_staff("nurse", new_date)

                elif new_type == "psychologist":
                    while True: 
                        session = input("Session length (30/60): ").strip()
                        if session == "":
                            print ("You cannot leave this empty")  
                        elif session != "30" and session != "60":
                            print ("Session length can only be 30 or 60 minutes, answer (30/60)")
                        else:
                            break 
                    new_appt = PsychologistAppointment(appt.client, new_date, new_time, session)
                    staff = self.find_available_staff("psychologist", new_date)

                else:
                    print("Invalid appointment type, no changes are made.")
                    self.appointments_list.append(appt)
                    appt.assigned_staff.add_appointment(appt)
                    return

                if staff:
                    new_appt.assigned_staff = staff
                    staff.add_appointment(new_appt)
                    self.appointments_list.append(new_appt)
                    new_appt.client.booking_list.append(new_appt)
                    print("Appointment updated successfully.")
                    self.save_to_txt(display_message = False) 
                    
                else:
                    print(f"No available staff for {new_type}. Reverting to original.")
                    self.appointments_list.append(appt)
                    appt.assigned_staff.add_appointment(appt)
                    self.save_to_txt(display_message = False) 

        if not found:
            print("No appointments were found for this client")

    def delete_appointment(self):
        '''
        Cancel an appointment.
        Input: None
        Output: None
        '''
        print("---- Cancel Appointment ----")
        name = input("Enter client name to cancel appointment: ")

        for appt in self.appointments_list:
            if appt.client.get_name() == name:
                # This one removes appointment from the staff's booking list
                appt.assigned_staff.remove_appointment(appt)

                # This one removes appointment from appointments list 
                self.appointments_list.remove(appt)

                # This one removes appointment from bookings lsit
                appt.client.booking_list.remove(appt)
                print("Appointment is canceled.")
                self.save_to_txt(display_message = False)  
                return
        print("Appointment was not found.")

    def load_from_txt(self, filename="appointment.txt"):
        '''
        This loads the text file.
        Input: filename (str): Name of the file
        Output: The contents if file exists
        '''
        try:
            with open(filename, "r") as file:
                data = file.readlines() 
                self.loaded_data = []

                for line in data:
                    cleaned_line = line.strip()   
                    if cleaned_line:              
                        self.loaded_data.append(cleaned_line)
        except FileNotFoundError:
            self.loaded_data = []


    def save_to_txt (self, display_message = True):
        '''
        This saves the staff and appointment details into a text file
        Input: None
        Output: Print confirmation if True, otherwise None
        '''
        try:
            with open ("appointment.txt", "w") as file:
                for staff in self.staff_list:  #loops through each staff in staff list
                    file.write(f"{staff.get_name().title()} {staff.get_role().upper()} Appointment:\n")
                    if staff.booking_list:  #this checks if the staff has any bookings
                        for appt in staff.booking_list:
                            if appt.appointment_type.lower() == "gp":
                                file.write(f"{appt.client.get_name().capitalize()}, {appt.client.get_contact()}, {appt.consultation_type}, {appt.reason_for_visit}\n")
                            elif appt.appointment_type.lower() == "nurse":
                                file.write(f"{appt.client.get_name().capitalize()}, {appt.client.get_contact()}, Vaccination, {appt.vaccine_name}\n")
                            elif appt.appointment_type.lower() == "psychologist":
                                file.write(f"{appt.client.get_name().capitalize()}, {appt.client.get_contact()}, Counselling, {appt.session_length} mins \n")
                    else:  #if staff has no bookings it will print that it has no appointments
                        file.write(" No appointments yet \n")
                    file.write("\n")  
            if display_message: # prints only if display_message is true
                print ("Appointments have been written to file")

        except Exception as e:
            print ("There was an error in saving the details into the file.", e)

    def run(self):
        '''
        Run the main menu.
        Input: None
        Output: None
        '''
        running = True
        while running:
            print('---- BeeHealthy Clinic System ----')
            print('1. Staff Menu')
            print('2. Client Menu')
            print('3. Exit')
            choice = input('Select your role: ')
            if choice == "1":
                self.staff_menu()
            elif choice == "2":
                self.client_menu()
            elif choice == "3":
                confirm = input("Are you sure you want to exit? (Y/N): ").strip().lower()
                if confirm == "y":
                    print('Thankyou')
                    running = False
            else:
                print('========== Please pick 1-3==========')


    def staff_menu(self):
        '''
        Displays the staff menu options.
        Input: None
        Output: None
        '''
        keep_staff_menu = True
        while keep_staff_menu:
            print('---- Staff Menu ----')
            print('1. Add a new staff')
            print('2. Edit the details of an existing staff')
            print('3. Display available staff')
            print('4. Delete a staff')
            print('5. Save details in a text file')
            print('6. Return to the main menu')
            choice_staff = input('Please Enter Your Choice: ')
            if choice_staff == "1":
                self.add_staff()
            elif choice_staff == "2":
                self.edit_staff()
            elif choice_staff == "3":
                self.display_staff()
            elif choice_staff == "4":
                self.delete_staff()
            elif choice_staff == "5":
                self.save_to_txt()
            elif choice_staff == "6":
                keep_staff_menu = False
            else:
                print('========== Please pick 1-6 ==========')


    def client_menu(self):
        '''
        Displays the client menu options.
        Input: None
        Output: None
        '''
        keep_client_menu = True
        while keep_client_menu:
            print('---- Client Menu ----')
            print('1. Book an appointment')
            print('2. Cancel an appointment')
            print('3. Edit an appointment')
            print('4. Return to the main menu')
            choice_client = input('Please Enter Your Choice: ')
            if choice_client == "1":
                self.add_appointment()
            elif choice_client == "2":
                self.delete_appointment()
            elif choice_client == "3":
                self.edit_appointment()
            elif choice_client == "4":
                keep_client_menu = False
            else:
                print('========== Please pick 1-4 =========')


class Client:
    '''
    Class Name: Client
    Purpose: This class represents a client inside the booking system with name and contact number.
    Student Name: Rachel Roselynn Pribadi, Jordy Awangsaputra, Brandon Wong Baldwin
    Student ID: 36677183, 35999225, 36680559

    Attributes of Client Class:
    - client_name: holds the name of the client
    - contact_number: holds the client's contact number
    '''
    def __init__(self, client_name: str, contact_number: str):
        '''
        This initialises a new object, which is Client.
        Input:  client_name (str): The client's name
                contact_number (str): The contact number of the client
                booking_list (lst): Client's booking list
        Output: None
        '''
        self.client_name = client_name
        self.contact_number = contact_number
        self.booking_list = [] 

    def get_name (self):
        '''
        Returns the name of the client
        Input: None
        Output: Name of the client
        '''
        return self.client_name
    
    def set_name (self, name: str):
        '''
        Sets a new name for the client
        Input: name (str) = the of the client
        Output: None
        '''
        self.client_name = name

    def get_contact (self):
        '''
        This returns the contact of the client
        Input: None
        Output: Contact number (str) of the client
        '''
        return self.contact_number
    
    def set_contact (self, number: str):
        '''
        This sets the new contact number of a client
        Input: number (str) = a client's contact number
        Output: None
        '''
        self.contact_number = number

    def __str__(self):
        '''
        Returns the string that show the details of the client
        Input: None
        Output: String containing name and contact
        '''
        return f"Client: {self.client_name}, Contact: {self.contact_number}"


class MedicalStaff (ABC):
    """
    Class Name: MedicalStaff
    Purpose: This class will represent MedicalStaff inside the booking system
    Student Name: Rachel Roselynn Pribadi, Jordy Awangsaputra, Brandon Wong Baldwin
    Student ID: 36677183, 35999225, 36680559

    Attributes of MedicalStaff Class:
    - staff_name: holds the name of the staff
    - role: holds the staff's job description
    - booking_list: the list of staff members appointment
    """
    def __init__(self,staff_name,role,max_appointment):
        '''
        Initializes the MedicalStaff object

        Input:  staff_name (str): The staff's name
                role (str): The staff's job description
                booking_list (lst): The staff's booking list
                max_appointment (int): The staff's max appointment
        Output: None
        '''
        self.staff_name = staff_name
        self.role = role.lower()
        self.booking_list = []
        self.max_appointment = max_appointment
    
    def get_name(self):
        '''
        Returns the name of the staff
        Input: None
        Output: The staff member's name (str)
        '''
        return self.staff_name

    def set_name(self, name: str):
        '''
        Sets a new name of staff

        Input: New name for the staff (str)
        Output: None
        '''
        self.staff_name = name

    def get_role(self):
        '''
        Return the job of the staff
        Input: None
        Output: The staff member's role
        '''
        return self.role

    def set_role(self, role: str):
        '''
        Sets the job of the staff
        Input: The staff member's role
        Output: None
        '''
        self.role = role.lower()
    def add_appointment(self, appt: str):
        '''
        This adds an appointment to the booking list
        Input: appt = the appointment object
        Output: None
        '''
        return self.booking_list.append(appt)

    def remove_appointment(self, appt: str):
        '''
        This removes an appointment from the booking list
        Input: appt = The appointment object
        Output: None
        '''
        if appt in self.booking_list:
            self.booking_list.remove(appt)

    @abstractmethod
    def check_max(self, date:str):
        '''
        Check if staff is fully booked for the date.
        Input: date (str) = date of the appointment that wanted to be booked
        Output: True or False
        '''
        pass

    def __str__(self):
        '''
        This returns tne string representation of the staff details
        Input: None
        Output: str: A string containing the staff details
        '''
        return f"Name: {self.staff_name}, Role: {self.role.capitalize()}, Number of appointments: {len(self.booking_list)}"


class GP(MedicalStaff):
    '''
    Represent a General Practitioner staff member with a maximum appointment of 5 on each day.
    '''
    def __init__(self,staff_name):
        '''
        Initialize a GP staff member
        Inputs: staff_name (str) = The staff with GP role name
        Outputs: None
        '''
        super().__init__(staff_name,"GP",5)

    
    def check_max(self, date: str):
        '''
        Check if staff is fully booked for the date.
        Input: date (str) = date of the appointment that wanted to be booked
        Output: True or False
        '''
        count = 0
        for appt in self.booking_list:
            if appt.appointment_date == date:
                count += 1
        return count >= self.max_appointment


class Nurse(MedicalStaff):
    '''
    Represent a Nurse staff member with a maximum appointment of 5 on each day.
    '''
    def __init__(self,staff_name):
        '''
        Initialize a nurse staff member
        Inputs: staff_name (str) = The staff with nurse role name
        Outputs: None
        '''
        super().__init__(staff_name,"Nurse",6)

    def check_max (self,date: str):
        '''
        Check if staff is fully booked for the date.
        Input: date (str) = date of the appointment that wanted to be booked
        Output: True or False
        '''
        count = 0
        for appt in self.booking_list:
            if appt.appointment_date == date:
                count += 1
        return count >= self.max_appointment

class Psychologist(MedicalStaff):
    '''
    Represent a Psychologist staff member with a maximum appointment of 5 on each day.
    '''

    def __init__(self,staff_name):
        '''
        Initialize a psychologist staff member
        Inputs: staff_name (str) = The staff with psychologist role name
        Outputs: None
        '''
        super().__init__(staff_name,"Psychologist",3)

    def check_max (self, date: str):
        '''
        Check if staff is fully booked for the date.
        Input: date (str) = date of the appointment that wanted to be booked
        Output: True or False
        '''
        count = 0
        for appt in self.booking_list:
            if appt.appointment_date == date:
                count += 1
        return count >= self.max_appointment

class Appointment (ABC):
    '''
    Class Name: MedicalStaff
    Purpose: This class represent a generic appointment in the booking system
    Student Name: Rachel Roselynn Pribadi, Jordy Awangsaputra, Brandon Wong Baldwin
    Student ID: 36677183, 35999225, 36680559

    Attributes of Appointment Class:
    - client (Client): The client for this appointment.
    - appointment_type (str): Type of appointment (GP/Nurse/Psychologist)
    - appointment_date (str): Date of appointment (YYYY-MM-DD)
    - appointment_time (str): Time of appointment (HH:MM)
    '''
    def __init__ (self, client: "Client", appointment_type: str, appointment_date: str, appointment_time: str):
        '''
        This initialises a new object, Appointment.
        Input:  client (Client): a client object that contains name and contact number
                appointment_type (str): The type of appointment
                appointment_date (str): The date of appointment
                appointment_time (str): The time of appointment
        Output: None
        '''
        self.client = client
        self.appointment_type = appointment_type
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time


    def get_client(self):
        '''
        Return the client object
        Input: None
        Output: client
        '''
        return self.client
    

    def get_appt_type (self):
        '''
        Return the appointment type of the client
        Input: None
        Output: appointment type of the the client (str)
        '''
        return self.appointment_type


    def get_appt_date (self):
        '''
        Return the date of appointment of the client
        Input: None
        Output: appointment date of the client (str)
        '''
        return self.appointment_date

    def set_appt_date (self, appt_date: str):
        '''
        Set the date of appointment of the client
        Input: Appointment date of the client (str)
        Output: None
        '''
        self.appointment_date = appt_date

    def get_appt_time(self):
        '''
        Return the appointment time of the client
        Input: None
        Output: appointment time of the client (str)
        '''

        return self.appointment_time

    def set_appt_time (self, appt_time: str):
        '''
        Set the appointment time of the client
        Input: appointment time of client (str)
        Output: None
        '''
        self.appointment_time = appt_time
    
    @abstractmethod

    def __str__ (self):
        '''
        Return a string that represent the appointment
        Input: None
        Output: string containing the appointment details
        '''
        pass


class GPAppointment(Appointment):
    '''
    Appointment specialized for GP consultations.
    '''

    def __init__(self, client: "Client",
                 appointment_date: str, appointment_time: str,
                 reason_for_visit: str, consultation_type: str):
        '''
        Initialize a GP appointment.

        Input: client (Client): a client object that contains name and contact number
               appointment_date (str): Date of appointment.
               appointment_time (str): Time of appointment.
               reason_for_visit (str): Reason for GP visit.
               consultation_type (str): Consultation mode/type.
        Output: None
        '''
        super().__init__(client, "GP", appointment_date, appointment_time)
        self.reason_for_visit = reason_for_visit
        self.consultation_type = consultation_type
        self.assigned_staff = None

    def __str__(self):
        '''
        Return a human-readable string of the GP appointment details.
        Input: None
        Output: Formatted summary including reason and consultation type. (str)
        '''
        return (self.client.get_name() + ", " + self.client.get_contact() + ", " +
                self.consultation_type + ", " + self.reason_for_visit)
        

class NurseAppointment(Appointment):
    '''
    Appointment specialized for Nurse services
    '''

    def __init__(self, client: "Client",
                 appointment_date: str, appointment_time: str,
                 vaccine_name: str):
        '''
        Initialize a Nurse appointment.

        Input: client (Client): a client object that contains name and contact number
                appointment_date (str): Date of appointment.
                appointment_time (str): Time of appointment.
                vaccine_name (str): Vaccine name.
        Output: None
        '''
        super().__init__(client, "Nurse", appointment_date, appointment_time)
        self.vaccine_name = vaccine_name
        self.assigned_staff = None

    def __str__(self):
        '''
        Return a human-readable string of the Nurse appointment details.
        Inputs: None
        Output: Formatted summary including vaccine name. (str)
        '''
        return (self.client.get_name() + ", " + self.client.get_contact() +
                ", Vaccination, " + self.vaccine_name)


class PsychologistAppointment(Appointment):
    '''
    Appointment specialized for Psychologist sessions.

    Additional Attributes: session_length (str) = Duration of the session in minutes.
    '''

    def __init__(self, client: Client,
                 appointment_date: str, appointment_time: str,
                 session_length: str):
        '''
        Initialize a Psychologist appointment.
        Input: client (Client): a client object that contains name and contact number
               appointment_date (str): Date of appointment.
               appointment_time (str): Time of appointment.
               session_length (int): Session duration in minutes.
        Output: None
        '''
        super().__init__(client, "Psychologist", appointment_date, appointment_time)
        self.session_length = session_length
        self.assigned_staff = None

    def __str__(self):
        '''
        Return a human-readable string of the Psychologist appointment details.
        Input: None
        Output: Formatted summary including session length. (str)
        '''
        return (self.client.get_name() + ", " + self.client.get_contact() +
                ", Counselling, " + str(self.session_length) + " mins")

def main():
    '''
    The main that starts BeeHealthy Clinic Booking System.
    '''
    system = BookingSystem()
    system.load_from_txt()
    system.run()

main()


