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

    dmv = dirtydf.loc[dirtydf.Location.map(lambda x: ', DC' in x)].Location.unique().tolist()
    md = dirtydf.loc[dirtydf.Location.map(lambda x: ', DC' in x)].Location.unique().tolist()
    va = ['MCLEAN, VA', 'RETSON, VA', 'STERLING, VA', 'ALEXANDRIA, VA',
           'ARLINGTON, VA', 'HERNDON, VA', 'ASHBURN, VA', 'MANASSAS, VA',
           'RESTON, VA', 'FALLS CHURCH, VA', 'FAIRFAX, VA',
           'DULLES, VA']
    dmv.extend(md)
    dmv.extend(va)

    cleandf['Region'] = ['BAYAREA' if x in bay_area else 'NYC' if x in nyc
                         else 'DC' if x in dmv else 'OTHER'
                         for x in cleandf.Location]
    return cleandf


def sort_into_industry(dirtydf):
    """
    Add INDUSTRY column based on EMPLOYER.
    Default categories are TECH and FINANCE. All else is OTHER.
    """
    cleandf = dirtydf
    
    tech = ['FACEBOOK INC', 'UBER TECHNOLOGIES INC', 'GROUPON INC'
            'LINKEDIN CORPORATION', 'AMAZONCOM SERVICES INC',
            'AIRBNB INC', 'TWITTER INC', 'LYFT INC', 'ZILLOW INC', 'NETFLIX INC',
            'APPLE INC', 'MICROSOFT CORPORATION', 'IBM CORPORATION', 'SAP LABS LLC', 
            'ORACLE AMERICA INC', 'INTEL CORPORATION', 'WAYFAIR LLC',
            'SALESFORCECOM INC', 'EBAY INC', 'STITCH FIX INC', 'PAYPAL INC',
            'TRIPADVISOR LLC', 'AMAZON WEB SERVICES INC','SQUARE INC',
            'HOTWIRE INC', 'UDEMY INC', 'JUSTENOUGH SOFTWARE CORPORATION INC',
            '23ANDME INC', 'ZYNGA INC', 'TWITCH INTERACTIVE INC', 'HOUZZ INC',
            'STRIPE INC', 'YELP INC', 'A MEDIUM CORPORATION', 'REDDIT INC',
            'WHATSAPP INC', 'UDACITY INC', 'CISCO SYSTEMS INC']
    
    fin = ['VISA USA INC', 'VISA TECHNOLOGY & OPERATIONS LLC', "MOODY'S ANALYTICS",
           'S&P GLOBAL MARKET INTELLIGENCE INC', 'S&P GLOBAL INC', 'BLOOMBERG LP',
           'HASH FINANCE LLC', 'ZESTFINANCE INC', 'APPLIED DATA FINANCE LLC',
           'VESTED FINANCE INC', 'SMARTFINANCE LLC', 'SNAP FINANCE LLC',
           'HASH FINANCE LLC', 'SVB FINANCIAL GROUP', 
           'FINANCIAL TECHNOLOGY PARTNERS LP', 'GLOBAL ATLANTIC FINANCIAL COMPANY',
           'CONTINENTAL FINANCE COMPANY LLC', 'CIRCLE INTERNET FINANCIAL INC',
           'DE LAGE LANDEN FINANCIAL SERVICES INC', 'NATIONAL FINANCIAL LLC',
           'VERUS FINANCIAL LLC', 'STASH FINANCIAL INC', 'SOCIAL FINANCE INC',
           'ATHENA ART FINANCE CORP', 'DOLLAR FINANCIAL GROUP INC', 
           'HEALTHCARE FINANCIAL INC', 'EXPRESS TECH-FINANCING LLC', 'LADDER FINANCIAL INC',
           "STANDARD & POOR'S FINANCIAL SERVICES LLC", 'BREAKOUT CAPITAL FINANCE LLC',
           'GENERAL MOTORS FINANCIAL COMPANY INC', 'VOUCH FINANCIAL INC', 
           'ENOVA FINANCIAL HOLDINGS LLC', 'TWO SIGMA INVESTMENTS LP',
           'MERCEDES-BENZ FINANCIAL SERVICES USA LLC', 'INVENTURE CAPITAL CORPORATION',
           'SRS INVESTMENT MANAGEMENT LLC', 'INVESCO GROUP SERVICES INC',
           'FIDELITY INVESTMENTS INSTITUTIONAL SERVICES COMPANY INC', 'Z5 INVENTORY INC',
           'UBM INVESTMENTS INC', 'AMERICAN CENTURY INVESTMENT MANAGEMENT INC',
           'TWO SIGMA INVESTMENTS LLC', 'CAPITAL ONE INVESTING LLC','JPMORGAN CHASE & CO'
           'ON DECK CAPITAL INC', 'ALIVIA CAPITAL LLC', 'CAPITAL ONE NATIONAL ASSOCIATION',
           'INVENTURE CAPITAL CORPORATION', 'CAPITAL ONE SERVICES LLC', 
           'DAVIDSON KEMPNER CAPITAL MANAGEMENT LP', 'REAL CAPITAL ANALYTICS',
           'HITCHWOOD CAPITAL MANAGEMENT LP', 'ROTELLA CAPITAL MANAGEMENT',
           'GOODWATER CAPITAL LLC', '12 WEST CAPITAL MANAGEMENT LP', 'RBC CAPITAL MARKETS LLC',
           'BLUEVINE CAPITAL INC', 'FARALLON CAPITAL MANAGEMENT LLC', 
           'PASSAGE GLOBAL CAPITAL MANAGEMENT LLC', 'KING STREET CAPITAL MANAGEMENT LP',
           'LIGHTER CAPITAL INC', 'NAJARIAN CAPITAL LLC', 
           'CAPITAL ONE SERVICES II LLC', 'CAPITAL GROUP COMPANIES GLOBAL', 
           'BREAKOUT CAPITAL FINANCE LLC', 'AMAZON CAPITAL SERVICES INC', 
           'CAPITAL ONE INVESTING LLC', 'CAPITALOGIX TRADING LP', 'EVERBANK',
           'AMERICAN BANKERS LIFE ASSURANCE COMPANY OF FLORIDA', 'AMERICAN SAVINGS BANK FSB',
           'BANK OF AMERICA NA', 'BANKERS HEALTHCARE GROUP LLC', 'BANKRATE INC',
           'BARCLAYS BANK PLC', 'CENTRAL PACIFIC BANK', 'COMMONWEALTH BANK OF AUSTRALIA',
           'EVERBANK', 'FIFTH THIRD BANK AN OHIO BANKING CORPORATION', 'KEYBANK NATIONAL ASSOCIATION',
           'LIVE OAK BANK', 'MUFG UNION BANK NA', 'OLD NATIONAL BANK', 'SALLIE MAE BANK',
           'STATE STREET BANK AND TRUST COMPANY', 'SUNTRUST BANKS INC', 'TD BANK NATIONAL ASSOCIATION',
           'THE HUNTINGTON NATIONAL BANK', 'US BANK NATIONAL ASSOCIATION']
    
    ins = ['ACCIDENT FUND INSURANCE COMPANY OF AMERICA', 'ACE AMERICAN INSURANCE COMPANY',
           'AETNA LIFE INSURANCE COMPANY', 'ALLSTATE INSURANCE COMPANY',
           'AMERICAN FAMILY MUTUAL INSURANCE COMPANY', 'AMERITAS LIFE INSURANCE CORP'
           'BERKLEY INSURANCE COMPANY', 'BUNKER HILL INSURANCE COMPANY'
           'CENTRAL MUTUAL INSURANCE COMPANY', 'CSAA INSURANCE SERVICES INC'
           'EHEALTHINSURANCE SERVICES INC', 'ESURANCE INSURANCE SERVICES INC',
           'FACTORY MUTUAL INSURANCE COMPANY', 'HALOS INSURANCE INC',
           'HARTFORD FIRE INSURANCE COMPANY', 'HEAVY DUTY VEHICLE INSURANCE INC',
           'HUMANA INSURANCE COMPANY', 'INSURANCE SERVICES OFFICE INC',
           'JEWELERS MUTUAL INSURANCE COMPANY', 'JOHN HANCOCK LIFE INSURANCE COMPANY',
           'JOHN HANCOCK LIFE INSURANCE COMPANY (USA)', 'MASSACHUSETTS MUTUAL LIFE INSURANCE COMPANY',
           'MUNICH REINSURANCE AMERICA INC', 'MUTUAL OF OMAHA INSURANCE COMPANY',
           'NATIONAL UNION FIRE INSURANCE COMPANY OF PITTSBURGH PA',
           'NORTHWESTERN MUTUAL LIFE INSURANCE COMPANY', 'PACIFIC LIFE INSURANCE COMPANY',
           'PHYSICIANS MUTUAL INSURANCE COMPANY', 'PROGRESSIVE CASUALTY INSURANCE COMPANY',
           'PROTECTIVE LIFE INSURANCE COMPANY', 'RAINWALK INSURANCE INC',
           'SAFE AUTO INSURANCE COMPANY', 'STATE FARM MUTUAL AUTOMOBILE INSURANCE COMPANY',
           'STILLWATER INSURANCE SERVICES INC', 'THE GUARDIAN LIFE INSURANCE COMPANY OF AMERICA',
           'THE HANOVER INSURANCE COMPANY', 'THE PRUDENTIAL INSURANCE COMPANY OF AMERICA',
           'UNITED STATES FIRE INSURANCE COMPANY DBA CRUM & FORSTER',
           'ZURICH AMERICAN INSURANCE COMPANY']
    
    cnslt = ['A2 CONSULTING LLC', 'AON CONSULTING INC', 'BARKAWI MANAGEMENT CONSULTANTS LP',
             'BEYONDSOFT CONSULTING INC', 'BIS CONSULTING INC', 'BIZCRAFT CONSULTING LLC',
             'BRIDGETOWN CONSULTING GROUP INC', 'BUXTON CONSULTING INC', 'COLSH CONSULTANTS LLC',
             'CONSULTADD INC', 'DAWAR CONSULTING INC', 'DELOITTE CONSULTING LLP',
             'EDATAFORCE CONSULTING LLC', 'FINO CONSULTING LLC', 'ICUBE CONSULTANCY SERVICES INC',
             'INTEGRITY WEB CONSULTING INC', 'ITTSTAR CONSULTING LLC', 'KSM CONSULTING LLC',
             'LIFTPOINT CONSULTING INC', 'LOGINSOFT CONSULTING LLC', 'MAXIMA CONSULTING INC',
             'PERSIS CONSULTING CO', 'PYRAMID CONSULTING INC', 'QUALEX CONSULTING SERVICES INC',
             'SOCIETY CONSULTING LLC', 'SOKAT CONSULTING LLC', 'SOLOMON CONSULTING GROUP LLC',
             'SRS CONSULTING INC', 'TATA CONSULTANCY SERVICES LIMITED', 'THE BOSTON CONSULTING GROUP INC',
             'THIRD EYE CONSULTING SERVICES & SOLUTIONS LLC', 'TTEC CONSULTING INC',
             'YOTABITES CONSULTING LLC', 'MCKINSEY & COMPANY INC UNITED STATES', 'BOOZ ALLEN HAMILTON INC',
             'THE ADVISORY BOARD COMPANY']
    
    cleandf['Industry'] = ['TECH' if x in tech 
                           else 'FINANCE' if x in fin 
                           else 'INSURANCE' if x in ins 
                           else 'CONSULTING' if x in cnslt
                           else 'OTHER' for x in cleandf.Company]
    
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
    cleaning_data7 = sort_into_industry(cleaning_data6)
    cleaned_data = remove_uncertified_data(cleaning_data7)

    cleaned_data.to_csv('./data/cleaned_for_testing.csv', index=False)

    return cleaned_data
