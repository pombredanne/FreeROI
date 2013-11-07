__author__ = 'zhouguangfu'
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.ticker import MultipleLocator


class VoxelTimePointCurveDialog(QDialog):
    """
    A dialog for action of voxel time point curve display.

    """

    def __init__(self, model, parent=None):
        super(VoxelTimePointCurveDialog, self).__init__(parent)
        self._model = model

        self._init_gui()
        self._create_actions()
        self._plot()

    def _init_gui(self):
        """
        Initialize GUI.

        """
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget,it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.meanlabel = QLabel("Mean:")
        self.varlabel = QLabel("Variance:")

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.meanlabel)
        hlayout.addWidget(self.varlabel)
        layout.addLayout(hlayout)
        self.setLayout(layout)

    def _create_actions(self):
        ''' create actions.'''
        self._model.cross_pos_changed.connect(self._plot)

    def _plot(self):
        ''' plot time time point curve.'''
        xyz = self._model.get_cross_pos()
        points = self._model.get_current_value([xyz[1], xyz[0], xyz[2]],True)
        self.meanlabel.setText("Mean:"+str(points.mean()))
        self.varlabel.setText("Variance:"+str(points.var()))
        # create an axis
        ax = self.figure.add_subplot(111)
        ax.hold(False)
        ax.plot(points, '*-')
        ax.xaxis.set_major_locator(MultipleLocator(2))
        plt.xlabel("Time Point")
        if(isinstance(points,np.ndarray)):
            plt.xlim(0,points.shape[0])
        else:
            plt.xlim(0,1)
        plt.ylabel("Intensity")
        plt.grid()
        self.canvas.draw()

    def closeEvent(self, QCloseEvent):
        self._model.cross_pos_changed.disconnect(self._plot)
