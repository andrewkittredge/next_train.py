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

def title_and_times_bus_xpath(stream):

    route = tree.xpath('//@routeTitle')[0]
    stop = tree.xpath('//@stopTitle')[0]
    direction = tree.xpath('//direction/@title')[0]

    predicted_arrival_minutes = tree.xpath('//@minutes')

    return route, direction, stop, predicted_arrival_minutes

def title_and_times_t_xpath(xpath):
    tree = etree.parse(stream)

    

def print_title_and_times(route, 
                          direction, 
                          stop, 
                          predicted_arrival_minutes):
    
    print 'Predicted arrivals for Route %s to %s  @ %s' % (route, 
                                                           direction, 
                                                           stop)

    print '\n'.join(predicted_arrival_minutes)

def decide_prediction_source(_args):

    if _args.indicate == 't':
        prediction_getter = get_prediction_t_args
    if _args.indicate == 'bus':
        prediction_getter = get_prediction_bus_args

    return prediction_getter(_args)

def main():

    route, direction, stop = get_params()

    tags = {'route_tag' : route,
                'direction_tag' : direction,
                'stop_tag' : stop
            }

    prediction_url = PREDICTION_URL % tags
    print prediction_url
    prediction_tree = etree.parse(urllib.urlopen(prediction_url))
    prediction_attributes = title_and_times_bus_xpath(prediction_tree)

    print_title_and_times(*prediction_attributes)
    
if __name__ == '__main__':
    sys.exit(main())
