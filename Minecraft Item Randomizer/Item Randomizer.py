from random import randint,choices
from itertools import accumulate
from bisect import bisect_right
import sys,re,webbrowser
from PySide6.QtWidgets import QApplication,QLabel,QWidget,QVBoxLayout,QMainWindow,QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence,QShortcut,QPainter,QPixmap,QColor
class StatusButton(QPushButton):
    def __init__(self,text,parent=None):
        super().__init__(text,parent)
        self.setCheckable(True); self.isHovered=False
        self.SDeactivated=QPixmap("Textures/DeactivatedButtonSide.png")
        self.CDeactivated=QPixmap("Textures/DeactivatedButtonCenter.png")
        self.SActivated=QPixmap("Textures/ActivatedButtonSide.png")
        self.CActivated=QPixmap("Textures/ActivatedButtonCenter.png")
    def enterEvent(self,event):
        self.isHovered=True; self.update()
        super().enterEvent(event)
    def leaveEvent(self,event):
        self.isHovered=False; self.update()
        super().leaveEvent(event)
    def paintEvent(self,event):
        painter=QPainter(self)
        ButtonWidth=self.width(); TextColor=Qt.white
        if self.isChecked(): side,center,Yoffset,ButtonHeight,TiltUp,shadow=self.SActivated,self.CActivated,10,self.height()-10,7,Qt.darkGreen
        else: side,center,Yoffset,ButtonHeight,TiltUp,shadow=self.SDeactivated,self.CDeactivated,0,self.height(),10,Qt.darkRed
        if not center.isNull(): painter.drawPixmap(5,Yoffset,ButtonWidth-10,ButtonHeight,center)
        if not side.isNull(): painter.drawPixmap(0,Yoffset,5,ButtonHeight,side)
        if not side.isNull(): painter.drawPixmap(ButtonWidth-5,Yoffset,5,ButtonHeight,side);
        if self.isHovered:
            painter.setCompositionMode(QPainter.CompositionMode_Plus)
            painter.fillRect(0,Yoffset,ButtonWidth,ButtonHeight,QColor(255,255,240,25))
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        Basetextrect=self.rect().adjusted(0,Yoffset,0,Yoffset-(self.height()-ButtonHeight))
        painter.setPen(shadow)
        shadow_rect=Basetextrect.adjusted(2,-TiltUp+2,2,-TiltUp+2)
        painter.drawText(shadow_rect,Qt.AlignCenter,self.text())
        painter.setPen(TextColor)
        textrect=Basetextrect.adjusted(0,-TiltUp,0,-TiltUp)
        painter.drawText(textrect,Qt.AlignCenter,self.text())
        painter.end()
class ClickableButton(QPushButton):
    def __init__(self,text,parent=None):
        super().__init__(text,parent)
        self.isHovered,self.isPressed=False,False
        self.SUnpressed=QPixmap("Textures/UnpressedButtonSide.png")
        self.CUnpressed=QPixmap("Textures/UnpressedButtonCenter.png")
        self.SPressed=QPixmap("Textures/PressedButtonSide.png")
        self.CPressed=QPixmap("Textures/PressedButtonCenter.png")
        self.SHover=QPixmap("Textures/UnpressedButtonSide.png")
        self.CHover=QPixmap("Textures/UnpressedButtonCenter.png")
    def enterEvent(self,event):
        self.isHovered=True; self.update()
        super().enterEvent(event)
    def leaveEvent(self,event):
        self.isHovered=False; self.update()
        super().leaveEvent(event)   
    def mousePressEvent(self,event):
        self.isPressed=True; self.update()
        super().mousePressEvent(event)
    def mouseReleaseEvent(self,event):
        self.isPressed=False; self.update()
        super().mouseReleaseEvent(event)
    def paintEvent(self,event):
        painter=QPainter(self); ButtonWidth=self.width(); TextColor=Qt.white
        if self.isPressed: side,center,Yoffset,ButtonHeight,TiltUp,shadow=self.SPressed,self.CPressed,13,self.height()-13,7,"#666666"
        elif self.isHovered:
            if hasattr(self, 'side_hover') and not self.SHover.isNull(): side,center=self.SHover,self.CHover
            else: side,center=self.SUnpressed,self.CUnpressed
            Yoffset,ButtonHeight,TiltUp,shadow=0,self.height(),13,"#666666"
        else: side,center,Yoffset,ButtonHeight,TiltUp,shadow=self.SUnpressed,self.CUnpressed,0,self.height(),13,"#666666"
        if not center.isNull(): painter.drawPixmap(5,Yoffset,ButtonWidth-10,ButtonHeight,center)
        if not side.isNull(): painter.drawPixmap(0,Yoffset,5,ButtonHeight,side); painter.drawPixmap(ButtonWidth-5,Yoffset,5,ButtonHeight,side)
        if self.isHovered and not self.isPressed:
            painter.setCompositionMode(QPainter.CompositionMode_Plus); painter.fillRect(0,Yoffset,ButtonWidth,ButtonHeight,QColor(255,255,240,25)); painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        Basetextrect=self.rect().adjusted(0,Yoffset,0,Yoffset-(self.height()-ButtonHeight)); painter.setPen(shadow); shadow_rect=Basetextrect.adjusted(2,-TiltUp+2,2,-TiltUp+2)
        painter.drawText(shadow_rect, Qt.AlignCenter, self.text()); painter.setPen(TextColor); textrect=Basetextrect.adjusted(0,-TiltUp,0,-TiltUp); painter.drawText(textrect,Qt.AlignCenter,self.text()); painter.end()
def isPressed(button):
    if button.isChecked(): return True
    return False
def changeTechnicalSetting(line,newSetting):
    settings,result=open("Technical Settings.txt").read().splitlines(),""
    settings[line]=settings[line][:(settings[line].index(": "))]+": "+newSetting
    for i in settings: result+=i+('\n' if i!=settings[-1] else '')
    file=open("Technical Settings.txt","w"); file.write(result); file.close()
def RandomMinecraftItemPosition(List1,List2,List3):
    settings=open("Technical Settings.txt").read().splitlines()
    groups=["Default item","April Fools item","Education Edition item"]
    booleans=[bool(int(settings[0].split(": ")[1])),bool(int(settings[1].split(": ")[1])),bool(int(settings[2].split(": ")[1]))]; group=["Default","April Fools","Education Edition"]
    ResultingList=List1*int(booleans[0])+List2*int(booleans[1])+List3*int(booleans[2]); Weight=([len(List1)] if booleans[0]>0 else [])+([len(List2)] if booleans[1]>0 else [])+([len(List3)] if booleans[2]>0 else [])
    if len(ResultingList)==0: rolled=(settings[3].split(": ")[1],settings[4].split(": ")[1])
    else:
        position=randint(0,len(ResultingList)-1)
        if sum(booleans)==1: group=group[booleans.index(1)]
        else:
            if booleans==[False,True,True]: group=["April Fools","Education Edition"]
            if booleans==[True,False,True]: group=["Default","Education Edition"]
            if booleans==[True,True,False]: group=["Default","April Fools"]
            Weight=list(accumulate(Weight)); group=group[bisect_right(Weight,position)]
        rolled=(ResultingList[position].replace("\\,", ","),group+" item")
    global ItemRolled,GroupRolled
    ItemRolled,GroupRolled=rolled
    global shadow_label_result,text_label_result,shadow_label_group,text_label_group
    shadow_label_result.setText(ItemRolled); text_label_result.setText(ItemRolled)
    shadow_label_group.setText(GroupRolled); text_label_group.setText(GroupRolled)
    changeTechnicalSetting(3,ItemRolled); changeTechnicalSetting(4,GroupRolled)
    return None
def UpdateViableAmount():
    settings=open("Technical Settings.txt").read().splitlines()
    global AvailableItemsAmount, amount_label_shadow, amount_label
    AvailableItemsAmount=len(Items*int(settings[0].split(': ')[1]) + ItemsAF*int(settings[1].split(': ')[1]) + ItemsEDU*int(settings[2].split(': ')[1]))
    amount_label_shadow.setText(f"Amount of items possible to roll: {AvailableItemsAmount}"); amount_label.setText(f"Amount of items possible to roll: {AvailableItemsAmount}")
    if AvailableItemsAmount==0: amount_label.setStyleSheet(f"background: transparent; border: none; color: #ff8888; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 24px;"); amount_label_shadow.setStyleSheet(f"background: transparent; border: none; color: #552323; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 24px;")
    else: amount_label.setStyleSheet(f"background: transparent; border: none; color: #ffffff; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 24px;"); amount_label_shadow.setStyleSheet(f"background: transparent; border: none; color: #555555; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 24px;")
    return None
def MinecraftWikiLink(Item,Group):
    wikipage=Item.replace(" ","_")
    if wikipage[:15]=="Enchanted_Book_": wikipage=wikipage[15:]
    if wikipage in ["Pufferfish","Tropical_Fish","Mine","Craft","Punch","Move","Build"]: wikipage+="_(item)"
    if wikipage=="Air": wikipage+="_(April_Fools'_joke)"
    elif wikipage=="???": wikipage="Unknown_Element"
    if wikipage[-10:]=="_Spawn_Egg": wikipage=wikipage[:-10]
    if wikipage=="Block_of_Coal" and Group=="April Fools item": wikipage+="_(April_Fools'_joke)"
    if wikipage in ["Iron","Copper","Lead","Gold","Sulfur","Tin","Silver"] and Group=="Education Edition item": wikipage="Element#"+wikipage
    if wikipage=="Water" and Group=="Education Edition item": wikipage+="_(compound)"
    webbrowser.open("https://minecraft.wiki/w/"+wikipage); return None;

Statuses=open("Technical Settings.txt").read().splitlines()
Items=open("Sets of Items/Minecraft items viable for Guess or Die.txt").readline(); Items=Items[:-1].split(", ")
ItemsAF=open("Sets of Items/Minecraft April Fools items.txt").readline(); ItemsAF=re.split(r'(?<!\\), ', ItemsAF[:-1])
ItemsEDU=open("Sets of Items/Minecraft Education Edition items.txt").readline(); ItemsEDU=ItemsEDU[:-1].split(", ")
AvailableItemsAmount=len(Items*int(Statuses[0].split(': ')[1]) + ItemsAF*int(Statuses[1].split(': ')[1]) + ItemsEDU*int(Statuses[2].split(': ')[1]))
ItemRolled,GroupRolled=Statuses[3].split(": ")[1],Statuses[4].split(": ")[1]

GUI,window=QApplication(sys.argv),QWidget()
window.setWindowTitle("Minecraft Item Randomizer")
window.setFixedSize(1000,550)
layout=QVBoxLayout()
block=QWidget(window)
block.setGeometry(16,16,968,60)
block.setStyleSheet("background-color: #717171;")
block=QWidget(window)
block.setGeometry(16,96,968,120)
block.setStyleSheet("background-color: #717171;")
block=QWidget(window)
block.setGeometry(16,236,968,275)
block.setStyleSheet("background-color: #717171;")
block=QWidget(window)
block.setGeometry(64,274,872,139)
block.setStyleSheet("background-color: #8d8d8d;")

shadow_label=QLabel("Enable Minecraft item sets",window)
shadow_label.setGeometry(19,99,968,60)
shadow_label.setStyleSheet(f"background: transparent; border: none; color: #555555; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 24px;")
shadow_label.setAlignment(Qt.AlignCenter)
text_label=QLabel("Enable Minecraft item sets",window)
text_label.setGeometry(16,96,968,60)
text_label.setStyleSheet(f"background: transparent; border: none; color: white; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 24px;")
text_label.setAlignment(Qt.AlignCenter)

shadow_label=QLabel(f"Amount of items possible to roll: {AvailableItemsAmount}",window)
shadow_label.setGeometry(19,19,968,60)
shadow_label.setStyleSheet(f"background: transparent; border: none; color: #555555; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 24px;")
shadow_label.setAlignment(Qt.AlignCenter)
text_label=QLabel(f"Amount of items possible to roll: {AvailableItemsAmount}",window)
text_label.setGeometry(16,16,968,60)
text_label.setStyleSheet(f"background: transparent; border: none; color: #; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 24px;")
text_label.setAlignment(Qt.AlignCenter)
global amount_label_shadow,amount_label; amount_label_shadow,amount_label=shadow_label,text_label
if AvailableItemsAmount==0: amount_label.setStyleSheet(f"background: transparent; border: none; color: #ff8888; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 24px;"); amount_label_shadow.setStyleSheet(f"background: transparent; border: none; color: #552323; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 24px;")
else: amount_label.setStyleSheet(f"background: transparent; border: none; color: #ffffff; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 24px;"); amount_label_shadow.setStyleSheet(f"background: transparent; border: none; color: #555555; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 24px;")

shadow_label=QLabel("Item Rolled:",window)
shadow_label.setGeometry(19,273,968,60)
shadow_label.setStyleSheet(f"background: transparent; border: none; color: #555555; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 32px;")
shadow_label.setAlignment(Qt.AlignCenter)
text_label=QLabel("Item Rolled:",window)
text_label.setGeometry(16,270,968,60)
text_label.setStyleSheet(f"background: transparent; border: none; color: white; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 32px;")
text_label.setAlignment(Qt.AlignCenter)

global shadow_label_result, text_label_result
shadow_label_result=QLabel(Statuses[3].split(": ")[1], window)
shadow_label_result.setGeometry(19,315,968,60)
shadow_label_result.setStyleSheet(f"background: transparent; border: none; color: #555555; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 24px;")
shadow_label_result.setAlignment(Qt.AlignCenter)
text_label_result=QLabel(Statuses[3].split(": ")[1], window)
text_label_result.setGeometry(16,312,968,60)
text_label_result.setStyleSheet(f"background: transparent; border: none; color: white; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 24px;")
text_label_result.setAlignment(Qt.AlignCenter)

global shadow_label_group, text_label_group
shadow_label_group=QLabel(Statuses[4].split(": ")[1], window)
shadow_label_group.setGeometry(19,355,968,60)
shadow_label_group.setStyleSheet(f"background: transparent; border: none; color: #484848; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 20px;")
shadow_label_group.setAlignment(Qt.AlignCenter)
text_label_group=QLabel(Statuses[4].split(": ")[1], window)
text_label_group.setGeometry(16.5,352.5,968,60)
text_label_group.setStyleSheet(f"background: transparent; border: none; color: #DEDEDE; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 20px;")
text_label_group.setAlignment(Qt.AlignCenter)

B=StatusButton("Default items",window); B.setGeometry(160,142,220,65); B.setStyleSheet(f"background: transparent; border: none; color: white; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 18px;")
B.setChecked(bool(int(Statuses[0].split(": ")[1]))); B.clicked.connect(lambda: changeTechnicalSetting(0,str(int(isPressed(B))))); B.clicked.connect(UpdateViableAmount)
C=StatusButton("April Fools items",window); C.setGeometry(400,142,220,65); C.setStyleSheet(f"background: transparent; border: none; color: white; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 18px;")
C.setChecked(bool(int(Statuses[1].split(": ")[1]))); C.clicked.connect(lambda: changeTechnicalSetting(1,str(int(isPressed(C))))); C.clicked.connect(UpdateViableAmount)
E=StatusButton("EDU items",window); E.setGeometry(640,142,220,65); E.setStyleSheet(f"background: transparent; border: none; color: white; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 18px;")
E.setChecked(bool(int(Statuses[2].split(": ")[1]))); E.clicked.connect(lambda: changeTechnicalSetting(2,str(int(isPressed(E))))); E.clicked.connect(UpdateViableAmount)
D=ClickableButton("Roll an item",window); D.setGeometry(300,425,400,65); D.setStyleSheet(f"background: transparent; border: none; color: white; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 18px;")
D.clicked.connect(lambda: RandomMinecraftItemPosition(Items,ItemsAF,ItemsEDU))
W=ClickableButton("Minecraft Wiki",window); W.setGeometry(725,425,200,65); W.setStyleSheet(f"background: transparent; border: none; color: white; font-family: '{Statuses[5].split(': ')[1]}'; font-size: 18px;")
W.clicked.connect(lambda: MinecraftWikiLink(ItemRolled,GroupRolled))

window.setStyleSheet("background-color: #849a76;")
window.setLayout(layout)
window.show()
sys.exit(GUI.exec())
