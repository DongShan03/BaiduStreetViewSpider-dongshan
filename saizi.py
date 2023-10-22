import pandas, os, glob, shutil

list_files = []
data = pandas.read_csv(r"./dir/sampling_points_wgs_100m.csv").iloc[:, 4:]
for i in range(len(data)):
    file_should_exist = str(round(data.iloc[i, 0], 6)) + "_" + str(round(data.iloc[i, 1], 6)) + ".png"
    list_files.append(file_should_exist)


for i in range(len(list_files)):
    try:
        shutil.copy(os.path.join(r".\images", list_files[i]), os.path.join(r".\images_100", list_files[i]))
        print("ok")
    except:
        print("miss")

