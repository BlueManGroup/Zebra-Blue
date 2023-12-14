import multiprocessing as mp
from sniffer import Sniffer
from connection import Connection
from selector import Selector

if __name__ == '__main__':
    q_sniff = mp.Queue()
    q_conn = mp.Queue()
    sniffer = Sniffer(q=q_sniff, interface='Wi-Fi', packet_count=1) # for other
    # sniffer = Sniffer(q=q_sniff, interface='wlan0', packet_count=1) # for pi5
    connection = Connection(q=q_conn)
    # needs boths qs to send relevant packets to connection process
    selector = Selector(q_sniff=q_sniff, q_conn=q_conn)
    
    sniff_proc = mp.Process(target=sniffer.sniff)
    conn_proc = mp.Process(target=connection.connect)
    selector_proc = mp.Process(target=selector.select)

    sniff_proc.start()
    conn_proc.start()
    selector_proc.start()

    sniff_proc.join()
    conn_proc.join()
    selector_proc.join()
