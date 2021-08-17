import os.path
import sys

scr = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
       + '/scr/')
sys.path.append(scr)

from src.MIP import Optimiser


def lineups(salary, projection, output, max_per_team, risk_missing, r,
            carry_over, n_lineups):
    x = Optimiser(salary, projection, output)
    x.mip(max_per_team, risk_missing, r)
    for i in range(0, n_lineups):
        x.solve()
        x.write_data(i)
        x.discard(carry_over)


if __name__ == "__main__":
    lineups('DKSalaries.csv', 'ffa_customrankings2020.csv',
            'DKSalaries Copy.csv', 3, 0.0, 0.0, 2, 5)
