#!/usr/bin/env python3

import os
from node import Node
shared_dir = os.path.join(os.getcwd(), "shared_directory")

N = 3
nid = "node_1"
nodes = {f"node_{i}": ("127.0.0.1", 8080 + i) for i in range(1, N + 1)}
(nip, nport) = nodes.pop(nid)

if __name__ == "__main__":
    Node(node_id=nid,
         hostaddr=nip,
         port=nport,
         directory=shared_dir,
         nodes=nodes.values()).listen()
