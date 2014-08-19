'''
This program is a checkbook balancer.  By: Trevor Hampton; On:1/17/10

The Checkbook Balancer app allows a person to easily input values that are normally seen on a check; pay to the
the order of, the date, the amount spent, etc.  The user must input the amount of money in their account and
program will calculate the total amount of money spent from all the checks the user inputed and subtract that
from the amount of money in the account.  The user can also input checks and cash deposits like a deposit slip.
The program will calculate the subtotal of all the money the user deposited and add that to the amount of money
in the account.
'''

import wx #This imports the wxPython functions that allow you to make a GUI for the program.
import pickle
from wx.lib.sheet import CSheet #This allows you to use functions that, when run make a spreadsheet.
from updateCheck import Updater
import time #This imports time functions that can be used to make the current date appear by default, etc.
from icons import checkico, totalico, aboutico, calcico, saveico, openico, printico
import os.path

#Every program in wxPython has to have a class to start the program.  The classes name is MainWindow
class MainWindow(wx.Frame):
	def __init__(self, parent, id, title):
		#These lines create the main program frame that is opened when you run it.
		wx.Frame.__init__(self, parent, id, title, size=(550,302), style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

		#This line creates a panel within the frame.  The panel then becomes the parent of all buttons, static text, etc.
		panel = wx.Panel(self, -1)
		
		self.SetIcon(checkico.GetIcon())

		#These lines create the buttons that are displayed on the main program frame.
		totalbtn = wx.BitmapButton(panel, -1, totalico.GetBitmap(), pos=(500, 180))
		newcheckbtn = wx.Button(panel, -1, 'New Check', pos=(1, 199))
		savebtn = wx.Button(panel, -1, 'Save Check', pos=(newcheckbtn.GetPosition()[0]+newcheckbtn.GetSize()[0]+4, newcheckbtn.GetPosition()[1]))
		delcheck = wx.Button(panel, -1, 'Delete Check', pos=(savebtn.GetPosition()[0]+savebtn.GetSize()[0]+4, savebtn.GetPosition()[1]))

		#These set the mouse over texts.
		totalbtn.SetToolTip(wx.ToolTip('Totals the amount spent and puts it on a spreadsheet'))
		newcheckbtn.SetToolTip(wx.ToolTip('Creates a new check'))
		savebtn.SetToolTip(wx.ToolTip('Saves the current check'))
		delcheck.SetToolTip(wx.ToolTip('Deletes the current check'))

		#This creates a dictionary.  This dictionary is used to save, load, delete and list all the saved checks.
		self.checklist = {}

		#This creates a combo box, or the drop down menu that lists all the checks made.
		self.checks  = wx.ComboBox(panel, -1, pos=(delcheck.GetPosition()[0]+delcheck.GetSize()[0]+4, delcheck.GetPosition()[1]), style=wx.CB_READONLY | wx.CB_SORT)

		updatebtn = wx.Button(panel, -1, 'Check for Updates')
		aboutbtn = wx.BitmapButton(panel, -1, aboutico.GetBitmap(), pos=(totalbtn.GetPosition()[0]-totalbtn.GetSize()[0]-4, totalbtn.GetPosition()[1]))
		depositbtn = wx.Button(panel, -1, 'Deposit', pos=(self.checks.GetPosition()[0]+self.checks.GetSize()[0]+4, self.checks.GetPosition()[1]))
		updatebtn.SetToolTip(wx.ToolTip('Checks for updates to the program'))
		aboutbtn.SetToolTip(wx.ToolTip('Shows who made the program'))
		depositbtn.SetToolTip(wx.ToolTip('For inputing multiple numbers into the account'))
		self.checks.SetToolTip(wx.ToolTip('Lists all saved checks using the check number'))

		#These lines create the text and symbols that you see when you run the program.
		accountamount = wx.StaticText(panel, -1, 'Account $:', pos=(150, 5))
		checknumtxt = wx.StaticText(panel, -1, 'Check #', pos=(400, 5))
		pod = wx.StaticText(panel, -1, 'Pay to the Order of', pos=(25, 75))
		damt = wx.StaticText(panel, -1, 'Dollars', pos=(450,103))
		domt = wx.StaticText(panel, -1, '$', pos=(435, 74))
		date1 = wx.StaticText(panel, -1, 'Date', pos=(350, 30))

		#These lines create the text boxes that let the user type in them.
		self.checknum = wx.TextCtrl(panel, -1, pos=(443, 1))
		self.pdo = wx.TextCtrl(panel, -1, pos=(125, 73), size=(300, -1))
		self.amt = wx.TextCtrl(panel, -1, pos=(98, 100), size=(350, -1))
		self.amount = wx.TextCtrl(panel, -1, pos=(443, 75))
		self.datebox = wx.TextCtrl(panel, -1, pos=(375, 30))
		self.aa = wx.TextCtrl(panel, -1, pos=(210, 1))
		
		self.status = self.CreateStatusBar()

		self.aa.SetValue(str(0.0))

		#This line sets the value of the date text box to the current date.
		self.datebox.SetValue(time.strftime('%m/%d/%y', time.localtime()))
		
		maintoolbar = self.CreateToolBar()
		
		maintoolbar.AddLabelTool(wx.ID_SAVE, '', saveico.GetBitmap())
		maintoolbar.AddLabelTool(wx.ID_OPEN, '', openico.GetBitmap())
		
		maintoolbar.Realize()

		#These lines bind the buttons to an event, which makes the buttons do something.
		self.Bind(wx.EVT_BUTTON, self.newcheckevt, newcheckbtn)
		self.Bind(wx.EVT_BUTTON, self.saveevt, savebtn)
		self.Bind(wx.EVT_BUTTON, self.delevt, delcheck)
		self.Bind(wx.EVT_BUTTON, lambda e: TotalFrame(), totalbtn)
		self.Bind(wx.EVT_BUTTON, lambda e: Updater(self, .8, 'http://seldomridgem.co.cc/trevor/Python Programs/Checkbook Balancer/version.txt', 'http://seldomridgem.co.cc/trevor/'), updatebtn)
		self.Bind(wx.EVT_BUTTON, self.credevt, aboutbtn)
		self.Bind(wx.EVT_BUTTON, lambda e: DepositFrame(), depositbtn)
		self.Bind(wx.EVT_TOOL, self.savechecks, id=wx.ID_SAVE)
		self.Bind(wx.EVT_TOOL, self.openchecks, id=wx.ID_OPEN)

		#This line binds the combo box to an event.
		self.Bind(wx.EVT_COMBOBOX, self.loadevt, self.checks)
		#All the defs create events that are used to make buttons, text boxes, ect do something.
	def newcheckevt(self, event):
		self.checknum.Clear()
		self.pdo.Clear()
		self.amt.Clear()
		self.amount.Clear()
		self.datebox.SetValue(time.strftime('%m/%d/%y', time.localtime()))
	def saveevt(self, event):
		if self.checknum.GetValue() == "":
			self.status.SetStatusText('Cannot save without a check number.')
		else:
			if self.checknum.GetValue() not in self.checklist:
				self.checks.Append(self.checknum.GetValue())
			self.checklist[self.checknum.GetValue()] = [self.pdo.GetValue(), self.amt.GetValue(), self.amount.GetValue(), self.datebox.GetValue()]	
	def loadevt(self, event):
		self.checknum.SetValue(self.checks.GetValue())
		self.pdo.SetValue(self.checklist[self.checks.GetValue()][0])
		self.amt.SetValue(self.checklist[self.checks.GetValue()][1])
		self.amount.SetValue(self.checklist[self.checks.GetValue()][2])
		self.datebox.SetValue(self.checklist[self.checks.GetValue()][3])
	def delevt(self, event):
		if self.checks.GetValue() != "":
				del self.checklist[self.checks.GetValue()]
				self.checks.Delete(self.checks.FindString(self.checks.GetValue()))
	def savechecks(self, event):
		if self.checklist ==  {}:
			self.status.SetStatusText('You have not made any checks.')
		else:
			output = open('Checks.pkl', 'wb')
			pickle.dump(self.checklist, output)
			output.close()
	def openchecks(self, event): 
		if os.path.isfile('Checks.pkl'):
			pkl_file = open('Checks.pkl', 'rb')
			self.checklist = pickle.load(pkl_file)
			pkl_file.close()
			for i in self.checklist.keys():
				self.checks.Append(i)
			self.pdo.SetValue(str(self.checklist['1'][0]))
			self.amt.SetValue(str(self.checklist['1'][1]))
			self.amount.SetValue(str(self.checklist['1'][2]))
			self.datebox.SetValue(str(self.checklist['1'][3]))
		else:
			self.status.SetStatusText('There is no saved file.')
	def credevt(self, event):
		credits = wx.AboutDialogInfo()
		credits.SetIcon(checkico.GetIcon())
		credits.SetName('Checkbook Balancer')
		credits.AddDeveloper('Trevor Hampton')
		credits.AddDocWriter('Trevor Hampton')
		credits.SetVersion('.8')
		credits.SetCopyright('(C) 2010 Trevor Hampton')
		wx.AboutBox(credits)
#This class creates the total window with the spreadsheet that totals all saved checks.
class TotalFrame(wx.Frame):
	def __init__(self):
			if frame.checklist == {}:
				frame.status.SetStatusText('There are no saved checks.')
			else:
				spent = 0.0
				#This is a try and except clause that allows for an error in the code to be replaced with the programmers code when
				#the error is the fault of the user.
				try:
					for val in frame.checklist.values():
						spent += float(val[2])
					inaccount = float(frame.aa.GetValue())
				except ValueError:
					frame.status.SetStatusText('Please input numbers where they are needed.')
					return

				#The next few lines create the frame and spreadsheet.
				numOfChecks = len(frame.checklist)
				cNums = frame.checklist.keys()
				wx.Frame.__init__(self, frame, -1, 'All Checks', size=(550, 250), style=wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.RESIZE_BORDER)

				spreadsheet = CSheet(self)
				spreadsheet.SetNumberRows(numOfChecks + 3)
				spreadsheet.SetNumberCols(5)
				spreadsheet.SetCellValue(0, 0, 'Check #')
				spreadsheet.SetCellValue(0, 1, 'Paid to:')
				spreadsheet.SetCellValue(0, 2, 'Word Amount:')
				spreadsheet.SetCellValue(0, 3, '$ Amount:')
				spreadsheet.SetCellValue(0, 4, 'Date:')
				spreadsheet.SetCellValue(numOfChecks + 1, 0, 'Total Spent:')
				spreadsheet.SetCellValue(numOfChecks + 2, 0, 'In Account:')
				spreadsheet.SetCellValue(numOfChecks + 1, 3, '$' + str(spent))
				spreadsheet.SetCellValue(numOfChecks + 2, 3, '$' + str(inaccount-spent))

				#These lines set the column size based on the last check the user inputed.
				spreadsheet.SetColSize(1, frame.pdo.GetLineLength(0) * 7)
				spreadsheet.SetColSize(2, frame.amt.GetLineLength(0) * 10)

				self.SetIcon(checkico.GetIcon())

				for row in range(1, numOfChecks + 1):
					spreadsheet.SetCellValue(row, 0, cNums[row - 1])
					for col in range(0, 4):
						spreadsheet.SetCellValue(row, col + 1, frame.checklist[cNums[row - 1]][col])
				self.Center()
				self.Show()	
#This class creates the deposit window that appears for you to input multiple checks and cash deposits into the account value.
class DepositFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, frame, -1, 'Deposit', size=(250,250), style=wx.SYSTEM_MENU | wx.CAPTION | wx. MINIMIZE_BOX | wx.CLOSE_BOX)

		panel = wx.Panel(self, -1)

		self.SetIcon(checkico.GetIcon())

		checktxt = wx.StaticText(panel, -1, 'Checks', pos=(1, 0))
		cashtxt = wx.StaticText(panel, -1, 'Cash(Including Coins)', pos=(140, 0))
		numtxt1 = wx.StaticText(panel, -1, '#1', pos=(0, 25))
		numtxt2 = wx.StaticText(panel, -1, '#2', pos=(0, 50))
		numtxt3 = wx.StaticText(panel, -1, '#3', pos=(0, 75))
		numtxt4 = wx.StaticText(panel, -1, '#4', pos=(0, 100))
		numtxt5 = wx.StaticText(panel, -1, '#1', pos=(145, 25))
		numtxt6 = wx.StaticText(panel, -1, '#2', pos=(145, 50))
		numtxt7 = wx.StaticText(panel, -1, '#3', pos=(145, 75))
		numtxt8 = wx.StaticText(panel, -1, '#4', pos=(145, 100))
		subtotal = wx.StaticText(panel, -1, 'Sub Total:', pos=(100, 125))
		subtotalnum = wx.StaticText(panel, -1, '0.0', pos=(117, 150))
		dsign = wx.StaticText(panel, -1, '$', pos=(105, 150))

		checkdeposit1 = wx.TextCtrl(panel, -1, pos=(20, 25), size=(75, -1))
		checkdeposit2 = wx.TextCtrl(panel, -1, pos=(20, 50), size=checkdeposit1.GetSize())
		checkdeposit3 = wx.TextCtrl(panel, -1, pos=(20, 75), size=checkdeposit1.GetSize())
		checkdeposit4 = wx.TextCtrl(panel, -1, pos=(20, 100), size=checkdeposit1.GetSize())

		cashdeposit1 = wx.TextCtrl(panel, -1, pos=(165, 25), size=checkdeposit1.GetSize())
		cashdeposit2 = wx.TextCtrl(panel, -1, pos=(165, 50), size=checkdeposit1.GetSize())
		cashdeposit3 = wx.TextCtrl(panel, -1, pos=(165, 75), size=checkdeposit1.GetSize())
		cashdeposit4 = wx.TextCtrl(panel, -1, pos=(165, 100), size=checkdeposit1.GetSize())

		calcbutton = wx.BitmapButton(panel, -1, calcico.GetBitmap(), pos=(103, 165))
		calcbutton.SetToolTip(wx.ToolTip('Calculates the subtotal'))

		deposits = [checkdeposit1, checkdeposit2, checkdeposit3, checkdeposit4, cashdeposit1, cashdeposit2, cashdeposit3, cashdeposit4]

		def calcsub(event):
			subtotal2 = 0.0
			for i in deposits:
				if str(i.GetValue()) != "":
					subtotal2 += float(i.GetValue())

			subtotalnum.SetLabel(str(subtotal2))
			frame.aa.SetValue(str(float(str(frame.aa.GetValue()))+subtotal2))

		panel.Bind(wx.EVT_BUTTON, calcsub, calcbutton)

		self.Center()
		self.Show()

#Every wx program needs to have an app = wx.App() line.  The app is a variable and a wx.App() is just the way a program is
#started.  The frame lines make the main frame of the program show.
app = wx.App(redirect=False)
frame = MainWindow(None, -1, 'Checkbook Balancer')
frame.Center()
frame.Show()

#This line makes the program run continously.
app.MainLoop()