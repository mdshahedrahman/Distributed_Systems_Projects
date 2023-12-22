from threading import Lock
import time

class PaxosNode:
    def __init__(self, node_id, value):
        self.node_id = node_id
        self.value = value
        self.accepted_value = None
        self.accepted_round = -1
        self.proposed_round = -1
        self.lock = Lock()

    def prepare(self, round_num):
        with self.lock:
            if round_num > self.proposed_round:
                self.proposed_round = round_num
                return True, (self.accepted_round, self.accepted_value)
            else:
                return False, None

    def accept(self, round_num, value):
        with self.lock:
            if round_num >= self.proposed_round:
                self.proposed_round = round_num
                self.accepted_round = round_num
                self.accepted_value = value
                return True
            else:
                return False

class PaxosProtocol:
    def __init__(self, nodes):
        self.nodes = nodes

    def run_paxos(self, value):
        round_num = 0
        attempts = 0
        max_attempts = 5

        while attempts < max_attempts:
            majority = len(self.nodes) // 2 + 1

            prepare_responses = []
            for node in self.nodes:
                response = node.prepare(round_num)
                prepare_responses.append(response)

            prepare_responses.sort(reverse=True)

            highest_round = prepare_responses[0][1][0] if prepare_responses else -1

            if highest_round == -1 or highest_round is None:
                highest_round = round_num


            accepted_count = 0
            accepted_value = None

            for response in prepare_responses[:majority]:
                if response[1] and response[1][0] == highest_round:
                    accepted_count += 1
                    accepted_value = response[1][1]

            if accepted_count >= majority:
                for node in self.nodes:
                    node.accept(round_num, accepted_value)
                return accepted_value
            else:
                round_num += 1
                attempts += 1
                time.sleep(1)

# Example usage
if __name__ == "__main__":
    # Create nodes
    node1 = PaxosNode(1, "Previous Value")
    node2 = PaxosNode(2, None)
    node3 = PaxosNode(3, None)

    nodes = [node1, node2, node3]

    paxos = PaxosProtocol(nodes)
    final_value_first_run = paxos.run_paxos("Previous Value")

    print("First Run - Final Decree Value:", final_value_first_run)

    new_proposer = PaxosNode(4, None)
    nodes.append(new_proposer)

    paxos = PaxosProtocol(nodes)
    final_value_second_run = paxos.run_paxos("New Value")

    print("Second Run - Final Decree Value:", final_value_second_run)
