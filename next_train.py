#! /usr/bin/python

'''An app for getting the next time an MBTA bus/train is arriving at Back-Bay and printing it to the terminal.

akittredge June 2011

'''

import urllib
import xml.dom
import sys
from lxml import etree

BACK_BAY_TAG = 'place-bbsta'

PREDICTION_URL = 'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=mbta&s=%(stop_tag)s&r=%(route_tag)s'

#PREDICTION_URL = 'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=mbta&r=39&s=22365&useShortTitles=true'


def get_params():
    try:
        route, direction, stop =sys.argv[1:4]
    except ValueError:
        #try something else,
        route, direction, stop = (None,) * 3
        

    return route, direction, stop

def title_and_times_xpath(stream):
    tree = etree.parse(stream)

    route = tree.xpath('//@routeTitle')[0]
    stop = tree.xpath('//@stopTitle')[0]

    predicted_arrival_minutes = tree.xpath('//@minutes')

    return route, stop, predicted_arrival_minutes

def print_title_and_times(route, stop, predicted_arrival_minutes):
    
    print 'Predicted arrivals for Route %s @ %s' % (route, stop)

    print '\n'.join(predicted_arrival_minutes)

def main():

    route, direction, stop = get_params()

    tags = {'route_tag' : route,
                'direction_tag' : direction,
                'stop_tag' : stop
            }

    prediction_url = PREDICTION_URL % tags
    print prediction_url
    prediction_stream = urllib.urlopen(prediction_url)
    prediction_attributes = title_and_times_xpath(prediction_stream)

    print_title_and_times(*prediction_attributes)
    
if __name__ == '__main__':
    sys.exit(main())
