# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Graphical representation of an ellipse on the QGraphicsScene.
"""

import math
import xml.etree.ElementTree as ET

from ..qt import QtWidgets
from .shape_item import ShapeItem


class EllipseItem(QtWidgets.QGraphicsEllipseItem, ShapeItem):

    """
    Class to draw an ellipse on the scene.
    """

    def __init__(self, width=200, height=200, **kws):
        super().__init__(width=width, height=height, **kws)


    def paint(self, painter, option, widget=None):
        """
        Paints the contents of an item in local coordinates.

        :param painter: QPainter instance
        :param option: QStyleOptionGraphicsItem instance
        :param widget: QWidget instance
        """

        super().paint(painter, option, widget)
        self.drawLayerInfo(painter)

    def toSvg(self):
        """
        Return an SVG version of the shape
        """
        svg = ET.Element("svg")
        svg.set("width", str(self.rect().width()))
        svg.set("height", str(self.rect().height()))

        ellipse = ET.SubElement(svg, "ellipse")
        ellipse.set("cx", str(math.floor(self.rect().width() / 2)))
        ellipse.set("rx", str(math.ceil(self.rect().width() / 2)))
        ellipse.set("cy", str(math.floor(self.rect().height() / 2)))
        ellipse.set("ry", str(math.ceil(self.rect().height() / 2)))

        ellipse = self._styleSvg(ellipse)

        return ET.tostring(svg, encoding="utf-8").decode("utf-8")

