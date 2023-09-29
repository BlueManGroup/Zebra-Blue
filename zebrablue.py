import multiprocessing as mp
from sniffer import Sniffer
from connection import Connection

if __name__ == '__main__':
    q_sniff = mp.Queue()
    q_conn = mp.Queue()
    sniffer = Sniffer(q=q_sniff, packet_count=5)
    connection = Connection(q=q_sniff)
    
    sniff_proc = mp.Process(target=sniffer.sniff).start()
    conn_proc = mp.Process(target=connection.connect).start()
    while True:
        pass
    sniff_proc.join()
    conn_proc.join()
    