"""

This module is for your data cleaning.
It should be repeatable.

## PRECLEANING
There should be a separate script recording how you transformed the json api
calls into a dataframe and csv.

## SUPPORT FUNCTIONS
There can be an unlimited amount of support functions.
Each support function should have an informative name and return the partially
cleaned bit of the dataset.
"""


def convert_obj_to_numerical(dirtydf, col):
    """Convert entries of a objects/string columns to integers by default."""
    out = dirtydf
    if 'Salary' in col:
        out[col] = out[col].map(lambda x: x.replace(',', '')).map(int)
    elif 'Year' in col:
        out[col] = out[col].map(int)

    return out


def rename_roles(dirtydf, subrole, grouprole):
    """Reassign titles (SUBROLE, GROUPROLE). Input as string"""
    out = dirtydf
    subrole = subrole.upper()
    grouprole = grouprole.upper()
    out.Role = out.Role.map(lambda x: x.replace(subrole, grouprole))

    return out


def sort_into_regions(dirtydf):
    """
    Add REGION column based on LOCATION.
    Default regions: Silicon Valley, NY, and Washington DC (DMV) area.
    Each location set determined by hand.
    """
    cleandf = dirtydf

    bay_area = ['ALAMEDA, CA', 'BELMONT, CA', 'BENICIA, CA', 'BERKELEY, CA',
                'BRISBANE, CA', 'BURLINGAME, CA', 'CAMPBELL, CA',
                'CUPERTINO, CA', 'DUBLIN, CA', 'EAST PALO ALTO, CA',
                'EL CERRITO, CA', 'EMERYVILLE, CA', 'FOLSOM, CA',
                'FOSTER CITY, CA', 'FREMONT, CA', 'HERCULES, CA',
                'LOS ALTOS, CA', 'LOS GATOS, CA', 'MENLO PARK, CA',
                'MILL VALLEY, CA', 'MILLBRAE, CA', 'MILPITAS, CA',
                'MOUNTAIN VIEW, CA', 'NEWARK, CA', 'NOVATO, CA', 'OAKLAND, CA',
                'PALO  ALTO, CA', 'PALO ALTO, CA', 'PASADENA, CA',
                'PETALUMA, CA', 'PLEASANT HILL, CA', 'PLEASANTON, CA',
                'REDLANDS, CA', 'REDWOOD CITY, CA', 'REDWOOD SHORES, CA',
                'RICHMOND, CA', 'SAN BRUNO, CA', 'SAN CARLOS, CA',
                'SAN FANCISCO, CA', 'SAN FRANCICSCO, CA', 'SAN FRANCISCO, CA',
                'SAN FRANCISCO, CA, CA', 'SAN JOSE, CA', 'SAN MATEO, CA',
                'SAN RAMON, CA', 'SANJOSE, CA', 'SAUSALITO, CA',
                'SOUTH SAN FRANCISCO, CA', 'SUNNYVALE, CA', 'TIBURON, CA',
                'UNION CITY, CA', 'VALLEJO, CA', 'VENICE, CA',
                'WALNUT CREEK, CA', 'SAN FRANCISCO, VA']

    nyc = ['NEW YORK, NY', 'BROOKLYN, NY', 'NEW  YORK, NY',
           'NEW YORK CITY, NY', 'IRVINGTON, NY', 'LONG ISLAND CITY, NY',
           'NYC, NY']

    dmv = ['WASHINGTON, DC', 'WASHINGTON, DC, DC', 'WASHINGTON DC, DC',
           'MCLEAN, VA', 'RETSON, VA', 'STERLING, VA', 'ALEXANDRIA, VA',
           'ARLINGTON, VA', 'HERNDON, VA', 'ASHBURN, VA', 'MANASSAS, VA',
           'RESTON, VA', 'FALLS CHURCH, VA', 'FAIRFAX, VA',
           'DULLES, VA', 'BETHESDA, MD', 'SILVER SPRING, MD', 'COLUMBIA, MD',
           'ROCKVILLE, MD']

    cleandf['Region'] = ['BAYAREA' if x in bay_area else 'NYC' if x in nyc
                         else 'DC' if x in dmv else 'OTHER'
                         for x in cleandf.Location]
    return cleandf


def remove_uncertified_data(dirtydf):
    """Remove data that has not been certified."""
    cleandf = dirtydf[dirtydf['Status'] == 'CERTIFIED'].reset_index(drop=True)
    return cleandf


def full_clean(dirty_data):
    """Run all helper cleaning functions."""
#     dirty_data = pd.read_csv("./data/dirty_data.csv")
    cleaning_data1 = convert_obj_to_numerical(dirty_data, 'Salary')
    cleaning_data2 = convert_obj_to_numerical(cleaning_data1, 'Year')
    cleaning_data3 = rename_roles(cleaning_data2, 'SR. DATA SCIENTIST',
                                  'SENIOR DATA SCIENTIST')
    cleaning_data4 = rename_roles(cleaning_data3, 'DATA SCIENCE',
                                  'DATA SCIENTIST')
    cleaning_data5 = rename_roles(cleaning_data4,
                                  'SENIOR ASSOCIATE, DATA SCIENCE',
                                  'ASSOCIATE DATA SCIENTIST')
    cleaning_data6 = sort_into_regions(cleaning_data5)
    cleaned_data = remove_uncertified_data(cleaning_data6)

    cleaned_data.to_csv('./data/cleaned_for_testing.csv')

    return cleaned_data
