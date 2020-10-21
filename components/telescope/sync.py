from astropy.coordinates import EarthLocation
from astropy.time import Time
from astropy.coordinates import AltAz
from astropy.coordinates import ICRS
from astropy.coordinates import BaseRADecFrame
from astropy.coordinates import FK5
from astropy import units as u
from astropy.coordinates import SkyCoord
import datetime
import config
from logger import LoggerClient as Logger

Alt_deg = config.Config.getFloat("park_alt", "telescope")
Az_deg = config.Config.getFloat("park_az", "telescope")
lat = config.Config.getValue("lat", "geographic")
lon = config.Config.getValue("lon", "geographic")
height = config.Config.getInt("height", "geographic")
name_obs = config.Config.getValue("name_obs", "geographic")
equinox = config.Config.getValue("equinox", "geographic")
#timezone= config.Config.getInt("timezone", "geographic")
#ora_leg = config.Config.getInt("ora_leg", "geographic")
#time = timezone + ora_leg

#Calcola i valori di Ar e Dec per la posizione di Alt e Az del momento
def conv_altaz_to_ardec(sync_time):
    name_obs = EarthLocation(lat, lon, (height)*u.m)
    time_local_sync = sync_time
    Logger.getLogger().debug("time utc sync letto in sync.py: %s", time_local_sync)

    aa = AltAz(location=name_obs, obstime=time_local_sync)
    coord_AltAz = SkyCoord((Alt_deg)*u.deg, (Az_deg)*u.deg, frame=aa, equinox=equinox)
    print (coord_AltAz)
    coord_ArDec = coord_AltAz.transform_to('fk5')
    print (coord_ArDec)
    ar_icrs = str(coord_ArDec.ra*u.deg)
    dec_icrs = str(coord_ArDec.dec*u.deg)
    ar_icrs_deg = ar_icrs[0:17]
    ar  = (float(ar_icrs_deg))/15 #conversione ar da gradi a ore
    dec_str = dec_icrs[0:17]
    dec = float(dec_str)
    Logger.getLogger().debug('ar_park (formato orario decimale): %s', ar)
    Logger.getLogger().debug('dec park (formato declinazione deccimale): %s', dec)

    return ar, dec

#passa i nuovi valori di Ar al js
#def push_newAr_Dec():
#    pass
#conv_altaz_to_ardec()
