import multiprocessing as mp
from sniffer import Sniffer
from connection import Connection

if __name__ == '__main__':
    q_sniff = mp.Queue()
    q_conn = mp.Queue()
    sniffer = Sniffer(q=q_sniff, interface="eth0", packet_count=5)
    connection = Connection(q=q_sniff)
    
    sniff_proc = mp.Process(target=sniffer.sniff).start()
    conn_proc = mp.Process(target=connection.connect).start()
    while True:
        pass
    sniff_proc.join()
    conn_proc.join()
    
<<<<<<< HEAD
=======
    sniff_proc = mp.Process(target=sniffer.sniff, args=()).start()
    test_proc = mp.Process(target=connection.test, args=()).start()
    sniff_proc.join()
    test_proc.join()
>>>>>>> 6986c15732d8ba52b6b76325b061d262ace47a62
