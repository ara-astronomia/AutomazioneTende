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
timezone= config.Config.getInt("timezone", "geografic")
ora_leg = config.Config.getValue("ora_leg", "geografic")
time = timezone + ora_leg

#Calcola i valori di Ar e Dec per la posizione di Alt e Az del momento
def conv_altaz_to_ardec():
    name_obs = EarthLocation(lat, lon, (height)*u.m)
    time_sync = datetime.datetime.now(datetime.timezone(datetime.timedelta((hours=time))))
    Logger.getLogger().info(time_sync, ' time sync')
    aa = AltAz(location=name_obs, obstime=time_sync)
    coord_AltAz = SkyCoord((Alt_deg)*u.deg, (Az_deg)*u.deg, frame=aa)
    coord_ArDec = coord_AltAz.transform_to('icrs')
    ar_icrs = str(coord_ArDec.ra*u.deg)
    dec_icrs = str(coord_ArDec.dec*u.deg)
    ar_icrs_deg = ar_icrs[0:17]
    ar  = (float(ar_icrs_deg))/15 #conversione ar da gradi a ore
    dec = dec_icrs[0:17]
    Logger.getLogger().info(ar, 'ar_park (formato orario decimale)')
    Logger.getLogger().info(dec, 'dec park')
    return ar, dec

#passa i nuovi valori di Ar al js
#def push_newAr_Dec():
#    pass
conv_altaz_to_ardec()
