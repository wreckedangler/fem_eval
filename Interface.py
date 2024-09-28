from tkinter import *
import os.path
import time
import os
from tkinter import filedialog


# Function for opening the file explorer window
def browseFiles():

    global filename
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                          filetypes=(("Text files","*.txt*"), ("all files","*.*")))
    entryPathS.insert(0, filename)
    return filename


def buttonReaderClick():

    listeAusgewaehlt1 = listboxNamen1.curselection()
    itemAusgewaehlt1 = listeAusgewaehlt1[0]
    save_path = listboxNamen1.get(itemAusgewaehlt1)
    labelStat.config(text="Wait...")
    unit = str(entryUnit.get()).upper()
    WoB = str(weldLabel1.get()).upper()
    start = time.time()

    try:
        try:

            with open(filename) as test_file:
                test_file.readline()
                list_test = []

                list_test += test_file.readline().rstrip().split(";")
                lastfall = int(list_test[1])
                ID = int(list_test[0])
                fn = "lastfall"
                complete_name = os.path.join(save_path, fn)

                if unit == "SO" and WoB == "B":
                    counter = 0
                    while test_file is not None:
                        # print(str(first_line) + "," + str(counter) + "," + str(lastfall))
                        lf1 = open(complete_name + str(counter) + ".txt", "w")

                        lastfall_alt = lastfall

                        while lastfall == lastfall_alt:
                            lenght_list = len(list_test)
                            imp_numbers = (list_test[(lenght_list - 6)] + "," + list_test[lenght_list - 5]
                                           + "," + list_test[lenght_list - 4] + "," + list_test[lenght_list - 3]
                                           + "," + list_test[lenght_list - 2] + "," + list_test[lenght_list - 1])
                            list_test = []
                            list_test += test_file.readline().rstrip().split(";")
                            lf1.write(str(ID) + "," + str(imp_numbers) + "\n")
                            ID = int(list_test[0])
                            lastfall = int(list_test[1])
                            # print(str(ID) + "," + str(imp_numbers) + "," + str(counter) + "," + str(lastfall))
                        counter += 1
                        lf1.close()
                        fn = "Index"
                        complete_name1 = os.path.join(save_path, fn)
                        Index = open(complete_name1 + ".txt", "w")
                        index_numbers = range(0, counter + 1)
                        for i in index_numbers:
                            Index.write("lastfall" + str(i) + ".txt" + "\n")
                        Index.close()
                        # if counter == 5:
                if unit == "SH" and WoB == "B":
                    counter = 0
                    while test_file is not None:
                        # print(str(first_line) + "," + str(counter) + "," + str(lastfall))
                        lf1 = open(complete_name + str(counter) + ".txt", "w")

                        lastfall_alt = lastfall

                        while lastfall == lastfall_alt:
                            lenght_list = len(list_test)
                            imp_numbers = (list_test[(lenght_list - 6)] + "," + list_test[lenght_list - 5]
                                           + "," + list_test[lenght_list - 4] + "," + list_test[lenght_list - 3]
                                           + "," + list_test[lenght_list - 2] + "," + list_test[lenght_list - 1])
                            list_test = []
                            list_test += test_file.readline().rstrip().split(";")
                            lf1.write(str(ID) + "," + str(imp_numbers) + "\n")
                            ID = str(list_test[0])
                            lastfall = int(list_test[1])
                            # print(str(ID) + "," + str(imp_numbers) + "," + str(counter) + "," + str(lastfall))
                            tkFenster.update()
                        counter += 1
                        lf1.close()
                        fn = "Index"
                        complete_name1 = os.path.join(save_path, fn)
                        Index = open(complete_name1 + ".txt", "w")
                        index_numbers = range(0, counter + 1)
                        for i in index_numbers:
                            Index.write("lastfall" + str(i) + ".txt" + "\n")
                        Index.close()
                        # if counter == 5:
                        #    break

                elif unit == "SH" and WoB == "W":
                    Pid = "D:\\gruppen.txt"  # customize path and filename
                    # Pid_ex = open("D:\\Python\\DVS_Gruppen_extrakt.txt", "w")
                    listPID = []
                    listEID = []

                    def readfile(Pid_file, counterA, listPID, listEID, lastfall,
                                 ID, list_test, complete_name):
                        print("reading file")

                        list_nr_group1 = []
                        list_pid_code = []

                        while Pid_file:

                            list_pid = []
                            list_pid += Pid_file.readline().rstrip().split(",")
                            # print(list_pid)

                            if list_pid[0] == "DVS":
                                propertyID = int(
                                    str(list_pid[1]) + str(list_pid[2]) + str(list_pid[3]) + str(list_pid[4]))
                                list_pid_code.append(propertyID)
                                list_nr_group1.append(propertyID)

                                while list_pid[0] != "       21":

                                    list_pid = []
                                    list_pid += Pid_file.readline().rstrip().split(",")

                                    if list_pid[0] == "       21":

                                        while list_pid[0] != "       -1":

                                            list_pid = []
                                            list_pid += Pid_file.readline().rstrip().split(",")
                                            # print(list_pid)

                                            if int(list_pid[1]) > int(list_pid[0]):

                                                maximum = int(list_pid[1])
                                                starting_nr = int(list_pid[0])
                                                list_nr_group1.append(starting_nr)

                                                while starting_nr < maximum:
                                                    starting_nr += 1
                                                    list_nr_group1.append(starting_nr)

                                            else:

                                                list_nr_group1.append(int(list_pid[0]))

                                        for item in list_nr_group1:
                                            if item != list_nr_group1[0] and item != -1:
                                                counterA += 1
                                                listPID.append(int(list_pid_code[0]))
                                                listEID.append(int(item))

                                        readfile(Pid_file, counterA, listPID, listEID, lastfall,
                                                 ID, list_test, complete_name)

                            elif list_pid[0] == "":
                                listEID, listPID = zip(*sorted(zip(listEID, listPID)))
                                counter = 0
                                while test_file is not None:
                                    # print(str(first_line) + "," + str(counter) + "," + str(lastfall))
                                    lf1 = open(complete_name + str(counter) + ".txt", "w")

                                    lastfall_alt = lastfall
                                    counter_pid = 0
                                    while lastfall == lastfall_alt:

                                        lenght_list = len(list_test)
                                        imp_numbers = (
                                                list_test[(lenght_list - 6)] + "," + list_test[lenght_list - 5]
                                                + "," + list_test[lenght_list - 4] + "," + list_test[
                                                    lenght_list - 3]
                                                + "," + list_test[lenght_list - 2] + "," + list_test[
                                                    lenght_list - 1])
                                        list_test = []
                                        list_test += test_file.readline().rstrip().split(";")
                                        lf1.write(str(ID) + "," + str(listPID[counter_pid]) + "," + str(
                                            imp_numbers) + "\n")
                                        ID = str(list_test[0])
                                        lastfall = int(list_test[1])
                                        counter_pid += 1
                                        tkFenster.update()
                                    counter += 1
                                    print("holla")
                                    lf1.close()
                                    if counterA != counter_pid:
                                        labelStat.config(text="Error in files")
                                        break
                                    fn = "Index"
                                    complete_name1 = os.path.join(save_path, fn)
                                    Index = open(complete_name1 + ".txt", "w")
                                    index_numbers = range(0, counter + 1)
                                    for i in index_numbers:
                                        Index.write("lastfall" + str(i) + ".txt" + "\n")
                                    Index.close()

                    with open(Pid) as Pid_file:

                        listPID = []
                        listEID = []
                        counterA = 0
                        # calling function
                        readfile(Pid_file, counterA, listPID, listEID, lastfall,
                                 ID, list_test, complete_name)


        except FileNotFoundError:
            output1 = "Bitte Angaben überprüfen!"
            labelStat.config(text=output1)
    except ValueError:
        print("ValueERROR")
        total_time = str((time.time() - start))
        output = f"Finished splitting and saving file. It took: {round(float(total_time), 2)} seconds."
        labelStat.config(text=output)

    except IndexError:
        print("IndexERROR")
        total_time = str((time.time() - start))
        output = f"Finished splitting and saving file. It took: {round(float(total_time), 2)} seconds."
        labelStat.config(text=output)



# Fenster
tkFenster = Tk()


# image import
import tkinter as tk
# from PIL import ImageTk, Image

# path1 = 'C:\\Users\\raphi\\Pictures\\Saved Pictures\\DK.jpg'
# img1 = ImageTk.PhotoImage(Image.open(path1))
# panel1 = tk.Label(tkFenster, image = img1)
# panel1.pack(side="bottom", fill="both", expand="yes")

# path = 'C:\\Users\\raphi\\Pictures\\Saved Pictures\\ingenis-logo1.jpg'
# img = ImageTk.PhotoImage(Image.open(path))
# panel = tk.Label(tkFenster, image=img)
# panel.pack(side="bottom", fill="both", expand="yes")
# panel.place(x=580, y=24)

button_explore = Button(tkFenster, bg="lightblue", text="Browse Files", command=browseFiles)
button_explore.place(x=413, y=184, width=120, height=27)
button_exit = Button(tkFenster, text="Exit", command=exit)

tkFenster.title('Ingenis-Reader')
tkFenster.geometry('830x320')

labelPathS = Label(master=tkFenster, bg='gold', text='File:')
labelPathS.place(x=24, y=24, width=100, height=27)
entryPathS = Entry(master=tkFenster, bg='white')
entryPathS.place(x=134, y=24, width=400, height=27)


labelPathV = Label(master=tkFenster, bg='gold', text='Save Path:')
labelPathV.place(x=24, y=84, width=100, height=27)
entryPathV = Entry(master=tkFenster, bg='white')
entryPathV.place(x=134, y=84, width=400, height=54)

labelUnit = Label(master=tkFenster, bg='pink', text='Solid/Shell:')
labelUnit.place(x=24, y=184, width=100, height=27)
entryUnit = Entry(master=tkFenster, bg='white')
entryUnit.place(x=134, y=184, width=100, height=27)

listboxNamen1 = Listbox(exportselection=0)
listboxNamen1.insert('end', 'F:\\Text_Dateien')
listboxNamen1.insert('end', 'C:\\Users\\raphi\\PycharmProjects\\pythonProject')
listboxNamen1.insert("end", "D:\\Python\\Auswertungen_LF")
listboxNamen1.place(x=134, y=84, width=400, height=54)

# Button
buttonRead = Button(master=tkFenster, bg='lightgreen', text='Start', command=buttonReaderClick)
buttonRead.place(x=413, y=224, width=60, height=27)

buttonQuit = Button(master=tkFenster, bg='orange', text='Exit', command=exit)
buttonQuit.place(x=473, y=224, width=60, height=27)
weldLabel = Label(master=tkFenster, bg='pink', text="Weld or Base")
weldLabel.place(x=24, y=224, width=100, height=27)
weldLabel1 = Entry(master=tkFenster, bg='white', text="")
weldLabel1.place(x=134, y=224, width=100, height=27)

labelStatus = Label(master=tkFenster, bg='lightgreen', text="Status:")
labelStatus.place(x=24, y=264, width=100, height=27)
labelStat = Label(master=tkFenster, bg='white', text="")
labelStat.place(x=134, y=264, width=400, height=27)

# Aktivierung des Fensters
tkFenster.mainloop()
