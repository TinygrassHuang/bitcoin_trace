# A bitcoin tracing software design
[MSc Computing -- Imperial College London](https://www.imperial.ac.uk/study/pg/computing/computing/)

## Description

This is bitcoin tracing software I developed during my master project. It can be used to trace and analyse any bitcoin
fund present in a given bitcoin address. A list of source addresses will be extracted and classified. The classifier was
trained by myself, the training data can be found in the project files. The final report was also included in the repository.

## To use it

To use the software, simply clone the project files:

```
git clone https://gitlab.doc.ic.ac.uk/zh1516/bitcoin_trace.git
cd bitcoin_trace
```

If the Python system doesn't have pip installed:

```
python -m ensurepip -upgrade
```

or,

```
python get-pip.py
```

Then install all the packages according to the configuration file *requirements.txt*:

```
pip install -r requirements.txt
```

Generate your own token in BitcoinAbuse.com and make a Python file named my_token.py in *bitcoin_trace* directory.

```
my_token.py:
  bitcoinAbuseToken = {your_token_here}
```

Before running the programme, make sure the parameters in *main.py* is what you want. To run the programme:

```
python main.py
```

## Alternative

I strongly suggest that you open *bitcoin_trace* as project directory in IDEs such as PyCharm and continue work from
there.

## Author
Zhiping (Mark) Huang, huangzp1212@gmail.com / zhiping.huang16@imperial.ac.uk
