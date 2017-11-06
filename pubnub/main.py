import communicator

comm = communicator.Communicator()
comm.subscribe()
comm.publish('hallo')
print(comm.subscribe())
