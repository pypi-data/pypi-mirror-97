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
# Licence APL2.0
#
###########################################################
# standard libraries
import logging
import os

# external packages
import PyQt5
from astropy.io import fits
import numpy as np

# local imports
from mountcontrol.convert import convertToAngle
from base import tpool
from logic.astrometry.astrometryNET import AstrometryNET
from logic.astrometry.astrometryASTAP import AstrometryASTAP


class AstrometrySignals(PyQt5.QtCore.QObject):
    """
    """

    __all__ = ['AstrometrySignals']

    done = PyQt5.QtCore.pyqtSignal(object)
    result = PyQt5.QtCore.pyqtSignal(object)
    message = PyQt5.QtCore.pyqtSignal(object)

    serverConnected = PyQt5.QtCore.pyqtSignal()
    serverDisconnected = PyQt5.QtCore.pyqtSignal(object)
    deviceConnected = PyQt5.QtCore.pyqtSignal(object)
    deviceDisconnected = PyQt5.QtCore.pyqtSignal(object)


class Astrometry:
    """
    the class Astrometry inherits all information and handling of astrometry.net
    handling

    Keyword definitions could be found under
        https://fits.gsfc.nasa.gov/fits_dictionary.html

        >>> astrometry = Astrometry(app=None)
    """

    __all__ = ['Astrometry',
               ]

    log = logging.getLogger(__name__)

    def __init__(self, app):
        self.app = app
        self.tempDir = app.mwGlob['tempDir']
        self.threadPool = app.threadPool
        self.signals = AstrometrySignals()

        self.data = {}
        self.defaultConfig = {'framework': '',
                              'frameworks': {}}
        self.framework = ''
        self.run = {
            'astrometry': AstrometryNET(self),
            'astap': AstrometryASTAP(self),
        }
        for fw in self.run:
            self.defaultConfig['frameworks'].update(self.run[fw].defaultConfig)

        self.mutexSolve = PyQt5.QtCore.QMutex()

    def readFitsData(self, fitsPath):
        """
        readFitsData reads the fits file with the image and tries to get some
        key fields out of the header for preparing the solver. if there is the
        need for understanding more FITS header data, it should be integrated
        in this method.

        :param fitsPath: fits file with image data
        :return: raHint, decHint, scaleHint
        """
        with fits.open(fitsPath) as fitsHDU:
            fitsHeader = fitsHDU[0].header
            scaleHint = float(fitsHeader.get('SCALE', 0))
            ra = fitsHeader.get('RA', 0)
            dec = fitsHeader.get('DEC', 0)
            raHint = convertToAngle(ra, isHours=True)
            decHint = convertToAngle(dec, isHours=False)

        self.log.debug(f'Header RA: {raHint} ({ra}), DEC: {decHint} ({dec})'
                       f', Scale: {scaleHint}')

        return raHint, decHint, scaleHint, ra, dec

    @staticmethod
    def calcAngleScaleFromWCS(wcsHeader=None):
        """
        calcAngleScaleFromWCS as the name says. important is to use the numpy
        arctan2 function, because it handles the zero points and extend the
        calculation back to the full range from -pi to pi

        :return: angle in degrees and scale in arc second per pixel (app) and
                 status if image is mirrored (not rotated for 180 degrees because
                 of the mount flip)
        """
        CD11 = wcsHeader.get('CD1_1', 0)
        CD12 = wcsHeader.get('CD1_2', 0)
        CD21 = wcsHeader.get('CD2_1', 0)
        CD22 = wcsHeader.get('CD2_2', 0)

        mirrored = (CD11 * CD22 - CD12 * CD21) < 0

        angleRad = np.arctan2(CD12, CD11)
        angle = np.degrees(angleRad)
        scale = CD11 / np.cos(angleRad) * 3600

        return angle, scale, mirrored

    def getSolutionFromWCS(self, fitsHeader=None, wcsHeader=None, updateFits=False):
        """
        getSolutionFromWCS reads the wcs fits file and uses the data in the
        header containing the wcs data and returns the basic data needed.
        in addition it embeds it to the given fits file with image. it removes
        all entries starting with some keywords given in selection. we starting
        with HISTORY

        CRVAL1 and CRVAL2 give the center coordinate as right ascension and
        declination or longitude and latitude in decimal degrees.

        the difference is calculated as real coordinate (= plate solved
        coordinate) and mount reported coordinate (= including the errors) and
        set positive in this case.

        we have to take into account if the mount is on the other pierside, the
        image taken will be upside down and the angle will reference a 180
        degrees turned image. this will lead to the negative error value (sign
        will change)

        :param fitsHeader:
        :param wcsHeader:
        :param updateFits:
        :return: ra in hours, dec in degrees, angle in degrees,
                 scale in arcsec/pixel
                 error in arcsec and flag if image is flipped
        """

        self.log.debug(f'wcs header: [{wcsHeader}]')
        raJ2000 = convertToAngle(wcsHeader.get('CRVAL1'), isHours=True)
        decJ2000 = convertToAngle(wcsHeader.get('CRVAL2'), isHours=False)

        angle, scale, mirrored = self.calcAngleScaleFromWCS(wcsHeader=wcsHeader)

        raMount = convertToAngle(fitsHeader.get('RA'), isHours=True)
        decMount = convertToAngle(fitsHeader.get('DEC'), isHours=False)

        deltaRA = (raJ2000._degrees - raMount._degrees) * 3600
        deltaDEC = (decJ2000.degrees - decMount.degrees) * 3600
        error = np.sqrt(np.square(deltaRA) + np.square(deltaDEC))

        solve = {
            'raJ2000S': raJ2000,
            'decJ2000S': decJ2000,
            'errorRA_S': deltaRA,
            'errorDEC_S': deltaDEC,
            'angleS': angle,
            'scaleS': scale,
            'errorRMS_S': error,
            'mirroredS': mirrored,
        }

        if not updateFits:
            return solve, fitsHeader

        fitsHeader.append(('SCALE', solve['scaleS'], 'MountWizzard4'))
        fitsHeader.append(('PIXSCALE', solve['scaleS'], 'MountWizzard4'))
        fitsHeader.append(('ANGLE', solve['angleS'], 'MountWizzard4'))
        fitsHeader.append(('MIRRORED', solve['mirroredS'], 'MountWizzard4'))

        fitsHeader.extend(wcsHeader,
                          unique=True,
                          update=True)

        # remove polynomial coefficients keys if '-SIP' is not selected in
        # CTYPE1 and CTYPE2 this might occur, if you solve a fits file a second
        # time with another solver

        if 'CTYPE1' not in fitsHeader or 'CTYPE2' not in fitsHeader:
            return solve, fitsHeader
        if '-SIP' in fitsHeader['CTYPE1'] and '-SIP' in fitsHeader['CTYPE2']:
            return solve, fitsHeader

        for key in list(fitsHeader.keys()):
            if key.startswith('A_'):
                del fitsHeader[key]
            elif key.startswith('B_'):
                del fitsHeader[key]
            elif key.startswith('AP_'):
                del fitsHeader[key]
            elif key.startswith('BP_'):
                del fitsHeader[key]

        return solve, fitsHeader

    def solveClear(self):
        """
        the cyclic or long lasting tasks for solving the image should not run
        twice for the same data at the same time. so there is a mutex to prevent
        his behaviour.

        :return: true for test purpose
        """
        if self.framework not in self.run:
            return False

        solver = self.run[self.framework]
        self.mutexSolve.unlock()
        self.signals.done.emit(solver.result)
        self.signals.message.emit('')
        return True

    def solveThreading(self, fitsPath='', raHint=None, decHint=None, scaleHint=None,
                       updateFits=False):
        """
        solveThreading is the wrapper for doing the solve process in a
        threadpool environment of Qt. Otherwise the HMI would be stuck all the
        time during solving. it is done with an securing mutex to avoid starting
        solving twice. to solveClear is the partner of solve Threading

        :param fitsPath: full path to the fits image file to be solved
        :param raHint:  ra dest to look for solve in J2000
        :param decHint:  dec dest to look for solve in J2000
        :param scaleHint:  scale to look for solve in J2000
        :param updateFits: flag, if the results should be written to the
                           original file
        :return: success
        """

        if self.framework not in self.run:
            return False

        solver = self.run[self.framework]

        if not os.path.isfile(fitsPath):
            self.signals.done.emit(solver.result)
            return False

        if not self.mutexSolve.tryLock():
            self.log.debug('overrun in solve threading')
            self.signals.done.emit(solver.result)
            return False

        self.signals.message.emit('solving')
        worker = tpool.Worker(solver.solve,
                              fitsPath=fitsPath,
                              raHint=raHint,
                              decHint=decHint,
                              scaleHint=scaleHint,
                              updateFits=updateFits,
                              )
        worker.signals.finished.connect(self.solveClear)
        self.threadPool.start(worker)
        return True

    def abort(self):
        """
        :return:
        """
        if self.framework not in self.run:
            return False

        solver = self.run[self.framework]
        suc = solver.abort()
        return suc

    def checkAvailability(self):
        """
        :return: list of available solutions
        """
        if self.framework not in self.run:
            return False, False

        val = self.run[self.framework].checkAvailability()
        return val

    def startCommunication(self, loadConfig=False):
        """
        :param loadConfig:
        :return: True for test purpose
        """
        self.signals.serverConnected.emit()
        sucApp, sucIndex = self.checkAvailability()
        name = self.run[self.framework].deviceName
        if sucApp and sucIndex:
            self.signals.deviceConnected.emit(name)
            self.app.message.emit(f'ASTROMETRY found:    [{name}]', 0)

        return True

    def stopCommunication(self):
        """
        :return: true for test purpose
        """
        name = self.run[self.framework].deviceName
        self.signals.serverDisconnected.emit({name: 0})
        self.signals.deviceDisconnected.emit(name)
        self.app.message.emit(f'ASTROMETRY remove:   [{name}]', 0)
        return True
