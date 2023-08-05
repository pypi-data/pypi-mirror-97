############################################################
# -*- coding: utf-8 -*-
#
#       #   #  #   #   #    #
#      ##  ##  #  ##  #    #
#     # # # #  # # # #    #  #
#    #  ##  #  ##  ##    ######
#   #   #   #  #   #       #
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
#
# written in python3, (c) 2019-2021 by mworion
#
# Licence APL2.0
#
###########################################################
# standard libraries

# external packages

# local imports
from base.ascomClass import AscomClass


class DomeAscom(AscomClass):
    """
    the class Dome inherits all information and handling of the Dome device. there will be
    some parameters who will define the slewing position of the dome relating to the
    mount.dome = DomeAscom(app=None)
    """

    __all__ = ['DomeAscom',
               ]

    CYCLE_DEVICE = 3000
    CYCLE_DATA = 1000

    def __init__(self, app=None, signals=None, data=None):
        super().__init__(app=app, data=data, threadPool=app.threadPool)

        self.signals = signals
        self.data = data

    def processPolledData(self):
        """
        :return: true for test purpose
        """
        azimuth = self.data.get('ABS_DOME_POSITION.DOME_ABSOLUTE_POSITION', 0)
        self.signals.azimuth.emit(azimuth)

        return True

    def workerPollData(self):
        """
        :return: true for test purpose
        """
        shutterStates = ['Open', 'Closed', 'Opening', 'Closing', 'Error']

        if not self.deviceConnected:
            return False

        azimuth = self.client.Azimuth
        self.dataEntry(azimuth, 'ABS_DOME_POSITION.DOME_ABSOLUTE_POSITION')
        self.signals.azimuth.emit(azimuth)
        self.dataEntry(self.client.Slewing, 'Slewing')
        self.dataEntry(self.client.CanSetAltitude, 'CanSetAltitude')
        self.dataEntry(self.client.CanSetAzimuth, 'CanSetAzimuth')
        self.dataEntry(self.client.CanSetShutter, 'CanSetShutter')

        state = self.client.ShutterStatus
        stateText = shutterStates[state]
        self.dataEntry(stateText, 'Status.Shutter')
        if state == 0:
            self.dataEntry(True,
                           'DOME_SHUTTER.SHUTTER_OPEN',
                           elementInv='DOME_SHUTTER.SHUTTER_CLOSED')
        elif state == 1:
            self.dataEntry(False,
                           'DOME_SHUTTER.SHUTTER_OPEN',
                           elementInv='DOME_SHUTTER.SHUTTER_CLOSED')
        else:
            self.data['DOME_SHUTTER.SHUTTER_OPEN'] = None
            self.data['DOME_SHUTTER.SHUTTER_CLOSED'] = None

        return True

    def slewToAltAz(self, altitude=0, azimuth=0):
        """
        :param altitude:
        :param azimuth:
        :return: success
        """
        if not self.deviceConnected:
            return False

        if self.data.get('CanSetAzimuth'):
            self.callMethodThreaded(self.client.SlewToAzimuth, azimuth)
        if self.data.get('CanSetAltitude'):
            self.callMethodThreaded(self.client.SlewToAltitude, altitude)
        return True

    def openShutter(self):
        """
        :return: success
        """
        if not self.deviceConnected:
            return False

        if self.data.get('CanSetShutter'):
            self.callMethodThreaded(self.client.OpenShutter)
        return True

    def closeShutter(self):
        """
        :return: success
        """
        if not self.deviceConnected:
            return False

        if self.data.get('CanSetShutter'):
            self.callMethodThreaded(self.client.CloseShutter)
        return True

    def abortSlew(self):
        """
        :return: success
        """
        if not self.deviceConnected:
            return False

        self.callMethodThreaded(self.client.AbortSlew)
        return True
