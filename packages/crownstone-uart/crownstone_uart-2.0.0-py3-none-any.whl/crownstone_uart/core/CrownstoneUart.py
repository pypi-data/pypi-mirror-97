# import signal  # used to catch control C
import time

from crownstone_core.protocol.BlePackets import ControlPacket
from crownstone_core.protocol.BluenetTypes import ControlType

from crownstone_uart.core.dataFlowManagers.UartWriter import UartWriter
from crownstone_uart.core.modules.MeshHandler import MeshHandler

from crownstone_uart.core.dataFlowManagers.StoneManager import StoneManager
from crownstone_uart.core.modules.UsbDevHandler import UsbDevHandler
import asyncio

from crownstone_uart.core.UartEventBus import UartEventBus
from crownstone_uart.core.uart.UartManager import UartManager
from crownstone_uart.core.uart.uartPackets.UartMessagePacket import UartMessagePacket
from crownstone_uart.core.uart.UartTypes import UartTxType, UartMessageType
from crownstone_uart.core.uart.uartPackets.UartWrapperPacket import UartWrapperPacket
from crownstone_uart.topics.SystemTopics import SystemTopics


class CrownstoneUart:
    __version__ = "2.0.0"

    def __init__(self, loop=None):
        self.uartManager = None
        self.running = True
        if loop is None:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

        self.uartManager = UartManager()
        
        self.stoneManager = StoneManager()

        self.mesh = MeshHandler()
        # only for development. Generally undocumented.
        self._usbDev = UsbDevHandler()

    def __del__(self):
        self.stop()

    def is_ready(self) -> bool:
        return self.uartManager.is_ready()


    async def initialize_usb(self, port = None, baudrate=230400, writeChunkMaxSize=0):
        '''
        writing in chunks solves issues writing to certain JLink chips. A max chunkSize of 64 was found to work well for our case.
        For normal usage with Crownstones this is not required.
        writeChunkMaxSize of 0 will not send the payload in chunks
        :param port:
        :param baudrate:
        :param writeChunkMaxSize:
        :return:
        '''
        self.uartManager.config(port, baudrate, writeChunkMaxSize)

        result = [False]
        def handleMessage(result, data):
            result[0] = True

        event = UartEventBus.subscribe(SystemTopics.connectionEstablished, lambda data: handleMessage(result, data))
        self.uartManager.start()

        while not result[0] and self.running:
            await asyncio.sleep(0.1)

        UartEventBus.unsubscribe(event)
        

    def initialize_usb_sync(self, port = None, baudrate=230400, writeChunkMaxSize=0):
        '''
                writing in chunks solves issues writing to certain JLink chips. A max chunkSize of 64 was found to work well for our case.
                For normal usage with Crownstones this is not required.
                writeChunkMaxSize of 0 will not send the payload in chunks
                :param port:
                :param baudrate:
                :param writeChunkMaxSize:
                :return:
                '''
        self.uartManager.config(port, baudrate, writeChunkMaxSize)

        result = [False]

        def handleMessage(result, data):
            result[0] = True

        event = UartEventBus.subscribe(SystemTopics.connectionEstablished, lambda data: handleMessage(result, data))
        self.uartManager.start()

        try:
            while not result[0] and self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nClosing Crownstone Uart.... Thanks for your time!")
            self.stop()

        UartEventBus.unsubscribe(event)


    def stop(self):
        if self.uartManager is not None:
            self.uartManager.stop()
        self.running = False

    #
    def switch_crownstone(self, crownstoneId: int, on: bool):
        """
        :param crownstoneId:
        :param on: Boolean
        :return:
        """
        if not on:
            self.mesh.turn_crownstone_off(crownstoneId)
        else:
            self.mesh.turn_crownstone_on(crownstoneId)


    def dim_crownstone(self, crownstoneId: int, switchVal: int):
        """
        :param crownstoneId:
        :param switchVal: 0% .. 100% or special values (SwitchValSpecial).
        :return:
        """

        self.mesh.set_crownstone_switch(crownstoneId, switchVal)


    def get_crownstone_ids(self):
        return self.stoneManager.getIds()

    def get_crownstones(self):
        return self.stoneManager.getStones()

    def uart_echo(self, payloadString):
        # wrap that in a control packet
        controlPacket = ControlPacket(ControlType.UART_MESSAGE).loadString(payloadString).getPacket()

        # wrap that in a uart message
        uartMessage   = UartMessagePacket(UartTxType.CONTROL, controlPacket).getPacket()

        # finally, wrap it in an uart wrapper packet
        uartPacket    = UartWrapperPacket(UartMessageType.UART_MESSAGE, uartMessage).getPacket()

        # send over uart
        result = UartWriter(uartPacket).write_sync()
