from db import Update,Read,establish_connection
import random
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer, Qt
from AtmGui import Ui_MainWindow
from Get_OTP import get_OTP
from Banks import Banks_widget  

class Ui_Authentication(QMainWindow):

#open the ATM window after Successful Authentication
    def openWindow(self):
        self.OTP=str(self.otp_text.toPlainText())
        if self.OTP=="":
                self.messagebox("Enter the OTP",2)
        elif self.OTP==self.otp:
                #print("match Found")
                self.choices=[]
                establish_connection()
                self.banks = Read("select bank from customer where ph_no={}".format(self.mono))
        
                for bank in self.banks:
                        self.choices.append(bank[0])

                bank_choice_dialog = Banks_widget(self.choices)
                result = bank_choice_dialog.exec_()
                if result == Banks_widget.Accepted:
                        selected_bank = bank_choice_dialog.selected_banks
                        if selected_bank:
                                #print(f"Selected bank: {selected_bank}")
                                establish_connection()
                                #retriving encrypted pin from database
                                #self.pin = Read("select pin from customer where ph_no='{}' and bank='{}'".format(self.mono,selected_bank))[0][0] 
                                self.window = QtWidgets.QMainWindow()
                                self.ui=Ui_MainWindow()
                                self.ui.setupUi(self.window,self.mono,selected_bank)
                                self.window.show()
                                self.otp_text.setText("")
                                self.textEdit_2.setText("")
                                self.otp_text.setEnabled(False)
                                self.textEdit_2.setDisabled(False)
                else:
                        pass
                
        else:
                #print("Enter Valid OTP")
                self.messagebox("Enter Valid OTP",2)
    
    def start_timer(self):
        self.remaining_time = 90
        self.timer.start(1000)          #Update the timer label every 1000 ms (1 second)
        self.timer_thread = threading.Timer(90.0, self.change_otp) 
        self.timer_thread.start()

    def update_timer_label(self):
        self.remaining_time -= 1
        if self.remaining_time >= 0:
                self.timer_label.setText(f"OTP valid till: {self.remaining_time} Sec")
        else:
                self.timer_label.setText("")
                self.otp=self.change_otp()
                self.timer.stop()
                self.timer_thread.cancel()
        
    def change_otp(self):
        otp = ''.join(random.choices('0123456789', k=6))
        return otp

    def setupUi(self, Authentication):

        self.remaining_time = 90  #Initial timer duration (seconds)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer_label)

        self.flag=0
        self.pin=""

        Authentication.setObjectName("Authentication")
        Authentication.resize(1100, 729)
        self.centralwidget = QtWidgets.QWidget(Authentication)
        self.centralwidget.setObjectName("centralwidget")

        self.msg = QtWidgets.QMessageBox()

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1101, 811))
        self.label.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.05, y1:0.0280455, x2:1, y2:1, stop:0.38806 rgba(29, 171, 173, 255), stop:1 rgba(0, 0, 58, 255));\n"
"background-color: qlineargradient(spread:pad, x1:0.124378, y1:0.119, x2:1, y2:1, stop:0.18408 rgba(37, 37, 37, 255), stop:0.850746 rgba(74, 74, 74, 255));")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(160, 40, 351, 41))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 20pt \"MS Serif\";")
        self.label_2.setObjectName("label_2")
        self.send_otp = QtWidgets.QPushButton(self.centralwidget)
        self.send_otp.setGeometry(QtCore.QRect(250, 180, 151, 61))
        self.send_otp.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.send_otp.setStyleSheet("background-color: rgb(0, 89, 255);\n"
"border-radius:10px;\n"
"font: 75 16pt \"MS Shell Dlg 2\";\n"
"color: rgb(85, 255, 255);")
        self.send_otp.setObjectName("send_otp")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(260, 280, 141, 41))
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 20pt \"MS Serif\";")
        self.label_3.setObjectName("label_3")
        self.otp_text = QtWidgets.QTextEdit(self.centralwidget)
        self.otp_text.setGeometry(QtCore.QRect(140, 320, 371, 71))
        self.otp_text.setStyleSheet("background-color: rgb(0, 0, 40);\n"
"font: 75 28pt \"MS Shell Dlg 2\";\n"
"color: rgb(199, 251, 255);\n"
"border-radius:10px;\n"
"border-bottom:2px solid white;\n"
"background-color: rgb(99, 99, 99);")
        self.otp_text.setObjectName("otp_text")
        self.otp_text.setDisabled(True)
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(60, 90, 541, 71))
        self.textEdit_2.setStyleSheet("background-color: rgb(99, 99, 99);\n"
"font: 75 28pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 255, 255);\n"
"border-radius:10px;\n"
"border-bottom:2px solid white;\n"
"color: rgb(199, 251, 255);")
        self.textEdit_2.setTabChangesFocus(False)
        self.textEdit_2.setObjectName("textEdit_2")
        self.continue_2 = QtWidgets.QPushButton(self.centralwidget)
        self.continue_2.setGeometry(QtCore.QRect(150, 410, 170, 50))
        self.continue_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.continue_2.setStyleSheet("background-color:rgb(90, 90, 90);\n"
"font: 22pt \"MV Boli\";\n"
"color:rgb(0, 170, 255);\n"
"border-radius:5px;")
        self.continue_2.setObjectName("continue_2")
        self.reset = QtWidgets.QPushButton(self.centralwidget)
        self.reset.setText("Reset")
        self.reset.setGeometry(QtCore.QRect(330, 410, 170, 50))
        self.reset.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.reset.setStyleSheet("background-color:rgb(90, 90, 90);\n"
"font: 22pt \"MV Boli\";\n"
"color:red;\n"
"border-radius:5px;")
        self.reset.setObjectName("RESET")

        self.timer_label = QtWidgets.QLabel(self.centralwidget)
        self.timer_label.setGeometry(QtCore.QRect(180, 465, 300, 50))
        self.timer_label.setStyleSheet("color: white;\n"
"font: 75 20pt \"MS Serif\";")
        self.timer_label.setObjectName("timer_label")

        self.four = QtWidgets.QPushButton(self.centralwidget)
        self.four.setGeometry(QtCore.QRect(700, 170, 81, 71))
        self.four.setStyleSheet("font: 75 20pt \"Tw Cen MT\";\n"
"background-color: rgb(255, 255, 255);\n"
"color: black;\n"
"border-radius:5px;")
        self.four.setObjectName("four")
        self.three = QtWidgets.QPushButton(self.centralwidget)
        self.three.setGeometry(QtCore.QRect(900, 90, 81, 71))
        self.three.setStyleSheet("font: 75 20pt \"Tw Cen MT\";\n"
"background-color: rgb(255, 255, 255);\n"
"color: black;\n"
"border-radius:5px;")
        self.three.setObjectName("three")
        self.two = QtWidgets.QPushButton(self.centralwidget)
        self.two.setGeometry(QtCore.QRect(800, 90, 81, 71))
        self.two.setStyleSheet("font: 75 20pt \"Tw Cen MT\";\n"
"background-color: rgb(255, 255, 255);\n"
"color: black;\n"
"border-radius:5px;")
        self.two.setObjectName("two")
        self.one = QtWidgets.QPushButton(self.centralwidget)
        self.one.setGeometry(QtCore.QRect(700, 90, 81, 71))
        self.one.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.one.setStyleSheet("font: 75 20pt \"Tw Cen MT\";\n"
"background-color: rgb(255, 255, 255);\n"
"color: black;\n"
"border-radius:5px;")
        self.one.setObjectName("one")
        self.five = QtWidgets.QPushButton(self.centralwidget)
        self.five.setGeometry(QtCore.QRect(800, 170, 81, 71))
        self.five.setStyleSheet("font: 75 20pt \"Tw Cen MT\";\n"
"background-color: rgb(255, 255, 255);\n"
"color: black;\n"
"border-radius:5px;")
        self.five.setObjectName("five")
        self.six = QtWidgets.QPushButton(self.centralwidget)
        self.six.setGeometry(QtCore.QRect(900, 170, 81, 71))
        self.six.setStyleSheet("font: 75 20pt \"Tw Cen MT\";\n"
"background-color: rgb(255, 255, 255);\n"
"color: black;\n"
"border-radius:5px;")
        self.six.setObjectName("six")
        self.seven = QtWidgets.QPushButton(self.centralwidget)
        self.seven.setGeometry(QtCore.QRect(700, 250, 81, 71))
        self.seven.setStyleSheet("font: 75 20pt \"Tw Cen MT\";\n"
"background-color: rgb(255, 255, 255);\n"
"color: black;\n"
"border-radius:5px;")
        self.seven.setObjectName("seven")
        self.eight = QtWidgets.QPushButton(self.centralwidget)
        self.eight.setGeometry(QtCore.QRect(800, 250, 81, 71))
        self.eight.setStyleSheet("font: 75 20pt \"Tw Cen MT\";\n"
"background-color: rgb(255, 255, 255);\n"
"color: black;\n"
"border-radius:5px;")
        self.eight.setObjectName("eight")
        self.nine = QtWidgets.QPushButton(self.centralwidget)
        self.nine.setGeometry(QtCore.QRect(900, 250, 81, 71))
        self.nine.setStyleSheet("font: 75 20pt \"Tw Cen MT\";\n"
"background-color: rgb(255, 255, 255);\n"
"color: black;\n"
"border-radius:5px;")
        self.nine.setObjectName("nine")
        self.zero = QtWidgets.QPushButton(self.centralwidget)
        self.zero.setGeometry(QtCore.QRect(800, 330, 81, 71))
        self.zero.setStyleSheet("font: 75 20pt \"Tw Cen MT\";\n"
"background-color: rgb(255, 255, 255);\n"
"color: black;\n"
"border-radius:5px;")
        self.zero.setObjectName("zero")
        self.Del = QtWidgets.QPushButton(self.centralwidget)
        self.Del.setGeometry(QtCore.QRect(900, 330, 81, 71))
        self.Del.setStyleSheet("font: 75 20pt \"Tw Cen MT\";\n"
"background-color: rgb(85, 170, 255);\n"
"color: black;\n"
"border-radius:5px;")
        self.Del.setObjectName("DEL")
        self.clr = QtWidgets.QPushButton(self.centralwidget)
        self.clr.setGeometry(QtCore.QRect(700, 330, 81, 71))
        self.clr.setStyleSheet("font: 75 20pt \"Tw Cen MT\";\n"
"background-color: red;\n"
"color: black;\n"
"border-radius:5px;")
        self.clr.setObjectName("clr")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(0, 570, 1101, 201))
        self.label_4.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(1050, 0, 61, 681))
        self.label_5.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(-10, 0, 61, 701))
        self.label_6.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(80, 620, 941, 51))
        self.textBrowser.setStyleSheet("font: 18pt \"Rockwell Condensed\";\n"
"background-color: transparent;\n"
"color: rgb(255, 255, 255);\n"
"border:none;")
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setText("")

        Authentication.setCentralWidget(self.centralwidget)

        self.retranslateUi(Authentication)
        QtCore.QMetaObject.connectSlotsByName(Authentication)

#action to be perform for each button
        self.continue_2.clicked.connect(self.openWindow)
        self.send_otp.clicked.connect(self.Send_OTP)
        
        self.zero.clicked.connect(self.Zero)
        self.one.clicked.connect(self.One)
        self.two.clicked.connect(self.Two)
        self.three.clicked.connect(self.Three)
        self.four.clicked.connect(self.Four)
        self.five.clicked.connect(self.Five)
        self.six.clicked.connect(self.Six)
        self.seven.clicked.connect(self.Seven)
        self.eight.clicked.connect(self.Eight)
        self.nine.clicked.connect(self.Nine)
        self.clr.clicked.connect(self.CLR)
        self.Del.clicked.connect(self.DEL)
        self.reset.clicked.connect(self.Reset)

#function for each action, to be perform after clicking button

    def Zero(self):
        if self.flag==0:
                self.textEdit_2.setText(self.textEdit_2.toPlainText()+"0")
        if self.flag==1:
                self.otp_text.setText(self.otp_text.toPlainText()+"0")
    def One(self):
        if self.flag==0:
                self.textEdit_2.setText(self.textEdit_2.toPlainText()+"1")
        if self.flag==1:
                self.otp_text.setText(self.otp_text.toPlainText()+"1")
    def Two(self):
        if self.flag==0:
                self.textEdit_2.setText(self.textEdit_2.toPlainText()+"2")
        if self.flag==1:
                self.otp_text.setText(self.otp_text.toPlainText()+"2")
    def Three(self):
        if self.flag==0:
                self.textEdit_2.setText(self.textEdit_2.toPlainText()+"3")
        if self.flag==1:
                self.otp_text.setText(self.otp_text.toPlainText()+"3")
    def Four(self):
        if self.flag==0:
                self.textEdit_2.setText(self.textEdit_2.toPlainText()+"4")
        if self.flag==1:
                self.otp_text.setText(self.otp_text.toPlainText()+"4")
    def Five(self):
        if self.flag==0:
                self.textEdit_2.setText(self.textEdit_2.toPlainText()+"5")
        if self.flag==1:
                self.otp_text.setText(self.otp_text.toPlainText()+"5")
    def Six(self):
        if self.flag==0:
                self.textEdit_2.setText(self.textEdit_2.toPlainText()+"6")
        if self.flag==1:
                self.otp_text.setText(self.otp_text.toPlainText()+"6")
    def Seven(self):
        if self.flag==0:
                self.textEdit_2.setText(self.textEdit_2.toPlainText()+"7")
        if self.flag==1:
                self.otp_text.setText(self.otp_text.toPlainText()+"7")
    def Eight(self):
        if self.flag==0:
                self.textEdit_2.setText(self.textEdit_2.toPlainText()+"8")
        if self.flag==1:
                self.otp_text.setText(self.otp_text.toPlainText()+"8")
    def Nine(self):
        if self.flag==0:
                self.textEdit_2.setText(self.textEdit_2.toPlainText()+"9")
        if self.flag==1:
                self.otp_text.setText(self.otp_text.toPlainText()+"9")
        
    def CLR(self):
        if self.flag==0:
                self.textEdit_2.setText("")
        if self.flag==1:
                self.otp_text.setText("")
    def DEL(self):
        if self.flag==0:
                self.textEdit_2.setText(self.textEdit_2.toPlainText()[:-1])
        if self.flag==1:
                self.otp_text.setText(self.otp_text.toPlainText()[:-1])

        #method to send the OTP
    def Send_OTP(self):
        self.mono=self.textEdit_2.toPlainText()
        print(self.mono)
        if len(self.mono)!=10 or self.mono=="":
                print("Enter valid 10-DIGIT Mobile No.")
                self.messagebox("Enter valid 10-DIGIT Mobile No.",2)
        else:   
                establish_connection()
                #we are just checking either account exists for the NUMBER or not(retriving data as pin no or anything)
                self.pin=Read("select pin from customer where ph_no={}".format(self.mono))[0][0]
                if self.pin != None:
                        self.otp=self.change_otp()
                        get_OTP(self.mono,self.otp)
                        self.start_timer()
                        self.flag=1
                        self.otp_text.setEnabled(True)
                        self.textEdit_2.setDisabled(True)
                else:
                        print("Account not EXISTS!!")
                        self.messagebox("Account not EXISTS!!",2)


    def Reset(self):
        self.flag=0
        self.otp_text.setText("")
        self.textEdit_2.setText("")
        self.otp_text.setEnabled(False)
        self.textEdit_2.setDisabled(False)

    #type 1= information message / type 2 = warning message
    def messagebox(self,message,type):     
        self.message=message
        self.type=type
                
        if self.type==1:
                self.msg.setIcon(self.msg.Information)

                # setting message for Message Box
                self.msg.setText(self.message)

                # setting Message box window title
                self.msg.setWindowTitle("Transaction Successful !!!")

                # declaring buttons on Message Box
                self.msg.setStandardButtons(self.msg.Ok | self.msg.Cancel)

        if self.type==2:
                self.msg.setIcon(self.msg.Warning)

                # setting message for Message Box
                self.msg.setText(self.message)

                # setting Message box window title
                self.msg.setWindowTitle("!!! Warning !!!")

                # declaring buttons on Message Box
                self.msg.setStandardButtons(self.msg.Ok | self.msg.Cancel)

        # start the app
        retval = self.msg.exec_()


    def retranslateUi(self, Authentication):
        _translate = QtCore.QCoreApplication.translate
        Authentication.setWindowTitle(_translate("Authentication", "MainWindow"))
        self.label_2.setText(_translate("Authentication", "Enter your mobile number"))
        self.send_otp.setText(_translate("Authentication", "SEND OTP"))
        self.label_3.setText(_translate("Authentication", "Enter OTP"))
        self.otp_text.setHtml(_translate("Authentication", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:28pt; font-weight:72; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textEdit_2.setHtml(_translate("Authentication", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:28pt; font-weight:72; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.continue_2.setText(_translate("Authentication", "Continue"))
        self.four.setText(_translate("Authentication", "4"))
        self.three.setText(_translate("Authentication", "3"))
        self.two.setText(_translate("Authentication", "2"))
        self.one.setText(_translate("Authentication", "1"))
        self.five.setText(_translate("Authentication", "5"))
        self.six.setText(_translate("Authentication", "6"))
        self.seven.setText(_translate("Authentication", "7"))
        self.eight.setText(_translate("Authentication", "8"))
        self.nine.setText(_translate("Authentication", "9"))
        self.zero.setText(_translate("Authentication", "0"))
        self.Del.setText(_translate("Authentication", "DEL"))
        self.clr.setText(_translate("Authentication", "CLR"))
        self.textBrowser.setHtml(_translate("Authentication", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Rockwell Condensed\'; font-size:18pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Please enter your Mobile number &amp; click on &quot;SEND OTP&quot;</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Authentication = QtWidgets.QMainWindow()
    ui = Ui_Authentication()
    ui.setupUi(Authentication)
    Authentication.show()
    sys.exit(app.exec_())
