# Connect to an "eval()" service over BLE UART.

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
ble.name = "Raptor 3"

uart_connections = []
MAX_CONNECTIONS = 1

while True:
    if len(uart_connections) < MAX_CONNECTIONS:
        print(f"Searching for other devices..., you currently are connected to {uart_connections} devices.")
        for adv in ble.start_scan(ProvideServicesAdvertisement):
            if UARTService in adv.services:
                print("Found a new connection, attempting to connect.")
                try:
                    uart_connections.append(ble.connect(adv))
                    print("Connected successfully!")
                except:
                    print("Failed to connect.")
        ble.stop_scan()

    for uart_connection in uart_connections:
        if not uart_connection.connected:
           continue
        
        uart_service = uart_connection[UARTService]
        while uart_connection.connected:
            s = "Hello World\n"
            uart_service.write(s.encode("utf-8"))
            # uart_service.write(b'\n') this is not needed if you add the \n direclty, I think at least
            print(uart_service.readline().decode("utf-8"))
