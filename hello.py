import pygeoip
from pygeoip import *
countryname={}
ipnum = util.ip2long('124.222.189.95')
GEOIP = pygeoip.GeoIP(r"C:\Users\bhava\PycharmProjects\untitled\GeoIP.dat", pygeoip.MEMORY_CACHE)
countryname = GEOIP._get_region(ipnum)
print(countryname)
# print(ipnum)