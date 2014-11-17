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

```python
    from betfair.models import MarketFilter
    from betfair import Betfair


    import betfair_pandas as bp
    import datetime
    import pandas as pd


    # ssologin
    # To use this you will need app_key,cert_file,username,password
    client=Betfair(app_key,cert_file)
    client.login(username,password)


    # List horse racing event ids
    event_types=bp.list_event_types(client,filter={'textQuery':"Horse Racing"})


    country_code='GB'
    marketFilter={'eventTypeIds':[event_types.id[0]],
                  'marketCountries':[country_code],
                  'marketTypeCodes':["WIN"],
                  'marketStartTime':{'from':datetime.datetime.now()}}


    # First 5 horse races, win market, from now
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


    # First race summary
    firstRace=summaryRaces.query('marketId=="'+marketId+'"')
    firstRace

```

<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>marketId</th>
      <th>marketName</th>
      <th>event.venue</th>
      <th>event.name</th>
      <th>marketStartTime</th>
      <th>selectionId</th>
      <th>runnerName</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td> 1.116406554</td>
      <td> 2m Nov Hrd</td>
      <td> Plumpton</td>
      <td> Plump 17th Nov</td>
      <td> 2014-11-17T13:00:00.000Z</td>
      <td> 6865392</td>
      <td>           Seedling</td>
    </tr>
    <tr>
      <th>1</th>
      <td> 1.116406554</td>
      <td> 2m Nov Hrd</td>
      <td> Plumpton</td>
      <td> Plump 17th Nov</td>
      <td> 2014-11-17T13:00:00.000Z</td>
      <td> 7633363</td>
      <td>          As De Mee</td>
    </tr>
    <tr>
      <th>2</th>
      <td> 1.116406554</td>
      <td> 2m Nov Hrd</td>
      <td> Plumpton</td>
      <td> Plump 17th Nov</td>
      <td> 2014-11-17T13:00:00.000Z</td>
      <td> 9002287</td>
      <td>       Stars Royale</td>
    </tr>
    <tr>
      <th>3</th>
      <td> 1.116406554</td>
      <td> 2m Nov Hrd</td>
      <td> Plumpton</td>
      <td> Plump 17th Nov</td>
      <td> 2014-11-17T13:00:00.000Z</td>
      <td> 1119547</td>
      <td>           Sea Wall</td>
    </tr>
    <tr>
      <th>4</th>
      <td> 1.116406554</td>
      <td> 2m Nov Hrd</td>
      <td> Plumpton</td>
      <td> Plump 17th Nov</td>
      <td> 2014-11-17T13:00:00.000Z</td>
      <td> 8199435</td>
      <td> The Geegeez Geegee</td>
    </tr>
    <tr>
      <th>5</th>
      <td> 1.116406554</td>
      <td> 2m Nov Hrd</td>
      <td> Plumpton</td>
      <td> Plump 17th Nov</td>
      <td> 2014-11-17T13:00:00.000Z</td>
      <td> 6251329</td>
      <td>           Dellbuoy</td>
    </tr>
    <tr>
      <th>6</th>
      <td> 1.116406554</td>
      <td> 2m Nov Hrd</td>
      <td> Plumpton</td>
      <td> Plump 17th Nov</td>
      <td> 2014-11-17T13:00:00.000Z</td>
      <td> 8930741</td>
      <td>  Knockyoursocksoff</td>
    </tr>
    <tr>
      <th>7</th>
      <td> 1.116406554</td>
      <td> 2m Nov Hrd</td>
      <td> Plumpton</td>
      <td> Plump 17th Nov</td>
      <td> 2014-11-17T13:00:00.000Z</td>
      <td> 7192335</td>
      <td>     Master Vintage</td>
    </tr>
    <tr>
      <th>8</th>
      <td> 1.116406554</td>
      <td> 2m Nov Hrd</td>
      <td> Plumpton</td>
      <td> Plump 17th Nov</td>
      <td> 2014-11-17T13:00:00.000Z</td>
      <td> 7323360</td>
      <td>          Al Guwair</td>
    </tr>
    <tr>
      <th>9</th>
      <td> 1.116406554</td>
      <td> 2m Nov Hrd</td>
      <td> Plumpton</td>
      <td> Plump 17th Nov</td>
      <td> 2014-11-17T13:00:00.000Z</td>
      <td> 6365550</td>
      <td>        Epsom Flyer</td>
    </tr>
  </tbody>
</table>
</div>

<p/>

```python
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


    runnersPriceInFirstRace['market.book'][['marketId','lastMatchTime','totalAvailable','totalMatched','numberOfActiveRunners']]

```


<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>marketId</th>
      <th>lastMatchTime</th>
      <th>totalAvailable</th>
      <th>totalMatched</th>
      <th>numberOfActiveRunners</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td> 1.116406554</td>
      <td> 2014-11-17T12:59:43.886Z</td>
      <td> 266490.09</td>
      <td> 724222.82</td>
      <td> 10</td>
    </tr>
  </tbody>
</table>
</div>

<p/>
```python

    runnerWithMostTotalMatched=runnersPriceInFirstRace['runners'].sort('totalMatched',ascending=False)


    # This is one particular runner
    runnerIdWithMostTotalMatched=runnerWithMostTotalMatched.ix[0,'selectionId']


    # Getthe overview price and volume for this selection
    runners=runnersPriceInFirstRace['runners']
    overview=runners[runners.selectionId==runnerIdWithMostTotalMatched]


    # Show the overview price and volume for this selected runner
    pd.merge(overview,firstRace[['selectionId','marketId','runnerName']],on=['selectionId','marketId'])

```


<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>adjustmentFactor</th>
      <th>handicap</th>
      <th>lastPriceTraded</th>
      <th>marketId</th>
      <th>selectionId</th>
      <th>status</th>
      <th>totalMatched</th>
      <th>runnerName</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td> 73.5</td>
      <td> 0</td>
      <td> 1.22</td>
      <td> 1.116406554</td>
      <td> 6865392</td>
      <td> ACTIVE</td>
      <td> 643910.59</td>
      <td> Seedling</td>
    </tr>
  </tbody>
</table>
</div>

<p/>
```python

    allsp=runnersPriceInFirstRace['runners.sp']
    sp=allsp[allsp.selectionId==runnerIdWithMostTotalMatched]


    # Show starting price summary
    sp

```


<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>farPrice</th>
      <th>marketId</th>
      <th>nearPrice</th>
      <th>selectionId</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td> 1.047462</td>
      <td> 1.116406554</td>
      <td> 1.2</td>
      <td> 6865392</td>
    </tr>
  </tbody>
</table>
</div>
<p/>
```python


    # Show back stake taken
    backStakeTaken=runnersPriceInFirstRace['runners.sp.backStakeTaken']
    backStakeTaken[backStakeTaken.selectionId==runnerIdWithMostTotalMatched]

```


<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>marketId</th>
      <th>price</th>
      <th>selectionId</th>
      <th>size</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td> 1.116406554</td>
      <td> 1.01</td>
      <td> 6865392</td>
      <td> 7574.55</td>
    </tr>
    <tr>
      <th>1</th>
      <td> 1.116406554</td>
      <td> 1.20</td>
      <td> 6865392</td>
      <td>    4.01</td>
    </tr>
    <tr>
      <th>2</th>
      <td> 1.116406554</td>
      <td> 1.33</td>
      <td> 6865392</td>
      <td>    2.00</td>
    </tr>
    <tr>
      <th>3</th>
      <td> 1.116406554</td>
      <td> 1.40</td>
      <td> 6865392</td>
      <td>   14.00</td>
    </tr>
    <tr>
      <th>4</th>
      <td> 1.116406554</td>
      <td> 1.48</td>
      <td> 6865392</td>
      <td>   41.27</td>
    </tr>
    <tr>
      <th>5</th>
      <td> 1.116406554</td>
      <td> 1.59</td>
      <td> 6865392</td>
      <td>   60.75</td>
    </tr>
    <tr>
      <th>6</th>
      <td> 1.116406554</td>
      <td> 2.06</td>
      <td> 6865392</td>
      <td>   56.60</td>
    </tr>
    <tr>
      <th>7</th>
      <td> 1.116406554</td>
      <td> 3.00</td>
      <td> 6865392</td>
      <td>   40.00</td>
    </tr>
    <tr>
      <th>8</th>
      <td> 1.116406554</td>
      <td> 5.00</td>
      <td> 6865392</td>
      <td>    9.98</td>
    </tr>
    <tr>
      <th>9</th>
      <td> 1.116406554</td>
      <td> 6.00</td>
      <td> 6865392</td>
      <td>   30.00</td>
    </tr>
  </tbody>
</table>
</div>
<p/>

```python

    # Show lay liabilty taken
    layLiabilityTaken=runnersPriceInFirstRace['runners.sp.layLiabilityTaken']
    layLiabilityTaken[layLiabilityTaken.selectionId==runnerIdWithMostTotalMatched]


```

<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>marketId</th>
      <th>price</th>
      <th>selectionId</th>
      <th>size</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td> 1.116406554</td>
      <td> 1000.0</td>
      <td> 6865392</td>
      <td> 681.16</td>
    </tr>
    <tr>
      <th>1</th>
      <td> 1.116406554</td>
      <td>    1.5</td>
      <td> 6865392</td>
      <td>  15.97</td>
    </tr>
  </tbody>
</table>
</div>

<p/>
```python

    # Get all lay prices for all the runners in the first race
    availableToLay=runnersPriceInFirstRace['runners.ex.availableToLay']
    # Get the lay prices for the one with the most total matched
    runnerIdWithMostTotalMatchedLayPrices=availableToLay[availableToLay.selectionId == runnerIdWithMostTotalMatched]
    # Rename to TotalAvailableToLay
    runnerIdWithMostTotalMatchedLayPrices=runnerIdWithMostTotalMatchedLayPrices.rename(columns={'size': 'TotalAvailableToLay'})


    runnerIdWithMostTotalMatchedLayPrices


```


<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>marketId</th>
      <th>price</th>
      <th>selectionId</th>
      <th>TotalAvailableToLay</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td> 1.116406554</td>
      <td> 1.22</td>
      <td> 6865392</td>
      <td>  123.12</td>
    </tr>
    <tr>
      <th>1</th>
      <td> 1.116406554</td>
      <td> 1.23</td>
      <td> 6865392</td>
      <td> 5615.98</td>
    </tr>
  </tbody>
</table>
</div>
<p/>

```python

    # Get all back prices for all the runners in the first race
    availableToBack=runnersPriceInFirstRace['runners.ex.availableToBack']
    # Get the back prices for the one with the most total matched
    runnerIdWithMostTotalMatchedBackPrices=availableToBack[availableToBack.selectionId == runnerIdWithMostTotalMatched]
    # Rename to TotalAvailableToBack
    runnerIdWithMostTotalMatchedBackPrices=runnerIdWithMostTotalMatchedBackPrices.rename(columns={'size': 'TotalAvailableToBack'})


    runnerIdWithMostTotalMatchedBackPrices


```

<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>marketId</th>
      <th>price</th>
      <th>selectionId</th>
      <th>TotalAvailableToBack</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td> 1.116406554</td>
      <td> 1.21</td>
      <td> 6865392</td>
      <td>  5471.57</td>
    </tr>
    <tr>
      <th>1</th>
      <td> 1.116406554</td>
      <td> 1.20</td>
      <td> 6865392</td>
      <td> 10690.61</td>
    </tr>
  </tbody>
</table>
</div>

<p/>
```python

    # Merge the prices by appending to make a price ladder
    priceLadder=runnerIdWithMostTotalMatchedBackPrices.append(runnerIdWithMostTotalMatchedLayPrices)[['price','TotalAvailableToBack','TotalAvailableToLay']].sort('price')
    priceLadder

```


<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>price</th>
      <th>TotalAvailableToBack</th>
      <th>TotalAvailableToLay</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td> 1.20</td>
      <td> 10690.61</td>
      <td>     NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td> 1.21</td>
      <td>  5471.57</td>
      <td>     NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td> 1.22</td>
      <td>      NaN</td>
      <td>  123.12</td>
    </tr>
    <tr>
      <th>1</th>
      <td> 1.23</td>
      <td>      NaN</td>
      <td> 5615.98</td>
    </tr>
  </tbody>
</table>
</div>
<p/>
```python


    client.logout()
```