# coding:utf-8
import sys
import os
import json

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QWidget, QCompleter
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, FluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, InfoBadge,
                            InfoBadgePosition, FluentBackgroundTheme, IconWidget, ComboBox, EditableComboBox,
                            PrimaryPushButton, LineEdit, InfoBar, InfoBarPosition)
from qfluentwidgets import FluentIcon as FIF 

data = None
with open("dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        
        # 必须给子界面设置全局唯一的对象名
        self.setObjectName('encoder')

        #initial title
        self.title = QWidget()
        self.title_layout = QHBoxLayout(self.title)
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.setSpacing(10)

        self.title_label = SubtitleLabel("编码器")
        self.title_label.setAlignment(Qt.AlignCenter)
        setFont(self.title_label, 24)
        self.title_label.setFixedHeight(50)

        self.iconWidget = IconWidget(FIF.UNIT)
        self.iconWidget.setFixedWidth(20)
        self.iconWidget.setFixedHeight(20)

        self.title_layout.addWidget(self.iconWidget)
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch(1)

        #encoders
        self.coder = QWidget()
        self.coder.setFixedHeight(200)
        self.coder.setFixedWidth(1200)
        self.coder_layout = QHBoxLayout(self.coder)
        self.coder_layout.setContentsMargins(0, 0, 0, 0)
        self.coder_layout.setSpacing(10)
        

        # initial first selection
        self.first_select = ComboBox()
        self.first_item = ['成品','半成品','材料']
        self.first_select.addItems(self.first_item)
        self.first_select.setPlaceholderText("选择一级分类")
        self.first_select.setCurrentIndex(-1)
        self.first_select.setFixedHeight(50)
        self.first_select.setFixedWidth(200)
        # when selected
        self.first_select.currentIndexChanged.connect(lambda: self.first_select_change(self.first_select.currentText()))
        # 注意使用信号槽函数（一种回调函数），不然在组件生成时就会触发函数导致报错


        # initial second selection
        self.second_select = ComboBox()
        self.second_select.clear()
        self.second_item = []
        self.second_select.addItems(self.second_item)
        self.second_select.setPlaceholderText("选择二级分类")
        self.second_select.setCurrentIndex(-1)
        self.second_select.setFixedHeight(50)
        self.second_select.setFixedWidth(200)


    # 1 from 2 feature
        # initial third selection
        self.third_select = ComboBox()
        self.third_select.clear()
        self.third_item = []
        self.third_select.addItems(self.third_item)
        self.third_select.setPlaceholderText("选择三级分类")
        self.third_select.setCurrentIndex(-1)
        self.third_select.setFixedHeight(50)
        self.third_select.setFixedWidth(200)
        self.third_select.setVisible(True)

        # initial third input
        self.third_input = LineEdit()
        self.third_input.setPlaceholderText("请输入产品号")
        self.third_input.setFixedHeight(50)
        self.third_input.setFixedWidth(200)
        self.third_input.setAlignment(Qt.AlignCenter)
        self.third_input.setVisible(False)

        # initial fourth input
        self.fourth_input = LineEdit()
        self.fourth_input.setPlaceholderText("请输入内部工序码")
        self.fourth_input.setFixedHeight(50)
        self.fourth_input.setFixedWidth(200)
        self.fourth_input.setAlignment(Qt.AlignCenter)
        self.fourth_input.setVisible(False)


        # initial button
        self.button = PrimaryPushButton('开始编码')
        # button click
        self.button.clicked.connect(self.generate_code)
        self.button.setFixedHeight(50)
        

        # initial code
        self.code = LineEdit()
        self.code.setPlaceholderText("等待编码内容输出")
        self.code.setReadOnly(True)
        self.code.setFixedHeight(50)
        self.code.setFixedWidth(200)
        self.code.setAlignment(Qt.AlignCenter)
        

        self.coder_layout.addWidget(self.first_select,0, Qt.AlignLeft)
        self.coder_layout.addWidget(self.second_select,0, Qt.AlignLeft)
        self.coder_layout.addWidget(self.third_select,0, Qt.AlignLeft)
        self.coder_layout.addWidget(self.third_input,0,Qt.AlignLeft)
        self.coder_layout.addWidget(self.fourth_input,0, Qt.AlignLeft)
        self.coder_layout.addStretch(1)
        self.coder_layout.addWidget(self.button,0, Qt.AlignRight)
        self.coder_layout.addWidget(self.code,0,Qt.AlignRight)

        # add to main layout
        main_layout.addWidget(self.title, 0, Qt.AlignTop)
        main_layout.addWidget(self.coder, 1, Qt.AlignCenter)
    

    def first_select_change(self, item):
        second_select_items = {
            '成品': ['工艺类型1','工艺类型2','工艺类型3'],
            '半成品': ['特殊参数1','特殊参数2','原材料代号'],
            '材料': ['添加剂类型1','添加剂类型2','备用分类']
        }

        self.second_select.clear()
        self.second_select.addItems(second_select_items[item])
        self.second_select.setPlaceholderText("选择二级分类")
        self.second_select.setCurrentText("")
        self.second_select.setCurrentIndex(-1)
        
        if item == '成品':
            self.third_select.setVisible(True)
            self.third_input.setVisible(False)
            self.fourth_input.setVisible(False)

            third_select_items = [x for x in data["三级"]]
            self.third_select.clear()
            self.third_select.addItems(third_select_items)
            self.third_select.setPlaceholderText("选择三级分类")
            self.third_select.setCurrentIndex(-1)

        elif item == '半成品':
            self.third_select.setVisible(False)
            self.third_input.setVisible(True)
            self.fourth_input.setVisible(True)
        
        elif item == '材料':
            self.third_select.setVisible(False)
            self.third_input.setVisible(False)
            self.fourth_input.setVisible(False)


    def generate_code(self):
        try:
            if self.first_select.currentText() == '成品' and self.second_select.currentIndex() != -1 and self.third_select.currentIndex() != -1:
                # first level
                firstcode = data["一级"][self.first_select.currentText()]

                # second level
                secondcode = data["二级"][self.second_select.currentText()]

                # third level
                thirdcode = data["三级"][self.third_select.currentText()]
                
                # fourth level
                flowcode = data["四级"][-1] + 1
                data["四级"].append(flowcode)

                encode = firstcode + secondcode + thirdcode + str(flowcode)

                data["编码"].append(encode)
                self.code.setText(encode)
                
                # save the data
                with open("dataset.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

                InfoBar.success(
                    title='生成成功',
                    content="编码内容已生成，请查看",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )

            elif self.first_select.currentText() == '半成品' and self.second_select.currentIndex() != -1 and self.third_input.text() != '' and self.fourth_input.text() != '':
                # first level
                firstcode = data["一级"][self.first_select.currentText()]

                # second level
                secondcode = data["二级"][self.second_select.currentText()]

                # third level
                thirdcode = self.third_input.text()

                # fourth level
                fourthcode = self.fourth_input.text()
                
                if int(thirdcode) in data["四级"]:
                    self.code.setText(firstcode + secondcode + thirdcode + fourthcode)

                    InfoBar.success(
                        title='生成成功',
                        content="编码内容已生成，请查看",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=self
                    )
                
                else:
                    InfoBar.warning(    
                        title='生成失败',
                        content="该产品不存在，请确认产品代码",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=self
                    )
            
            elif self.first_select.currentText() == '材料' and self.second_select.currentIndex() != -1:
                # first level
                firstcode = data["一级"][self.first_select.currentText()]

                # second level
                secondcode = data["二级"][self.second_select.currentText()]

                self.code.setText(firstcode + secondcode + '001')

                InfoBar.success(
                    title='生成成功',
                    content="编码内容已生成，请查看",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )

            else:
                InfoBar.warning(
                    title='警告',
                    content="请选择正确的分类",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )

        except:
            print("Error")
            InfoBar.error(
                title='错误',
                content="请检查输入内容",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )

            
    

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Frame()
    w.show()
    app.exec_()