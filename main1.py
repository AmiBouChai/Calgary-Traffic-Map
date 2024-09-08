# January 26, 2024

import time
import network
import socket
import ssl
import urequests
import ubinascii
import LEDMatrix
import time

ssid = "airuc-guest"
password = ""
streets = {"Macleod Trail SE": 6, "Macleod Trail": 5, "Centre Street": 4, "4 Street": 3, "5 Street": 2, "8 Street": 1}
avenues = {"4 Avenue": 5, "5 Avenue": 4, "6 Avenue": 3, "7 Avenue": 2, "8 Avenue": 1}
led_matrix = LEDMatrix.LEDMatrix(5, 6)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print(mac)

def connect():
# Connect to WLAN
# Connect function from https://projects.raspberrypi.org/en/projects/get-started-pico-w/2
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)

# Function to get all of the current downtown closures and return the closures and their data as a list
def get_cdc():
    # Keep trying to fetch API data unitl it returns data
    r = None
    while r == None:
        try:
            r = urequests.get("https://gis.calgary.ca/arcgis/rest/services/pub_CalgaryDotCa/Events/MapServer/0/query?where=1=1&outFields=*&returnGeometry=false&f=geojson&orderByFields=TITLE")
        except:
            print("Could not fetch data")
            continue

    # Store the list of closures in the closures variable
    closures = r.json()["features"]
    cdc = []

    # Get epoch time
    current_time = time.time() + 25200
    print(current_time)

    # Make a list of current downtown closures
    for closure in closures:
        if closure["properties"]["ISDOWNTOWN"] == 1 and closure["properties"]["START_DT_UTC"] < current_time*1000:
            cdc.append(closure)
    
    return cdc

# Function to convert street and avenue location into an LED location on the model
def light_closure(closure):
    location = closure["properties"]["TITLE"]
    x = None
    y = None
    
    # Make sure the location string doesn't contain 1 in order to filter unmappable results
    if "1" not in location:
        # Determine the x coordinate on the LED grid based on the street
        for street in streets:
            if street in location:
                y = streets[street]
        
        # Determine the y coordinate on the LED grid based on the avenue
        for avenue in avenues:
            if avenue in location:
                x = avenues[avenue]
        
    # Light the LED on the map corresponding to the closure location
    if x == None or y == None:
        print(f"Closure {location} can't be mapped")
    else:
        print(f"Mapped {location} at {x},{y}")
        led_matrix.light(x, y)
    print(x, y)

# Connect to the u of c guest network
try:
    connect()
except KeyboardInterrupt:
    machine.reset()
print("Connected")

while True:
    if wlan.isconnected():
        # Get current downtown closures
        cdc = get_cdc()
        print(len(cdc))
    else:
        # Connect to the u of c guest network
        try:
            connect()
        except KeyboardInterrupt:
            machine.reset()
        print("Connected")
        
    
    # Reset LED grid in order to get rrid of closures that aren't active anymore
    led_matrix.all_off()

    # Light up all current closures
    for closure in cdc:
        light_closure(closure)

    # Check for updates every 30 seconds
    time.sleep(30)
