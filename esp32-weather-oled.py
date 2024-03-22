from machine import Pin, SoftI2C
import network
import urequests as requests
import ssd1306
import time

# WiFi configuration
WIFI_SSID = ""  # Enter your WiFi SSID
WIFI_PASSWORD = ""  # Enter your WiFi password

# OLED display configuration
OLED_WIDTH = 128
OLED_HEIGHT = 64

# Weather API configuration
WEATHER_API_KEY = ""  # Weather API key
WEATHER_API_URL = "" + WEATHER_API_KEY + "&q="  # Weather API endpoint URL

# Initialize WiFi connection
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print("WiFi Connected!")
    print("IP Address:", wlan.ifconfig()[0])

# Initialize OLED display
def init_oled():
    i2c = SoftI2C(scl=Pin(), sda=Pin()) # Pins connected to the development board's GPIO pins.
    oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)
    oled.fill(0)
    oled.show()
    return oled

# Get weather information
def get_weather(city):
    url = WEATHER_API_URL + city
    response = requests.get(url)
    weather_data = response.json()
    return weather_data

# Main program
def main():
    connect_wifi(WIFI_SSID, WIFI_PASSWORD)
    oled = init_oled()
    
    city = input("Enter city name: ")
    weather_data = get_weather(city)

    # Check if weather data is successfully fetched
    if 'main' in weather_data:
        # Parse weather information
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        cloudiness = weather_data['clouds']['all']

        # Display weather information
        oled.text("Weather Data", 15, 0)
        oled.text("City: "+city, 0, 12)
        oled.text("Temperature:{}C".format(temperature), 0, 24)
        oled.text("Humidity: {}%".format(humidity), 0, 36)
        oled.text("Cloudiness: {}%".format(cloudiness), 0, 48)
        oled.show()
    else:
        print("Failed to fetch weather data!")

if __name__ == "__main__":
    main()
