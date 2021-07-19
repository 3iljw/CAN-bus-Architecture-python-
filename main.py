import csv
from datetime import datetime
from multiprocessing import Event, Manager, Process, Queue, RLock, Value, current_process
### Manager.list, Value is not appeared in code, but usually been used in multiprocessing-program
from time import sleep

import can
import log

class router() :
    def __init__(self) :
        # Inital all var, start all processing 
        # manager = Manager()

        ###############################
        # Canbus
        ###############################
        self.bus = can.interface.Bus(channel='can0', bustype='socketcan')       # Canbus info 
        
        # Queue
        sendque = Queue()                                                       # Canbus send message queue 
        recvque = Queue()                                                       # Canbus receive message queue
        
        ###############################
        # event & lock init
        ###############################
        self.send_available = Event()                                           # Canbus event
        self.lock = RLock()
        
        # process initial
        ###############################
        # canbus
        canbus_th1 = Process(target=self.listen, 
            args=(recvque,))
        canbus_th2 = Process(target=self.parser, 
            args=(recvque,))
        canbus_th3 = Process(target=self.send, 
            args=(sendque,))
        canbus_th4 = Process(target=self.listen_fun,
            args=(sendque,))
            
        process_list = [canbus_th1, canbus_th2, canbus_th3, canbus_th4]
        for pl in process_list : 
            pl.open = True
            pl.start()
        """ Set your condiction """
        # for pl in process_list : pl.open = False
        for pl in process_list : pl.join()
         

    def can_que(self, sendque, ar_id, data) :
        """Command register queue"""
        with self.lock : sendque.put([ar_id,data])
            
    def listen(self, recvque):
        """Listen can port."""
        canbus_th1 = current_process()
        while canbus_th1.open :
            msg = self.bus.recv(0.03)
            if msg : 
                with self.lock : recvque.put([msg.channel, msg.arbitration_id, msg.data])

    def parser(self, recvque) :
        """Parse the receve data."""
        canbus_th2 = current_process()
        while canbus_th2.open :
            while recvque.qsize() :
                ### Set your condiction ###
                msg = recvque.get()
                msg_arid = hex(msg[1])
                msg_data = list(msg[2])
                print(msg_data)
                self.send_available.set()
                log.log_socket_communication(datetime.now(), 'CAN_Log', [msg_arid, msg_data])

    def send(self, sendque) :
        """Send command from queue."""

        canbus_th3 = current_process()
        while canbus_th3.open :
            while sendque.qsize() :
                with self.lock : msg = sendque.get() 
                # print('send:', hex(msg[0]), msg[1])
                msg = can.Message(arbitration_id=msg[0], data=msg[1], extended_id=False)
                freq = 0

                while freq < 2 :
                    freq += 1
                    try :
                        self.bus.send(msg)
                    except can.CanError :
                        print('reconnecting')
                        time.sleep(1)
                        continue

                    self.send_available.clear()
                    if self.send_available.wait(0.1) :
                        ### Set your condiction 
                        break
                        
    def listen_fun(self, sendque) :
        """ send-message-task """
        listen_th = current_process()
        while listen_th.open :
            """ Set you want to send to CAN bus """
            # ar_id, data = None, None
            # self.can_que(sendque, ar_id, data)
            sleep(1)

if __name__ == "__main__" :
    Router = router()
