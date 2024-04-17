import json
import requests
from datetime import datetime
from flask import Flask
from pymongo import MongoClient


class ultraChatBot():
    def __init__(self, json):
        app = Flask(__name__)
        app.config['MONGO_URI'] = 'mongodb+srv://abineshjain:ILdXThPVkagMdNof@cars.xzjiizn.mongodb.net/'
        mongo = MongoClient(app.config['MONGO_URI'])
        self.db = mongo.get_database('ultrabot')
        self.json = json
        self.dict_messages = json['data']
        self.ultraAPIUrl = 'https://api.ultramsg.com/instance83729/'
        self.token = 'jupjgvdf8cokxh7p'

    def send_requests(self, type, data):
        url = f"{self.ultraAPIUrl}{type}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()

    def send_message(self, chatID, text):
        data = {"to": chatID,
                "body": text}
        answer = self.send_requests('messages/chat', data)
        return answer

    def send_image(self, chatID):
        data = {"to": chatID,
                "image": "https://file-example.s3-accelerate.amazonaws.com/images/test.jpeg"}
        answer = self.send_requests('messages/image', data)
        return answer

    def send_video(self, chatID):
        data = {"to": chatID,
                "video": "https://file-example.s3-accelerate.amazonaws.com/video/test.mp4"}
        answer = self.send_requests('messages/video', data)
        return answer

    def send_audio(self, chatID):
        data = {"to": chatID,
                "audio": "https://file-example.s3-accelerate.amazonaws.com/audio/2.mp3"}
        answer = self.send_requests('messages/audio', data)
        return answer

    def send_voice(self, chatID):
        data = {"to": chatID,
                "audio": "https://file-example.s3-accelerate.amazonaws.com/voice/oog_example.ogg"}
        answer = self.send_requests('messages/voice', data)
        return answer

    def send_contact(self, chatID):
        data = {"to": chatID,
                "contact": "14000000001@c.us"}
        answer = self.send_requests('messages/contact', data)
        return answer

    def time(self, chatID):
        t = datetime.datetime.now()
        time = t.strftime('%Y-%m-%d %H:%M:%S')
        return self.send_message(chatID, time)

    def welcome(self, chatID, noWelcome=False):
        welcome_string = ''
        if (noWelcome == False):
            welcome_string = "Hi , welcome to WhatsApp chatbot using Python\n"
        else:
            welcome_string = """wrong command
Please type one of these commands:
*hi* : Saluting
*time* : show server time
*image* : I will send you a picture
*video* : I will send you a Video
*audio* : I will send you a audio file
*voice* : I will send you a ppt audio recording
*contact* : I will send you a contact
"""
        return self.send_message(chatID, welcome_string)

    def send_booking_confirmation(self, chatID, pet, service, date, slot):
        # Logic to calculate price based on service, date, and slot
        price = self.calculate_price(service, date, slot)

        # Apply discounts based on conditions
        discount = self.calculate_discount(date)

        # Calculate final price after discount
        final_price = price - discount

        # Prepare message to send to customer
        message = f"Booking Confirmation:\nPet: {pet}\nService: {service}\nDate: {date}\nSlot: {slot}\nPrice: ${final_price:.2f}"

        # Send message to customer
        return self.send_message(chatID, message)

    def calculate_price(self, service, date, slot):
        # Logic to calculate base price based on service, date, and slot
        # You need to implement this based on your pricing structure
        # For example, you might have different prices for different services, dates, and slots
        # Return the calculated price
        pass

    def calculate_discount(self, date):
        # Logic to calculate discount based on the date
        # For example, you might offer discounts on Saturdays or premium on Mondays
        # Return the calculated discount
        pass

    def Processingـincomingـmessages(self):
        message = self.dict_messages
        chatID = message['from']
        if not message['fromMe']:
            text = message['body'].split()
            collection = self.db['customers']
            phone_numbers = [str(doc.get('phone', '')) +
                             '@c.us' for doc in collection.find()]
            phone = int(chatID.split("@")[0])
            # Query the pet collection from the database
            collection = self.db['customers']
            query = {"phone": phone}
            # Assuming each document in the collection has a "name" field
            pets = collection.find(query, {"pets": 1})
            # Construct the pet menu dynamically
            pet_menu = []
            for pet in pets:
                if 'pets' in pet:
                    for index, pet_details in enumerate(pet['pets'], start=1):
                        pet_menu.append(pet_details['name'].lower())
            print("pet_menu", pet_menu)
            if chatID not in phone_numbers:
                return self.send_message(chatID, 'User Not Found')
            if text[0].lower() == 'hi':
                # Send the initial message and start the interaction
                return self.send_welcome_message(chatID), self.send_pet_menu(chatID)
            elif text[0].lower() in pet_menu:
                # Ask user to select a service
                return self.send_service_menu(chatID)
            elif text[0].lower() in ['bathing', 'grooming', 'training']:
                # Ask user to select a date
                return self.send_date_menu(chatID)

            elif datetime.strptime(text[0].lower(), '%d/%m/%Y'):
                if datetime.strptime(text[0].lower(), '%d/%m/%Y') <= datetime.today():
                    return self.send_message(chatID, "Invalid date.")
                # Ask user to select a slot
                return self.send_slot_menu(chatID)
            elif text[0].lower() in ['bathing', 'grooming', 'training']:
                # Ask user to select a date
                return self.send_date_menu(chatID)
            elif text[0].lower() == 'confirm':
                # Confirm the booking and send confirmation message
                return self.send_booking_confirmation(chatID, self.selected_pet, self.selected_service, self.selected_date, self.selected_slot)
            else:
                # Invalid command
                return self.send_message(chatID, "Invalid command.")
        else:
            return 'NoCommand'

    def send_welcome_message(self, chatID):
        # Send welcome message with available commands
        welcome_message = "Hi, welcome to our pet booking service"
        return self.send_message(chatID, welcome_message)

    def send_pet_menu(self, chatID):
        phone = int(chatID.split("@")[0])
        # Query the pet collection from the database
        collection = self.db['customers']
        query = {"phone": phone}
        # Assuming each document in the collection has a "name" field
        pets = collection.find(query, {"pets": 1})
        # Construct the pet menu dynamically
        pet_menu = "Please select your pet:\n"
        for pet in pets:
            if 'pets' in pet:
                for index, pet_details in enumerate(pet['pets'], start=1):
                    pet_menu += f"{index}. {pet_details['name']}\n"

        # Send the menu to the user
        return self.send_message(chatID, pet_menu)

    def send_service_menu(self, chatID):
        # Logic to send menu for selecting service
        # You need to implement this based on your available services
        # Example:
        service_menu = """Please select the service:
                        1. Bathing
                        2. Grooming
                        3. Training"""
        return self.send_message(chatID, service_menu)

    def send_date_menu(self, chatID):
        # Logic to send menu for selecting date
        # You need to implement this based on your available dates
        # Example:
        date_menu = """Please Enter the Date in dd/mm/yyyy format"""
        return self.send_message(chatID, date_menu)

    def send_slot_menu(self, chatID):
        # Logic to send menu for selecting slot
        # You need to implement this based on your available slots
        # Example:
        slot_menu = """Please select the time slot:
                    1. 10:00 AM - 12:00 PM
                    2. 2:00 PM - 4:00 PM
                    3. 6:00 PM - 8:00 PM"""
        return self.send_message(chatID, slot_menu)
