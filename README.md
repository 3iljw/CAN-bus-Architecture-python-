# CAN-bus-Architecture-python-
CAN bus Architecture on python3 with multiprocessing.

It include send data, recevice message and log it.

I create a default interface with "listen_fun" to do send-message-task.
You also can design you own interface. For example : socket input, os input, button event on GUI etc.

I didn't set a point to interrupt all program. You can cancel the annotation, for pl in process_list : pl.open = False, to stop all process.
Of course you can design a break-condition belongs in you only.
