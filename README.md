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

There is a samples directory which demonstartes the features of addding panadas

