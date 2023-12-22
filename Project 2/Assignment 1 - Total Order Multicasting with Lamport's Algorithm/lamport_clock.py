import multiprocessing
import socket
import threading
import time
from collections import defaultdict, namedtuple
from heapq import heappop, heappush

NUM_MACHINES = 3
PORTS = [5001, 5002, 5003]
BUFFER = 4096
FORMAT = "utf-8"

Event = namedtuple("Event", ["clock", "pid"])

class CommunicationThread(threading.Thread):
    def __init__(self, id, clock, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.clock = clock
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", PORTS[id]))
        self.acks = defaultdict(int)
        self.acknowledged = defaultdict(bool)
        self.queue = []
        
    def deliver(self, event):
        print(f"[Processing] Machine P{self.id} is processing P{event.pid} process with Lamport clock [P{event.pid}.{event.clock}]")

    def acknowledge(self, event):
        with self.clock.get_lock():
            self.clock.value += 1

        pid = event.pid
        clock = event.clock
        action = "ack"
        msg = f"{pid}@{clock}@{action}"

        data = msg.encode(FORMAT)
        
        for port in PORTS:
            self.sock.sendto(data, ("localhost", port))
        self.acknowledged[event] = True

    def run(self):
        while True:
            data = self.sock.recvfrom(BUFFER)[0].decode(FORMAT)
            data = data.split("@")
            
            received_pid = data[0]
            received_clock = data[1]
            received_msg_type = data[2]
            
            event = Event(clock=received_clock, pid=received_pid)
            if received_msg_type == "ack":
                self.acks[event] += 1
                if self.queue:
                    if self.acks[self.queue[0]] >= NUM_MACHINES:
                        self.deliver(heappop(self.queue))
                    elif not self.acknowledged[self.queue[0]]:
                        self.acknowledge(event)

            elif received_msg_type == "event":
                with self.clock.get_lock():
                    self.clock.value += 1
                    
                heappush(self.queue, event)
                self.acks[event] = 0
                if not self.acknowledged[event]:
                    self.acknowledge(event)
            
class MachineProcess(multiprocessing.Process):
    def __init__(self, id, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.clock = multiprocessing.Value("i", 0)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def do_operation(self):
        time.sleep(0.05)
        
    def broadcast_event(self):
        with self.clock.get_lock():
            self.clock.value += 1
        
        pid = self.id
        clock = self.clock.value
        action = "event"
        msg = f"{pid}@{clock}@{action}"
        
        data = msg.encode(FORMAT)
        
        for port in PORTS:
            self.sock.sendto(data, ("localhost", port))
        print(f"[Broadcast]  Machine P{pid} has sent some data with Lamport clock [P{pid}.{clock}]")

    def run(self):
        communication_thread = CommunicationThread(id=self.id, clock=self.clock)
        communication_thread.start()

        time.sleep(0.1)

        for _ in range(3):
            self.do_operation()
            self.broadcast_event()
            

if __name__ == "__main__":
    machines = [MachineProcess(id = i) for i in range(NUM_MACHINES)]

    for machine in machines:
        machine.start()
        time.sleep(0.05)

    for machine in machines:
        machine.join()