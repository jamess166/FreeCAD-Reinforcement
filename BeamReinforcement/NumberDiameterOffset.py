# -*- coding: utf-8 -*-
# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2019 - Suraj <dadralj18@gmail.com>                      *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

__title__ = "Number Diameter Offset Dialog"
__author__ = "Suraj"
__url__ = "https://www.freecadweb.org"


import os
from PySide2 import QtWidgets, QtCore, QtGui

from Rebarfunc import getdictofNumberDiameterOffset

import FreeCADGui


class _NumberDiameterOffsetDialog:
    def __init__(self, number_diameter_offset_tuple):
        self.NumberDiameterOffsetTuple = number_diameter_offset_tuple
        self.Layers = []
        self.SetsDict = {}
        self.AddSetButtonList = []
        self.RemoveSetButtonList = []
        self.form = FreeCADGui.PySideUic.loadUi(
            os.path.splitext(__file__)[0] + ".ui"
        )
        self.form.setWindowTitle(
            QtWidgets.QApplication.translate(
                "Arch", "Rebar Number Diameter Offset", None
            )
        )
        layers_count = len(self.NumberDiameterOffsetTuple)
        sets_count_list = [
            len(x.split("+")) for x in self.NumberDiameterOffsetTuple
        ]
        number_diameter_offset_dict = getdictofNumberDiameterOffset(
            self.NumberDiameterOffsetTuple
        )
        for layer in range(0, layers_count):
            self.addLayerButtonClicked(layer)
            for sets in range(1, sets_count_list[layer] + 1):
                if sets < sets_count_list[layer]:
                    self.addSetButtonClicked(self.AddSetButtonList[layer])
                _, number, diameter, offset, _ = self.SetsDict[
                    "layer" + str(layer + 1)
                ][sets - 1]
                number.setValue(
                    number_diameter_offset_dict["layer" + str(layer + 1)][
                        sets - 1
                    ][0]
                )
                diameter.setText(
                    str(
                        number_diameter_offset_dict["layer" + str(layer + 1)][
                            sets - 1
                        ][1]
                    )
                    + "mm"
                )
                offset.setText(
                    str(
                        number_diameter_offset_dict["layer" + str(layer + 1)][
                            sets - 1
                        ][2]
                    )
                    + "mm"
                )

    def setupUi(self):
        """This function is used to set values in ui."""
        self.form.scrollArea.setWidget(self.form.dataWidget)
        self.connectSignalSlots()
        print("WIP")

    def connectSignalSlots(self):
        """This function is used to connect different slots in UI to appropriate
        functions."""
        self.form.addLayerButton.clicked.connect(self.addLayerButtonClicked)
        self.form.buttonBox.accepted.connect(self.accept)
        self.form.buttonBox.rejected.connect(lambda: self.form.close())

    def addSetButtonClicked(self, button):
        layer = self.AddSetButtonList.index(button) + 1
        sets = len(self.SetsDict["layer" + str(layer)])
        self.SetsDict["layer" + str(layer)].append([])
        # Create horizontal layout and its components
        h_layout = QtWidgets.QHBoxLayout()
        set_label = QtWidgets.QLabel("Set " + str(sets + 1))
        set_label.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
            )
        )
        number = QtWidgets.QSpinBox()
        number.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
            )
        )
        diameter = QtWidgets.QLineEdit()
        diameter.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
            )
        )
        offset = QtWidgets.QLineEdit()
        offset.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
            )
        )
        h_layout.addWidget(set_label)
        h_layout.addWidget(number)
        h_layout.addWidget(diameter)
        h_layout.addWidget(offset)
        v_layout = self.form.verticalLayout
        index = v_layout.indexOf(button)
        v_layout.insertLayout(index, h_layout)
        self.SetsDict["layer" + str(layer)][-1].append(set_label)
        self.SetsDict["layer" + str(layer)][-1].append(number)
        self.SetsDict["layer" + str(layer)][-1].append(diameter)
        self.SetsDict["layer" + str(layer)][-1].append(offset)
        self.SetsDict["layer" + str(layer)][-1].append(h_layout)

    def removeSetButtonClicked(self, button):
        print("WIP")

    def addLayerButtonClicked(self, layer=None):
        if not layer:
            layer = len(self.Layers)
        layer += 1
        layout = self.form.verticalLayout
        index = layout.indexOf(self.form.addLayerButton)
        # Create Layer label
        layer_label = QtWidgets.QLabel("Layer" + str(layer) + ":")
        layer_label.setFont(QtGui.QFont("Sans", weight=QtGui.QFont.Bold))
        layout.insertWidget(index, layer_label)
        self.Layers.append(layer_label)
        index += 1
        # Create Add Set button
        add_set_button = QtWidgets.QPushButton("Add Set")
        add_set_button.clicked.connect(
            lambda: self.addSetButtonClicked(add_set_button)
        )
        layout.insertWidget(index, add_set_button)
        self.AddSetButtonList.append(add_set_button)
        index += 1
        if layer == 1:
            self.RemoveSetButtonList.append(None)
        else:
            # Create Remove Set Button
            remove_set_button = QtWidgets.QPushButton("Remove Set")
            remove_set_button.clicked.connect(
                lambda: self.removeSetButtonClicked(remove_set_button)
            )
            layout.insertWidget(index, remove_set_button)
            self.RemoveSetButtonList.append(remove_set_button)

        self.SetsDict["layer" + str(layer)] = []
        self.addSetButtonClicked(add_set_button)
        print("WIP")

    def accept(self):
        """This function is executed when 'OK' button is clicked from ui."""
        print("WIP")
        self.form.close()


def runNumberDiameterOffsetDialog(self, number_diameter_offset):
    if isinstance(number_diameter_offset, str):
        number_diameter_offset = (number_diameter_offset,)
    dialog = _NumberDiameterOffsetDialog(number_diameter_offset)
    dialog.setupUi()
    dialog.form.exec_()
    self.NumberDiameterOffsetTuple = dialog.NumberDiameterOffsetTuple
    print("WIP")
