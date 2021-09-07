# Connect to an "eval()" service over BLE UART.

# TODO: Fred you should read this: https://circuitpython.readthedocs.io/projects/ble/en/latest/api.html

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
ble.name = "Raptor 3"

uart_connections = []
MAX_CONNECTIONS = 1
TIME_TO_SCAN = 10

def send_message_to_connections(msg):
    for uart_connection in ble.connections:        
        uart_service = uart_connection[UARTService]
        while uart_connection.connected:
            uart_service.write(msg.encode("utf-8"))
            print(uart_service.readline().decode("utf-8"))

while True: 
    print(f"Searching for other devices..., you currently are connected to {len(ble.connections)} devices.")
    for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=TIME_TO_SCAN):
        if adv in ble.connections:
            continue

        if UARTService in adv.services:
            print("Found a new connection, attempting to connect.")
            try:
                ble.connect(adv)
                print("Connected successfully!")
            except:
                print("Failed to connect.")

    # ble.stop_scan() may or may not need this

    send_message_to_connections(msg)

