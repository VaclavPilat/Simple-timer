#!/usr/bin/env python3


from Timer import *
import sys, os


try:
    from PyQt5 import QtGui, QtWidgets, QtCore
except:
    print("Please make sure that you have installed PyQt5 package.")
    sys.exit()


def active():
    start.setVisible(False)
    status_active.setVisible(True)
    stop.setVisible(True)
    status_inactive.setVisible(False)
    tray.setIcon( QtGui.QIcon( os.path.join(os.path.dirname(__file__), "Icon_active.png") ) )


def inactive():
    start.setVisible(True)
    status_active.setVisible(False)
    stop.setVisible(False)
    status_inactive.setVisible(True)
    tray.setIcon( QtGui.QIcon( os.path.join(os.path.dirname(__file__), "Icon_inactive.png") ) )


def start_timestamp():
    timer.start_timestamp()
    timestamps = timer.load()
    if len(timestamps) > 0 and timestamps[-1]["type"] == "start":
        active()


def stop_timestamp():
    timer.stop_timestamp()
    timestamps = timer.load()
    if len(timestamps) > 0 and timestamps[-1]["type"] == "stop":
        inactive()


if __name__ == '__main__':
    timer = Timer()
    app = QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)
    # Creating tray icon
    tray = QtWidgets.QSystemTrayIcon()
    tray.setIcon( QtGui.QIcon( os.path.join(os.path.dirname(__file__), "Icon_default.png") ) )
    tray.setVisible(True)
    # Creating menu
    menu = QtWidgets.QMenu()
    # Creating "labels"
    status_active = QtWidgets.QAction("Timer is active")
    status_active.setEnabled(False)
    menu.addAction(status_active)
    status_inactive = QtWidgets.QAction("Timer is not active")
    status_inactive.setEnabled(False)
    menu.addAction(status_inactive)
    # Start & Stop
    menu.addSeparator()
    start = QtWidgets.QAction("Start")
    start.triggered.connect(start_timestamp)
    menu.addAction(start)
    stop = QtWidgets.QAction("Stop")
    stop.triggered.connect(stop_timestamp)
    menu.addAction(stop)
    # Showing widgets based on file contents
    timestamps = timer.load()
    if len(timestamps) > 0 and timestamps[-1]["type"] == "start":
        active()
    else:
        inactive()
    # Exit button
    menu.addSeparator()
    exitAction = QtWidgets.QAction("Exit")
    exitAction.triggered.connect(app.quit)
    menu.addAction(exitAction)
    tray.setContextMenu(menu)
    # Event loop
    app.exec_()