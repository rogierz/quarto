files = ["evolve.py",
"main.py",
"players/base.py",
"players/evolutionary.py",
"players/minmax.py",
# "players/mmmontecarlo.py",
"players/montecarlo.py",
"players/montecarlo_utils/montecarlo.py",
"players/montecarlo_utils/node.py",
"players/montecarlo_utils/__init__.py",
"players/naive.py",
"players/random.py",
"players/risky.py",
"players/rl.py",
"players/__init__.py",
"quarto/main.py",
"quarto/quarto/objects.py",
"quarto/quarto/__init__.py",
"quinto/quinto.py",
"train_rl.py",
"utils/logger.py",
"utils/parser.py",
"utils/__init__.py"]

for f in files:
    escaped = f.replace("_", "\\_")
    print(f"\\begin{{listing}}[!h]\n\inputminted{{python}}{{{f}}}\n\caption{{src\{escaped}}}\n\label{{src:{f}}}\n\end{{listing}}\n")