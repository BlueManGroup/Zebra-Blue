import multiprocessing as mp
from sniffer import Sniffer
from connection import Connection

if __name__ == '__main__':
    q_sniff = mp.Queue()
    q_conn = mp.Queue()
    sniffer = Sniffer(q=q_sniff, packet_count=1)
    connection = Connection(q=q_sniff)
    
    sniff_proc = mp.Process(target=sniffer.sniff)
    conn_proc = mp.Process(target=connection.connect)

    sniff_proc.start()
    conn_proc.start()

    sniff_proc.join()
    conn_proc.join()
