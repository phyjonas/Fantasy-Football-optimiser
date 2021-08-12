import csv


class Data:
    def __init__(self):
        self.Teams = set()
        self.Cost_QB = dict()
        self.Cost_TE = dict()
        self.Cost_DST = dict()
        self.Cost_WR = dict()
        self.Cost_RB = dict()
        self.Cost_FLX = dict()
        self.Player_Team = dict()
        self.Proj_QB = dict()
        self.Proj_TE = dict()
        self.Proj_RB = dict()
        self.Proj_WR = dict()
        self.Proj_DST = dict()
        self.Proj_FLX = dict()
        self.Risk_QB = dict()
        self.Risk_TE = dict()
        self.Risk_RB = dict()
        self.Risk_WR = dict()
        self.Risk_DST = dict()
        self.Risk_FLX = dict()

    def Get_cost(self, filename):
        with open(filename, 'r') as f:
            reader = list(csv.reader(f))[8:]
            reader = [row[10:13] + row[14::] for row in reader]
            for row in reader[0:]:
                self.Teams.add(row[6].strip())
                if row[0] == 'RB':
                    RB = row[2]
                    self.Cost_RB.update({RB: float(row[4])})
                    self.Player_Team.update({RB: row[6].strip()})
                if row[0] == 'QB':
                    QB = row[2]
                    self.Cost_QB.update({QB: float(row[4])})
                    self.Player_Team.update({QB: row[6].strip()})
                if row[0] == 'TE':
                    TE = row[2]
                    self.Cost_TE.update({TE: float(row[4])})
                    self.Player_Team.update({TE: row[6].strip()})
                if row[0] == 'WR':
                    WR = row[2]
                    self.Cost_WR.update({WR: float(row[4])})
                    self.Player_Team.update({WR: row[6].strip()})
                if row[0] == 'DST':
                    DST = row[2].strip()
                    self.Cost_DST.update({DST: float(row[4])})
                    self.Player_Team.update({DST: row[6].strip()})

    def Get_proj(self, filename, r):
        with open(filename, 'r') as f:
            reader = list(csv.reader(f))
            header = reader[0]
            for i in range(0, len(reader[0])):
                if header[i] == "player":
                    player = i
                if header[i] == "position":
                    position = i
                if header[i] == "points":
                    points = i
                if header[i] == 'risk':
                    risk = i
            for row in reader[1:]:
                if row[position] == 'RB':
                    RB = row[player]
                    self.Proj_RB.update({RB: float(row[points])})
                    try:
                        self.Risk_RB.update({RB: float(row[risk])})
                    except:
                        self.Risk_RB.update({RB: r * float(row[points])})
                if row[position] == 'QB':
                    QB = row[player]
                    self.Proj_QB.update({QB: float(row[points])})
                    try:
                        self.Risk_QB.update({QB: float(row[risk])})
                    except:
                        self.Risk_QB.update({QB: r * float(row[points])})
                if row[position] == 'TE':
                    TE = row[player]
                    self.Proj_TE.update({TE: float(row[points])})
                    try:
                        self.Risk_TE.update({TE: float(row[risk])})
                    except:
                        self.Risk_TE.update({TE: r * float(row[points])})
                if row[position] == 'WR':
                    WR = row[player]
                    self.Proj_WR.update({WR: float(row[points])})
                    try:
                        self.Risk_WR.update({WR: float(row[risk])})
                    except:
                        self.Risk_WR.update({WR: r * float(row[points])})
                if row[position] == 'DST':
                    DST = row[player]
                    self.Proj_DST.update({DST: float(row[points])})
                    try:
                        self.Risk_DST.update({DST: float(row[risk])})
                    except:
                        self.Risk_DST.update({DST: r * float(row[points])})

    def match_data(self):
        QB_DK = set(self.Cost_QB)
        TE_DK = set(self.Cost_TE)
        DST_DK = set(self.Cost_DST)
        WR_DK = set(self.Cost_WR)
        RB_DK = set(self.Cost_RB)
        QB_FFA = set(self.Proj_QB)
        TE_FFA = set(self.Proj_TE)
        RB_FFA = set(self.Proj_RB)
        WR_FFA = set(self.Proj_WR)
        DST_FFA = set(self.Proj_DST)

        QB_matched = QB_DK.intersection(QB_FFA)
        TE_matched = TE_DK.intersection(TE_FFA)
        DST_matched = DST_DK.intersection(DST_FFA)
        WR_matched = WR_DK.intersection(WR_FFA)
        RB_matched = RB_DK.intersection(RB_FFA)

        self.Cost_QB = {qb: self.Cost_QB[qb] for qb in QB_matched}
        self.Cost_TE = {te: self.Cost_TE[te] for te in TE_matched}
        self.Cost_DST = {dst: self.Cost_DST[dst] for dst in DST_matched}
        self.Cost_WR = {wr: self.Cost_WR[wr] for wr in WR_matched}
        self.Cost_RB = {rb: self.Cost_RB[rb] for rb in RB_matched}

        self.Proj_QB = {qb: self.Proj_QB[qb] for qb in QB_matched}
        self.Proj_TE = {te: self.Proj_TE[te] for te in TE_matched}
        self.Proj_DST = {dst: self.Proj_DST[dst] for dst in DST_matched}
        self.Proj_WR = {wr: self.Proj_WR[wr] for wr in WR_matched}
        self.Proj_RB = {rb: self.Proj_RB[rb] for rb in RB_matched}

        self.Cost_FLX.update(self.Cost_RB)
        self.Cost_FLX.update(self.Cost_WR)
        self.Risk_FLX.update(self.Risk_WR)
        self.Risk_FLX.update(self.Risk_RB)
        self.Proj_FLX.update(self.Proj_RB)
        self.Proj_FLX.update(self.Proj_WR)
