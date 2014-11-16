'''
Created on 4 Nov 2014

@author: obod
'''
from __future__ import print_function
from betfair.models import MarketFilter
from betfair import Betfair
import betfair_pandas as bp
import datetime

if __name__ == '__main__':
    # ssologin
    client=Betfair(app_key,cert_file)
    client.login(username,password)
    # List horse racing event ids
    event_types=bp.list_event_types(client,filter={'textQuery':"Horse Racing"})
    # First 5 UK horse races, win market, from now
    country_code='GB'
    marketFilter={'eventTypeIds':[event_types.id[0]],
                  'marketCountries':[country_code],
                  'marketTypeCodes':["WIN"],
                  'marketStartTime':{'from':datetime.datetime.now()}}
    races=bp.list_market_catalogue(client,
                                   filter=marketFilter,
                                   market_projection=['COMPETITION','EVENT','EVENT_TYPE','MARKET_DESCRIPTION','RUNNER_DESCRIPTION','MARKET_START_TIME'],
                                   sort="FIRST_TO_START",
                                   max_results=5
                                   )
    # First race
    marketId=races['description'].marketId[0]
    # All exchange and starting prices to a depth of 2 max price of 20
    projection={'priceData':['EX_ALL_OFFERS','SP_AVAILABLE','SP_TRADED','EX_TRADED'],
                'virtualise':False,
                'exBestOffersOverrides':{'bestPricesDepth':2L,
                                         'rollupModel':"STAKE",
                                         'rollupLimit':20L},
                'rolloverStakes':False
                }
    # Get all the runners/prices book for this market
    # According to the projections
    runnersPriceInFirstRace=bp.list_market_book(client,
                                                market_ids=[marketId],
                                                price_projection=projection,
                                                order_projection='ALL',
                                                match_projection='ROLLED_UP_BY_PRICE'
                                                )
    print(runnersPriceInFirstRace['market.book'][['marketId','lastMatchTime','totalAvailable','totalMatched','numberOfActiveRunners']])
    print(runnersPriceInFirstRace['runners'])
    
    client.logout()
    
        