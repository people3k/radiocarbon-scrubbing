import shapefile
from shapely.geometry import Point
from shapely.geometry import shape
import matplotlib.pyplot as plt
import pandas as pd
from pyproj import Proj

# Dictionary  of US state/territory codes
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

# Reversed version of the dictionary
abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))

US_shp = shapefile.Reader('cb_2018_us_county_500k.shp')
all_US_shapes  = [shape(b) for b in US_shp.shapes()]
all_US_records = US_shp.records()

CA_shp = shapefile.Reader('lcd_000a16a_e.shp', encoding='Latin-1')
all_CA_shapes  = [shape(b) for b in CA_shp.shapes()]
all_CA_records = CA_shp.records()

# Canadian data projection info from the reference guide (p2-160-g2016002-eng.pdf) pg 25
CAconv = Proj(
        proj='lcc', # Projection: Lambert Conformal Conic
        datum='NAD83', # Datum: North American 1983
        lat_1=49.0, # First standard parallel
        lat_2=77.0, # Second standard parallel
        lon_0=-91.866667, # Longitude of projection center
        lat_0=63.390675, # Latitude of projection center
        x_0=6200000.0, # False easting
        y_0=3000000.0 # False northing
       )

#x,y=8395429.268569998,1661955.754285
#
#lon,lat = CAconv(x,y, inverse=True)
#print(lon,lat)
#
#
#lat,lon= 43.741686, -79.387622
#
#exit()



centroids = pd.read_csv('centroids.csv').set_index('FIPS')


# Fetch the names of the division and subdivions for the given point
def getInfo(lon, lat):
    # First try US shapes
    US_point = Point((lon,lat))
    for i in range(len(all_US_shapes)):
        boundary = all_US_shapes[i]
        if US_point.within(boundary):
            fips = all_US_records[i][4]
            county = all_US_records[i][5]
            state = abbrev_us_state[centroids.at[fips, 'State']]
            return county,state
    # Then try CA shapes. Be sure to convert to easting/northing first.
    easting,northing = CAconv(lon,lat)
    CA_point = Point((easting,northing))
    for i in range(len(all_CA_shapes)):
        boundary = all_CA_shapes[i]
        if CA_point.within(boundary):
            census_division = all_CA_records[i][1]
            province = all_CA_records[i][4]
            return census_division,province

lat,lon = 54.596093, -104.966212

subdiv,div = getInfo(lon,lat)
print('The point is in {}, {}'.format(subdiv,div))

#records = pd.read_csv('radiocarbon_scrubbed.csv',index_col=0)
#
#NArecords = pd.DataFrame(records[records['Country'].isin(['USA'])])



