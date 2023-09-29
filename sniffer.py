import pyshark
import time

#TODO: FIGURE OUT TO GRACIOUSLY EXIT TSHARK - DO NOT LET IT BE OPEN TO CONSUME MEMORY


class Sniffer():
    '''
    BASE CLASS
    PACKET_COUNT = AMOUNT OF PACKETS PER SNIFF
    INTERFACE = INTERFACE TO MONITOR (DEFAULT IS FIRST INTERFACE WHEN USING tshark -D)
    MONITOR_MODE = FOR MONITOR MODE (PROMISCUOUS MODE IF NONE)(STANDARD AFTER DEPLOYMENT SHOULD BE MONITOR)
    CONT_SNIFF = BOOLEAN TO STOP WHILE LOOP SNIFFING (TODO: FIGURE OUT TO NEGATE THIS DURING RUNTIME)
    Q = QUEUE MANAGER FROM OTHER FILE (TRANSMITS PACKETS TO MACHINE LEARNING MODEL (THIS IS NOT MODULAR OR GOOD PRACTICE TO HARDCODE LIKE THIS))
    '''
    def __init__(self, packet_count=1, interface=None, monitor_mode=True, cont_sniff=True, q=None):
        self.packet_count = packet_count
        self.interface = interface
        self.monitor_mode = monitor_mode
        self.cont_sniff = cont_sniff
        self.q = q

    def stop_sniffing(self):
        self.cont_sniff = False

    def sniff(self):
        print("sniffer beginning........")
        # set up for continuous capturing
        capture = pyshark.LiveCapture(interface=self.interface)
        while self.cont_sniff:
            capture.sniff_continuously(packet_count=self.packet_count)
            # go through sniffed packets and put into queue
            for packet in capture:
                self.q.put(packet.__str__())
                print("sniffer.py queue size:", self.q.qsize())
        capture.close()


#sniffer = Sniffer(interface = 'Wi-Fi', monitor_mode = None)
#sniffer.sniff()
