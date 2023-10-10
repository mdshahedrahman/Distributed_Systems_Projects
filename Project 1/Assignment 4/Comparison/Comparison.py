import asyncio
import timeit
import numpy as np

class SynchronousRPCServer:
    def __init__(self):
        pass

    def foo(self, A, B):
        return np.matmul(A, B)

class AsynchronousRPCServer(SynchronousRPCServer):
    async def foo(self, A, B):
        return np.matmul(A, B)

class SynchronousRPCClient:
    def __init__(self, server):
        self.server = server

    def foo(self, A, B):
        return self.server.foo(A, B)

class AsynchronousRPCClient(SynchronousRPCClient):
    async def foo(self, A, B):
        return await self.server.foo(A, B)

def synchronous_rpc_test():
    server = SynchronousRPCServer()
    client = SynchronousRPCClient(server)

    A = np.random.rand(1000, 1000)
    B = np.random.rand(1000, 1000)

    start_time = timeit.default_timer()
    for i in range(1000):
        client.foo(A, B)
    end_time = timeit.default_timer()

    return end_time - start_time

def asynchronous_rpc_test():
    server = AsynchronousRPCServer()
    client = AsynchronousRPCClient(server)

    A = np.random.rand(1000, 1000)
    B = np.random.rand(1000, 1000)

    async def main():
        start_time = timeit.default_timer()
        for i in range(1000):
            await client.foo(A, B)
        end_time = timeit.default_timer()

        return end_time - start_time

    return asyncio.run(main())

if __name__ == '__main__':
    synchronous_rpc_time = synchronous_rpc_test()
    asynchronous_rpc_time = asynchronous_rpc_test()

    print('Synchronous RPC time:', synchronous_rpc_time)
    print('Asynchronous RPC time:', asynchronous_rpc_time)
