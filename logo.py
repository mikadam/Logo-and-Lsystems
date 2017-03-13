'''
File name: logo.py
Author: Michal Adamkiewicz
Date: 2014

Interpreted turtle language with L-system module

Please note that this code is quite old and was written for myself so commenting/style may vary
'''


import tkinter as tk
import math
from random import choice
from time import sleep

from parsers import treeParser, DictParser

class LogoUi:
	'UI and command interpreter for turtles and l-systems'
	def __init__(self,size,center_location=True):
		"Initialize the logo UI and creates corresponding turtle object"
		self.size=size
		#Initialize window
		self.root=tk.Tk()
		self.root.title('Logo')

		#create and place canvas
		self.m=tk.Canvas(self.root, width=size, height=size,bg="#f5f5dc")
		self.m.grid(row=0,column=0,columnspan=3,rowspan=2,sticky='ewns')

		#create and place command entry textbox
		self.command=tk.Entry(self.root,width=30)
		self.command.grid(row=2,column=0,columnspan=1,sticky='ew')
		self.command.focus()

		#create and place run button, and bind it to run command
		self.run_button=tk.Button(self.root,text='Enter',command=self.run)
		self.run_button.grid(row=2,column=1,columnspan=1,sticky='ew')

		self.cler=tk.Button(self.root,text='Clear',command=self.clear_screen)
		self.cler.grid(row=2,column=2,columnspan=1,sticky='ew')

		self.rules=tk.Text(self.root,width=25,font=('Ariel', '16', ''))
		self.rules.grid(row=1,column=3,columnspan=6,rowspan=1,sticky='ewns',pady=5,padx=5)
		self.rules.insert(tk.END,'p:[p]f[p]f++f[p]f++ff\nf:ff')

		self.l_system_plot=tk.Button(self.root,text='Plot',command=self.plot_l_system)
		self.l_system_plot.grid(row=2,column=7,columnspan=2,sticky='ew',pady=5,padx=2)

		tk.Label(self.root,text='I:').grid(row=0,column=7,columnspan=1,sticky='ew')
		tk.Label(self.root,text='D:').grid(row=0,column=5,columnspan=1,sticky='ew')
		tk.Label(self.root,text='A:').grid(row=0,column=3,columnspan=1,sticky='ew')

		self.iter=tk.Entry(self.root,width=2)
		self.iter.grid(row=0,column=8,columnspan=1,sticky='ew',pady=5)
		self.iter.insert(0,'6')
		self.distance=tk.Entry(self.root,width=2)
		self.distance.grid(row=0,column=6,columnspan=1,sticky='ew')
		self.distance.insert(0,'4')
		self.angle=tk.Entry(self.root,width=2)
		self.angle.grid(row=0,column=4,columnspan=1,sticky='ew')
		self.angle.insert(0,'60')
		self.init=tk.Entry(self.root,width=2)
		self.init.grid(row=2,column=3,columnspan=4,sticky='ew')
		self.init.insert(0,'p')


		self.root.grid_columnconfigure(0,weight=10)
		self.root.grid_columnconfigure(1,weight=0)
		self.root.grid_columnconfigure(2,weight=0)
		self.root.grid_columnconfigure(3,weight=0)
		self.root.grid_columnconfigure(4,weight=1)
		self.root.grid_columnconfigure(5,weight=0)
		self.root.grid_columnconfigure(6,weight=1)
		self.root.grid_columnconfigure(7,weight=0)
		self.root.grid_columnconfigure(8,weight=1)

		self.root.grid_rowconfigure(0,weight=0)
		self.root.grid_rowconfigure(1,weight=1)
		self.root.grid_rowconfigure(2,weight=0)

		#cause pressing "Enter" to have same effect as buttor
		self.command.bind('<Return>', lambda x: self.run())
		self.command.bind('<Up>', lambda x: self.history_up())
		self.command.bind('<Down>', lambda x: self.history_down())

		#mac tkinter bug workaround
		self.angle.bind("<Key>", self.arrow_bug_workaround)
		self.init.bind("<Key>", self.arrow_bug_workaround)
		self.iter.bind("<Key>", self.arrow_bug_workaround)
		self.distance.bind("<Key>", self.arrow_bug_workaround)

		#draw elements
		self.root.update()

		#create turtle and place in the center facing up
		# self.t=Turtle(self.m,[size//2,size//2,270])
		if(center_location):
			self.t=Turtle(self.m,[size//2,2*size//4,270])
		else:
			self.t=Turtle(self.m,[size//2,4*size//4,270])

		#store names of commands linked to turtles methods
		self.command_palete={'fd':self.t.forward,
								'tr':self.t.turn,
								'pu':self.t.pen_up,
								'pd':self.t.pen_down,
								'st':self.t.save_state,
								'rc':self.t.recall_state,
								'cl':self.t.clear,
								'pr':print}

		self.command_history=[]
		self.history_position=0

		self.defined_variables=[{}]
		self.defined_funcations={}
		self.cancel=False

	def clear_screen(self):
		self.m.delete("all")
		self.cancel=True
		self.t.position=[self.m.winfo_width()//2,self.m.winfo_height()//2,270]
		self.t.pen=1
		self.t.stack=[]

	def plot_l_system(self):
		a=float(self.angle.get())
		d=float(self.distance.get())
		i=int(self.iter.get())
		start=self.init.get()
		r=self.rules.get("1.0",tk.END).replace("'","").replace('"',"")
		r=list(filter(lambda x: x!="" ,r.split('\n')))

		rules={}

		for entry in r:
			e=entry.split(':',1)
			if(len(e[0])!=1): raise KeyError
			k=e[1].split(',')
			if(len(k)==1):
				rules[e[0]]=k[0]
			else:
				rules[e[0]]=k

		if(start[0]==':'):
			start=start[1:]
			self.python_run_slow(self.iterate(i,start,rules),length=d,angle=a)
		else:
			self.python_run(self.iterate(i,start,rules),length=d,angle=a)

	def arrow_bug_workaround(self,event): 
		if event.keycode in {8320768, 8255233}: 
			#print ("ignoring", event.keycode)
			return "break" 
		#print (event.keycode, "accepted")

	def history_up(self):
		self.command.delete(len(self.command.get())-1, tk.END)
		if(len(self.command_history)-self.history_position>0):
			self.history_position+=1
			self.command.delete(0,tk.END)
			self.command.insert(0,self.command_history[len(self.command_history)-self.history_position])
		return "break"

	def history_down(self):
		self.command.delete(len(self.command.get())-1, tk.END)
		if(self.history_position>0):
			self.history_position-=1
			self.command.delete(0,tk.END)
			if(self.history_position!=0):
				self.command.insert(0,self.command_history[len(self.command_history)-self.history_position])
		return "break"

	def run(self):
		"GUI Wrapper: Executes turtle command present in text box"

		com_string=self.command.get()
		self.command.delete(0, tk.END)
		self.command_history.append(com_string)
		self.history_position=0

		# self.run_interpeter(com_string)
		self.run_interpeter(com_string)
		self.root.update()

	def get_variable_dictioanry(self):
		'From all scopes selects appropriate variables and outputs dictionary'

		out={}
		for scope in reversed(self.defined_variables):
			for var in scope:
				try:
					out[var]
				except KeyError:
					out[var]=scope[var]
		out.update({'#x':self.t.position[0],'#y':self.t.position[1],'#a':self.t.position[2],'#p':self.t.pen})
		return out

	def run_interpeter(self,com_string):
		'New Command interpreter supporting variable and function assignment'

		loop_detection=0
		asingment_detection=0
		braket_level=0

		for pos,char in enumerate(com_string):
			if(braket_level==0 and char=='='): 
				asingment_detection=1
			elif(braket_level==0 and char=='{'):
				loop_detection=1

			if(char=='[' or char=='(' or char=='{'):
				braket_level+=1
			elif(char==']' or char==')' or char=='}'):
				braket_level-=1

			elif(char==';' and braket_level==0):
				next_com_string=com_string[pos+1:]
				com_string=com_string[:pos]
				break

		com_string=com_string.strip()

		if(loop_detection==1 and asingment_detection==1):
			self.definition_parse(com_string)
			# print('function detected')
			

		elif(loop_detection==0 and asingment_detection==1):
			# print('variable detected')
			self.assingment_parse(com_string)


		elif(loop_detection==1 and asingment_detection==0):
			# print('loop detected')
			self.loop_parse(com_string)

		else:
			# print('command detected')
			self.command_parse(com_string)
			
		try:
			self.run_interpeter(next_com_string)
		except UnboundLocalError:
			pass

		# self.root.update()

	def command_parse(self,st):
		
		#Space as function delimiter
		li=st.split(' ')

		# self.command_palete[li.pop(0)](*map(lambda x: treeParser(x).travel()() ,li))

		#Combine built-in and user defined functions
		combined_comands = dict(list(self.command_palete.items()) + list(self.defined_funcations.items()))

		#Execute command with arguments parsed
		combined_comands[li.pop(0)](*list(map(lambda x: DictParser(x).travel()(**self.get_variable_dictioanry()) ,li)))
	
	def loop_parse(self,st):

		self.defined_variables.append({})

		comands_to_loop=st.split('{',1)[1][:-1]

		loop_args=st.split('{',1)[0].strip().split(' ')

		self.defined_variables[len(self.defined_variables)-1][loop_args[0]]=0

		max_counter=int(DictParser(loop_args[1]).travel()(**self.get_variable_dictioanry()))

		while(self.defined_variables[len(self.defined_variables)-1][loop_args[0]]<max_counter):
			self.run_interpeter(comands_to_loop)
			self.defined_variables[len(self.defined_variables)-1][loop_args[0]]+=1

		self.defined_variables.pop() 

	def assingment_parse(self,st):

		li=st.split('=')
		li=list(map(lambda x: x.strip(), li))

		self.defined_variables[len(self.defined_variables)-1][li[0]]=DictParser(li[1]).travel()(**self.get_variable_dictioanry())

		try:
			self.t.position[0]=self.defined_variables[len(self.defined_variables)-1]['#x']
		except KeyError:
			pass

		try:
			self.t.position[1]=self.defined_variables[len(self.defined_variables)-1]['#y']
		except KeyError:
			pass

		try:
			self.t.position[2]=self.defined_variables[len(self.defined_variables)-1]['#a']
		except KeyError:
			pass

		try:
			self.t.pen=self.defined_variables[len(self.defined_variables)-1]['#p']
		except KeyError:
			pass

	def definition_parse(self,st):
		definition,comand_content=st.split('=',1)

		definition=definition.strip()
		comand_content=comand_content[1:-1]

		definition=definition.split(' ')
		name=definition.pop(0)

		def some_function(*args):

			assert len(args)==len(definition)
			self.defined_variables.append(dict(zip(definition,args)))
			self.run_interpeter(comand_content)
			self.defined_variables.pop() 

		self.defined_funcations[name]=some_function

	def python_run_slow(self,inpu, length=10, angle=15):
		'Runs pre-iterated l-systems via a python interface'

		single_com={'f':lambda :self.t.forward(length),
					'r':lambda :self.t.forward(-length),
					'+':lambda :self.t.turn(angle),
					'-':lambda :self.t.turn(-angle),
					# 'u':self.t.pen_up,
					# 'd':self.t.pen_down,
					'[':self.t.save_state,
					']':self.t.recall_state}
		self.cancel=False
		for x in inpu:
			if(x in single_com):
				if(self.cancel):
					return
				single_com[x]()
				self.root.update()
				sleep(0.01)

	def python_run(self,inpu, length=10, angle=15):
		'Runs pre-iterated l-systems via a python interface'

		single_com={'f':lambda :self.t.forward(length),
					'r':lambda :self.t.forward(-length),
					'+':lambda :self.t.turn(angle),
					'-':lambda :self.t.turn(-angle),
					# 'u':self.t.pen_up,
					# 'd':self.t.pen_down,
					'[':self.t.save_state,
					']':self.t.recall_state}

		for x in inpu:
			if(x in single_com):
				single_com[x]()

	def iterate(self,num_iter, init_st, rule):
		'l-systems iterator'

		for num in range(num_iter):
			out=[]
			for char in init_st:
				if(char in rule):
					if(type(rule[char])==type([])):
						out.append(choice(rule[char]))
					else:
						out.append(rule[char])

				else:
					out.append(char)

			init_st=''.join(out)

		return init_st

class Turtle:
	'2D turtle object'
	def __init__(self,canvas,initial):
		self.canvas=canvas
		self.position=initial
		self.pen=1
		self.stack=[]

	def clear(self):
		self.canvas.delete(tk.ALL)

	def pen_up(self):
		self.pen=0
	def pen_down(self):
		self.pen=1

	def forward(self,distance):
		old_position=self.position[:]

		self.position[0]=old_position[0]+distance*math.cos(old_position[2]*math.pi/180)
		self.position[1]=old_position[1]+distance*math.sin(old_position[2]*math.pi/180)

		if(self.pen==1):
			self.canvas.create_line(old_position[0],old_position[1],self.position[0],self.position[1])

	def turn(self,angle):
		self.position[2]-=angle

	def save_state(self):
		self.stack.append(self.position[:])

	def recall_state(self):
		self.position=self.stack.pop()


if __name__ == '__main__':
	l=LogoUi(500,center_location=True)

	#Ideas:
	#Special Variables for: color position etc
	#Save and open files
	#L-systems function


	l.root.mainloop()