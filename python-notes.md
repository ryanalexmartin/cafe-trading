# Python notes

install packages with pip3 (or maybe just pip)


Set up virtual environment before installing packages:

```
python3 -m venv venv
```

Then, _source_ it with:
```
source venv/bin/activate # macOS
venv/bin/activate.bat # Windows
```


### Backtesting notes:

`next()` is every trading iteration

`I()` is an indicator.  It is updated over time.  Like a "parameter" in neural networks.