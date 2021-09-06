from numpy.core.numeric import NaN
import pandas as pd
import numpy as np
import random
from operator import itemgetter # to get key with max value in dict
from import_list import *

class individual:
    def __init__(self,args,n):
        self.fname = args["fname"]
        self.fixed_fname = args["fixed_fname"]
        self.prof_data = None
        self.place_data = None
        self.class_names = None
        self.prof_names = None  
        self.periods = [int(str(i)+str(j)) for i in [1,2,3,4,5] for j in [1,2,3,4,5,6]]
        
        self.seed = args["seed"]*(n+1)
        random.seed(self.seed)
        # print("Seed",self.seed)

        self.flat_TT = None
        self.TT_pos = None
        self.flat_fixed_TT = None
        self.SCM()

        self.cost = None
        self.cost_TT = None
        self.fitness = None
        self.tot_fitness = None
        self.get_fitness()
        
    def init_timetable(self):
        self.prof_data, self.place_data, self.class_names, self.prof_names = get_data(self.fname, self.fixed_fname)

        self.flat_TT = pd.DataFrame(index=self.class_names, columns=self.periods)
        
        self.TT_pos = {}
        for name in self.class_names:
            self.TT_pos[name] = [int(str(i)+str(j)) for i in [1,2,3,4,5] for j in [1,2,3,4,5,6]]

        self.flat_fixed_TT = self.flat_TT.applymap(lambda _: 0)

    def SCM(self):
        while 1:
            self.init_timetable()

            # fill the timetables with Sequential Construction Method
            x = 1
            while x: # x = 0: finish, x = 1: continue, x = 99: restart
                x = self.allocate_to_TT()

                if x == 99: # if error, go back to initial while
                    break
                    
                if x == 0: # if finished, store final TT and return
                    print("individual generated")
                    return

    def allocate_to_TT(self):

        self.place_data = self.place_data.sort_values(by=["Fix","Type","Sat"],ascending=[False,False,True])

        val = self.place_data.iloc[0]

        if val["Type"] >= 0 and val["Sat"] > 0:
            if val["Type"] == 0:
                pos = random.choice(val["Pos"])
                pos2 = None

                self.flat_TT.loc[val["Class"], pos] = val["Teacher"]
                val["Type"] = -1

                if val["Fix"]:
                    self.flat_fixed_TT.loc[val["Class"], pos] += 1
                    val["Fix"] = 0

            elif val["Type"] == 1:
                pos = None
                for p in random.sample(val["Pos"],len(val["Pos"])):
                    if p+1 in val["Pos"]:
                        pos = p
                        pos2 = p+1
                        break

                if not pos:
                    return 99

                self.flat_TT.loc[val["Class"], pos] = val["Teacher"]
                self.flat_TT.loc[val["Class"], pos2] = val["Teacher"]
                val["Type"] = -1

                if val["Fix"]:
                    self.flat_fixed_TT.loc[val["Class"], pos] += 1
                    self.flat_fixed_TT.loc[val["Class"], pos2] += 1
                    val["Fix"] = 0

            elif val["Type"] == 2:
                pos = None
                for p in random.sample(val["Pos"],len(val["Pos"])):
                    if p%10 == 1 and p+1 in val["Pos"]:
                        pos = p
                        pos2 = p+1
                        break
                
                if not pos:
                    return 99

                self.flat_TT.loc[val["Class"], pos] = val["Teacher"]
                self.flat_TT.loc[val["Class"], pos2] = val["Teacher"]
                val["Type"] = -1

                self.flat_fixed_TT.loc[val["Class"], pos] += 1
                self.flat_fixed_TT.loc[val["Class"], pos2] += 1

                if val["Fix"]: val["Fix"] = 0

            if pos in self.TT_pos[val["Class"]]:     self.TT_pos[val["Class"]].remove(pos)
            if pos2 in self.TT_pos[val["Class"]]:    self.TT_pos[val["Class"]].remove(pos2)

            # remove all the possibilities that are no more possible
            for _, val2 in self.place_data.iterrows():
                # remove single
                # 1- same class and position for all the profs
                if val2["Class"] == val["Class"] and pos in val2["Pos"]:
                    val2["Pos"].remove(pos)
                    val2["Sat"]-=1
                # 2- same teacher and position for all the classes
                if val2["Teacher"] == val["Teacher"] and pos in val2["Pos"]:
                    val2["Pos"].remove(pos)
                    val2["Sat"]-=1

                # remove double
                # 1- same class and position for all the profs
                if val2["Class"] == val["Class"] and pos2 in val2["Pos"]:
                    val2["Pos"].remove(pos2)
                    val2["Sat"]-=1
                # 2- same teacher and position for all the classes
                if val2["Teacher"] == val["Teacher"] and pos2 in val2["Pos"]:
                    val2["Pos"].remove(pos2)
                    val2["Sat"]-=1

                # remove in-day slots same prof
                if val2["Class"] == val["Class"] and val2["Teacher"] == val["Teacher"]:
                    for p in val2["Pos"].copy():
                        if pos//10 == p//10:
                            val2["Pos"].remove(p)  
                            val2["Sat"]-=1

            return 1

        # case random
        elif val["Type"] >= 0:
            if val["Type"] == 0:
                pos = random.choice(self.TT_pos[val["Class"]])
                self.flat_TT.loc[val["Class"], pos] = val["Teacher"]
                val["Type"] = -1
                
            if pos in self.TT_pos[val["Class"]]: self.TT_pos[val["Class"]].remove(pos)
            
            # remove all the possibilities that are no more possible
            for _, val2 in self.place_data.iterrows():
                # remove single
                # 1- same class and position for all the profs
                if val2["Class"] == val["Class"] and pos in val2["Pos"]:
                    val2["Pos"].remove(pos)
                    val2["Sat"]-=1
                # 2- same teacher and position for all the classes
                if val2["Teacher"] == val["Teacher"] and pos in val2["Pos"]:
                    val2["Pos"].remove(pos)
                    val2["Sat"]-=1
                # remove in-day slots same prof
                if val2["Class"] == val["Class"] and val2["Teacher"] == val["Teacher"]:
                    for p in val2["Pos"].copy():
                        if pos//10 == p//10:
                            val2["Pos"].remove(p)
                            val2["Sat"]-=1

            return 1
        
        return 0

    # -------------------------- MANIPULATION --------------------------
    def teacher_class_TT(self, name, cls):
        cls_week = self.flat_TT.loc[cls].tolist()
        teacher_week = []
        for slot in cls_week:
            if slot == name:
                teacher_week.append(name)
            else:
                teacher_week.append(" ")
        teacher_class_TT = [list(teacher_week)[i:i+6] for i in [0,6,12,18,24]]
        return teacher_class_TT

    def teacher_TT(self,name):
        teacher_week = []
        for period in self.flat_TT:
            slot_list = list(self.flat_TT[period])
            if name in slot_list:
                val = self.flat_TT.index[self.flat_TT[period]==name].tolist()
                teacher_week.append(val[0])
            else:
                teacher_week.append(" ")
        teacher_TT = [teacher_week[i:i+6] for i in [0,6,12,18,24]]
        return teacher_TT

    def find_holes(self,day,tot=True):
        if day.count(" ") != 6:
            while day[0] == " ":  del day[0]
            while day[-1] == " ": del day[-1]

        if tot:
            res = 0
            record = False
            for slot in day:
                if not record and slot != " ":
                    record = True
                elif record and slot == " ":
                    res += 1

            return res
        else:
            res = []
            record = False
            for slot in day:
                if slot != " ":
                    if record: res[-1]+=1
                    else:
                        res.append(1)
                        record = True
                else: record = False
            
            return res

    # ------------------------------ FITNESS -------------------------------
    def update_cost_TT(self,row,col,val):
        # update the cost only if the slot is not fixed
        if not self.is_fixed(row,col):
            self.cost += val
            self.cost_TT.loc[row,col] += val

    def HC1(self): # collisions in periods
        self.cost = 0
        for period in self.flat_TT:
            for teacher in self.prof_names:
                if list(self.flat_TT[period]).count(teacher) > 1:
                    idxs = np.where(self.flat_TT[period] == teacher)[0].tolist()
                    for i in idxs:
                        self.update_cost_TT(self.class_names[i], period, 100)
        
        self.fitness["HC1"] = self.cost

    def HC2(self): # only one meet per day and with correct pattern
        self.cost = 0

        for _, val in self.prof_data.iterrows():
            name = val["Teacher"]
            cls = val["Class"]
            sub = val["Subject"]

            teacher_class_TT = self.teacher_class_TT(name,cls)

            if   sub == "ISG":  pattern = [2,2,2,2,2]
            elif sub == "I":    pattern = [2,1,1,1,1]
            elif sub == "SG":   pattern = [1,1,1,1,0]
            elif sub == "IS":   pattern = [2,2,2,1,1]
            elif sub == "G":    pattern = [1,1,0,0,0]
            elif sub == "MS":   pattern = [2,1,1,1,1]
            elif sub == "ING":  pattern = [1,1,1,0,0]
            elif sub == "M":    pattern = [1,1,0,0,0]
            elif sub == "T":    pattern = [1,1,0,0,0]
            elif sub == "SL":   pattern = [1,1,0,0,0]
            elif sub == "TED":  pattern = [1,1,0,0,0]
            elif sub == "FRA":  pattern = [1,1,0,0,0]
            elif sub == "SPA":  pattern = [1,1,0,0,0]
            elif sub == "MOT":  pattern = [1,1,0,0,0]
            elif sub == "A":    pattern = [2,0,0,0,0]
            elif sub == "R":    pattern = [1,0,0,0,0]

            # remove fixed from pattern
            day_idx = 0
            for day in teacher_class_TT:
                day_idx += 1
                cnt = self.find_holes(day.copy(),tot=False) 
                if len(cnt)==1 and cnt[0] in pattern:
                    idxs = np.where(np.array(day) == name)[0].tolist()
                    fixed = False
                    for i in idxs:
                        if self.is_fixed(cls,int(str(day_idx)+str(i+1))):
                            fixed = True
                    if fixed:
                        pattern.remove(cnt[0])

            day_idx = 0
            for day in teacher_class_TT:
                day_idx += 1
                cnt = self.find_holes(day.copy(),tot=False)                
                if len(cnt)>1:
                    idxs = np.where(np.array(day) == name)[0].tolist()
                    i = random.choice(idxs)
                    self.update_cost_TT(cls, int(str(day_idx)+str(i+1)), 100)
                elif len(cnt)==0 and 0 in pattern:
                    pattern.remove(0)
                elif len(cnt)==1:
                    if cnt[0] in pattern: 
                        pattern.remove(cnt[0])
                    else:
                        for p in pattern:
                            if cnt[0] > p:
                                idxs = np.where(np.array(day) == name)[0].tolist()
                                i = idxs[-1]
                                self.update_cost_TT(cls, int(str(day_idx)+str(i+1)), 100)
                                break

        self.fitness["HC2"] = self.cost

    def HC3(self): # not all six hours
        self.cost = 0

        for name in self.prof_names:
            teacher_TT = self.teacher_TT(name)

            day_idx = 0
            for day in teacher_TT:
                day_idx += 1
                if day.count(" ") == 0:
                    i = 5
                    self.update_cost_TT(day[i], int(str(day_idx)+str(i+1)), 100)

        self.fitness["HC3"] = self.cost

    def SC1(self): # count number of holes, taking max and mean
        hole_map = {}
        for name in self.prof_names:
            teacher_TT = self.teacher_TT(name)
            hole_map[name] = 0
            for day in teacher_TT:
                cnt = self.find_holes(day)
                hole_map[name] += cnt

        self.fitness["SC1_max"] = np.max(list(hole_map.values()))
        self.fitness["SC1_mean"] = round(np.mean(list(hole_map.values())),2)

    def get_fitness(self):
        self.fitness = {}
        self.cost_TT = self.flat_TT.applymap(lambda x: 0)

        self.HC1()
        self.HC2()
        self.HC3()
        self.SC1()

        self.tot_fitness = round(sum(self.fitness.values()),2)

    # ------------------------------ MUTATION -------------------------------
    def is_fixed(self,row,col):
        if self.flat_fixed_TT.loc[row,col] == 1:
            return True
        return False

    def find_two_max_cost(self):
        tot_max = 0
        idx_max, col_max = None, None
        for index, row in self.cost_TT.iterrows():
            tot = sum(list(row.nlargest(2)))
            if tot >= tot_max:
                tot_max = tot
                idx_max = index
                col_max = list(row.nlargest(2).index)

        return idx_max, col_max

    def chose_rand(self,cls_week,row,i1):
        i2_pos = random.sample(range(len(cls_week)),len(cls_week))
        for i2 in i2_pos:
            if not self.is_fixed(row,list(self.flat_TT.columns)[i2]):
                if not i1: return i2
                elif i1 and cls_week[i1] != cls_week[i2]: return i2
        
        print("NO POSSIBILITIES")

    def offspring_worst_rand_swap(self):
        row, col = self.find_two_max_cost()
        cls_week = self.flat_TT.loc[row].tolist()

        i1 = list(self.flat_TT.columns).index(col[0])
        i2 = self.chose_rand(cls_week,row,i1)

        cls_week[i1], cls_week[i2] = cls_week[i2], cls_week[i1]
        self.flat_TT.loc[row] = cls_week

        self.get_fitness()

    def offspring_rand_swap(self):
        row = random.choice(self.flat_TT.index.tolist())  
        cls_week = self.flat_TT.loc[row].tolist()

        i1 = self.chose_rand(cls_week,row,None)
        i2 = self.chose_rand(cls_week,row,i1)

        cls_week[i1], cls_week[i2] = cls_week[i2], cls_week[i1]
        self.flat_TT.loc[row] = cls_week

        self.get_fitness()