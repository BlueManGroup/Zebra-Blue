import pyshark
import time
import datetime

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
    def __init__(self, packet_count=1, interface=None, monitor_mode=None, cont_sniff=True, q=None, ip_address="192.168.1.6"):
        self.packet_count = packet_count
        self.interface = interface
        self.monitor_mode = monitor_mode
        self.cont_sniff = cont_sniff
        self.q = q # useless
        # self.custom = [ #id.orig_p, id.resp_p, proto, orig_bytes, resp_bytes, orig_ip_bytes, resp_ip_bytes, encoding
        #     '-T', 'fields',
        #     '-e', 'tcp.srcport',       # Maps to Zeek's 'id.orig_p' (for TCP)
        #     '-e', 'udp.srcport',       # Maps to Zeek's 'id.orig_p' (for UDP)
        #     '-e', 'tcp.dstport',       # Maps to Zeek's 'id.resp_p' (for TCP)
        #     '-e', 'udp.dstport',       # Maps to Zeek's 'id.resp_p' (for UDP)
        #     '-e', 'ip.proto',          # protocol
        #     '-e', 'tcp.len',           # Maps to Zeek's 'orig_bytes' or 'resp_bytes' (for TCP)
        #     '-e', 'udp.length',        # Maps to Zeek's 'orig_bytes' or 'resp_bytes' (for UDP)
        #     '-e', 'ip.len',            # orig/resp_ip_bytes
        # ]
        self.our_network = self.create_our_network(ip_address)

    def create_our_network(self, ip_address):
        ip_address = ip_address.strip().split(".")
        ip_address = ip_address[:-1]
        ip_address = ".".join(ip_address)
        return ip_address

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
                try:
                    if "IP" in packet:
                        ip_from_home_network = self.create_our_network(packet.ip.src) == self.our_network
                    src_port = packet[packet.transport_layer].srcport # Maps to Zeek's 'id.orig_p'
                    dst_port = packet[packet.transport_layer].dstport # Maps to Zeek's 'id.resp_p'
                    protocol = packet.transport_layer  # Protocol 
                    orig_ip_length = packet.ip.len if "IP" in packet else -1 # orig/resp_ip_bytes
                    orig_bytes = packet[packet.transport_layer].len if "TCP" in packet else packet[packet.transport_layer].length # orig_bytes
                    ip_src = packet.ip.src
                    ip_dst = packet.ip.dst
                    
                    content = [
                        src_port, # Maps to Zeek's 'id.orig_p'
                        dst_port, # Maps to Zeek's 'id.resp_p'
                        protocol,
                        orig_ip_length, 
                        orig_bytes,
                        ip_from_home_network,
                        ip_src,
                        ip_dst
                    ]
                        # Display the information
                    # print(content)
                    # print(packet)
                    # self.q.put(packet.__str__()) 
                    self.q.put(content.__str__())
                except Exception as e:
                    with open("error_log.txt", "a") as f:
                        f.write(f"{datetime.datetime.now()} : {e}\n")
        capture.close()

if __name__ == "__main__":
    sniffer = Sniffer(interface = 'Wi-Fi') # for other
    # sniffer = Sniffer(interface = 'eth0') #For raspberry pi
    sniffer.sniff()
