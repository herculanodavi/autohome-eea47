pipes = [ [0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2] ]

	radio = NRF24()
	radio.begin(1,0,"P9_23", "P9_24") #Set CE and IRQ pins
	radio.setRetries(15,15)
	radio.setPayloadSize(8)
	radio.setChannel(0x60)
	radio.setDataRate(NRF24.BR_250KBPS)
	radio.setPALevel(NRF24.PA_MAX)
	radio.openWritingPipe(pipes[0])
	radio.openReadingPipe(1,pipes[1])

	radio.printDetails()