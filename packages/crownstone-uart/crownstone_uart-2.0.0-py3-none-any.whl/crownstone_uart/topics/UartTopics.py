
class UartTopics:

    newDataAvailable = "UART_newDataAvailable"

    uartMessage = "UART_Message" # data is dictionary: {"string": str, "data": [uint8, uint8, ...] }

    hello = "UART_hello" # Data is: UartCrownstoneHelloPacket

    log = "UART_log" # Data is UartLogPacket
    logArray = "UART_logArray" # Data is UartLogArrayPacket