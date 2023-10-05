import random

# TODO: IMPLEMENT ML MODEL TO FIRST ANALYSE PACKETS
# IF PACKET NON-SUS RUN THROUGH RANDOMIZER

class Selector():
    def __init__(self, q_sniff=None, q_conn=None):
        self.q_sniff = q_sniff
        self.q_conn = q_conn
        self.cont_select = True

    def stop_select(self):
        self.cont_select = False

    # RENAME WHEN ML MODEL IMPLEMENTED
    def select(self):
        random.seed()
        
        while self.cont_select:
            # fetch packet from q. if q empty wait for packet to be put into q
            curPacket = self.q_sniff.get(True)
            print(rnd := random.randint(0, 100))
            if rnd > 99:
                self.q_conn.put(curPacket)
            
