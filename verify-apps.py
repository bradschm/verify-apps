#!/usr/bin/python

import requests # You will need to install requests
import getpass
# Authored by Brad Schmidt on 2017-07-19
'''Determine how many apps are on each device based on a search entered
After a search is completed, app counts are displayed. 
An opportunity to send an Update Inventory command is presented.
If all devices have the same amount of apps, an option to Shutdown devices will be presented.
'''

# Usage: python <thisscript.py>
# Python version note: raw_input is used for Python 2, switch to input for Python 3

jss_username = raw_input("Please enter your JSS username: ")
jss_password = getpass.getpass("Please enter your JSS password: ")

jss_url = 'https://potato.local:8443'

print("")

while True:
    match = raw_input("Search term (username, serialnumber, device name, etc)\n \
    	Note use * as wildcard: ")
    
    print("-" * 50)
    print("Searching for: %s" % match)


    mobile_devices_request = requests.get(jss_url + '/JSSResource/mobiledevices/match/%s' % match,
                            auth=(jss_username,jss_password),
                            headers={'Accept': 'application/json'}
                            )

    print("Search term: %s" % match)
    print("Found %s mobile devices" % len(mobile_devices_request.json()['mobile_devices']))
    
    raw_input("--Press enter to see results--")

    mobile_devices = mobile_devices_request.json()['mobile_devices']
    
    device_ids = ''
    device_app_counts = []
    
    for mobile_device in mobile_devices:
        
        device_ids = device_ids + str(mobile_device['id']) + ','
        
        r = requests.get(jss_url + '/JSSResource/mobiledevices/serialnumber/' + mobile_device.get('serial_number'), 
        	headers={'Accept': 'application/json'}, 
        	auth=(jss_username, jss_password))
        
        print("Mobile Device Name: %s" % mobile_device['name'])
        print("Username: %s" % mobile_device['username'])
        print("Serial Number: %s" %mobile_device['serial_number'])
        print("Applications Installed: %s" % len(r.json()['mobile_device']['applications']))
        device_app_counts.append(len(r.json()['mobile_device']['applications']))
        print("")
    
    if sum(device_app_counts) / float(len(device_app_counts)) == max(device_app_counts):
        print("All devices have the same number of apps: %s" % max(device_app_counts))

        if raw_input("Would you like to shutdown the devices? ") in 'yesYESYes':
            if raw_input("Are you sure you want to do this %s? " % jss_username) in 'yesYESYes':
                r = requests.post(jss_url + '/JSSResource/mobiledevicecommands/command/ShutDownDevice/id/%s' % device_ids.rstrip(','), 
                	auth=(jss_username, jss_password))
            print(r.text)
                
    else:
        print("Count of most installed: %s" % max(device_app_counts))
        print("Average number of apps: %s" % (sum(device_app_counts) / float(len(device_app_counts))))

    if raw_input("Would you like to ask the devices to submit inventory? ") in 'yesYESYes':

        r = requests.post(jss_url + '/JSSResource/mobiledevicecommands/command/UpdateInventory/id/%s' % device_ids.rstrip(','), 
        	auth=(jss_username, jss_password))

    if raw_input("Would you like to continue? ") in 'yesYESYes':
        continue
    else:
        break

print("Goodbye")

