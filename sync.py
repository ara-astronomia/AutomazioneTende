from astropy.coordinates import EarthLocation
from astropy.time import Time
from astropy.coordinates import AltAz
from astropy.coordinates import ICRS
from astropy.coordinates import Baseright_ascDecFrame
from astropy import units as u
from astropy.coordinates import SkyCoord
import datetime
import config
from logger import LoggerClient as Logger

Alt_deg = config.Config.getInt("park_alt", "telescope")
Az_deg = config.Config.getInt("park_az", "telescope")
lat = config.Config.getValue("lat", "geografic")
lon = config.Config.getValue("lon", "geografic")
height = config.Config.getInt("height", "geografic")
name_obs = config.Config.getValue("name_obs", "geografic")

#converte la ar decimale in ore minuti e secondi
def deg2hms(ra, round=False):
    right_asc,rs = '', ''
    if str(ra)[0] == '-':
        rs, ra = '-', abs(ra)
    raH = int(ra/15)
    raM = int(((ra/15)-raH)*60)
    if round:
        raS = int(((((ra/15)-raH)*60)-raM)*60)
    else:
        raS = ((((ra/15)-raH)*60)-raM)*60
    right_asc = '{0}{1} {2} {3}'.format(rs, raH, raM, raS)
    Logger.getLogger().info("ascenzione retta del telescopio al momento dello start del motore di ar ", right_asc)
    Logger.getLogger().info(right_asc, 'Ar in formato orario')
    return right_asc_h

#Calcola i valori di Ar e Dec per la posizione di Alt e Az del momento
def conv_altaz_to_ardec():
    name_obs = EarthLocation(lat, lon, (height)*u.m)
    time_sync = datetime.datetime.utcnow()
    print (time_sync, 'timenow')
    aa = AltAz(location=name_obs, obstime=time_sync)
    coord_AltAz = SkyCoord((Alt_deg)*u.deg, (Az_deg)*u.deg, frame=aa)
    coord_ArDec = coord_AltAz.transform_to('icrs')
    ar_icrs = str(coord_ArDec.ra*u.deg)
    dec_icrs = coord_ArDec.dec
    ar_icrs_deg = ar_icrs[0:17]
    Logger.getLogger().info(ar_icrs_deg, 'ar_park decimale')
    Logger.getLogger().info(dec_icrs, 'dec park')
    ar_icrs = deg2hms(float(ar_icrs_deg))

#passa i nuovi valori di Ar al js
def push_newAr_Dec():
    pass
conv_altaz_to_ardec()
