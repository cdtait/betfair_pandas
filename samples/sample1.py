'''
Created on 4 Nov 2014

@author: obod
'''
from __future__ import print_function
from betfair.models import MarketFilter
from betfair import Betfair
import betfair_pandas as bp
import datetime
import pandas as pd

if __name__ == '__main__':
    # ssologin
    # To use this you will need app_key,cert_file,username,password
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
    # Get a summary set of columns for winHorseRacing from description
    summaryDesc=races['description'][['marketId','marketName','event.venue','event.name','marketStartTime']]
    # Get a summary set of the runners names
    summaryRunners=races['runners'][['marketId','selectionId','runnerName']]
    # Join the 2 together baes on the marketId to show summary of the runners in the races together
    summaryRaces=pd.merge(summaryDesc,summaryRunners,on='marketId')
    # First race
    marketId=races['description'].marketId[0]
    print(marketId)
    # First race summary
    firstRace=summaryRaces.query('marketId=="'+marketId+'"')
    print(firstRace)
    # All exchange and starting prices to a depth of 2 max price of 20
    projection={'priceData':['EX_BEST_OFFERS','SP_AVAILABLE','SP_TRADED'],
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
    # Runner prices summary
    print(runnersPriceInFirstRace['market.book']
          [['marketId','lastMatchTime','totalAvailable','totalMatched','numberOfActiveRunners']])
    # Runner with the most macthed
    runnerWithMostTotalMatched=runnersPriceInFirstRace['runners'].sort('totalMatched',ascending=False)
    # This is one particular runner id
    runnerIdWithMostTotalMatched=runnerWithMostTotalMatched.ix[0,'selectionId']
    # Get the overview price and volume for this selection
    runners=runnersPriceInFirstRace['runners']
    overview=runners[runners.selectionId==runnerIdWithMostTotalMatched]
    # Show the overview price and volume for this selected runner
    print(pd.merge(overview,firstRace[['selectionId','marketId','runnerName']],on=['selectionId','marketId']))
    #
    allsp=runnersPriceInFirstRace['runners.sp']
    sp=allsp[allsp.selectionId==runnerIdWithMostTotalMatched]
    # Show starting price summary
    print(sp)
    # Show back stake taken
    backStakeTaken=runnersPriceInFirstRace['runners.sp.backStakeTaken']
    print(backStakeTaken[backStakeTaken.selectionId==runnerIdWithMostTotalMatched])
    # Show lay liabilty taken
    layLiabilityTaken=runnersPriceInFirstRace['runners.sp.layLiabilityTaken']
    print(layLiabilityTaken[layLiabilityTaken.selectionId==runnerIdWithMostTotalMatched])
    # Get all lay prices for all the runners in the first race
    availableToLay=runnersPriceInFirstRace['runners.ex.availableToLay']
    # Get the lay prices for the one with the most total matched
    runnerIdWithMostTotalMatchedLayPrices=availableToLay[availableToLay.selectionId == runnerIdWithMostTotalMatched]
    # Rename to TotalAvailableToLay
    runnerIdWithMostTotalMatchedLayPrices=runnerIdWithMostTotalMatchedLayPrices.rename(columns={'size': 'TotalAvailableToLay'})
    print(runnerIdWithMostTotalMatchedLayPrices)
    # Get all back prices for all the runners in the first race
    availableToBack=runnersPriceInFirstRace['runners.ex.availableToBack']
    # Get the back prices for the one with the most total matched
    runnerIdWithMostTotalMatchedBackPrices=availableToBack[availableToBack.selectionId == runnerIdWithMostTotalMatched]
    # Rename to TotalAvailableToBack
    runnerIdWithMostTotalMatchedBackPrices=runnerIdWithMostTotalMatchedBackPrices.rename(columns={'size': 'TotalAvailableToBack'})
    print(runnerIdWithMostTotalMatchedBackPrices)
    # Merge the prices by appending to make a price ladder
    priceLadder=runnerIdWithMostTotalMatchedBackPrices.append(runnerIdWithMostTotalMatchedLayPrices)[['price','TotalAvailableToBack','TotalAvailableToLay']].sort('price')
    print(priceLadder)
    #
    client.logout()
    
        