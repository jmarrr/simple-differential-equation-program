import tkinter as tk
import tkFont as tkfont
import tkMessageBox
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class SampleApp(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		
		self.title_font = tkfont.Font(family='Tahoma', size=15, weight="bold")
		self.text_font  = tkfont.Font(family='Verdana', size=12)
		self.head_font  = tkfont.Font(family='Tahoma', size=11, weight="normal")
		self.mini_font  = tkfont.Font(family='Verdana', size=10)
			
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}
		for F in (StartPage, ChemSol, ElCircuit, Circuits1, Circuits2):
			page_name = F.__name__
			frame = F(parent=container, controller=self)
			self.frames[page_name] = frame

			#Put all of the pages in the same location;
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("StartPage")

	def show_frame(self, page_name):
		#Show a frame for the given page name
		frame = self.frames[page_name]
		frame.tkraise()


class StartPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		label = tk.Label(self, text="ODE Applications Simulator", font=controller.title_font)
		label.pack(side="top", fill="x", pady=35)

		button1 = tk.Button(self, text="Chemical Solutions", command=lambda: controller.show_frame("ChemSol"), bg = "lightgrey", font = controller.text_font)
		button2 = tk.Button(self, text="Electric Circuits", command=lambda: controller.show_frame("ElCircuit"), bg = "lightgrey", font = controller.text_font)
		button3 = tk.Button(self, text="Exit", command=lambda: quit(self), bg = "lightgrey", font = controller.text_font)
		button1.pack(pady = 5)
		button2.pack(pady = 5)
		button3.pack(pady = 5)

class ChemSol(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller

		label = tk.Label(self, text="Input the values of the following:", font=controller.head_font)
		home_button2 = tk.Button(self, text="HOME", command=lambda: controller.show_frame("StartPage"), bg = "lightgrey", font = controller.mini_font)
		overflow_butt = tk.Button(self, text = "Tank Overflow", bg = "lightgreen", fg = "black", font = controller.mini_font, command=self.overflowshow)
		filling_butt = tk.Button(self, text = "Tank Filling",bg = "lightgreen", fg = "black", font = controller.mini_font, command=self.fillshow)
		empty_butt = tk.Button(self, text = "Tank Emptying", bg = "lightgreen", fg = "black", font = controller.mini_font, command=self.emptyshow)

		label.grid(row = 0, column = 2)
		home_button2.grid(row = 0, column = 3, sticky = "NE", pady = 10)
		overflow_butt.grid(row = 7, column = 1, padx= 21, sticky = "S", pady = 12)
		filling_butt.grid(row = 7, column = 2)
		empty_butt.grid(row = 7, column = 3)
	
		label_1 = tk.Label(self, text='C(in):', font=controller.head_font)
		label_2 = tk.Label(self, text='X0:', font=controller.head_font)
		label_3 = tk.Label(self, text='q(in):', font=controller.head_font)
		label_4 = tk.Label(self, text='q(out):', font=controller.head_font)
		label_5 = tk.Label(self, text='V0:', font=controller.head_font)
		label_6 = tk.Label(self, text='V(max):', font=controller.head_font)
		
		self.Cin  = tk.Entry(self)
		self.X0  = tk.Entry(self)
		self.qin  = tk.Entry(self)
		self.qout = tk.Entry(self)
		self.V0   = tk.Entry(self)
		self.Vmax = tk.Entry(self)
		
		label_1.grid(row=1, column=1)
		label_2.grid(row=2, column=1)
		label_3.grid(row=3, column=1)
		label_4.grid(row=4, column=1)
		label_5.grid(row=5, column=1)
		label_6.grid(row=6, column=1)

		self.Cin.grid(row=1, column=2)
		self.X0.grid(row=2, column=2)
		self.qin.grid(row=3, column=2)
		self.qout.grid(row=4, column=2)
		self.V0.grid(row=5, column=2)
		self.Vmax.grid(row=6, column=2)		
		self.tmax = 0
		self.fillingx = 0
		self.tx = 0
		self.tempty = 0
		
		
	def maxV(self):
		try:
			CinGet  = int(self.Cin.get())
			qinGet  = int(self.qin.get())  
			qoutGet = int(self.qout.get())  
			V0Get   = int(self.V0.get())  
			VmaxGet = int(self.Vmax.get())  
		except ValueError:
			raise tkMessageBox.showinfo("Invalid Input", "Please enter a valid input")
		
		self.tmax = (VmaxGet - V0Get)/(qinGet - qoutGet)
		self.tempty = V0Get / qoutGet

	def filling(self,X,t):  
		try:
			CinGet  = int(self.Cin.get())
			qinGet  = int(self.qin.get())  
			qoutGet = int(self.qout.get())  
			V0Get   = int(self.V0.get())  
			VmaxGet = int(self.Vmax.get())  
		except ValueError:
			raise tkMessageBox.showinfo("Invalid Input", "Please enter a valid input")
		
		V = (qinGet - qoutGet) * t + V0Get
		
		dXdt = CinGet * qinGet- (X / int(V)) * qoutGet
		return(dXdt)
		
	def fillshow(self):
		X0Get = self.X0.get()
		self.maxV()
		maxtime = self.tmax 
		t = np.linspace(0, maxtime, 100)  
		X = odeint(self.filling,X0Get,t).ravel()
		
		self.fillingx = X
		self.tx = t
		

		fig = plt.figure()
		fig.suptitle('Tank Filling', fontsize=14, fontweight='bold')
		plt.xlabel('Time', fontsize=16)
		plt.ylabel('Salt Concentration', fontsize=16)
		plt.plot(t, X)
		plt.show()

	def overflowing(self,X,t): 
		try:
			CinGet = int(self.Cin.get())
			qinGet = int(self.qin.get())  
			qoutGet  =int(self.qout.get()) 
			V0Get = int(self.V0.get())  
			VmaxGet = int(self.Vmax.get())  
		except ValueError:
			raise tkMessageBox.showinfo("Invalid Input", "Please enter a valid input")
	
		V = VmaxGet
		
		dXdt = CinGet * qinGet - (X / V) * qinGet
		return (dXdt)

	def overflowshow(self):
		t = np.linspace(self.tmax, 100,100)
		X1 = np.interp(self.tmax, self.tx, self.fillingx)
		X = odeint(self.overflowing,X1,t)
		
	
		fig = plt.figure()
		fig.suptitle('Tank Overflowing', fontsize=14, fontweight='bold')
		plt.xlabel('Time', fontsize=16)
		plt.ylabel('Salt Concentration', fontsize=16)
		plt.plot(t,X)
		plt.show()

	def emptying(self,X,t): 
		try:
			CinGet = int(self.Cin.get())
			qinGet = int(self.qin.get())  
			qoutGet = int(self.qout.get())  
			V0Get = int(self.V0.get())  
			VmaxGet = int(self.Vmax.get())                                 
		except ValueError:
			raise tkMessageBox.showinfo("Invalid Input", "Please enter a valid input")                     
		
		dXdt = 0 - (X / V0Get) * qoutGet
		
		return (dXdt)

	def emptyshow(self): 
		self.maxV()
		X2 = self.X0.get()
		t = np.linspace(0,self.tempty,100)     
		X = odeint(self.emptying,X2, t)

		
		fig = plt.figure()
		fig.suptitle('Tank Emptying', fontsize=14, fontweight='bold')
		plt.xlabel('Time Interval', fontsize=16)
		plt.ylabel('Salt Concentration', fontsize=16)
		plt.plot(t,X)
		plt.show()


class ElCircuit(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		
		label 		 = tk.Label(self, text="Select type of circuit:", font=controller.head_font)
		home_button1 = tk.Button(self, text="HOME", command=lambda: controller.show_frame("StartPage"), bg = "lightgrey", font = controller.mini_font)
		rl_butt 	 = tk.Button(self, text="RL Circuit", command=lambda: controller.show_frame("Circuits1"), bg="grey",font=controller.text_font)
		rc_butt 	 = tk.Button(self, text="RC Circuit", command=lambda: controller.show_frame("Circuits2"), bg="grey", font=controller.text_font)
		
		label.grid(row = 0, column = 1, sticky = "N", pady = 10)
		home_button1.grid(row = 0, column = 2, sticky = "NE", pady = 10)
		rl_butt.grid(row = 1, column = 0, padx = 50, pady = 70)
		rc_butt.grid(row = 1, column = 2, padx = 10)



class Circuits1(tk.Frame):   
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller

		label        = tk.Label(self, text="Input the values for the following:", font=controller.head_font)
		home_button1 = tk.Button(self, text="HOME", command=lambda: controller.show_frame("StartPage"), bg="lightgrey", font=controller.mini_font)
		
		self.label_11 = tk.Label(self, text='R(ohms):', font=controller.head_font)
		self.label_22 = tk.Label(self, text='L(Henry):', font=controller.head_font)
		self.label_33 = tk.Label(self, text='E(volts):', font=controller.head_font)
		self.resistance1 = tk.Entry(self)
		self.inductance1 = tk.Entry(self)
		self.voltage1    = tk.Entry(self)

		simulate1_butt = tk.Button(self, text="Simulate", command=self.showcircuit1, bg="lightgreen", font=controller.mini_font)

		label.grid(row = 0, column = 1, sticky = "N", pady = 10, padx = 50)
		home_button1.grid(row = 0, column = 2, sticky = "NE", pady = 10)
		
		self.label_11.grid(row=1, column=0, pady = 10, padx = 20)
		self.label_22.grid(row=2, column=0, pady = 10, padx = 20)
		self.label_33.grid(row=3, column=0, pady = 10, padx = 20)
		
		self.resistance1.grid(row = 1, column = 1)
		self.inductance1.grid(row = 2, column = 1)
		self.voltage1.grid(row = 3, column = 1)
		
		simulate1_butt.grid(row = 4, column = 1, pady = 30)

	def circuit1(self,I,t):
		try:
			R = int(self.resistance1.get())      
			L = int(self.inductance1.get())     
			E = int(self.voltage1.get())     
		except ValueError:
			raise tkMessageBox.showinfo("Invalid Input", "Please use a valid input")	                                  
	
		dIdt = (E/L) - (R*I/L)
		return(dIdt)

	def showcircuit1(self):
		I0 = 0.0
		t = np.linspace(0, 100, 100)
		I = odeint(self.circuit1, I0, t)
		fig = plt.figure(1)
		fig.suptitle('RL Circuit', fontsize=14, fontweight='bold')
		plt.xlabel('Time', fontsize=16)
		plt.ylabel('Current (Amphere)', fontsize=16)
		plt.plot(t,I)
		plt.show()



class Circuits2(tk.Frame):  
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller

		label 		 = tk.Label(self, text="Input the values for the following:", font=controller.head_font)
		home_button1 = tk.Button(self, text="HOME", command=lambda: controller.show_frame("StartPage"), bg="lightgrey", font=controller.mini_font)

		self.label_111 = tk.Label(self, text='R(ohms):', font=controller.head_font)
		self.label_222 = tk.Label(self, text='C(Farads):', font=controller.head_font)
		self.label_333 = tk.Label(self, text='E(volts):', font=controller.head_font)

		self.resistance2 = tk.Entry(self)
		self.inductance2 = tk.Entry(self)
		self.voltage2    = tk.Entry(self)

		self.simulate2_butt = tk.Button(self, text="Simulate", command=self.showcircuit2, bg="lightgreen", font=controller.mini_font)

		label.grid(row = 0, column = 1, sticky = "N", pady = 10, padx = 50)
		home_button1.grid(row = 0, column = 2, sticky = "NE", pady = 10)
		
		self.label_111.grid(row=1, column=0, pady = 10, padx = 20)
		self.label_222.grid(row=2, column=0, pady = 10, padx = 20)
		self.label_333.grid(row=3, column=0, pady = 10, padx = 20)
		
		self.resistance2.grid(row = 1, column = 1)
		self.inductance2.grid(row = 2, column = 1)
		self.voltage2.grid(row = 3, column = 1)
		
		self.simulate2_butt.grid(row = 4, column = 1, pady = 30)
	
	def circuit2(self,Q,t):
		try:
			R = int(self.resistance2.get())      
			C = float(self.inductance2.get())     
			E = int(self.voltage2.get())     
		except ValueError:
			raise tkMessageBox.showinfo("Invalid Input", "Please use a valid input")
		
		dQdt = E / R - (1 / (R * C)) * Q
		return(dQdt)

	def showcircuit2(self):
		Q0 = 0.0
		t = np.linspace(0, 100, 100)
		Q = odeint(self.circuit2, Q0, t)
		fig = plt.figure(1)
		fig.suptitle('RC Circuit', fontsize=14, fontweight='bold')
		plt.xlabel('Time', fontsize=16)
		plt.ylabel('Charge (Columb)', fontsize=16)
		plt.plot(t,Q)
		plt.show()


if __name__ == "__main__":
	app = SampleApp()
	app.resizable(0,0)
	app.geometry('500x250') 
	app.title('Differential Equations')
	app.mainloop()