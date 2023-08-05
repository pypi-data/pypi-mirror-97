"""
UK SportsHall Athletics format for younger children

http://www.sportshall.org

Focusing on... http://www.sportshall.org/homepentathlon


Codes of interest:  
    SLJ
    STJ
    SHJ

"""

from decimal import Decimal
from math import floor, ceil
from typing import Dict

FUZZ = 0.0001

def load_data() -> Dict:
    "Transform data on first load into something more usable"

    data_by_event_code = {}
    event_codes = []
    by_col = list(zip(*RAWDATA))
    keys = by_col[0]
    for col in by_col[1:]:
        d = dict(zip(keys, col))
        code = d['code']
        data_by_event_code[code] = d


    # this is just strings, a bit clunky.  We want some facts about each event, 
    # and a mapping of performances to points

    db = {}
    for (code, info) in data_by_event_code.items():
        e = {}
        e['name'] = info['name']
        e['units'] = info['units']
        e['incpoints'] = info['incpoints']
        inctext = info['increment']
        if inctext.endswith('cm'):
            inc = float(inctext[0:-2]) * 0.01
            e['increment'] = inc
        elif inctext.endswith('sec'):
            inc = float(inctext[0:-3])
            e['increment'] = inc
        perf2points = []
        for points in range(1, 81):
            perf = info[str(points)]
            if perf != '-':
                if code == 'SHJ':  # given in cm, convert to metres
                    perf = '0.'+ perf
                perf2points.append((points, perf))
        e['perf2points'] = perf2points
        db[code] = e

    return db


def score_high_event(dperf: Decimal, info: Dict, verbose: bool = False) -> int:
    "Look in given event's info dict - binary search, high numbers good"
    if verbose:
        print("Looking for performance of", dperf)
    p2p = info['perf2points']
    max_points, dmax_perf = p2p[-1]
    max_perf = Decimal(dmax_perf)


    points = 0
    if dperf > max_perf:
        # above 80 points, use increment
        excess = dperf - max_perf
        if 'increment' in info:
            excess_steps = int(floor(float(excess) /  info['increment']))
        else:
            excess_steps = 0
        incpoints = info['incpoints']
        if (incpoints == "n/a"):
            incpoints = 0
        else:
            incpoints = int(incpoints)
        excess_points = excess_steps * incpoints
        points = max_points + excess_points
    elif dperf == max_perf:
        # special case, avoid binary search
        return max_points

    else:
        # binary search in 80 point array
        lo = 0
        hi = len(p2p)
        mid = int(floor(0.5 * (lo + hi)))

        tries = 0
        while 1:
            tries += 1
            (p0, v0) = p2p[mid]
            (p1, v1) = p2p[mid+1]

            if verbose:
                print("try %d: index %d, p0=%s, v0=%s; p1=%s, v1=%s" % (
                    tries, mid, p0, v0, p1, v1))

            if tries > 10: 
                return 0
            
            if dperf >= Decimal(v1):  # look higher
                lo = mid # narrow the range if we overshoot later
                mid = int(floor(0.5 * (mid + hi)))
                if verbose: print("    look higher")
            elif dperf < Decimal(v0): # look higher
                hi = mid
                mid = int(floor(0.5 * (lo + mid)))
                if verbose: print("    look lower")
            else:
                points = p0
                if verbose: print("    found it")

                break

    return points


def score_low_event(dperf: Decimal, info: Dict, verbose: bool = False) -> int:
    "Look in given event's info dict - binary search, low numbers good"
    if verbose:
        print("Looking for performance of", dperf)
    p2p = info['perf2points']
    max_points, dmax_perf = p2p[-1]
    max_perf = Decimal(dmax_perf)


    points = 0
    if dperf < max_perf:
        # above 80 points, use increment
        excess = max_perf - dperf
        excess_steps = int(floor(float(excess) /  info['increment']))
        excess_points = excess_steps * int(info['incpoints'])
        points = max_points + excess_points
    elif dperf == max_perf:
        # special case, avoid binary search
        return max_points

    else:
        # binary search in 80 point array
        lo = 0
        hi = len(p2p)
        mid = int(floor(0.5 * (lo + hi)))

        tries = 0
        while 1:
            tries += 1
            (p0, v0) = p2p[mid]
            (p1, v1) = p2p[mid+1]

            if verbose:
                print("try %d: index %d, p0=%s, v0=%s; p1=%s, v1=%s" % (
                    tries, mid, p0, v0, p1, v1))

            if tries > 10: 
                return 0
            
            if dperf <= Decimal(v1):  # look higher
                lo = mid # narrow the range if we overshoot later
                mid = int(floor(0.5 * (mid + hi)))
                if verbose: print("    look higher")
            elif dperf > Decimal(v0): # look higher
                hi = mid
                mid = int(floor(0.5 * (lo + mid)))
                if verbose: print("    look lower")
            else:
                points = p0
                if verbose: print("    found it")

                break

    return points


_DB = None

def sportshall_score(event_code: str, perf: str, verbose=False) -> int:
    "Return Sportshall At Home score for the event"
    global _DB # initialize on first call
    if not _DB:
        _DB = load_data()
    perf = Decimal(perf)
    ec = event_code.upper()

    event_info = _DB.get(ec, None)
    if not event_info:
        raise KeyError("Event Code '%s' not defined in sportshall scoring" % ec)
    
    if ec in ['SLJ', 'SHJ', 'STJ', 'SP', 'BAL', 'SPB', 'TART', 'OHT', 'CHT', 'JT']:  
        return score_high_event(perf, event_info, verbose=verbose)
    else:
        return score_low_event(perf, event_info, verbose=verbose)





# Data provided in a Google Sheet we cleaned up.  Explicit points values
# given from 1 to 80 

RAWDATA = [
  ["code","SLJ","SHJ","STJ","SP","BAL","SPB","TART","OHT","32H","CHT","100","JT","800"  ],
  ["name","Standing long jump","vertical jump","standing triple jump","shot","balance 4x15secs","Stepped Bounce 20s","Target Throw","Overhead Heave","hi step, 4x8m","chest push girls 1kg,boys 2","shuttle 10x10rm","indoor javelin","800 metres"  ],
  ["increment","2cm","1cm","6cm","0.25cm","n/a","1 no.","n/a","25cm","0.2sec","25cm","0.2sec","1m","1sec"  ],
  ["incpoints","1","1","1","1","n/a","1","n/a","2","1","2","1","2","1"  ],
  ["units","mtrs","cms","mtrs","mtrs","secs","no.","no.","mtrs","secs","mtrs","secs","mtrs","secs"  ],
  ["80","2.80","68","8.00","12.00","-","80","-","12.00","11.0","11.75","24.0","-","126"  ],
  ["79","2.75","67","7.87","11.75","-","79","-","-","11.2","-","24.2","28","127"  ],
  ["78","2.70","66","7.75","11.50","-","78","-","11.75","11.4","11.50","24.4","-","128"  ],
  ["77","2.65","65","7.67","11.25","-","77","-","-","11.6","-","24.6","27","129"  ],
  ["76","2.60","64","7.50","11.00","-","76","-","11.50","11.8","11.25","24.8","-","131"  ],
  ["75","2.55","63","7.37","10.75","-","75","-","-","12.0","-","25.0","26","133"  ],
  ["74","2.52","62","7.25","10.50","-","74","-","11.25","12.2","11.00","25.2","-","133"  ],
  ["73","2.49","61","7.12","10.25","-","73","-","-","12.4","-","25.4","25","135"  ],
  ["72","2.46","-","7.05","10.00","-","72","24","11.00","12.5","10.75","25.6","-","138"  ],
  ["71","2.43","60","6.95","9.75","-","71","-","-","12.6","-","25.8","24","141"  ],
  ["70","2.40","59","6.85","9.50","-","70","-","10.75","12.7","10.50","26.0","-","144"  ],
  ["69","2.37","-","6.75","9.25","-","69","23","-","12.8","-","26.2","23","148"  ],
  ["68","2.34","58","6.65","9.00","-","68","-","10.50","12.9","10.25","26.4","-","148"  ],
  ["67","2.31","57","6.55","8.75","-","67","-","-","13.0","-","26.6","-","151"  ],
  ["66","2.28","-","6.45","8.50","-","66","22","10.25","13.1","10.00","26.8","22","154"  ],
  ["65","2.25","56","6.36","8.25","60","65","-","-","13.2","9.75","27.0","-","157"  ],
  ["64","2.22","55","6.28","8.00","59","64","-","10.00","13.3","9.50","27.2","-","163"  ],
  ["63","2.19","-","6.20","7.75","58","63","21","9.75","13.4","-","27.4","21","166"  ],
  ["62","2.16","54","6.12","7.50","57","62","-","-","13.5","9.25","27.6","-","166"  ],
  ["61","2.13","53","6.04","7.25","56","61","-","9.50","13.6","-","27.8","-","169"  ],
  ["60","2.10","-","5.96","7.00","55","60","20","9.25","13.7","9.00","28.0","20","172"  ],
  ["59","2.07","52","5.88","6.75","54","59","-","-","13.8","-","28.2","-","175"  ],
  ["58","2.04","51","5.80","6.50","53","58","-","9.00","13.9","8.75","28.4","-","178"  ],
  ["57","2.01","-","5.72","6.25","52","57","19","8.75","14.0","8.50","28.6","19","181"  ],
  ["56","1.98","50","5.64","6.00","51","56","-","-","14.1","8.25","28.8","-","181"  ],
  ["55","1.95","49","5.56","-","50","55","-","8.50","14.2","8.00","29.0","-","184"  ],
  ["54","1.92","48","5.48","5.75","49","54","18","8.25","14.3","-","29.2","18","184"  ],
  ["53","1.89","47","5.40","-","48","53","-","8.00","14.4","7.75","29.4","-","187"  ],
  ["52","1.86","46","5.34","5.50","47","52","-","7.75","14.5","7.50","29.6","-","187"  ],
  ["51","1.83","45","5.28","-","46","51","17","-","14.6","-","29.8","17","191"  ],
  ["50","1.80","44","5.22","5.25","45","50","-","7.50","14.7","7.25","30.0","-","191"  ],
  ["49","1.78","43","5.16","-","44","49","-","7.25","14.8","7.00","30.2","-","191"  ],
  ["48","1.76","42","5.10","5.00","43","-","16","-","14.9","-","30.4","16","191"  ],
  ["47","1.74","41","5.04","-","42","48","-","7.00","15.0","6.75","30.6","-","195"  ],
  ["46","1.72","40","4.98","4.75","41","-","-","6.75","15.1","6.50","30.8","-","195"  ],
  ["45","1.70","-","4.92","-","-","47","15","-","15.2","-","31.0","15","199"  ],
  ["44","1.68","39","4.86","4.50","40","46","-","6.50","15.3","6.25","31.2","-","199"  ],
  ["43","1.66","38","4.80","-","-","45","-","-","15.4","-","31.4","-","199"  ],
  ["42","1.64","-","4.75","4.25","39","44","14","6.25","15.5","6.00","31.6","14","199"  ],
  ["41","1.62","37","4.70","-","-","43","-","-","15.6","-","31.8","-","203"  ],
  ["40","1.60","36","4.65","4.00","38","42","-","6.00","15.7","5.75","32.0","-","203"  ],
  ["39","1.59","-","4.60","-","-","41","13","-","15.8","-","32.2","13","206"  ],
  ["38","1.58","35","4.55","-","37","40","-","5.75","15.9","5.50","32.4","-","206"  ],
  ["37","1.57","34","4.50","3.75","-","39","-","-","16.0","-","32.6","-","209"  ],
  ["36","1.56","-","4.45","-","36","38","12","5.50","16.1","5.25","32.8","12","209"  ],
  ["35","1.55","33","4.40","-","35","37","-","-","16.2","-","33.0","-","212"  ],
  ["34","1.54","32","4.35","-","34","36","-","-","16.3","-","33.2","-","212"  ],
  ["33","1.53","-","4.30","-","33","35","11","5.25","16.4","5.00","33.4","11","215"  ],
  ["32","1.52","31","4.25","3.50","32","34","-","-","16.5","-","33.6","-","215"  ],
  ["31","1.51","30","4.20","-","31","33","-","5.00","16.6","4.75","33.8","-","218"  ],
  ["30","1.50","29","4.15","-","30","32","10","-","16.8","-","34.0","10","218"  ],
  ["29","1.48","-","4.10","-","29","31","-","4.75","17.0","-","34.2","-","221"  ],
  ["28","1.46","28","4.05","-","28","30","-","-","17.2","4.50","34.4","-","221"  ],
  ["27","1.44","27","4.00","3.25","27","29","9","4.50","17.4","-","34.6","9","224"  ],
  ["26","1.42","26","3.95","-","26","28","-","-","17.6","-","34.8","-","224"  ],
  ["25","1.40","-","3.90","-","25","27","-","4.25","18.0","4.25","35.0","-","227"  ],
  ["24","1.38","25","3.80","-","24","26","8","-","18.3","-","35.5","8","227"  ],
  ["23","1.36","24","3.70","-","23","-","-","-","18.6","-","36.0","-","230"  ],
  ["22","1.34","23","3.60","3.00","22","25","-","4.00","18.9","4.00","36.5","-","230"  ],
  ["21","1.32","-","3.50","-","21","24","7","-","19.2","-","37.0","-","236"  ],
  ["20","1.30","22","3.40","-","20","23","-","-","19.6","-","37.5","7","236"  ],
  ["19","1.25","-","3.30","-","19","22","-","3.75","20.0","3.75","38.0","-","242"  ],
  ["18","1.20","21","3.20","-","18","-","6","-","20.5","-","38.5","-","242"  ],
  ["17","1.15","-","3.10","2.75","17","21","-","-","21.0","-","39.0","-","248"  ],
  ["16","1.10","20","3.00","-","16","20","-","3.50","21.5","3.50","39.5","6","248"  ],
  ["15","1.05","19","2.90","-","15","19","5","-","22.0","-","40.0","-","254"  ],
  ["14","1.00","18","2.80","-","14","18","-","-","22.5","-","40.5","-","254"  ],
  ["13","0.95","17","2.70","-","13","17","-","3.25","23.0","3.25","41.0","-","260"  ],
  ["12","0.90","16","2.60","2.50","12","16","4","-","24.0","-","42.0","5","260"  ],
  ["11","0.85","15","2.50","-","11","15","-","-","25.0","-","43.0","-","266"  ],
  ["10","0.80","14","2.40","2.25","10","14","-","3.00","26.0","3.00","44.0","-","266"  ],
  ["9","0.75","13","2.20","-","9","13","3","-","27.0","-","45.0","-","272"  ],
  ["8","0.70","12","2.00","2.00","8","12","-","2.75","28.0","2.75","46.0","4","272"  ],
  ["7","0.65","11","1.90","-","7","11","-","-","29.0","-","48.0","-","278"  ],
  ["6","0.60","10","1.80","1.50","6","10","2","2.50","30.0","2.50","50.0","-","278"  ],
  ["5","0.55","9","1.70","-","5","9","-","-","32.0","-","52.0","-","284"  ],
  ["4","0.50","8","1.50","1.00","4","8","-","2.00","34.0","2.00","54.0","3","284"  ],
  ["3","0.45","7","1.30","-","3","6","1","-","36.0","-","56.0","-","290"  ],
  ["2","0.40","6","1.10","0.50","2","4","-","-","38.0","-","58.0","-","290"  ],
  ["1","0.35","4","1.00","-","1","3","-","1.50","40.0","1.50","60.0","2","296"  ]
]



if __name__=='__main__':
    d = load_data()
    
    print(sportshall_score("800", "144", verbose=True))
    print(d)
    print(type(d))

