from numpy.lib.function_base import place
import pandas as pd

def get_names(prof_data):
    class_names, prof_names = [], []
    for _,val in prof_data.iterrows():
        class_names.append(val["Class"])
        prof_names.append(val["Teacher"])

    class_names, prof_names = list(set(class_names)), list(set(prof_names))

    return class_names, prof_names

def create_row(val,type):
    periods = [int(str(i)+str(j)) for i in [1,2,3,4,5] for j in [1,2,3,4,5,6]]
    new_row = {}
    new_row["Teacher"] = val["Teacher"]
    new_row["Class"] = val["Class"]
    new_row["Type"] = type
    new_row["Pos"] = periods
    new_row["Sat"] = len(periods)
    new_row["Fix"] = 0

    return new_row

def init_place_data(file): 
    prof_data = pd.read_csv(file,delimiter=';').dropna()  

    place_data = pd.DataFrame(columns=["Teacher","Class","Type","Pos", "Sat", "Fix"])
    
    for _, val in prof_data.iterrows():
         
        if val["Subject"] == "ISG": # 1 test, 4 double = 10
            for _ in range(1):
                new_row = create_row(val,2)
                place_data = place_data.append(new_row, ignore_index=True)
            for _ in range(4):
                new_row = create_row(val,1)
                place_data = place_data.append(new_row, ignore_index=True)

        if val["Subject"] == "IS": # 1 test, 2 double, 2 single = 8
            for _ in range(1):
                new_row = create_row(val,2)
                place_data = place_data.append(new_row, ignore_index=True)
            for _ in range(2):
                new_row = create_row(val,1)
                place_data = place_data.append(new_row, ignore_index=True)
            for _ in range(2):
                new_row = create_row(val,0)
                place_data = place_data.append(new_row, ignore_index=True)
        
        if val["Subject"] == "I": # 1 test, 4 single = 6
            for _ in range(1):
                new_row = create_row(val,2)
                place_data = place_data.append(new_row, ignore_index=True)
            for _ in range(4):
                new_row = create_row(val,0)
                place_data = place_data.append(new_row, ignore_index=True)

        if val["Subject"] == "SG":  # 4 single
            for _ in range(4):
                new_row = create_row(val,0)
                place_data = place_data.append(new_row, ignore_index=True)
        
        if val["Subject"] == "G": # 2 single 
            for _ in range(2):
                new_row = create_row(val,0)
                place_data = place_data.append(new_row, ignore_index=True)

        if val["Subject"] == "MS":  
            for _ in range(1):
                new_row = create_row(val,2)
                place_data = place_data.append(new_row, ignore_index=True)
            for _ in range(4):
                new_row = create_row(val,0)
                place_data = place_data.append(new_row, ignore_index=True)

        if val["Subject"] == "ING":  
            for _ in range(3):
                new_row = create_row(val,0)
                place_data = place_data.append(new_row, ignore_index=True)

        if val["Subject"] == "M":  
            for _ in range(2):
                new_row = create_row(val,0)
                place_data = place_data.append(new_row, ignore_index=True)

        if val["Subject"] == "T":  
            for _ in range(2):
                new_row = create_row(val,0)
                place_data = place_data.append(new_row, ignore_index=True)

        if val["Subject"] == "SL":  
            for _ in range(2):
                new_row = create_row(val,0)
                place_data = place_data.append(new_row, ignore_index=True)

        if val["Subject"] == "TED":  
            for _ in range(2):
                new_row = create_row(val,0)
                place_data = place_data.append(new_row, ignore_index=True)

        if val["Subject"] == "FRA":  
            for _ in range(2):
                new_row = create_row(val,0)
                place_data = place_data.append(new_row, ignore_index=True)

        if val["Subject"] == "SPA":  
            for _ in range(2):
                new_row = create_row(val,0)
                place_data = place_data.append(new_row, ignore_index=True)
        
        if val["Subject"] == "MOT":  
            for _ in range(2):
                new_row = create_row(val,0)
                place_data = place_data.append(new_row, ignore_index=True)

        if val["Subject"] == "A":  
            for _ in range(1):
                new_row = create_row(val,1)
                place_data = place_data.append(new_row, ignore_index=True)

        if val["Subject"] == "R":  
            for _ in range(1):
                new_row = create_row(val,0)
                place_data = place_data.append(new_row, ignore_index=True)
                
    return prof_data, place_data

def fix(place_data, name, cls, types, pos):
    for _, val in place_data.iterrows(): 
        if val["Teacher"] == name and val["Class"] == cls:
            for t in types:
                if val["Type"] == t and len(val["Pos"]) > len(pos):
                    val["Pos"] = pos
                    val["Sat"] = len(pos)
                    val["Fix"] = 1
                    return place_data

    print("Can't fix")
    return place_data            

def set_fixed(place_data,file):
    fixed_data = pd.read_csv(file,delimiter=';').dropna()

    for _, val in fixed_data.iterrows():
        types = None
        l = val["Hours"].split(',')
        if len(l) == 2 and int(l[0]) == 1:
            types = [2,1]
        elif len(l) == 2:
            types = [1]
        elif len(l) == 1:
            types = [0]
        pos = [int(str(val["Day"])+str(i)) for i in l]

        place_data = fix(place_data, val["Teacher"], val["Class"], types, pos)

    return place_data    

def get_data(fname, fixed_fname):
    prof_data, place_data = init_place_data(fname)
    class_names, prof_names = get_names(prof_data)

    place_data = set_fixed(place_data, fixed_fname)

    return prof_data, place_data, class_names, prof_names