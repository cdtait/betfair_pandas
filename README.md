betfair_pandas
==============

Pandas adapter for the Betfair API-NG implementation in the Python programming language

betfair_pandas uses Joshua Carps' betfair python implementation - https://github.com/jmcarp/betfair.py which is the reference implementation on https://developer.betfair.com/

Install using GIT

Checkout v0.1.3 for betfair.py, as this is what betfair pandas is based on for now. 
We require this specific version as we have to patch the betfair.py

```bash
git clone -b v0.1.3 https://github.com/jmcarp/betfair.py.git
git clone https://github.com/cdtait/betfair_pandas.git
```

A patch is needed to fix some betfair.py issues

```bash
cd  betfair.py
patch -p1 -i ../betfair_pandas/betfair.py-json-datetime-2-1.patch
```

Now install betfair.py

```bash
python setup.py install
```

and install betfair_pandas

```bash
cd ../betfair_pandas
python setup.py install
```

There is a samples directory which show the combination of betfair.py with pandas features

Each sample will need to have user,password,ssl certificate and app key set

### Betfair Pandas sample

Import betfair_pandas and betfair plus some support for datetime
```python
    from betfair.models import MarketFilter
    from betfair import Betfair
    import betfair_pandas as bp
    import datetime
    import dateutil
    import pandas as pd
```
Login to betfair, so you will need to add the varibles app_key,cert_file,username,password with valid values
```python
    # ssologin
    # To use this you will need app_key,cert_file,username,password
    client=Betfair(app_key,cert_file)
    client.login(username,password)
```
This is the first betfair_pandas call we make. We pass the client as a parameter instead of calling the the client object. The interface is identical apart from that. It will return panadas DataFrame rather tahn a model object
```python
    # List horse racing event ids
    event_types=bp.list_event_types(client,filter={'textQuery':"Horse Racing"})
```
Now we will use the id from event_types to create a market filter and then call on the catalogue to list the markets.In this case we set up a filter to ask for the first 5 horse races with WIN market in the UK from now
```python
    country_code='GB'
    marketFilter={'eventTypeIds':[event_types.id[0]],
                  'marketCountries':[country_code],
                  'marketTypeCodes':["WIN"],
                  'marketStartTime':{'from':datetime.datetime.now()}}
                  
    # First 5 horse races, win market, from now
    races=bp.list_market_catalogue(client,
      filter=marketFilter,
      market_projection=['COMPETITION','EVENT','EVENT_TYPE','MARKET_DESCRIPTION',
                         'RUNNER_DESCRIPTION','MARKET_START_TIME'],
      sort="FIRST_TO_START",
      max_results=5
    )
```
We have this set of races so extract some of the details. This demonstrates that the use of a DataFrame with selecting columns and merging DataFrame's together.
```python
    # Get a summary set of columns for winHorseRacing from description
    summaryDesc=races['description'][['marketId','marketName','event.venue',
                                      'event.name','marketStartTime']]
    # Get a summary set of the runners names
    summaryRunners=races['runners'][['marketId','selectionId','runnerName']]
    # Join the 2 together baes on the marketId to show summary of the runners in the races together
    summaryRaces=pd.merge(summaryDesc,summaryRunners,on='marketId')
```
Now show groupby and printout what we find.
```python
    summaryDesc.groupby(['marketStartTime','event.venue'])
    print('Races:')
    for name, group in summaryDesc.groupby(['marketStartTime','event.venue']):
        print("{0:s} {1:s} {2:s} {3:%I:%M%p}".format(group.values[0][1],
                                                     group.values[0][2],
                                                     group.values[0][3],
                                                     dateutil.parser.parse(group.values[0][4])
                                                    ))
```
Output of group printout
```coffee
    Races:
    2m Hcap Chs Fakenham Fake 18th Nov 03:30PM
    7f Hcap Southwell Sthl 18th Nov 03:40PM
    2m NHF Doncaster Donc 18th Nov 03:50PM
    1m Nursery Lingfield Ling 19th Nov 12:00PM
    2m Mdn Hrd Hexham Hex 19th Nov 12:20PM
```
Select the first race, they are order in terms of time so get marketId from row 0
```python
    # First race
    marketId=races['description'].marketId[0]
```
We use this now to construct another output for details of the first race, this demonstartes the query method on a DataFrame
```python
    # First race summary
    firstRaceDesc=summaryDesc.query('marketId=="'+marketId+'"')[['marketId','marketName',
                                                         'event.name','event.venue','marketStartTime']]
    firstRaceRunners=summaryRaces.query('marketId=="'+marketId+'"')[['selectionId','runnerName']]
    print(firstRaceDesc)
    print(firstRaceRunners)
```
Output of first race description
```coffee
          marketId   marketName     event.name event.venue             marketStartTime
    0  1.116413138  2m Hcap Chs  Fake 18th Nov    Fakenham    2014-11-18T15:30:00.000Z
```
Output to display runners in first race
```coffee
       selectionId     runnerName
    0      5718959      Carobello
    1      7572682        Larteta
    2      4363561   Dynamic Idol
    3      4815491  Full Ov Beans
```
Get hold of the prices. This call uses a more complex filter based on a pure dictionary structure as there is a gotcha when using model objects within model objects. So in this case we get 5 levels of the pricing book for exchange and sp and limit this to rollup to 20
```python
    # All exchange and starting prices to a depth of 5 max price of 20
    projection={'priceData':['EX_BEST_OFFERS','SP_AVAILABLE','SP_TRADED'],
                'virtualise':False,
                'exBestOffersOverrides':{'bestPricesDepth':5L,
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
    # Note the book time
    priceTime=datetime.datetime.now()


    print(runnersPriceInFirstRace['market.book'][['marketId','lastMatchTime',
                                                  'totalAvailable','totalMatched',
                                                  'numberOfActiveRunners']])
```
Ouput the summary of the book
```coffee
          marketId             lastMatchTime  totalAvailable  totalMatched  \
    0  1.116413138  2014-11-18T15:27:04.235Z       102182.84     191392.47   
    
       numberOfActiveRunners  
    0                      4  
```
This section now looks for the runner with the largest total match as this is what we will extract the book for shown later. Gets the overview of the one particular runner we want. This demonstartes the DataFrame where selection
```python
    runnerWithMostTotalMatched=runnersPriceInFirstRace['runners'].sort('totalMatched',
                                                                        ascending=False)

    # This is one particular runner
    runnerIdWithMostTotalMatched=runnerWithMostTotalMatched.ix[0,'selectionId']

    # Getthe overview price and volume for this selection
    runners=runnersPriceInFirstRace['runners']
    overview=runners[runners.selectionId==runnerIdWithMostTotalMatched]
```
Demostrate the use of merge on multiple columns to create the runner overview used later
```python
    # Getthe overview price and volume for this selected runner
    runnerOverview=pd.merge(overview,summaryRaces[['selectionId','marketId','runnerName']],
                            on=['selectionId','marketId'])

    allsp=runnersPriceInFirstRace['runners.sp']
    sp=allsp[allsp.selectionId==runnerIdWithMostTotalMatched]

    # Show starting price summary
    print(sp)
```
Output the starting price summary
```coffee
       farPrice     marketId  nearPrice  selectionId
    0      2.32  1.116413138          3      5718959
```
Extract the back stake taken. Her eit would be useful to point out that runnersPriceInFirstRace is a dictionary which flattens out the list lines and levels in the return structure and this is what enables us to extract the data in DatFrame format. So you may find it useful to look at the code or look at data returned
```python
runnersPriceInFirstRace.keys()
```
Get the back stake taken
```python
    # Show back stake taken
    backStakeTaken=runnersPriceInFirstRace['runners.sp.backStakeTaken']
    print(backStakeTaken[backStakeTaken.selectionId==runnerIdWithMostTotalMatched])
```
Output the back stake taken
```coffee
          marketId  price  selectionId    size
    0  1.116413138   1.01      5718959  891.27
    1  1.116413138   1.80      5718959  186.34
    2  1.116413138   3.00      5718959  980.99
    3  1.116413138   3.45      5718959  498.04
    4  1.116413138   6.00      5718959    5.00
```
Get the lay liability taken
```python
    # Show lay liabilty taken
    layLiabilityTaken=runnersPriceInFirstRace['runners.sp.layLiabilityTaken']
    print(layLiabilityTaken[layLiabilityTaken.selectionId==runnerIdWithMostTotalMatched])
```
Output the lay liability taken
```coffee
          marketId    price  selectionId    size
    0  1.116413138  1000.00      5718959  823.10
    1  1.116413138     3.20      5718959   15.95
    2  1.116413138     2.32      5718959  967.62
```
Extract the lay and back prices. This demonstrates the renaming ability we have with DatFrame's
```python
    # Get all lay prices for all the runners in the first race
    availableToLay=runnersPriceInFirstRace['runners.ex.availableToLay']
    # Get the lay prices for the one with the most total matched
    runnerIdWithMostTotalMatchedLayPrices=availableToLay[availableToLay.selectionId == runnerIdWithMostTotalMatched]
    # Rename to TotalAvailableToLay
    runnerIdWithMostTotalMatchedLayPrices=runnerIdWithMostTotalMatchedLayPrices.rename(
    columns={'size': 'LayTotal','price':'LayPrice'})

    # Get all back prices for all the runners in the first race
    availableToBack=runnersPriceInFirstRace['runners.ex.availableToBack']
    # Get the back prices for the one with the most total matched
    runnerIdWithMostTotalMatchedBackPrices=availableToBack[availableToBack.selectionId == runnerIdWithMostTotalMatched]
    # Rename to TotalAvailableToBack
    runnerIdWithMostTotalMatchedBackPrices=runnerIdWithMostTotalMatchedBackPrices.rename(
    columns={'size': 'BackTotal', 'price':'BackPrice'})
```
Join the lay and back prices and this will allowus to see what the pricing book or ladder looks like
```python
    # Merge the prices by appending to make a price ladder
    priceLadder=runnerIdWithMostTotalMatchedBackPrices[['BackTotal','BackPrice']].join(
    runnerIdWithMostTotalMatchedLayPrices[['LayPrice','LayTotal']])
    print("Market:{0:s} {1:s} {2:s} {3:%I:%M%p}".format(firstRaceDesc['marketName'][0],
                                                 firstRaceDesc['event.name'][0],
                                                 firstRaceDesc['event.venue'][0],
                                                 dateutil.parser.parse(firstRaceDesc['marketStartTime'][0]))
    )
    print("Runner:{0:s} Total {1:f} ".format(runnerOverview['runnerName'][0],
                                                 runnerOverview['totalMatched'][0]))
    print('Book at {0:s}'.format(priceTime.isoformat(' ')))
    print(priceLadder)
```
Output the book
```coffee
    Market:2m Hcap Chs Fake 18th Nov Fakenham 03:30PM
    Runner:Carobello Total 111261.690000 
    Book at 2014-11-18 15:27:04.563642
       BackTotal  BackPrice  LayPrice  LayTotal
    0    1075.11       3.00      3.05    625.80
    1     458.76       2.98      3.10    538.69
    2    1314.45       2.96      3.15    350.37
    3    1383.35       2.94      3.20    491.22
    4     524.50       2.92      3.25    651.02
```
Logout
```python
    client.logout()
```
