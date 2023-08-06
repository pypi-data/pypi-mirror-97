from astroquery.vizier import Vizier
import astropy.coordinates as coord
import astropy.units as u

catalog = Vizier(catalog="UCAC4", row_limit=1000000)

result = catalog.query_region(coord.SkyCoord(ra=323.24, dec=3.2, unit=(
    u.deg, u.deg), frame='icrs'), width=0.75*u.deg, height=0.5*u.deg)[0]
print(result)
#print(result['RAJ2000'], result['DEJ2000'], result['f.mag'])

stars = [(ra, de, mag) for ra, de, mag in zip(result['RAJ2000'], result['DEJ2000'], result['f.mag'])]

print(stars)