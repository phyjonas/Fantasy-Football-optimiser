from MIP import optimiser


def lineups(salary, projection, output, max_per_team, risk_missing, r,
            carry_over, n_lineups):
    x = optimiser(salary, projection, output)
    x.MIP(max_per_team, risk_missing, r)
    for i in range(0, n_lineups):
        x.solve(False)
        x.write_data(i)
        x.discard(carry_over)


if __name__ == "__main__":
    lineups('DKSalaries.csv', 'ffa_customrankings2020.csv',
            'DKSalaries Copy.csv', 3, 0.0, 0.0, 2, 5)
