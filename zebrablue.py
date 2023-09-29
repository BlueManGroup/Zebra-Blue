import multiprocessing as mp
from sniffer import Sniffer
import connection

if __name__ == '__main__':
    q_sniff = mp.Queue()
    q_conn = mp.Queue()
    sniffer = Sniffer(q=q_sniff, interface='wlan0')
    
    sniff_proc = mp.Process(target=sniffer.sniff, args=()).start()
    test_proc = mp.Process(target=connection.test, args=()).start()
    sniff_proc.join()
    test_proc.join()
