#!/usr/bin/env python

import os
import sys
import threading, time, random
from PySide.QtGui import *
from PySide.QtCore import *
from opcode import *
        
class CreateCecWidget(QWidget):
    global i2c
    def __init__(self):
        super(CreateCecWidget, self).__init__()
        self.setWindowTitle('CEC Demo')
        self.InitiatorLabel         = QLabel('Initiator',self)
        self.FollowerLabel          = QLabel('Follower',self)
        self.OpcodeLabel            = QLabel('Opcode',self)
        self.operandLabel           = QLabel('Operand',self)
        
        self.cecInitiatorCombo      = QComboBox(self)
        self.cecFollowerCombo       = QComboBox(self)
        self.cecOpcodeCombo         = QComboBox(self)
        self.cecOperandCombo        = QComboBox(self)
        self.cecSendButton          = QPushButton("send", self)
        self.cecClearButton         = QPushButton("clear", self)     
        self.cecDisplay             = QTextEdit(self)
        self.curDisplay             = None
        self.operand                = False
        self.opcode                 = None
        self.cecOperandCombo.addItem("--------------Add--space---- ----------")
        self.cecSendButton.clicked.connect(self.cecSendButtonClick)
        self.cecClearButton.clicked.connect(self.cecClearButtonClick)
        self.cecOpcodeCombo.activated[str].connect(self.cecOpcodeComboClick)
        item = []
        for k in CecLogicalAddress:
            item.append(k)
        item.sort()
        self.cecInitiatorCombo.addItems(item)  
        self.cecFollowerCombo.addItems(item);

        #load the cec opcode    
        cecopcodeList = []
        for k in CecOpcode:
            cecopcodeList.append(k)
        cecopcodeList.sort()            
        self.cecOpcodeCombo.addItems(cecopcodeList)
        
        topVerLayout  = QVBoxLayout()
        
        hlo  = QHBoxLayout()
        hlo.addWidget(self.InitiatorLabel)
        hlo.addWidget(self.cecInitiatorCombo)
        hlo.addWidget(self.FollowerLabel)
        hlo.addWidget(self.cecFollowerCombo)
        hlo.addWidget(self.OpcodeLabel)
        hlo.addWidget(self.cecOpcodeCombo)
        hlo.addWidget(self.operandLabel)
        hlo.addWidget(self.cecOperandCombo)
        hlo2  = QHBoxLayout()
        hlo2.addStretch()
        hlo2.addWidget(self.cecSendButton)
        
        vlo  = QVBoxLayout()
        vlo.addWidget(self.cecDisplay)
        blo  = QHBoxLayout()
        blo.addWidget(self.cecClearButton)
        topVerLayout.addLayout(hlo)
        topVerLayout.addLayout(hlo2)
        topVerLayout.addLayout(vlo)
        topVerLayout.addLayout(blo)
        self.setLayout(topVerLayout)

    def cecOpcodeComboClick(self, text):
        self.cecOperandCombo.clear()
        self.operand = False
        self.operandList = None
        self.opcode = CecOpcode[text]
        if self.opcode in CecOperand:
            self.operandList = CecOperand[self.opcode]
            item1 = []
            for k in self.operandList:
                item1.append(k)
            item1.sort()
            self.cecOperandCombo.addItems(item1)  
            self.operand = True

    #send the cec packet    
    def cecSendButtonClick(self):
        outBufferOpcode = 3
        outdata = []
        outdata.append(outBufferOpcode) 
        initiator = CecLogicalAddress[self.cecInitiatorCombo.currentText()]
        follower  = CecLogicalAddress[self.cecFollowerCombo.currentText()]
        loggicAddr   = (initiator<<4) | follower
        self.opcode = CecOpcode[self.cecOpcodeCombo.currentText()]
        outdata.append(loggicAddr)
        outdata.append(self.opcode)
        val = "%02X:%02X" % (loggicAddr,self.opcode)
        if self.operand:
            operand = self.operandList[self.cecOperandCombo.currentText()]
            outdata.append(operand)    
            val +=  ":%02X" % operand
        cmd = "echo tx " + val + " | cec-client RPI -s -d 1"
        self.cecDisplay.append(self.curDisplay)
        val += "\n"            
        #write packet
        print ('----------------------------------------')
        #print (val)
        print (cmd)
        os.system(cmd)
         
    def cecClearButtonClick(self):
        self.cecDisplay.clear()

    def cecCloseButtonClick(self):
        print 'cecCloseButtonClick'
        self.regThread.threadStop()
        self.regThread.join()
        QMainWindow.closeEvent(self, QCoreApplication.instance().quit)
              
        
def main():
    app = QApplication(sys.argv)
    ex = CreateCecWidget()
    ex.show() 
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()    

