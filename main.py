import os

input_directory="/Users/akarshansrivastava/Documents/Email_extarctor/input"
output_directory="/Users/akarshansrivastava/Documents/Email_extarctor/output/"


directory = input_directory

for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path) and filename.lower().endswith(".eml"):
        pass
    else:
        try:
            os.remove(file_path)
        except:
            pass

directory=output_directory
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
        except:
            pass

from script.gemini_extarction import gemini_extraction


System_Message="""System: You are a cab booking agent's assistant, who needs to extract all the required information/fields, asked by a user, from a booking request email. Create 'individual bookings' if mentioned in a mail and provide respective all booking's fields information, mentioned in that mail if multiple bookings."""
User_Requirements="""User: I need these below information from the booking request mail given below. Your output should have only information mentioned in mail given below without adding any additional information from your end.

1. Account Name/ Company Name/Entity Name
2. User/Traveler First Name
3. User/Traveler Last Name
4. Must Predict User/Traveler's Gender based on his/her First and Last name just tell Male/Female
5. Traveler/ User Email id/s (provide comma "," separated values in case of multiple email ids mentioned)
6. Traveler/User Mobile number/s (provide comma "," separated values in case of multiple mobile numbers mentioned)
7. Billing type/Entity/information/Recoverable type or Any Payment method mentioned like credit card, card name etc.
8. Cab Pickup/Start/ Required/Reporting Location
9. Drop/Destination Location
10. Tell me whether the booking request is for City Local, Outstation or Airport transfer (if pickup or drop location is any Airport)
11. Booking/Start/Pickup date (mention only the first date if multiple dates are mentioned and keep it in IST format, DD/mmm/YY)
12. Booking/Start/Pickup time (keep IST format)
13. Booking End date/ Cab required End date /Last mentioned Booking date/Last Mentioned Pickup date/ last mentioned cab required date in the request mail (keep IST format, DD/mmm/yy)
14. Requested car type or category (give car name/ type/Cab brand a preference if car category and car brand both are mentioned)
15. Continuous Booking Yes/No, select "Yes" if multiple Booking start dates/pickup dates/cab required dates mentioned in the respective booking but only one pickup location is mentioned, else select "No"
16. Mention on/at Disposal (Yes or No)
17. Flight Number
18. Arrival/Departure? “Arrival” if Traveler/User is taking cab from the airport else “Departure” if Traveler/User’s drop location is Airport
20. All Special Instructions/Note if mentioned
21. Mention all the dates, between the first mentioned date and last mentioned date, which are in the booking mail, including start and end dates ( only if continuous booking is yes)
22. Number of days cab is required for if mentioned

Booking email: """

User_Input=""""""

output=gemini_extraction(input_directory,output_directory,System_Message,User_Requirements,User_Input,temperature=0.20,top_p=.90)
print(output)

