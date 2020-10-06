from astropy.coordinates import EarthLocation
from astropy.time import Time
from astropy.coordinates import AltAz
from astropy.coordinates import ICRS
from astropy.coordinates import BaseRADecFrame
from astropy import units as u
from astropy.coordinates import SkyCoord
import datetime
import config
from logger import LoggerClient as Logger

Alt_deg = config.Config.getInt("park_alt", "telescope")
Az_deg = config.Config.getInt("park_az", "telescope")

deltaSec = 1439.99 #questo il valore del tempo trascorso tra l'accensione dell'Fs2 e l'azione del Sync, funzione da definre

#converte la ar decimale in ore minuti e secondi
def deg2HMS(ra, round=False):
    RA,rs = '', ''
    if str(ra)[0] == '-':
        rs, ra = '-', abs(ra)
    raH = int(ra/15)
    raM = int(((ra/15)-raH)*60)
    if round:
        raS = int(((((ra/15)-raH)*60)-raM)*60)
    else:
        raS = ((((ra/15)-raH)*60)-raM)*60
    RA = '{0}{1} {2} {3}'.format(rs, raH, raM, raS)
    print (RA, 'Ar in formato orario')
    if ra:
        return RA

#Calcola i valori di Ar e Dec per la posizione di Alt e Az del momento
FrassoSabino = EarthLocation(lat='42d13.76m', lon='+12d48.69m', height=465*u.m)
t1 = datetime.datetime.utcnow()
print (t1, 'timenow')
aa = AltAz(location=FrassoSabino, obstime=t1)
#print (aa)
#coord_AltAz = SkyCoord(float(AltAz_deg[0])*u.deg, float(AltAz_deg[1])*u.deg, frame=aa)
coord_AltAz = SkyCoord((Alt_deg)*u.deg, (Az_deg)*u.deg, frame=aa)
coord_ArDec = coord_AltAz.transform_to('icrs')
ar_icrs = str(coord_ArDec.ra*u.deg)
dec_icrs = coord_ArDec.dec
ar_icrs_deg = ar_icrs[0:17]
print (ar_icrs_deg, 'ar_park decimale')
print (dec_icrs, 'dec park')
AR = deg2HMS(float(ar_icrs_deg))

#converisone dei secondi da aggiungere al valore di Ar del Sync
def AddRA(add_sec):
    if add_sec < 60:
        h = 0
        m = 0
        s = add_sec

    if add_sec < 3600 and add_sec >= 60:
        h = 0
        m = int(add_sec/60)
        s = ((add_sec/60) - m) * 60
    else:
        h = int(add_sec/3600)
        m = int((add_sec/3600 -h)*60)
        s = (((add_sec/3600 -h)*60)-(int((add_sec/3600 -h)*60)))*60
    return h, m, s
AddArNow = AddRA(deltaSec)
#print (AddArNow)

#aggiunge gli arcsec necessari per il sync corretto
def newAr(RA,AddAr):
    h =RA[0:2]
    m = RA[3:5]
    s = RA[6:]
    h1 = AddAr[0]
    m1 = AddAr[1]
    s1 = AddAr[2]
    print (h, m ,s, h1, m1, s1)
    s_now = float(s) + float(s1)
    m_now = int(m) + int(m1)
    h_now = int(h) + int(h1)
    if s_now >=60:
        s_now = s_now - 60
        m_now = m_now + 1
        if m_now >=60:
            m_now = m_now -60
            h_now = h_now + 1
    print (h_now, m_now, s_now,'ar per sync')
    return h, m, s
ar = newAr(AR, AddArNow)

#passa i nuovi valori di Ar al js
def push_newAr_Dec():
    pass
