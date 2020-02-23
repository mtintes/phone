#!/usr/bin/env python

from gnuradio import gr,audio

class my_graph(gr.flow_graph):
	def __init__(self):
		gr.flow_graph.__init__(self)		
		
		#build flow graph
		#create two sinusoidal sources with a sample rate
		# of 48000s/s and frequencies of 350 and 440
		#amplitude of 0.1
		src0 = gr.sig_source_f(48000,gr.GR_SIN_WAVE,350,0.1)
		src1 = gr.sig_source_f(48000,gr.GR_SIN_WAVE,440,0.1)

		#create a destination sink 
		dst = audio.sink(48000)

		#connect each of the sources to the sink
		self.connect(src0,(dst,0))
		self.connect(src1,(dst,1))

		#puts 350 Hz into a data file
		fs = gr.file_sink(gr.sizeof_float,"audio.dat")
		self.connect(src0 ,fs)		

#The main function
def main():
	fg = my_graph()
	try:
		fg.run()
	except KeyboardInterrupt:
		pass
main()
