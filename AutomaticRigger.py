import pymel.core as pm
from PySide2 import QtCore, QtGui, QtWidgets

guiWindow = QtWidgets.QWidget()
guiWindow.resize(300,100)
guiWindow.setWindowTitle("Simple Automatic FK Rig")

mainLayout = QtWidgets.QVBoxLayout(guiWindow)
groupBox = QtWidgets.QGroupBox("Basic options")
basicOptionLayout = QtWidgets.QVBoxLayout()

mainLayout.addWidget(groupBox)    

groupControllers = QtWidgets.QCheckBox("Group CTRLs")
setNurbScale = QtWidgets.QCheckBox("Set CTRLs Scale")
groupBox.setLayout(basicOptionLayout)    
scaleSize = QtWidgets.QLabel()
scaleSize.setText("Scale size")

inputsection = QtWidgets.QLineEdit()
inputsection.resize(30, 30)

#vSectionValidator = QtGui.QIntValidator(0, 1000)
#inputsection.setValidator(vSectionValidator)

basicOptionLayout.addWidget(groupControllers)
basicOptionLayout.addWidget(setNurbScale)
basicOptionLayout.addWidget(scaleSize)
basicOptionLayout.addWidget(inputsection)

executeOptions = QtWidgets.QGroupBox("Select your joints and press Create FK CTRL")
executeOptionLayout = QtWidgets.QHBoxLayout()
executeOptions.setLayout(executeOptionLayout)   

exportButton = QtWidgets.QPushButton("Create FK CTRL")
undoButton = QtWidgets.QPushButton("Undo")
closeButton = QtWidgets.QPushButton("Close")

basicOptionLayout.addWidget(exportButton)
basicOptionLayout.addWidget(undoButton)
basicOptionLayout.addWidget(closeButton)

guiWindow.show()
amount = 0
def export():
    global amount 
    targetJoints = pm.ls(sl=True)
    amount = len(targetJoints)
    ctrlgroups = []
    
    for i in range(len(targetJoints)): 
        targetJoint = targetJoints[i]    
        
        ctrl = targetJoint + '_CTRL'
        pm.circle(name=targetJoint + '_CTRL')
        ctrlgroups.append(ctrl)    
        
        jointGrp = targetJoint + '_GRP'
        pm.group( em=True, name=targetJoint + '_GRP' )
        
        parentConstrName = 'tempConstraint'
        pm.parentConstraint( targetJoint, jointGrp, name = parentConstrName, mo=False)
        
        pm.delete(parentConstrName)        
        pm.parent( ctrl, jointGrp )
                
        pm.xform( ctrl, t=(0, 0, 0) )
        pm.xform( ctrl, ro=(0, 90, 0) )
        
        if setNurbScale.isChecked() == True:
            value = float(inputsection.text())
            pm.xform( ctrl, s=(value, value, value) )
        else:
            pm.xform( ctrl, s=(1.0, 1.0, 1.0) )            
        
        pm.makeIdentity( ctrl, apply=True)
        
        pm.orientConstraint( ctrl, targetJoint, w=1 )
        pm.setAttr(ctrl +".translate", lock = 1)
        pm.setAttr(ctrl +".scale", lock = 1)
        
        if groupControllers.isChecked() == True:
            parentjnt = targetJoint.getParent()
            searchname = parentjnt + '_CTRL'
            for i in range(len(ctrlgroups)):  
                if ctrlgroups[i] == searchname:
                    pm.parent(jointGrp, searchname)
                    break
    
    del ctrlgroups[:]
    del targetJoints[:]    

def undoStuff():
    for i in range(amount*13):
        pm.undo()

def closeWidget():
    return guiWindow.close()


undoButton.clicked.connect(undoStuff)
exportButton.clicked.connect(export)
closeButton.clicked.connect(closeWidget)