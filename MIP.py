# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from pulp import *
from Data_processing import Data


class optimiser:
    def __init__(self, salary, projection, output):
        self.salary = salary
        self.projection = projection
        self.output = output
        self.prob = LpProblem('Fantasy Football', LpMaximize)
        self.selection = []

    def MIP(self, max_per_team, risk_missing, r):
        data = Data()
        data.Get_cost(self.salary)
        data.Get_proj(self.projection, risk_missing)
        data.match_data()
        QB = LpVariable.dicts('QB', {qb for qb in data.Cost_QB.keys()},
                              cat=LpBinary)
        TE = LpVariable.dicts('TE', {te for te in data.Cost_TE.keys()},
                              cat=LpBinary)
        RB = LpVariable.dicts('RB', {rb for rb in data.Cost_RB.keys()},
                              cat=LpBinary)
        WR = LpVariable.dicts('WR', {wr for wr in data.Cost_WR.keys()},
                              cat=LpBinary)
        DST = LpVariable.dicts('DST', {dst for dst in data.Cost_DST.keys()},
                               cat=LpBinary)
        FLX = LpVariable.dicts('FLX', {flx for flx in data.Cost_FLX.keys()},
                               cat=LpBinary)

        self.prob += (lpSum(QB[qb] * data.Proj_QB[qb] for qb in
                            data.Cost_QB.keys())
                      +
                      lpSum(TE[te] * data.Proj_TE[te] for te in data.Cost_TE.keys())
                      +
                      lpSum(RB[rb] * data.Proj_RB[rb] for rb in data.Cost_RB.keys())
                      +
                      lpSum(WR[wr] * data.Proj_WR[wr] for wr in data.Cost_WR.keys())
                      +
                      lpSum([DST[dst] * data.Proj_DST[dst] for dst in data.Cost_DST.keys()])
                      +
                      lpSum([FLX[flx] * data.Proj_FLX[flx] for flx in data.Cost_FLX.keys()])
                      -
                      r * (lpSum(QB[qb] * data.Risk_QB[qb] for qb in data.Cost_QB.keys())
                           +
                           lpSum(TE[te] * data.Risk_TE[te] for te in data.Cost_TE.keys())
                           +
                           lpSum(RB[rb] * data.Risk_RB[rb] for rb in data.Cost_RB.keys())
                           +
                           lpSum(WR[wr] * data.Risk_WR[wr] for wr in data.Cost_WR.keys())
                           +
                           lpSum([DST[dst] * data.Risk_DST[dst] for dst in
                                  data.Cost_DST.keys()])
                           +
                           lpSum([FLX[flx] * data.Risk_FLX[flx] for flx
                                  in data.Cost_FLX.keys()])))

        self.prob += (lpSum(QB[qb] for qb in data.Cost_QB.keys()) == 1)
        self.prob += (lpSum(TE[te] for te in data.Cost_TE.keys()) == 1)
        self.prob += (lpSum(RB[rb] for rb in data.Cost_RB.keys()) == 2)
        self.prob += (lpSum(WR[wr] for wr in data.Cost_WR.keys()) == 3)
        self.prob += (lpSum(DST[dst] for dst in data.Cost_DST.keys()) == 1)
        self.prob += (lpSum(FLX[flx] for flx in data.Cost_FLX.keys()) == 1)

        for wr in data.Cost_WR.keys():
            self.prob += (FLX[wr] + WR[wr] <= 1)
        for rb in data.Cost_RB.keys():
            self.prob += (RB[rb] + FLX[rb] <= 1)

        salary_cap = 50000
        self.prob += (lpSum(QB[qb] * data.Cost_QB[qb] for qb in
                            data.Cost_QB.keys())
                      +
                      lpSum(TE[te] * data.Cost_TE[te] for te in data.Cost_TE.keys())
                      +
                      lpSum(RB[rb] * data.Cost_RB[rb] for rb in data.Cost_RB.keys())
                      +
                      lpSum(WR[wr] * data.Cost_WR[wr] for wr in data.Cost_WR.keys())
                      +
                      lpSum(DST[dst] * data.Cost_DST[dst] for dst in
                            data.Cost_DST.keys())
                      +
                      lpSum(FLX[flx] * data.Cost_FLX[flx] for flx in
                            data.Cost_FLX.keys())
                      <= salary_cap)

        for t in data.Teams:
            self.prob += (lpSum(QB[qb] for qb in data.Cost_QB.keys()
                                if data.Player_Team[qb] == t)
                          +
                          lpSum(TE[te] for te in data.Cost_TE.keys()
                                if data.Player_Team[te] == t)
                          +
                          lpSum(RB[rb] for rb in data.Cost_RB.keys()
                                if data.Player_Team[rb] == t)
                          +
                          lpSum(WR[wr] for wr in data.Cost_WR.keys()
                                if data.Player_Team[wr] == t)
                          +
                          lpSum(DST[dst] for dst in data.Cost_DST.keys()
                                if data.Player_Team[dst] == t)
                          +
                          lpSum(FLX[flx] for flx in data.Cost_FLX.keys()
                                if data.Player_Team[flx] == t)
                          <= max_per_team)

    def solve(self, print_out):
        self.prob.solve()
        self.selection = []

        for v in self.prob.variables():
            if v.varValue > 0:
                self.selection.append(str(v))
                if print_out:
                    print(v.name, "=", v.varValue)

    def discard(self, carry_over):
        self.prob += (lpSum(v for v in self.prob.variables() if v.varValue > 0)
                      <= carry_over)

    def write_data(self, position):
        with open(self.salary, 'r') as f:
            reader = list(csv.reader(f))[8:]
            reader = [row[10:] for row in reader]
            self.selection = [word.replace('_', ' ') for word in self.selection]
            x = [([i for i in self.selection if i[0:2] == 'QB'][0][3:]),
                 [i for i in self.selection
                  if i[0:2] == 'RB'][0][3:],
                 [i for i in self.selection
                  if i[0:2] == 'RB'][1][3:],
                 [i for i in self.selection
                  if i[0:2] == 'WR'][0][3:],
                 [i for i in self.selection
                  if i[0:2] == 'WR'][1][3:],
                 [i for i in self.selection
                  if i[0:2] == 'WR'][2][3:],
                 [i for i in self.selection
                  if i[0:2] == 'TE'][0][3:],
                 [i for i in self.selection
                  if i[0:3] == 'FLX'][0][4:],
                 [i for i in self.selection
                  if i[0:3] == 'DST'][0][4:]]

            setup = []
            for i in x:
                for row in reader:
                    if row[2].strip() == i:
                        setup.append(row[1])
                        break

        with open(self.output, 'r') as f:
            reader = list(csv.reader(f))

            for i in range(0, 9):
                reader[1 + position][i] = setup[i]
            with open(self.output, 'w', newline='') as w:
                writer = csv.writer(w)
                for rows in reader:
                    writer.writerow(rows)
