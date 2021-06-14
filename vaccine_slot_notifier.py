from decouple import config
import tweepy
import time
import requests
from datetime import datetime, timedelta


def add_pincode(pincode, file_name):
    with open(file_name, "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        file_object.write(pincode)


def retrieve_pincodes(file_name):
    f_read = open(file_name, 'r')
    pincodes = list()
    for pincode in f_read:
        pincodes.append(pincode)
    return pincodes


def delete_pincode(pincode, file_name):
    f_read = open(file_name, "r")
    lines = f_read.readlines()
    f_read.close()

    new_file = open(file_name, "w")
    for line in lines:
        if line.strip("\n") != pincode:
            new_file.write(line)
    new_file.close()

def check_slots():
    pincodes = retrieve_pincodes("vaccine_pincodes.txt")
    print("Starting search for Covid vaccine slots!")
    date_now = datetime.today().date().strftime("%d-%m-%Y")

    for pincode in pincodes:
        print(pincode)
        counter = 0
        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}".format(
            pincode, date_now)

        result = requests.get(url)
        if result.ok:
            response_json = result.json()
            for session in response_json["sessions"]:
                if session["available_capacity"] > 0:
                    print('Pincode: ' + pincode)
                    print("Available on: {}".format(date_now))
                    print(session["name"])
                    print("Min Age: ", session["min_age_limit"])
                    print(session["block_name"])
                    print("Price: ", session["fee_type"])
                    print("Availablity : ", session["available_capacity"])
                    if session["vaccine"] != '':
                        print("Vaccine type: ", session["vaccine"])
                    print("\n")
                    counter = counter + 1
            if counter == 0:
                print("No Vaccination slot available at ", pincode)
        else:
            print("No Response!")


while True:
    check_slots()
    time.sleep(10)
