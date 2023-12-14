import random
import pickle
import sklearn
import numpy
import pandas
import ast

class Selector():
    def __init__(self, q_sniff=None, q_conn=None):
        self.q_sniff = q_sniff
        self.q_conn = q_conn
        self.cont_select = True
        self.model = self.get_pkl("models/20_rnd_forest_3d.pkl")
        self.protocol_dictionary = {
                                    'udp': 0,
                                    'tcp': 1,
                                    'icmp': 2,
                                    "-1": -1,
                                    "0": 0,
                                    "1": 1,
                                    "2": 2
                                }
        print(self.model, type(self.model))

    def get_pkl(self, name):
        with open(name, 'rb') as f:
            data = pickle.load(f)
        return data

    def stop_select(self):
        self.cont_select = False

    # RENAME WHEN ML MODEL IMPLEMENTED
    def select(self):
        random.seed()
        
        while self.cont_select:
            # fetch packet from q. if q empty wait for packet to be put into q
            curPacket = self.q_sniff.get(True)
            rnd = random.randint(0, 100)
            if rnd > 0:
                print(rnd)
                print(curPacket, type(curPacket))

                ###################### make string into 2d-list/correct format
                list_cur_packet = ast.literal_eval(curPacket)
                tmp_list = []
                for item in list_cur_packet:
                    try:
                        if item.isnumeric():
                            tmp_list.append(int(item))
                        else:
                            tmp_list.append(item)
                    except AttributeError:
                        tmp_list.append(item)
                tmp_list[2] = self.protocol_dictionary[tmp_list[2].lower()] # encode protocol        
                list_cur_packet = [tmp_list[:-1]]
                ######################

                # Making the prediction
                print(list_cur_packet)
                tmp = [list_cur_packet[0][:-2]]
                prediction = self.model.predict(tmp)
                print("prediction", prediction)

                print(list_cur_packet, type(list_cur_packet))
                self.q_conn.put(curPacket[:-1] + f", {prediction[0]}]")

