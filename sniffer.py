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
    def __init__(self, packet_count=1, interface=None, monitor_mode=None, cont_sniff=True, q=None):
        self.packet_count = packet_count
        self.interface = interface
        self.monitor_mode = monitor_mode
        self.cont_sniff = cont_sniff
        self.q = q
        self.custom = [
            '-T', 'fields',
            '-e', 'tcp.srcport',       # Maps to Zeek's 'id.orig_p' (for TCP)
            '-e', 'udp.srcport',       # Maps to Zeek's 'id.orig_p' (for UDP)
            '-e', 'tcp.dstport',       # Maps to Zeek's 'id.resp_p' (for TCP)
            '-e', 'udp.dstport',       # Maps to Zeek's 'id.resp_p' (for UDP)
            '-e', 'ip.proto'           # protocl
            '-e', 'tcp.flags',         # Related to Zeek's 'conn_state' (for TCP)
            '-e', 'tcp.seq',           # Related to TCP sequence numbers
            '-e', 'tcp.ack',           # Related to TCP acknowledgment numbers
            '-e', 'tcp.window_size',   # Related to TCP window size
            '-e', 'tcp.len',           # Maps to Zeek's 'orig_bytes' or 'resp_bytes' (for TCP)
            '-e', 'udp.length',        # Maps to Zeek's 'orig_bytes' or 'resp_bytes' (for UDP)
            '-e', 'ip.len',            # orig/resp_ip_bytes
            '-E', 'header=n',
            '-E', 'separator=,',
            '-E', 'quote=d',
            '-E', 'occurrence=f'
        ]

    def stop_sniffing(self):
        self.cont_sniff = False

    def sniff(self):
        print("sniffer beginning........")
        # set up for continuous capturing
        capture = pyshark.LiveCapture(interface=self.interface, custom_parameters=self.custom)
        while self.cont_sniff:
            capture.sniff_continuously(packet_count=self.packet_count)
            # go through sniffed packets and put into queue
            for packet in capture:
                print(packet)
                self.q.put(packet.__str__())
        capture.close()

#sniffer = Sniffer(interface = 'Wi-Fi', monitor_mode = None)
#sniffer.sniff()
