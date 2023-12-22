from threading import Lock
import time

class CentralizedCoordinator:
    def __init__(self, acceptors):
        self.acceptors = acceptors
        self.proposals = []

    def collect_proposal(self, proposer_id, proposal_value):
        self.proposals.append((proposer_id, proposal_value))

    def run_paxos(self):
        for proposer_id, proposal_value in self.proposals:
            prepare_responses = []
            for acceptor in self.acceptors:
                response = acceptor.prepare(proposer_id)
                prepare_responses.append(response)

            accepted_count = 0
            accepted_value = None

            for response in prepare_responses:
                if response[0]:  # Check if prepare succeeded
                    acceptor_response = response[1]
                    if acceptor_response[0]:  # Check if accept succeeded
                        accepted_count += 1
                        accepted_value = acceptor_response[1]

            proposer = next((p for p in proposers if p.proposer_id == proposer_id), None)
            if accepted_count >= len(self.acceptors) // 2 + 1:
                proposer.propose_success(accepted_value)
            else:
                proposer.propose_failure()

class PaxosNode:
    def __init__(self, node_id, value):
        self.node_id = node_id
        self.value = value
        self.accepted_value = None
        self.accepted_round = -1
        self.proposed_round = -1
        self.lock = Lock()

    def prepare(self, proposer_id):
        with self.lock:
            if self.proposed_round == -1 or self.proposed_round < proposer_id:
                return True, (self.accepted_round, self.accepted_value)
            else:
                return False, None

    def accept(self, proposer_id, round_num, value):
        with self.lock:
            if round_num >= self.proposed_round:
                self.proposed_round = proposer_id
                self.accepted_round = round_num
                self.accepted_value = value
                return True
            else:
                return False

class Proposer:
    def __init__(self, proposer_id, coordinator):
        self.proposer_id = proposer_id
        self.value = None
        self.coordinator = coordinator

    def propose(self, value):
        self.value = value
        self.coordinator.collect_proposal(self.proposer_id, value)

    def propose_success(self, accepted_value):
        print(f"Proposer {self.proposer_id} proposal succeeded. Final Value: {accepted_value}")

    def propose_failure(self):
        print(f"Proposer {self.proposer_id} proposal failed.")


if __name__ == "__main__":
    # Create nodes
    acceptors = [PaxosNode(i, None) for i in range(1, 6)]
    proposers = [Proposer(i, CentralizedCoordinator(acceptors)) for i in range(1, 6)]

    proposers[0].propose("Scenario (a) Value")
    proposers[1].propose("Scenario (a) Value")
    proposers[2].propose("Scenario (a) Value")
    proposers[3].propose("Scenario (a) Value")
    proposers[4].propose("Scenario (a) Value")
    CentralizedCoordinator(acceptors).run_paxos()

    proposers[0].propose(None)
    proposers[1].propose(None)
    proposers[2].propose(None)
    proposers[3].propose("Scenario (b) Value")
    proposers[4].propose(None)
    CentralizedCoordinator(acceptors).run_paxos()

    proposers[0].propose(None)
    proposers[1].propose("Scenario (c) Value")
    proposers[2].propose(None)
    proposers[3].propose(None)
    proposers[4].propose(None)
    CentralizedCoordinator(acceptors).run_paxos()
