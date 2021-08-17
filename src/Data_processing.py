# Class to read in and matches the Data from DraftKings and the projection (from FantasyFootballAnalytics)
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

    def get_cost(self, filename):
        with open(filename, 'r') as f:
            reader = list(csv.reader(f))[8:]
            reader = [row[10:13] + row[14::] for row in reader]
            for row in reader[0:]:
                self.Teams.add(row[6].strip())
                if row[0] == 'RB':
                    rb = row[2]
                    self.Cost_RB.update({rb: float(row[4])})
                    self.Player_Team.update({rb: row[6].strip()})
                if row[0] == 'QB':
                    qb = row[2]
                    self.Cost_QB.update({qb: float(row[4])})
                    self.Player_Team.update({qb: row[6].strip()})
                if row[0] == 'TE':
                    te = row[2]
                    self.Cost_TE.update({te: float(row[4])})
                    self.Player_Team.update({te: row[6].strip()})
                if row[0] == 'WR':
                    wr = row[2]
                    self.Cost_WR.update({wr: float(row[4])})
                    self.Player_Team.update({wr: row[6].strip()})
                if row[0] == 'DST':
                    dst = row[2].strip()
                    self.Cost_DST.update({dst: float(row[4])})
                    self.Player_Team.update({dst: row[6].strip()})

    def get_proj(self, filename, r):
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
        qb_dk = set(self.Cost_QB)
        te_dk = set(self.Cost_TE)
        dst_dk = set(self.Cost_DST)
        wr_dk = set(self.Cost_WR)
        rb_dk = set(self.Cost_RB)
        qb_ffa = set(self.Proj_QB)
        te_ffa = set(self.Proj_TE)
        rb_ffa = set(self.Proj_RB)
        wr_ffa = set(self.Proj_WR)
        dst_ffa = set(self.Proj_DST)

        qb_matched = qb_dk.intersection(qb_ffa)
        te_matched = te_dk.intersection(te_ffa)
        dst_matched = dst_dk.intersection(dst_ffa)
        wr_matched = wr_dk.intersection(wr_ffa)
        rb_matched = rb_dk.intersection(rb_ffa)

        self.Cost_QB = {qb: self.Cost_QB[qb] for qb in qb_matched}
        self.Cost_TE = {te: self.Cost_TE[te] for te in te_matched}
        self.Cost_DST = {dst: self.Cost_DST[dst] for dst in dst_matched}
        self.Cost_WR = {wr: self.Cost_WR[wr] for wr in wr_matched}
        self.Cost_RB = {rb: self.Cost_RB[rb] for rb in rb_matched}

        self.Proj_QB = {qb: self.Proj_QB[qb] for qb in qb_matched}
        self.Proj_TE = {te: self.Proj_TE[te] for te in te_matched}
        self.Proj_DST = {dst: self.Proj_DST[dst] for dst in dst_matched}
        self.Proj_WR = {wr: self.Proj_WR[wr] for wr in wr_matched}
        self.Proj_RB = {rb: self.Proj_RB[rb] for rb in rb_matched}

        self.Cost_FLX.update(self.Cost_RB)
        self.Cost_FLX.update(self.Cost_WR)
        self.Risk_FLX.update(self.Risk_WR)
        self.Risk_FLX.update(self.Risk_RB)
        self.Proj_FLX.update(self.Proj_RB)
        self.Proj_FLX.update(self.Proj_WR)
