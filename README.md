# quarto

Computational Intelligence exam repository

> 292537 - Benedetto Leto
>
> 292442 - Ruggero Nocera

## Installing dependencies

```
pip install -r requirements.txt
```

## Run code

```
python main.py -v -p0 {naive,minmax,random,risky,montecarlo,evolutionary,rl} -p1 {naive,minmax,random,risky,montecarlo,evolutionary,rl}
```

To run a tournament (all vs all except random):

```
python main.py -p0 random -p1 random -t -v
```

To run a tournament (all vs random):

```
python main.py -p0 random -p1 random -tr -v
```

To run a benchmark over 1000 games:

```
python main.py -v -b -p0 {naive,minmax,random,risky,montecarlo,evolutionary,rl} -p1 {naive,minmax,random,risky,montecarlo,evolutionary,rl}
```

### Usage

```
user@host $ python .\main.py -h
usage: main.py [-h] [-b] [-t] [-tr] -p0 {naive,minmax,random,risky,montecarlo,evolutionary,rl} -p1 {naive,minmax,random,risky,montecarlo,evolutionary,rl} [-v] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -b, --benchmark       execute 100 iterations
  -t, --tournament      execute a tournament among all agents except random
  -tr, --tournament_against_random
                        execute a tournament of all agents against random
  -p0 {naive,minmax,random,risky,montecarlo,evolutionary,rl}
                        selects player 0
  -p1 {naive,minmax,random,risky,montecarlo,evolutionary,rl}
                        selects player 1
  -v, --verbose         increase log verbosity
  -d, --debug           log debug messages (same as -vv)
```
