# Simple Recolor created by konstap
# Created on 25/02/2021

import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore
from functools import partial
import maya.OpenMayaUI as omu
import shiboken2 as sh


# Returns Maya's main window for the Simple UI class
# With out this Maya does not recognize our simpleUI window as part of Maya's UI
def maya_main_window():
    main_window = omu.MQtUtil.mainWindow()
    return sh.wrapInstance(long(main_window), QtWidgets.QWidget)


class SimpleColorOverride(QtWidgets.QDialog):

    COLORS = []

    def __init__(self, parent=maya_main_window()):
        super(SimpleColorOverride, self).__init__(parent)
        self.setWindowTitle("Palette")
        self.setFixedSize(192, 120)
        self.__getColors()
        self.buildUI()

    def __getColors(self):
        # This gets Maya's default indexed RGB palette and
        # maps values into range 0-255
        for i in range(1, 32):
            color = cmds.colorIndex(i, q=True)
            for j, c in enumerate(color):
                color[j] = c * 255
            self.COLORS.append(color)

    def buildUI(self):
        # Layout for the window is vertical
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(0)
        # This adds grid of color swatches into our window
        palette = self.__createPalette()
        for row in palette:
            main_layout.addLayout(row)

    def __setColor(self, color):
        index = self.COLORS.index(color) + 1
        sel = cmds.ls(selection=True)
        if sel:
            for obj in sel:
                cmds.setAttr(obj + ".overrideEnabled", True)
                cmds.setAttr(obj + ".overrideColor", index)
        else:
            cmds.warning("Nothing selected.")


    def __setDefault(self):
        sel = cmds.ls(selection=True)
        if sel:
            for obj in sel:
                cmds.setAttr(obj + ".overrideEnabled", False)
        else:
            cmds.warning("Nothing selected. ")

    def __createSwatch(self, color):
        # This creates color swatch
        swatch = QtWidgets.QPushButton()
        swatch.setFixedSize(QtCore.QSize(24, 24))
        swatch.setStyleSheet("background-color: rgb(%s, %s, %s)"
                             % (color[0], color[1], color[2]))
        # This adds functionality to out swatch
        swatch.clicked.connect(partial(self.__setColor, color))
        return swatch

    def __createPalette(self):
        swatches = []
        # This creates color reset button for the swatch palette
        reset = QtWidgets.QPushButton("0")
        reset.setFixedSize(QtCore.QSize(24, 24))
        reset.clicked.connect(self.__setDefault)
        swatches.append(reset)
        # This creates color swatches for the swatch palette
        for color in self.COLORS:
            swatch = self.__createSwatch(color)
            swatches.append(swatch)
        # This creates 4 color swatch rows to the palette
        # There is 8 color swatches on a each row
        palette = []
        for y in range(4):
            palette_row = QtWidgets.QHBoxLayout()
            palette_row.setSpacing(0)
            palette_row.setContentsMargins(0, 0, 0, 0)
            for x in range(8):
                swatch = swatches.pop(0)
                palette_row.addWidget(swatch)
            palette.append(palette_row)
        return palette


if __name__ == "__main__":
    # Destroys window if it exist already
    try:
        ui.close()
    except:
        pass
    # Creates a new window
    ui = SimpleColorOverride()
    ui.show()