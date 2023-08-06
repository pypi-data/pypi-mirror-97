"""
Handles instrument specific info for the HARPS spectrograph

Mostly reading data from the header
"""
import os.path
import glob
import logging
from datetime import datetime
import fnmatch
import re

import numpy as np
from astropy.io import fits
from astropy.time import Time
from dateutil import parser

from .common import getter, InstrumentWithModes, observation_date_to_night
from .filters import Filter

logger = logging.getLogger(__name__)


class MCDONALD(InstrumentWithModes):
    def _convert_time_deg(self, v):
        v = [float(s) for s in v.split(":")]
        v = v[0] + v[1] / 60 + v[2] / 3600
        return v

    def add_header_info(self, header, mode, **kwargs):
        """ read data from header and add it as REDUCE keyword back to the header """
        # "Normal" stuff is handled by the general version, specific changes to values happen here
        # alternatively you can implement all of it here, whatever works

        header = super().add_header_info(header, mode, **kwargs)
        info = self.load_info()
        get = getter(header, info, mode)

        header["e_orient"] = get("orientation", 0)

        trimsec = get("trimsec")

        if trimsec is not None:
            pattern = r"\[(\d*?):(\d*?),(\d*?):(\d*?)\]"
            res = re.match(pattern, trimsec)
            prescan_x = int(res[1]) + 1
            overscan_x = int(res[2])
            prescan_y = int(res[3])
            overscan_y = int(res[4])
        else:
            prescan_x = 2
            overscan_x = 2048
            prescan_y = 2
            overscan_y = 2047

        header["e_xlo"] = prescan_x
        header["e_xhi"] = overscan_x

        header["e_ylo"] = prescan_y
        header["e_yhi"] = overscan_y

        amp = get("amplifier")
        gain = info["gain"].format(amplifier=amp)
        readnoise = info["readnoise"].format(amplifier=amp)

        header["e_gain"] = get(gain, 1)
        header["e_readn"] = get(readnoise, 0)
        header["e_exptim"] = get("exposure_time", 0)

        header["e_sky"] = get("sky", 0)
        header["e_drk"] = get("dark", 0)
        header["e_backg"] = header["e_gain"] * (header["e_drk"] + header["e_sky"])

        header["e_imtype"] = get("observation_type")
        header["e_ctg"] = get("observation_type")

        obs_date = get("date")
        ut = get("universal_time")
        dark_time = get("dark_time")
        ra = get("ra")
        dec = get("dec")

        if ra is not None:
            ra = self._convert_time_deg(ra)
        if dec is not None:
            dec = self._convert_time_deg(dec)
        if ut is not None and dark_time is not None:
            tmid = self._convert_time_deg(ut) + dark_time / 2
        else:
            tmid = 0
        if obs_date is not None:
            jd = Time(obs_date).mjd + tmid + 0.5
        else:
            jd = 0

        header["e_ra"] = ra
        header["e_dec"] = dec
        header["e_jd"] = jd

        header["e_obslon"] = self._convert_time_deg(info["longitude"])
        header["e_obslat"] = self._convert_time_deg(info["latitude"])
        header["e_obsalt"] = info["altitude"]

        return header

    def get_wavecal_filename(self, header, mode, **kwargs):
        """ Get the filename of the wavelength calibration config file """
        cwd = os.path.dirname(__file__)
        fname = "{instrument}_{mode}_2D.npz".format(instrument="harps", mode=mode)
        fname = os.path.join(cwd, "..", "wavecal", fname)
        return fname
