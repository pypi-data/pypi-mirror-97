import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtWidgets, QtCore
import pyqtgraph.opengl as gl
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
from OpenGL.GL import *
import queue
import time
from ifmO3rViewer.colorbar import Colorbar


class ImageItem(pg.ImageItem):
    pixelSelected = QtCore.Signal(object)

    def __init__(self, **kwargs):
        super().__init__(axisOrder='col-major', **kwargs)
        self.selected = None
        self.pixelSelected.connect(self.on_pixel_selected)

    def paint(self, p, *args):
        super().paint(p, *args)
        if self.selected is not None:
            x, y = self.selected
            p.drawRect(x, y, 1, 1)

    def mousePressEvent(self, event):
        p = event.pos()
        if event.button() == QtCore.Qt.RightButton:
            self.pixelSelected.emit(None)
            event.accept()
            return

        if event.button() == QtCore.Qt.LeftButton:
            x, y = int(p.x()), int(p.y())
            if 0 <= x < self.image.shape[0] and 0 <= y < self.image.shape[1]:
                self.pixelSelected.emit((x, y))
            else:
                self.pixelSelected.emit(None)
            event.accept()
            return

    def on_pixel_selected(self, value):
        self.selected = value


class ImageWidget(QtGui.QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.img = ImageItem(border='w')
        self.info = QtGui.QLabel('')
        self.original = None
        self.img.pixelSelected.connect(self.on_pixel_selected)
        self.colorbar = Colorbar((20, 250), (20, 50))

        glw = pg.GraphicsLayoutWidget()
        view = glw.addViewBox()
        view.setAspectLocked(True)
        view.invertY()
        view.addItem(self.img)
        view.addItem(self.colorbar)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(glw, 0, 0)
        layout.addWidget(self.info, 1, 0)
        self.setLayout(layout)

    def setImage(self, image):
        self.img.setImage(image)
        self.update_info(self.img.selected)

    def update_info(self, selected):
        if selected is None or self.original is None:
            self.info.setText('')
        else:
            x, y = selected
            value = self.original[x, y]
            self.set_label(value, x, y)

    def on_pixel_selected(self, value):
        self.img.on_pixel_selected(value)

    def set_label(self, value):
        self.info.setText("Selected value: {:.3f}".format(value))


class AmplitudeWidget(ImageWidget):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self._logarithmic = True

    def toggle_logarithmic(self):
        self._logarithmic = not self._logarithmic

    def setImage(self, im, cmap=cm.gray):
        im = im.T
        self.original = im.copy()
        with np.errstate(invalid='ignore', divide='ignore'):
            if self._logarithmic:
                im = np.log10(im)
            else:
                im = im.astype(np.float)
            invalid = ~np.isfinite(im)
            im[invalid] = np.nan
            self.colorbar.setIntColorScale(np.nanmin(im), np.nanmax(im), cmap, log=self._logarithmic)
            norm = mpl.colors.Normalize(vmin=np.nanmin(im), vmax=np.nanmax(im))
            m = cm.ScalarMappable(norm=norm, cmap=cmap)
            color = m.to_rgba(im)
        color[invalid, :] = [0, 0, 0, 0]
        super().setImage(color)

    def set_label(self, amp, x, y):
        self.info.setText("[x={:d},y={:d}] amplitude value: {:.3f}".format(x, y, amp))


class DistanceWidget(ImageWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setImage(self, im, cmap=cm.viridis):
        im = im.T
        if not np.any(np.isfinite(im)):
            vmin = 0
            vmax = 1
        else:
            vmin = np.nanmin(im)
            vmax = np.nanmax(im)
        self.colorbar.setIntColorScale(vmin, vmax, cmap)
        self.original = im.copy()
        invalid = np.isnan(im)
        if not np.any(np.isfinite(im)):
            vmin = 0
            vmax = 1
        else:
            vmin = np.nanmin(im)
            vmax = np.nanmax(im)
            if vmax == vmin:
                vmax += 0.1
        norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
        m = cm.ScalarMappable(norm=norm, cmap=cmap)
        color = m.to_rgba(im)
        color[invalid, :] = [0, 0, 0, 0]
        super().setImage(color)

    def set_label(self, value, x, y):
        self.info.setText("[x={:d},y={:d}] distance: {:.3f} [m]".format(x, y, value))


class Crosshair(gl.GLGraphicsItem.GLGraphicsItem):
    def __init__(self, xyz=None, color=(255, 255, 255, 76.5), glOptions='translucent'):
        super().__init__()
        self.setGLOptions(glOptions)
        self.xyz = xyz

    def set(self, xyz):
        self.xyz = xyz

    def paint(self):
        if self.xyz is None:
            return
        self.setupGLState()
        x, y, z = self.xyz
        glBegin(GL_LINES)
        glVertex3f(x - 10, y, z)
        glVertex3f(x + 10, y, z)
        glEnd()
        glBegin(GL_LINES)
        glVertex3f(x, y - 10, z)
        glVertex3f(x, y + 10, z)
        glEnd()
        glBegin(GL_LINES)
        glVertex3f(x, y, z - 10)
        glVertex3f(x, y, z + 10)
        glEnd()


class PointCloud(gl.GLViewWidget):
    selectedCoords = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected = None
        self.pc = gl.GLScatterPlotItem(pos=np.zeros((0, 3)), size=2)
        self.pc.setGLOptions('opaque')

        self.crosshair = Crosshair()
        # self.zgrid = gl.GLGridItem(size=QtGui.QVector3D(10, 10, 1))

        # self.addItem(self.zgrid)
        self.addItem(self.pc)
        self.addItem(self.crosshair)

        self.setMinimumHeight(800)
        self.setMinimumWidth(800)
        self.orbit(90 + 45, 0)
        self.original = None
        self.timestamps = []

    def set(self, X, Y, Z, cmap=cm.viridis):
        self.timestamps.append(time.time())
        if len(self.timestamps) > 10:
            self.timestamps = self.timestamps[-10:]
        X, Y, Z = Z, -X, -Y
        self.original = (X, Y, Z)
        with np.errstate(invalid='ignore', divide='ignore'):
            if not np.any(np.isfinite(X)):
                vmin = 0
                vmax = 1
            else:
                vmin = np.nanmin(X)
                vmax = np.nanmax(X)
            norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
            m = cm.ScalarMappable(norm=norm, cmap=cmap)
            color = m.to_rgba(X.flatten())
        data = np.vstack((X.flatten(), Y.flatten(), Z.flatten())).T.copy()
        self.pc.setData(pos=data, color=color)
        self.update_info(self.selected)

    def update_info(self, selected):
        if self.original is None or selected is None:
            self.selectedCoords.emit(None)
        else:
            py, px = selected
            X, Y, Z = self.original
            x, y, z = X[px, py], Y[px, py], Z[px, py]
            self.selectedCoords.emit((x, y, z) )

    def on_pixel_selected(self, selected):
        self.selected = selected
        if self.original is None or selected is None:
            self.crosshair.set(None)
        else:
            py, px = selected
            X, Y, Z = self.original
            x, y, z = X[px, py], Y[px, py], Z[px, py]
            self.crosshair.set((x, y, z))


class PointCloudWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pc = PointCloud()
        self.info = QtGui.QLabel('')
        self.pc.selectedCoords.connect(self.set_label)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.pc, 0, 0)
        # layout.setRowStretch(0, 100)
        layout.addWidget(self.info, 1, 0)
        # layout.setRowStretch(1, 0)
        self.setLayout(layout)

    def on_pixel_selected(self, selected):
        self.pc.on_pixel_selected(selected)

    def set(self, X, Y, Z, cmap=cm.viridis):
        self.pc.set(X, Y, Z, cmap)

    def set_label(self, value):
        ts = self.pc.timestamps
        framerate = (len(ts)-1)/(ts[-1] - ts[0]) if (len(ts) > 1 and (ts[-1] - ts[0]) > 0) else 0
        if value is None:
            self.info.setText("<table width=\"100%\"><td width=\"50%\" align=\"left\"></td><td width=\"50%\" align=\"right\">framerate: {:.1f} [Hz]</td></table>".format(framerate))
        else:
            x, y, z = value
            self.info.setText("<table width=\"100%\"><td width=\"50%\" align=\"left\">(X, Y, Z): ({:.3f}, {:.3f}, {:.3f}) [m]</td><td width=\"50%\" align=\"right\">framerate: {:.1f} [Hz]</td></table>".format(x, y, z, framerate))


class MainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.aw = AmplitudeWidget()
        self.dw = DistanceWidget()
        self.pcw = PointCloudWidget()

        self.aw.img.pixelSelected.connect(self.dw.on_pixel_selected)
        self.dw.img.pixelSelected.connect(self.aw.on_pixel_selected)
        self.aw.img.pixelSelected.connect(self.pcw.on_pixel_selected)
        self.dw.img.pixelSelected.connect(self.pcw.on_pixel_selected)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.aw, 0, 0)
        layout.addWidget(self.dw, 1, 0)
        layout.addWidget(self.pcw, 0, 1, 2, 1)
        self.setLayout(layout)
        self.pause = False
        self.last = None

    def render(self):
        if self.last is None:
            return
        frame, amp, dist, conf, x, y, z = self.last
        self.aw.setImage(amp)
        self.dw.setImage(dist)
        self.pcw.set(x, y, z)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_P or event.key() == QtCore.Qt.Key_Space:
            self.pause = not self.pause
            event.accept()
        if event.key() == QtCore.Qt.Key_L:
            self.aw.toggle_logarithmic()
            event.accept()
        event.ignore()
        self.render()

    def on_data(self, data):
        frame, amp, dist, conf, x, y, z = data
        if not self.pause:
            self.last = frame, amp, dist, conf, x, y, z
        self.render()


class DataSource(QtCore.QThread):
    # framecnt, amp, dist, conf, x, y, z
    resultReady = QtCore.Signal(object)
    queueClosed = QtCore.Signal()

    def __init__(self, stop, queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stop = stop
        self.queue = queue

    def run(self):
        while not self.stop.is_set():
            try:
                data = self.queue.get(timeout=0.01)
                if data is not None:
                    self.resultReady.emit(data)
                else:
                    self.queueClosed.emit()
            except queue.Empty:
                pass


class MainWindow(QtGui.QMainWindow):
    def __init__(self, stop, queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stop = stop
        self.queue = queue
        self.resize(2 * 800, 800)
        self.widget = MainWidget()
        self.setCentralWidget(self.widget)
        self.thread = DataSource(stop, queue)
        self.thread.resultReady.connect(self.widget.on_data)
        self.thread.queueClosed.connect(self.shutdown)
        self.thread.start()
        self.setWindowTitle('PCIC Client/Viewer')

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Q or event.key() == QtCore.Qt.Key_Escape:
            self.shutdown()
            event.accept()

    def closeEvent(self, event):
        self.shutdown()
        event.accept()

    def shutdown(self):
        self.stop.set()
        self.thread.quit()
        self.close()
