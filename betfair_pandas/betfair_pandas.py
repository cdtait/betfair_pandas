import pandas as pd
import itertools
from betfair import utils
import operator

"""
This is a package of functions that:
    1. Support functions which 'flatten out' the list methods return structure
    so that they are compatible with a DataFrame or relational data table concept
    2. Implement the list methods found in  betfair.py and return pandas
    DataFrame objects and lists as an alternative to that of the default 
    betfair.py Model objects
"""

def combine_dicts(a, b, op=operator.add):
    """
    Helper:Combines dictionaries that will enable us to flatten data structure appropriately
    
    :param dict a: first of the dictionaries we want to merge
    :param dict a: second of the dictionaries we want to merge
    """
    return dict(a.items() + b.items() +
        [(k, op(a[k], b[k])) for k in set(b) & set(a)])

def market_books(books):
    """
    Give a market book list we extract all the top level attributes to form a DataFrame
    The only sub object is runners so we ignore this as it is treated separately
    
    :param list books: The market book list
    """
    mbooks=[]
    for mbook in books:
        book_attributes={key:value for key,value in mbook.iteritems() 
         if key != 'runners'}
        mbooks.append(book_attributes)
    return pd.DataFrame(mbooks)

def add_marketId(d,marketId):
    """
    Helper: Adds the marketId as key to a dict row
    
    :param dict d: Dictionary representing a row for the DataFrame
    :param obj marketId: the market id we want to add to this row
    """
    if (len(d)>0):
        d['marketId']=marketId
    return d

def add_marketId_selectionId(d,marketId,selectionId):
    """
    Helper: Adds the marketId and a selectionId as keys to a dict row
    
    :param dict d: Dictionary representing a row for the DataFrame
    :param obj marketId: the market id we want to add to this row
    :param obj selectionId: the market id we want to add to this row
    """
    if (len(d)>0):
        add_marketId(d,marketId)['selectionId']=selectionId
    return d

def runner(runner,marketId):
    """
    Give a runner in a market book we extract all the top level 
    attributes to form a row. sp,ex,orders and matches are all sub lists
    and can be treated as individual DataFrames or data tables
    of the runner and effectively represent separate entities
    The market id serves as the relational key which all related
    entities can be joined
    
    :param obj runner: the runner to 
    :param obj marketId: the market id we want to add to this row
    """
    runner_attributes={key:value for key,value in runner.iteritems() 
     if key not in ('sp','ex','orders','matches')}
    return add_marketId(runner_attributes,marketId)

def runners(books):
    """
    Take all the runners in each book and produce a DataFrame with
    each runner as a row for the market it belongs.
    
    :param obj books: market book
    """
    rs=[]
    for book in books:
        marketId=book['marketId']
        for r in book['runners']:
            rs.append(runner(r,marketId))
    return pd.DataFrame(rs) 
            
def runners_prices(books,priceType,priceSide):
    """
    Extract all the prices for all the runners in all the books
    and produce a DataFrame with the rows for the particular priceType and priceSide
    
    :param obj books: market book
    :param obj priceType: The price type we are extracting i.e ex or sp
    :param obj priceSide: The price side we are extracting for sp(backStakeTaken,layLiabilityTaken)
                          and for ex(availableToBack,availableToLay,tradedVolume)
    """
    pricesizes=[]
    for book in books:
        marketId=book['marketId']
        for runner in book['runners']:
            selectionId=runner['selectionId']
            if (priceType in runner and priceSide in runner[priceType]):
                for backPrices in runner[priceType][priceSide]:
                    pricesize=add_marketId_selectionId(backPrices,marketId,selectionId)
                    pricesizes.append(pricesize)
    return pd.DataFrame(pricesizes)

def runners_sp(books):
    """
    Extract all the top level attributes of the sp structure for 
    all the runners in all the books and produce a DataFrame with the rows
    
    :param obj books: market book
    """
    sps=[]
    for book in books:
        marketId=book['marketId']
        for runner in book['runners']:
            selectionId=runner['selectionId']
            if ('sp' in runner):
                sp={key:value for key,value in runner['sp'].iteritems() 
                    if key not in ('backStakeTaken','layLiabilityTaken')}
                sps.append(add_marketId_selectionId(sp,marketId,selectionId))
    return pd.DataFrame(sps)

def runners_orders(books,orderType):
    """
    Extract all the orders or matches sub lists of the sp for 
    all the runners in all the books and produce a DataFrame with the rows
    
    :param obj books: market book
    :param obj orderType: either orders or matches 
    """
    runners_order_items=[]
    for book in books:
        marketId=book['marketId']
        for runner in book['runners']:
            selectionId=runner['selectionId']
            if (orderType in runner):
                for order in runner[orderType]:
                    order=add_marketId_selectionId(order,marketId,selectionId)
                    runners_order_items.append(order)
    return pd.DataFrame(runners_order_items)

def market_catalogue(markets):
    """
    Extract the top level of each catalogue in the markets. We do an extensive flattening here
    by merging each market row with attributes from event,eventType,competition or description
    as these are not sub lists like runners which is treated as a different entity
    
    :param obj markets: list of market catalogues
    """
    market_items=[]
    for market in markets:
        market_attributes={key:value for key,value in market.iteritems() 
         if key != 'runners'}
        if 'event' in  market_attributes:
            event=market_attributes.pop('event')
            event_attributes={'event.'+key:value for key,value in event.iteritems()}
            market_attributes=combine_dicts(market_attributes,event_attributes)
        if 'eventType' in  market_attributes:
            eventType=market_attributes.pop('eventType')
            event_type_attributes={'eventType.'+key:value for key,value in eventType.iteritems()}
            market_attributes=combine_dicts(market_attributes,event_type_attributes)
        if 'competition' in  market_attributes:
            competition=market_attributes.pop('competition')
            competition_attributes={'competition.'+key:value for key,value in competition.iteritems()}
            market_attributes=combine_dicts(market_attributes,competition_attributes)
        if 'description' in  market_attributes:
            description=market_attributes.pop('description')
            description_attributes={'description.'+key:value for key,value in description.iteritems()}
            market_attributes=combine_dicts(market_attributes,description_attributes)
        market_items.append(market_attributes)
    return pd.DataFrame(market_items)


def market_catalogue_runners(markets):
    """
    Extract the runners in each catalogue and create a DataFrame 
    from all the runners referenced in all the catalogues
    
    :param obj markets: list of market catalogues
    """
    runners=[]
    for book in markets:
        marketId=book['marketId']
        if 'runners' in  book:
            for runner in book['runners']:
                runner=add_marketId(runner,marketId)
                runners.append(runner)
    return pd.DataFrame(runners)

def commission_applied(pnls):
    """
    Extract the commission applied for each pnl
    
    :param obj pnls: list of pnl per market
    """
    market_commissions=[]
    for pnl in pnls:
        pnl_attributes={key:value for key,value in pnl.iteritems() 
         if key != 'profitAndLosses'}
        market_commissions.append(pnl_attributes)
    return pd.DataFrame(market_commissions)

def profit_and_loss(pnls):
    """
    Extract the pnl value applied for each pnl
    
    :param obj pnls: list of pnl per market
    """
    pnl_items=[]
    for pnl in pnls:
        marketId=pnl['marketId']
        for profitAndLoss in pnl['profitAndLosses']:
            pnl_item=add_marketId(profitAndLoss,marketId)
            pnl_items.append(pnl_item)
    return pd.DataFrame(pnl_items)

# event,eventType,competition,timeRange,countryCode,marketType,venue
def flatten_simple_list(simple_list,simple_type):
    """
    Pop the attributes of a simple type up one level to flatten into one row
    
    :param obj pnls: list of pnl per market
    """
    for simpleItem in simple_list:
        simpleItem.update(simpleItem.pop(simple_type))
    return pd.DataFrame(simple_list)

#clearedOrders,currentOrders
def list_orders(orders,orderType):
    """
    Turn moreAvailable into a column of current or cleared orders
    
    :param obj pnls: list of pnl per market
    """
    return {orderType:pd.DataFrame(orders[orderType]),
            'moreAvailable':orders['moreAvailable']}

"""
    These are the list methods found in  betfair.py and return pandas
    DataFrame objects and lists as an alternative to that of the default 
    betfair.py Model objects.
    They are identical in interface to the betfair.py but use no model
    and return a named list of DataFrame objects
"""

# Bet query methods

@utils.requires_login
def list_event_types(self, filter, locale=None):
    """

    :param MarketFilter filter:
    :param str locale:

    """
    event_types=self.make_api_request(
        'listEventTypes',
        utils.get_kwargs(locals()),
        model=None,
    )
    return flatten_simple_list(event_types,'eventType')

@utils.requires_login
def list_competitions(self, filter, locale=None):
    """

    :param MarketFilter filter:
    :param str locale:

    """
    listCompetitions=self.make_api_request(
        'listCompetitions',
        utils.get_kwargs(locals()),
        model=None,
    )
    return flatten_simple_list(listCompetitions,'competition')

@utils.requires_login
def list_time_ranges(self, filter, granularity):
    """

    :param MarketFilter filter:
    :param TimeGranularity granularity:

    """
    listTimeRanges=self.make_api_request(
        'listTimeRanges',
        utils.get_kwargs(locals()),
        model=None,
    )
    return flatten_simple_list(listTimeRanges,'timeRange')

@utils.requires_login
def list_events(self, filter, locale=None):
    """

    :param MarketFilter filter:
    :param str locale:

    """
    listEvents=self.make_api_request(
        'listEvents',
        utils.get_kwargs(locals()),
        model=None,
    )
    return flatten_simple_list(listEvents,'event')

@utils.requires_login
def list_market_types(self, filter, locale=None):
    """

    :param MarketFilter filter:
    :param str locale:

    """
    listMarketTypes=self.make_api_request(
        'listMarketTypes',
        utils.get_kwargs(locals()),
        model=None,
    )
    return flatten_simple_list(listMarketTypes,'marketType')
    
@utils.requires_login
def list_countries(self, filter, locale=None):
    """

    :param MarketFilter filter:
    :param str locale:

    """
    listCountries=self.make_api_request(
        'listCountries',
        utils.get_kwargs(locals()),
        model=None,
    )
    return flatten_simple_list(listCountries,'countryCode')

@utils.requires_login
def list_venues(self, filter, locale=None):
    """

    :param MarketFilter filter:
    :param str locale:

    """
    listVenues=self.make_api_request(
        'listVenues',
        utils.get_kwargs(locals()),
        model=None,
    )
    return flatten_simple_list(listVenues,'venue')

@utils.requires_login
def list_market_catalogue(
        self, filter, max_results=100, market_projection=None, locale=None,
        sort=None):
    """

    :param MarketFilter filter:
    :param int max_results:
    :param list market_projection:
    :param MarketSort sort:
    :param str locale:

    """
    markets=self.make_api_request(
        'listMarketCatalogue',
        utils.get_kwargs(locals()),
        model=None,
    )
    return {'description':market_catalogue(markets),
            'runners':market_catalogue_runners(markets)}

@utils.requires_login
def list_market_book(
        self, market_ids, price_projection=None, order_projection=None,
        match_projection=None, currency_code=None, locale=None):
    """

    :param list market_ids: List of market IDs
    :param PriceProjection price_projection:
    :param OrderProjection order_projection:
    :param MatchProjection match_projection:
    :param str currency_code:
    :param str locale:

    """
    books=self.make_api_request(
        'listMarketBook',
        utils.get_kwargs(locals()),
        model=None,
    )
    return {'market.book':market_books(books),
    'runners':runners(books),
    'runners.sp':runners_sp(books),
    'runners.sp.backStakeTaken':runners_prices(books,'sp','backStakeTaken'),
    'runners.sp.layLiabilityTaken':runners_prices(books,'sp','layLiabilityTaken'),
    'runners.ex.availableToBack':runners_prices(books,'ex','availableToBack'),
    'runners.ex.availableToLay':runners_prices(books,'ex','availableToLay'),
    'runners.ex.tradedVolume':runners_prices(books,'ex','tradedVolume'),
    'runners.orders':runners_orders(books,'orders'),
    'runners.matches':runners_orders(books,'matches')}

@utils.requires_login
def list_market_profit_and_loss(
        self, market_ids, include_settled_bets=False,
        include_bsp_bets=None, net_of_commission=None):
    """Retrieve profit and loss for a given list of markets.

    :param list market_ids: List of markets to calculate profit and loss
    :param bool include_settled_bets: Option to include settled bets
    :param bool include_bsp_bets: Option to include BSP bets
    :param bool net_of_commission: Option to return profit and loss net of
        users current commission rate for this market including any special
        tariffs

    """
    pnls=self.make_api_request(
        'listMarketProfitAndLoss',
        utils.get_kwargs(locals()),
        model=None,
    )
    return {'commision':commission_applied(pnls),
            'runners':profit_and_loss(pnls)}

# Chunked iterators for list methods

def iter_list_market_book(self, market_ids, chunk_size, **kwargs):
    """Split call to `list_market_book` into separate requests.

    :param list market_ids: List of market IDs
    :param int chunk_size: Number of records per chunk
    :param dict kwargs: Arguments passed to `list_market_book`

    """
    return itertools.chain(*(
        list_market_book(self,market_chunk, **kwargs)
        for market_chunk in utils.get_chunks(market_ids, chunk_size)
    ))

def iter_list_market_profit_and_loss(
        self, market_ids, chunk_size, **kwargs):
    """Split call to `list_market_profit_and_loss` into separate requests.

    :param list market_ids: List of market IDs
    :param int chunk_size: Number of records per chunk
    :param dict kwargs: Arguments passed to `list_market_profit_and_loss`

    """
    return itertools.chain(*(
        list_market_profit_and_loss(self,market_chunk, **kwargs)
        for market_chunk in utils.get_chunks(market_ids, chunk_size)
    ))


# Betting methods

@utils.requires_login
def list_current_orders(
        self, bet_ids, market_ids, order_projection, date_range, order_by,
        sort_dir, from_record, record_count):
    """

    :param bet_ids:
    :param market_ids:
    :param order_projection:
    :param date_range:
    :param order_by:
    :param sort_dir:
    :param from_record:
    :param record_count:

    """
    currentOrders=self.make_api_request(
        'listCurrentOrders',
        utils.get_kwargs(locals()),
        model=None,
    )
    return list_orders(currentOrders,'currentOrders')

@utils.requires_login
def list_cleared_orders(
        self, bet_status, event_type_ids, event_ids, market_ids,
        runner_ids, bet_ids, side, settled_date_range, group_by,
        include_item_description, locale, from_record, record_count):
    """

    :param bet_status:
    :param event_type_ids:
    :param event_ids:
    :param market_ids:
    :param runner_ids:
    :param bet_ids:
    :param side:
    :param settled_date_range:
    :param group_by:
    :param include_item_description:
    :param locale:
    :param from_record:
    :param record_count:

    """
    clearedOrders=self.make_api_request(
        'listClearedOrders',
        utils.get_kwargs(locals()),
        model=None,
    )
    return list_orders(clearedOrders,'clearedOrders')
