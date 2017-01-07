#staircase generation with PyQt5 for Maya 2017
#Author - Sunil S Nayak
import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
import functools 
import maya.cmds as mc

class stairUI(qw.QDialog):
	def __init__(self):
		#init the main dialog
		qw.QDialog.__init__(self)
		#set window title
		self.setWindowTitle('Stair Generator')
		self.setFixedWidth(400)
		#init the fields
		#height range min, max
		self.hrm = qw.QDoubleSpinBox()
		self.hrM = qw.QDoubleSpinBox()
		self.hrm.setRange(0.0,1000.0)
		self.hrM.setRange(0.0,2000.0)
		#depth range min, max
		self.drm = qw.QDoubleSpinBox()
		self.drM = qw.QDoubleSpinBox()
		self.drm.setRange(0.0,1000.0)
		self.drM.setRange(0.0,2000.0)
		#width range min, max
		self.wrm = qw.QDoubleSpinBox()
		self.wrM = qw.QDoubleSpinBox()
		self.wrm.setRange(0.0,1000.0)
		self.wrM.setRange(0.0,2000.0)
		#init sliders,
		#connect to slideApply function to make dynamic editing possible
		#number of steps
		self.st = qw.QSlider(qc.Qt.Horizontal)
		self.st.setMinimum(10)
		self.st.setMaximum(100)
		self.st.valueChanged.connect(self.slideApply)
		self.st.setValue(50)
		#step gap - divide by 1000
		self.stgp = qw.QSlider(qc.Qt.Horizontal)
		self.stgp.setMinimum(1)
		self.stgp.setMaximum(99)
		self.stgp.valueChanged.connect(self.slideApply)
		#apply button, link to apply function
		btnapp = qw.QPushButton('Apply')
		btnapp.clicked.connect(functools.partial(self.apply))
		#Form layout - add all widgets with labels
		self.setLayout(qw.QFormLayout())
		self.layout().addRow('Height Range: Min:',self.hrm)
		self.layout().addRow('Max:',self.hrM)
		self.layout().addRow(' Width Range: Min:', self.wrm)
		self.layout().addRow('Max:',self.wrM)
		self.layout().addRow(' Depth Range: Min:', self.drm)
		self.layout().addRow('Max:',self.drM)
		self.layout().addRow('Number of Steps:', self.st)
		self.layout().addRow('Step Gap:',self.stgp)
		self.layout().addRow('',btnapp)

	#apply function callback
	def apply(self):
		#delete staircase if it already exists
		sl = mc.ls('Staircase')
		if (len(sl)!=0):
			mc.delete(sl)
			sl = mc.ls('Stair__List')
			mc.delete(sl)
		#build staircase with the other params
		hr = [self.hrm.value(),self.hrM.value()]
		dr = [self.drm.value(),self.drM.value()]
		wr = [self.wrm.value(),self.wrM.value()]
		st = self.st.value()
		sg = (100.0 - float(self.stgp.value()))/100.0
		self.staircase = self.stairs(hr, wr, dr, st, sg)
		sl = mc.ls('Stair__*')
		mc.group(sl,n="Stair__List")

	#function to make the staircase
	#params - pHr - Height range
	#	  pWr - Width range
	#	  pDr - Depth range
	#	  pSt - Number of steps
	#	  pSg - Step Gap
	#return - nothing
	def stairs(self, pHr, pWr, pDr, pSt, pSg):
		pHr = sorted(pHr)
		pWr = sorted(pWr)
		pDr = sorted(pDr)
		h = pHr[1] - pHr[0]
		w = pWr[1] - pWr[0]
		d = pDr[1] - pDr[0]
		d/=pSt
		staircase = []
		#generate staircase step by step and add each step to the staircase list
		for i in range(pSt):
			sht = (h/pSt) * i
			single = h/pSt
			sh = sht + single/2
			sd = (i+0.5)*(d)
			cube = mc.polyCube(h = pSg, n = "Stair__"+str(i+1))
			staircase.append(cube)
			mc.move(w/2, sh, sd, cube)
			mc.scale(w, single, d, cube)
		staircase = mc.polyUnite(*staircase, n = "Staircase")
		return staircase

	def slideApply(self):
		sl = mc.ls('Staircase')
		if(len(sl)==0):
			return
		else:
			self.apply()

s = stairUI()
s.show()
