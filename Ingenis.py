import os.path
import time
from tkinter import *
from numpy import abs
from numpy import log10 as log
from numpy import sqrt
import tkinter as tk
# from PIL import ImageTk, Image
import datetime

global entryS1, entryComp, entryCrit, interface2


def buttonSolve(labelStat, output_set_name, entryCrit, labelWeldy, entryUnit, labelnorme, entryRm, entryFsig, entryFtau,
entryNsig, entryKf, entryRmN, entryRsig, entryR_Z, entryK_V, entryK_S, entryK_Nle, entryA_m, entryBm,
entryNreq, entryN_Dsig, entryN_D2sig, entryKsig, entryK2sig, entryN_Dtau, entryN_D2tau, entryKtau,
entryK2tau, entryf2sig, entryf2tau, entryjF, entryUnit2, entryS1, entryComp, interface2):
    labelStat.config(text="Starting Calculation...")
    global lenght_list, estimated_time_left, EoK, douEQVb_list, douEQVt_list, current_time
    global douxxt_list, douyyt_list, douxyt_list, douxxb_list, douyyb_list, douxyb_list
    current_time = datetime.datetime.now()
    output_set_name = output_set_name
    crit = entryCrit
    weld_yes_no = labelWeldy
    function_def = entryUnit
    sf = entryS1
    norm = labelnorme
    print(norm)
    Rm = entryRm
    fwsig = entryFsig
    fwtau = entryFtau
    nsig = entryNsig
    ntau = nsig
    Kf = entryKf
    RmNmin = entryRmN
    aRsig = entryRsig
    Rz = entryR_Z
    KV = entryK_V
    Ks = entryK_S
    KNLE = entryK_Nle
    am = entryA_m
    bm = entryBm
    Nreq = entryNreq
    NDsig = entryN_Dsig
    ND2sig = entryN_D2sig
    Ksig = entryKsig
    K2sig = entryK2sig
    NDtau = entryN_Dtau
    Nd2tau = entryN_D2tau
    Ktau = entryKtau
    K2tau = entryK2tau
    f2sig = entryf2sig
    f2tau = entryf2tau
    jF = entryjF
    EoK = entryUnit2

    # initial math
    SigWzd = fwsig * Rm
    TauWs = fwtau * SigWzd
    KrSig = 1 - aRsig * log(Rz) * ((2 * Rm) / RmNmin)
    KrTau = 1 - fwtau * aRsig * log(Rz) * log((2 * Rm) / RmNmin)
    KwkSig = (1 / nsig) * ((1 + (1 / Kf)) * ((1 / KrSig) - 1)) * (1 / (KV * Ks * KNLE))
    KwkTau = (1 / ntau) * ((1 + (1 / Kf)) * ((1 / KrTau) - 1)) * (1 / (KV * Ks))
    SigWk = SigWzd / KwkSig  # xx, yy, zz
    TauWk = TauWs / KwkTau  # xy, xz, yz
    SigWkxx = SigWk
    TauWkxy = TauWk
    SigWkyy = SigWk
    TauWkxz = TauWk
    SigWkzz = SigWk
    TauWkyz = TauWk
    Msig = am * 0.001 * Rm + bm
    Mtau = fwtau * Msig

    # function defined (solid)
    def math_solid(file1, file2, douxx_list1, douyy_list1, douzz_list1, douxy_list1,
                   douxz_list1, douyz_list1, douEQV_list1):

        counter = 0  # counting loops
        line = file1.readline()
        line2 = file2.readline()
        save_path = "C:\\Users\\raphi\\PycharmProjects\\pythonProject"  # customizeable to wanted directory
        fn = "maxima_solid"  # end_file name variable
        complete_name = os.path.join(save_path, fn)  # joining end_file name and save_path
        result_sheet = open(complete_name + ".txt", "w")  # absolute name of file
        result_sheet.write("ID, DOUxx, DOUyy, DOUzz, DOUxy, DOUxz, DOUyz, DOUeqv\n")
        werte = line.strip()
        werte_split = werte.split(",")
        ID = int(werte_split[0].rstrip(","))
        fa1 = 1000000  # einheits-ziffer
        while line:
            # read first file plus implementing ID number. Defining variables.
            werte = line.strip()
            werte_split = werte.split(",")
            line = file1.readline()
            ID = int(werte_split[0].rstrip(","))
            SigX = (float(werte_split[1].rstrip(","))) / fa1
            SigY = (float(werte_split[2].rstrip(","))) / fa1
            SigZ = (float(werte_split[3].rstrip(","))) / fa1
            TauXY = (float(werte_split[4].rstrip(","))) / fa1
            TauXZ = (float(werte_split[5].rstrip(","))) / fa1
            TauYZ = (float(werte_split[6].rstrip(","))) / fa1

            # read second file. Defining variables
            werte2 = line2.strip()
            werte2_split = werte2.split(",")
            line2 = file2.readline()
            SigX2 = (float(werte2_split[1].rstrip(","))) / fa1
            SigY2 = (float(werte2_split[2].rstrip(","))) / fa1
            SigZ2 = (float(werte2_split[3].rstrip(","))) / fa1
            TauXY2 = (float(werte2_split[4].rstrip(","))) / fa1
            TauXZ2 = (float(werte2_split[5].rstrip(","))) / fa1
            TauYZ2 = (float(werte2_split[6].rstrip(","))) / fa1

            # math function between first and second file / line per line and with corresponding column
            SigXM = (SigX + SigX2) * 0.5
            SigYM = (SigY + SigY2) * 0.5
            SigZM = (SigZ + SigZ2) * 0.5
            TauXYM = (TauXY + TauXY2) * 0.5
            TauXZM = (TauXZ + TauXZ2) * 0.5
            TauYZM = (TauYZ + TauYZ2) * 0.5
            SigXA = abs((SigX - SigX2) * 0.5)
            SigYA = abs((SigY - SigY2) * 0.5)
            SigZA = abs((SigZ - SigZ2) * 0.5)
            TauXYA = abs((TauXY - TauXY2) * 0.5)
            TauXZA = abs((TauXZ - TauXZ2) * 0.5)
            TauYZA = abs((TauYZ - TauYZ2) * 0.5)
            SigXmin = SigXM - SigXA
            SigYmin = SigYM - SigYA
            SigZmin = SigZM - SigZA
            SigXmax = SigXM + SigXA
            SigYmax = SigYM + SigYA
            SigZmax = SigZM + SigZA
            TauXYmin = TauXYM - TauXYA
            TauXZmin = TauXZM - TauXZA
            TauYZmin = TauYZM - TauYZA
            TauXYmax = TauXYM + TauXYA
            TauXZmax = TauXZM + TauXZA
            TauYZmax = TauYZM + TauYZA
            Rxx = SigXmin / SigXmax
            Ryy = SigYmin / SigYmax
            Rzz = SigZmin / SigZmax
            Rxy = TauXYmin / TauXYmax
            Rxz = TauXZmin / TauXZmax
            Ryz = TauYZmin / TauYZmax

            # Rxx
            if Rxx > 1:
                KAKxx = 1 / (1 - Msig)
                #  print(ID, KAKxx, Msig)
            elif (Rxx <= 0) and (Rxx >= - 10 ** 20):
                KAKxx = 1 / (1 + Msig * (SigXM / SigXA))
                #  print(ID, KAKxx, counter)
            elif (Rxx < 0.5) and (Rxx > 0.0):
                KAKxx = (3 + Msig) / ((1 + Msig) * (3 + Msig * (SigXM / SigXA)))
                #  print(ID, KAKxx, counter)
            elif Rxx >= 0.5:
                KAKxx = (3 + Msig) / (3 * (1 + Msig) * (1 + Msig))
                #  print(ID, KAKxx, Msig)
            # Ryy
            if Ryy > 1:
                KAKyy = 1 / (1 - Msig)
                #  print(ID, KAKyy, counter)
            elif (Ryy <= 0) and (Ryy >= - 10 ** 20):
                KAKyy = 1 / (1 + Msig * (SigYM / SigYA))
                #  print(ID, KAKyy, counter)
            elif (Ryy < 0.5) and (Ryy > 0.0):
                KAKyy = (3 + Msig) / ((1 + Msig) * (3 + Msig * (SigYM / SigYA)))
                #  print(ID, KAKyy, counter)
            elif Ryy >= 0.5:
                KAKyy = (3 + Msig) / (3 * (1 + Msig) * (1 + Msig))
                #  print(ID, KAKyy, counter)
            # Rzz
            if Rzz > 1:
                KAKzz = 1 / (1 - Msig)
                #  print(ID, KAKzz, counter)
            elif (Rzz <= 0) and (Rzz >= - 10 ** 20):
                KAKzz = 1 / (1 + Msig * (SigZM / SigZA))
                #  print(ID, KAKzz, counter)
            elif (Rzz < 0.5) and (Rzz > 0.0):
                KAKzz = (3 + Msig) / ((1 + Msig) * (3 + Msig * (SigZM / SigZA)))
                #  print(ID, KAKzz, counter)
            elif Rzz >= 0.5:
                KAKzz = (3 + Msig) / (3 * (1 + Msig) * (1 + Msig))
                #  print(ID, KAKzz, counter)
            # Rxy
            if Rxy > 1:
                KAKxy = 1 / (1 - Mtau)
                #  print(ID, KAKxy, counter)
            elif (Rxy <= 0) and (Rxy >= - 10 ** 20):
                KAKxy = 1 / (1 + Mtau * (TauXYM / TauXYA))
                #  print(ID, KAKxy, counter)
            elif (Rxy < 0.5) and (Rxy > 0.0):
                KAKxy = (3 + Mtau) / ((1 + Mtau) * (3 + Mtau * (TauXYM / TauXYA)))
                #  print(ID, KAKxy, counter)
            elif Rxy >= 0.5:
                KAKxy = (3 + Mtau) / (3 * (1 + Mtau) * (1 + Mtau))
                #  print(ID, KAKxy, counter)
            # Rxz
            if Rxz > 1:
                KAKxz = 1 / (1 - Mtau)
                #  print(ID, KAKxz, counter)
            elif (Rxz <= 0.0) and (Rxz >= - 10 ** 20):
                KAKxz = 1 / (1 + Mtau * (TauXZM / TauXZA))
                #  print(ID, KAKxz, counter)
            elif (Rxz < 0.5) and (Rxz > 0.0):
                KAKxz = (3 + Mtau) / ((1 + Mtau) * (3 + Mtau * (TauXZM / TauXZA)))
                #  print(ID, KAKxz, counter)
            elif Rxz >= 0.5:
                KAKxz = (3 + Mtau) / (3 * (1 + Mtau) * (1 + Mtau))
                #  print(ID, KAKxz, counter)
            # Ryz
            if Ryz > 1:
                KAKyz = 1 / (1 - Mtau)
                #  print(ID, KAKyz, counter)
            elif (Ryz <= 0) and (Ryz >= - 10 ** 20):
                KAKyz = 1 / (1 + Mtau * (TauYZM / TauYZA))
                #  print(ID, KAKyz, counter)
            elif (Ryz < 0.5) and (Ryz > 0.0):
                KAKyz = (3 + Mtau) / ((1 + Mtau) * (3 + Mtau * (TauYZM / TauYZA)))
                #  print(ID, KAKyz, counter)
            elif Ryz >= 0.5:
                KAKyz = (3 + Mtau) / (3 * (1 + Mtau) * (1 + Mtau))
                #  print(ID, KAKyz, counter)
            SigAKxx = KAKxx * SigWkxx
            SigAKyy = KAKyy * SigWkyy
            SigAKzz = KAKzz * SigWkzz
            TauAKxy = KAKxy * TauWkxy
            TauAKxz = KAKxz * TauWkxz
            TauAKyz = KAKyz * TauWkyz

            if Nreq <= NDsig:
                KBKsig = (NDsig / Nreq) ** (1 / Ksig)
            elif (NDsig < Nreq) and (Nreq <= ND2sig):
                KBKsig = (NDsig / Nreq) ** (1 / K2sig)
            elif Nreq > ND2sig:
                KBKsig = f2sig

            if Nreq <= NDtau:
                KBKtau = (NDtau / Nreq) ** (1 / Ktau)
            elif (NDtau < Nreq) and (Nreq <= Nd2tau):
                KBKtau = (NDtau / Nreq) ** (1 / K2tau)
            elif Nreq > Nd2tau:
                KBKtau = f2tau

            SigBKxx = KBKsig * SigAKxx
            SigBKyy = KBKsig * SigAKyy
            SigBKzz = KBKsig * SigAKzz
            TauBKxy = KBKtau * TauAKxy
            TauBKxz = KBKtau * TauAKxz
            TauBKyz = KBKtau * TauAKyz

            aBKxx = SigXA / (SigBKxx / jF)
            aBKyy = SigYA / (SigBKyy / jF)
            aBKzz = SigZA / (SigBKzz / jF)
            aBKxy = TauXYA / (TauBKxy / jF)
            aBKxz = TauXZA / (TauBKxz / jF)
            aBKyz = TauYZA / (TauBKyz / jF)

            q = (sqrt(3) - (1 / fwtau)) / (sqrt(3) - 1)
            aNH = max(abs(aBKxx), abs(aBKyy), abs(aBKzz))
            aGH = sqrt(0.5 * ((aBKxx - aBKyy) ** 2 + (aBKxx - aBKzz) ** 2 + (aBKyy - aBKzz) ** 2))

            aBKeqv = q * aNH + (1 - q) * aGH

            if aBKxx > douxx_list1[counter]:
                douxx_list1[counter] = aBKxx
            if aBKyy > douyy_list1[counter]:
                douyy_list1[counter] = aBKyy
            if aBKzz > douzz_list1[counter]:
                douzz_list1[counter] = aBKzz
            if aBKxy > douxy_list1[counter]:
                douxy_list1[counter] = aBKxy
            if aBKxz > douxz_list1[counter]:
                douxz_list1[counter] = aBKxz
            if aBKyz > douyz_list1[counter]:
                douyz_list[counter] = aBKyz
            if aBKeqv > douEQV_list1[counter]:
                douEQV_list1[counter] = aBKeqv
            # writing end_file when comparison between file1 and file2 is done.
            result_sheet.write(str(ID) + "," + str(douxx_list1[counter]) + "," + str(douyy_list1[counter])
                               + "," + str(douzz_list1[counter]) + "," + str(douxy_list1[counter])
                               + "," + str(douxz_list1[counter]) + "," + str(douyz_list1[counter])
                               + "," + str(douEQV_list1[counter]) + "\n")
            # print(str(ID) + "," + str(douxx_list1[counter]) + "," + str(douyy_list1[counter])
            #      + "," + str(douzz_list1[counter]) + "," + str(douxy_list1[counter])
            #      + "," + str(douxz_list1[counter]) + "," + str(douyz_list1[counter])
            #      + "," + str(douEQV_list1[counter]))
            counter += 1
            output1 = total_time = ((time.time() - start))
            output2 = round(output1, 1)

            if output2 < 60:
                output3 = str(output2) + " " + "sek"
                labelStat.config(text=f"Calculation in progress... {output3}")
            elif output2 >= 60:
                output3 = str(round((output2 / 60), 1)) + " " + "min"
                labelStat.config(text=f"Calculation in progress... {output3}")

            interface.update()
        result_sheet.close()

    # function defined (shell)
    def math_shell(file1, file2, douxxt_list1, douyyt_list1, douxyt_list1, douxxb_list1, douyyb_list1,
                   douxyb_list1, douEQVt_list1, douEQVb_list1, list_lf, counter11, counter21):

        a = "   "
        b = "\n"
        counter = 0  # counting lines (to call corresponding indexes)
        line = file1.readline()
        line2 = file2.readline()
        save_path = "C:\\Users\\raphi\\PycharmProjects\\pythonProject\\"  # customizeable to wanted directory
        fn = "maxima"  # end_file name variable
        complete_name = os.path.join(save_path, fn)  # joining end_file name and save_path
        result_sheet = open(complete_name + ".txt", "w")  # absolute name of file
        result_sheet.write(a + "-1" + b + a + "100" + b + "<NULL>" + b + "21.1," + b + a + "-1" + b + a + "-1" + b + a
                           + "450" + "\n" + "1," + b + f"{output_set_name}" + b + "36,1,0,1," + b + "0.," + b + "5," + b
                           + "xxxx" + b
                           + f"Date : {current_time}" + b + "<NULL>" + b + "SHELL_FORMAT" + b + "DRUCK" + b
                           + "0,1,1," + b + "-1,-1,0.," + b + "0,0," + b + "1," + b + "127,0,0," + b + "0,0,0,0,0,0,"
                           + b + "0,0,0,0,0,0," + b + a + "-1" + b)
        werte = line.strip()
        werte_split = werte.split(",")
        ID = int(werte_split[0].rstrip(","))
        fa1 = 1000000
        total_time = ((time.time() - start))
        ID_list = []

        if weld_yes_no == "NO":
            # beginning of comparison between file1 and file2
            while line:
                # read first file plus implementing ID number. Defining variables.
                werte = line.strip()
                werte_split = werte.split(",")
                line = file1.readline()
                ID = int(werte_split[0].rstrip(","))
                ID_list.append(ID)
                SigXt = (float(werte_split[1].rstrip(","))) / fa1
                SigYt = (float(werte_split[2].rstrip(","))) / fa1
                TauXYt = (float(werte_split[3].rstrip(","))) / fa1
                SigXb = (float(werte_split[4].rstrip(","))) / fa1
                SigYb = (float(werte_split[5].rstrip(","))) / fa1
                TauXYb = (float(werte_split[6].rstrip(","))) / fa1
                # read second file. Defining variables
                werte2 = line2.strip()
                werte2_split = werte2.split(",")
                line2 = file2.readline()
                SigX2t = (float(werte2_split[1].rstrip(","))) / fa1
                SigY2t = (float(werte2_split[2].rstrip(","))) / fa1
                TauXY2t = (float(werte2_split[3].rstrip(","))) / fa1
                SigX2b = (float(werte2_split[4].rstrip(","))) / fa1
                SigY2b = (float(werte2_split[5].rstrip(","))) / fa1
                TauXY2b = (float(werte2_split[6].rstrip(","))) / fa1

                # math function between first and second file / line per line and with corresponding column

                # Top stress
                SigXMt = (SigXt + SigX2t) * 0.5
                SigYMt = (SigYt + SigY2t) * 0.5
                TauXYMt = (TauXYt + TauXY2t) * 0.5
                SigXAt = abs((SigXt - SigX2t) * 0.5)
                SigYAt = abs((SigYt - SigY2t) * 0.5)
                TauXYAt = abs((TauXYt - TauXY2t) * 0.5)
                SigXmint = SigXMt - SigXAt
                SigYmint = SigYMt - SigYAt
                SigXmaxt = SigXMt + SigXAt
                SigYmaxt = SigYMt + SigYAt
                TauXYmint = TauXYMt - TauXYAt
                TauXYmaxt = TauXYMt + TauXYAt
                Rxxt = SigXmint / SigXmaxt
                Ryyt = SigYmint / SigYmaxt
                Rxyt = TauXYmint / TauXYmaxt

                # Rxx
                if Rxxt > 1:
                    KAKxxt = 1 / (1 - Msig)
                    #  print(ID, KAKxx, Msig)
                elif (Rxxt <= 0) and (Rxxt >= - 10 ** 20):
                    KAKxxt = 1 / (1 + Msig * (SigXMt / SigXAt))
                    #  print(ID, KAKxx, counter)
                elif (Rxxt < 0.5) and (Rxxt > 0.0):
                    KAKxxt = (3 + Msig) / ((1 + Msig) * (3 + Msig * (SigXMt / SigXAt)))
                    #  print(ID, KAKxx, counter)
                elif Rxxt >= 0.5:
                    KAKxxt = (3 + Msig) / (3 * (1 + Msig) * (1 + Msig))
                    #  print(ID, KAKxx, Msig)
                # Ryy
                if Ryyt > 1:
                    KAKyyt = 1 / (1 - Msig)
                    #  print(ID, KAKyy, counter)
                elif (Ryyt <= 0) and (Ryyt >= - 10 ** 20):
                    KAKyyt = 1 / (1 + Msig * (SigYMt / SigYAt))
                    #  print(ID, KAKyy, counter)
                elif (Ryyt < 0.5) and (Ryyt > 0.0):
                    KAKyyt = (3 + Msig) / ((1 + Msig) * (3 + Msig * (SigYMt / SigYAt)))
                    #  print(ID, KAKyy, counter)
                elif Ryyt >= 0.5:
                    KAKyyt = (3 + Msig) / (3 * (1 + Msig) * (1 + Msig))
                    #  print(ID, KAKyy, counter)
                # Rxy
                if Rxyt > 1:
                    KAKxyt = 1 / (1 - Mtau)
                    #  print(ID, KAKxy, counter)
                elif (Rxyt <= 0) and (Rxyt >= - 10 ** 20):
                    KAKxyt = 1 / (1 + Mtau * (TauXYMt / TauXYAt))
                    #  print(ID, KAKxy, counter)
                elif (Rxyt < 0.5) and (Rxyt > 0.0):
                    KAKxyt = (3 + Mtau) / ((1 + Mtau) * (3 + Mtau * (TauXYMt / TauXYAt)))
                    #  print(ID, KAKxy, counter)
                elif Rxyt >= 0.5:
                    KAKxyt = (3 + Mtau) / (3 * (1 + Mtau) * (1 + Mtau))
                    #  print(ID, KAKxy, counter)

                SigAKxxt = KAKxxt * SigWkxx
                SigAKyyt = KAKyyt * SigWkyy
                TauAKxyt = KAKxyt * TauWkxy

                if Nreq <= NDsig:
                    KBKsig = (NDsig / Nreq) ** (1 / Ksig)
                elif (NDsig < Nreq) and (Nreq <= ND2sig):
                    KBKsig = (NDsig / Nreq) ** (1 / K2sig)
                elif Nreq > ND2sig:
                    KBKsig = f2sig

                if Nreq <= NDtau:
                    KBKtau = (NDtau / Nreq) ** (1 / Ktau)
                elif (NDtau < Nreq) and (Nreq <= Nd2tau):
                    KBKtau = (NDtau / Nreq) ** (1 / K2tau)
                elif Nreq > Nd2tau:
                    KBKtau = f2tau

                SigBKxxt = KBKsig * SigAKxxt
                SigBKyyt = KBKsig * SigAKyyt
                TauBKxyt = KBKtau * TauAKxyt

                aBKxxt = SigXAt / (SigBKxxt / jF)
                aBKyyt = SigYAt / (SigBKyyt / jF)
                aBKxyt = TauXYAt / (TauBKxyt / jF)

                # Bottom stress
                SigXMb = (SigXb + SigX2b) * 0.5
                SigYMb = (SigYb + SigY2b) * 0.5
                TauXYMb = (TauXYb + TauXY2b) * 0.5
                SigXAb = abs((SigXb - SigX2b) * 0.5)
                SigYAb = abs((SigYb - SigY2b) * 0.5)
                TauXYAb = abs((TauXYb - TauXY2b) * 0.5)
                SigXminb = SigXMb - SigXAb
                SigYminb = SigYMb - SigYAb
                SigXmaxb = SigXMb + SigXAb
                SigYmaxb = SigYMb + SigYAb
                TauXYminb = TauXYMb - TauXYAb
                TauXYmaxb = TauXYMb + TauXYAb
                Rxxb = SigXminb / SigXmaxb
                Ryyb = SigYminb / SigYmaxb
                Rxyb = TauXYminb / TauXYmaxb

                # Rxx
                if Rxxb > 1:
                    KAKxxb = 1 / (1 - Msig)
                    #  print(ID, KAKxx, Msig)
                elif (Rxxb <= 0) and (Rxxb >= - 10 ** 20):
                    KAKxxb = 1 / (1 + Msig * (SigXMb / SigXAb))
                    #  print(ID, KAKxx, counter)
                elif (Rxxb < 0.5) and (Rxxb > 0.0):
                    KAKxxb = (3 + Msig) / ((1 + Msig) * (3 + Msig * (SigXMb / SigXAb)))
                    #  print(ID, KAKxx, counter)
                elif Rxxb >= 0.5:
                    KAKxxb = (3 + Msig) / (3 * (1 + Msig) * (1 + Msig))
                    #  print(ID, KAKxx, Msig)
                # Ryy
                if Ryyb > 1:
                    KAKyyb = 1 / (1 - Msig)
                    #  print(ID, KAKyy, counter)
                elif (Ryyb <= 0) and (Ryyb >= - 10 ** 20):
                    KAKyyb = 1 / (1 + Msig * (SigYMb / SigYAb))
                    #  print(ID, KAKyy, counter)
                elif (Ryyb < 0.5) and (Ryyb > 0.0):
                    KAKyyb = (3 + Msig) / ((1 + Msig) * (3 + Msig * (SigYMb / SigYAb)))
                    #  print(ID, KAKyy, counter)
                elif Ryyb >= 0.5:
                    KAKyyb = (3 + Msig) / (3 * (1 + Msig) * (1 + Msig))
                    #  print(ID, KAKyy, counter)
                # Rxy
                if Rxyb > 1:
                    KAKxyb = 1 / (1 - Mtau)
                    #  print(ID, KAKxy, counter)
                elif (Rxyb <= 0) and (Rxyb >= - 10 ** 20):
                    KAKxyb = 1 / (1 + Mtau * (TauXYMb / TauXYAb))
                    #  print(ID, KAKxy, counter)
                elif (Rxyb < 0.5) and (Rxyb > 0.0):
                    KAKxyb = (3 + Mtau) / ((1 + Mtau) * (3 + Mtau * (TauXYMb / TauXYAb)))
                    #  print(ID, KAKxy, counter)
                elif Rxyb >= 0.5:
                    KAKxyb = (3 + Mtau) / (3 * (1 + Mtau) * (1 + Mtau))
                    #  print(ID, KAKxy, counter)

                SigAKxxb = KAKxxb * SigWkxx
                SigAKyyb = KAKyyb * SigWkyy
                TauAKxyb = KAKxyb * TauWkxy

                SigBKxxb = KBKsig * SigAKxxb
                SigBKyyb = KBKsig * SigAKyyb
                TauBKxyb = KBKtau * TauAKxyb

                aBKxxb = SigXAb / (SigBKxxb / jF)
                aBKyyb = SigYAb / (SigBKyyb / jF)
                aBKxyb = TauXYAb / (TauBKxyb / jF)

                qt = (sqrt(3) - (1 / fwtau)) / (sqrt(3) - 1)
                aNHt = 0.5 * (abs(aBKxxt + aBKyyt) + sqrt(((aBKxxt - aBKyyt) ** 2) + 4 * (aBKxyt) ** 2))
                aGHt = sqrt((aBKxxt ** 2) + (aBKyyt ** 2) - (aBKxxt * aBKyyt) + (aBKxyt ** 2))

                qb = (sqrt(3) - (1 / fwtau)) / (sqrt(3) - 1)
                aNHb = 0.5 * (abs(aBKxxb + aBKyyb) + sqrt(((aBKxxb - aBKyyb) ** 2) + 4 * (aBKxyb) ** 2))
                aGHb = sqrt((aBKxxb ** 2) + (aBKyyb ** 2) - (aBKxxb * aBKyyb) + (aBKxyb ** 2))

                aBKeqvt = qt * aNHt + (1 - qt) * aGHt
                if aBKeqvt > douEQVt_list1[counter]:
                    douEQVt_list1[counter] = aBKeqvt

                aBKeqvb = qb * aNHb + (1 - qb) * aGHb
                if aBKeqvb > douEQVb_list1[counter]:
                    douEQVb_list1[counter] = aBKeqvb

                if aBKxxt > douxxt_list1[counter]:
                    douxxt_list1[counter] = aBKxxt
                if aBKyyt > douyyt_list1[counter]:
                    douyyt_list1[counter] = aBKyyt
                if aBKxyt > douxyt_list1[counter]:
                    douxyt_list1[counter] = aBKxyt

                if aBKxxb > douxxb_list1[counter]:
                    douxxb_list1[counter] = aBKxxb
                if aBKyyb > douyyb_list1[counter]:
                    douyyb_list1[counter] = aBKyyb
                if aBKxyb > douxyb_list1[counter]:
                    douxyb_list1[counter] = aBKxyb

                douxxt_list = douxxt_list1
                douyyt_list = douyyt_list1
                douxyt_list = douxyt_list1
                douEQVt_list = douEQVt_list1
                douxxb_list = douxxb_list1
                douyyb_list = douyyb_list1
                douxyb_list = douxyb_list1
                douEQVb_list = douEQVb_list1

                counter += 1
                output1 = total_time = ((time.time() - start))
                output2 = round(output1, 1)

                if output2 < 60:
                    output3 = str(output2) + " " + "sek."
                    labelStat.config(text=f"Calculation in progress... {output3}")
                elif output2 >= 60:
                    output3 = str(round((output2 / 60), 1)) + " " + "min."
                    labelStat.config(text=f"Calculation in progress... {output3}")
                interface.update()
            # writing end_file when comparison between file1 and file2 is done.

            result_sheet.write(a + "-1" + b + "  " + "1051" + b + "1,7040,1," + b + "DOUxxTop" + b
                               + "9.9900002E+30,-9.9900002E+30,9.9900002E+30," + b + "11033,15033,19033,23033,0,0,0,0,0,0,"
                               + b + "0,0,0,0,0,0,0,0,0,0," + b + "0," + b + f"0,0,4,{EoK},0," + b + "1,0,1,0," + b)
            id_counter_xxt = 0
            for item in douxxt_list1:
                result_sheet.write(str(ID_list[id_counter_xxt]) + " " + str(item) + b)
                id_counter_xxt += 1

            result_sheet.write("-1,0.," + b)
            result_sheet.write("1,7041,1," + b + "DOUyyTop" + b
                               + "9.9900002E+30,-9.9900002E+30,9.9900002E+30," + b + "11033,15033,19033,23033,0,0,0,0,0,0,"
                               + b + "0,0,0,0,0,0,0,0,0,0," + b + "0," + b + f"0,0,4,{EoK},0," + b + "1,0,1,0," + b)
            id_counter_yyt = 0
            for item in douyyt_list1:
                result_sheet.write(str(ID_list[id_counter_yyt]) + " " + str(item) + b)
                id_counter_yyt += 1
            result_sheet.write("-1,0.," + b)
            result_sheet.write("1,7042,1," + b + "DOUxyTop" + b
                               + "9.9900002E+30,-9.9900002E+30,9.9900002E+30," + b + "11033,15033,19033,23033,0,0,0,0,0,0,"
                               + b + "0,0,0,0,0,0,0,0,0,0," + b + "0," + b + f"0,0,4,{EoK},0," + b + "1,0,1,0," + b)
            id_counter_xyt = 0
            for item in douxyt_list1:
                result_sheet.write(str(ID_list[id_counter_xyt]) + " " + str(item) + b)
                id_counter_xyt += 1
            result_sheet.write("-1,0.," + b)
            result_sheet.write("1,7043,1," + b + "DOUeqvTop" + b
                               + "9.9900002E+30,-9.9900002E+30,9.9900002E+30," + b + "11033,15033,19033,23033,0,0,0,0,0,0,"
                               + b + "0,0,0,0,0,0,0,0,0,0," + b + "0," + b + f"0,0,4,{EoK},0," + b + "1,0,1,0," + b)
            id_counter_EQVt = 0
            for item in douEQVt_list1:
                result_sheet.write(str(ID_list[id_counter_EQVt]) + " " + str(item) + b)
                id_counter_EQVt += 1
            result_sheet.write("-1,0.," + b)
            result_sheet.write("1,9040,1," + b + "DOUxxBot" + b
                               + "9.9900002E+30,-9.9900002E+30,9.9900002E+30," + b + "13033,17033,21033,25033,0,0,0,0,0,0,"
                               + b + "0,0,0,0,0,0,0,0,0,0," + b + "0," + b + f"0,0,4,{EoK},0," + b + "1,0,1,0," + b)
            id_counter_xxb = 0
            for item in douxxb_list1:
                result_sheet.write(str(ID_list[id_counter_xxb]) + " " + str(item) + b)
                id_counter_xxb += 1
            result_sheet.write("-1,0.," + b)
            result_sheet.write("1,9041,1," + b + "DOUyyBot" + b
                               + "9.9900002E+30,-9.9900002E+30,9.9900002E+30," + b + "13033,17033,21033,25033,0,0,0,0,0,0,"
                               + b + "0,0,0,0,0,0,0,0,0,0," + b + "0," + b + f"0,0,4,{EoK},0," + b + "1,0,1,0," + b)
            id_counter_yyb = 0
            for item in douyyb_list1:
                result_sheet.write(str(ID_list[id_counter_yyb]) + " " + str(item) + b)
                id_counter_yyb += 1
            result_sheet.write("-1,0.," + b)
            result_sheet.write("1,9042,1," + b + "DOUxyBot" + b
                               + "9.9900002E+30,-9.9900002E+30,9.9900002E+30," + b + "13033,17033,21033,25033,0,0,0,0,0,0,"
                               + b + "0,0,0,0,0,0,0,0,0,0," + b + "0," + b + f"0,0,4,{EoK},0," + b + "1,0,1,0," + b)
            id_counter_xyb = 0
            for item in douxyb_list1:
                result_sheet.write(str(ID_list[id_counter_xyb]) + " " + str(item) + b)
                id_counter_xyb += 1
            result_sheet.write("-1,0.," + b)
            result_sheet.write("1,9043,1," + b + "DOUeqvBot" + b
                               + "9.9900002E+30,-9.9900002E+30,9.9900002E+30," + b + "13033,17033,21033,25033,0,0,0,0,0,0,"
                               + b + "0,0,0,0,0,0,0,0,0,0," + b + "0," + b + f"0,0,4,{EoK},0," + b + "1,0,1,0," + b)
            id_counter_EQVb = 0
            for item in douEQVb_list1:
                result_sheet.write(str(ID_list[id_counter_EQVb]) + " " + str(item) + b)
                id_counter_EQVb += 1

            # End of result file
            result_sheet.write("-1,0.," + b + a + "-1" + b + a + "-1" + b + "  " + "1056" + b + "1,"
                               + b + "shell_format" + b + "36,1," + b + "1613143822,1," + b + "1," + b
                               + "<NULL>" + b + a + "-1")

        elif weld_yes_no == "YES" and norm == "DVS":
            # beginning of comparison between file1 and file2
            while line:
                # read first file plus implementing ID number and property. Defining variables.
                werte = line.strip()
                werte_split = werte.split(",")
                line = file1.readline()
                ID = int(werte_split[0].rstrip(","))
                ID_list.append(ID)
                propertyID = str(werte_split[1].rstrip(";"))

                # properties
                schub_list = [93, 82, 73, 65, 59, 53]
                property_list = []
                for i in propertyID:
                    property_list += i
                # Stahl
                property1 = int(str(property_list[0]) + str(property_list[1]) + str(property_list[2]))
                # Dicke
                property2 = float(str(property_list[3]) + str(property_list[4]) + str(property_list[5])) / 10
                # für x
                property3 = int(str(property_list[6]) + str(property_list[7]))
                # für y
                property4 = int(str(property_list[8]))
                # print(property1, property2, property3, property4)

                # get property
                if property1 == 235:
                    s235_list = [4.33, 5, 5.67, 6.33, 7, 7.67, 8.33, 9, 9.67, 10.33, 11, 11.67, 12.33, 13, 13.67, 14,
                                 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 33.70, 41]
                    x = s235_list[property3]
                elif property1 == 355:
                    s355_list = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                 23, 24, 25, 26, 27, 28, 33.7, 41]
                    x = s355_list[property3]
                y = schub_list[property4]

                if property2 <= 10:
                    df = 1.0
                else:
                    df = (10 / property2) ** 0.1

                SigN = (float(werte_split[2].rstrip(","))) / fa1
                SigP = (float(werte_split[3].rstrip(","))) / fa1
                Tau = (float(werte_split[4].rstrip(","))) / fa1
                SigNb = (float(werte_split[5].rstrip(","))) / fa1
                SigPb = (float(werte_split[6].rstrip(","))) / fa1
                Taub = (float(werte_split[7].rstrip(","))) / fa1
                # read second file. Defining variables
                werte2 = line2.strip()
                werte2_split = werte2.split(",")
                line2 = file2.readline()
                SigN2 = (float(werte2_split[2].rstrip(","))) / fa1
                SigP2 = (float(werte2_split[3].rstrip(","))) / fa1
                Tau2 = (float(werte2_split[4].rstrip(","))) / fa1
                SigN2b = (float(werte2_split[5].rstrip(","))) / fa1
                SigP2b = (float(werte2_split[6].rstrip(","))) / fa1
                Tau2b = (float(werte2_split[7].rstrip(","))) / fa1

                SigMaxN = max(SigN, SigN2)
                SigMinN = min(SigN, SigN2)
                SigMaxP = max(SigP, SigP2)
                SigMinP = min(SigP, SigP2)
                TauMax = max(Tau, Tau2)
                TauMin = min(Tau, Tau2)
                SigMaxNb = max(SigNb, SigN2b)
                SigMinNb = min(SigNb, SigN2b)
                SigMaxPb = max(SigPb, SigP2b)
                SigMinPb = min(SigPb, SigP2b)
                TauMaxb = max(Taub, Tau2b)
                TauMinb = min(Taub, Tau2b)

                if Tau == 0:
                    Tau = 0.0001
                if Tau2 == 0:
                    Tau2 = 0.0001
                if SigMaxN == 0:
                    SigMaxN = 0.0001
                if SigMinN == 0:
                    SigMinN = 0.0001
                if SigMaxP == 0:
                    SigMaxP = 0.0001
                if SigMinP == 0:
                    SigMinP = 0.0001
                if TauMax == 0:
                    TauMax = 0.0001
                if TauMin == 0:
                    TauMin = 0
                if Taub == 0:
                    Taub = 0.0001
                if Tau2b == 0:
                    Tau2b = 0.0001
                if SigMaxNb == 0:
                    SigMaxNb = 0.0001
                if SigMinNb == 0:
                    SigMinNb = 0.0001
                if SigMaxPb == 0:
                    SigMaxPb = 0.0001
                if SigMinPb == 0:
                    SigMinPb = 0.0001
                if TauMaxb == 0:
                    TauMaxb = 0.0001
                if TauMinb == 0:
                    TauMinb = 0

                if 0.5 * (SigMaxN + SigMinN) >= 0:
                    Rn = SigMinN / SigMaxN
                    if Rn == 1:
                        Rn = 1.0001
                    SigMaxZuln = df * (150 * (1.04 ** -x) * ((2 * (1 - 0.3 * Rn)) / (1.3 * (1 - Rn))))

                else:
                    Rn = SigMaxN / SigMinN
                    if Rn == 1:
                        Rn = 1.0001
                    SigMaxZuln = df * (150 * (1.04 ** -x) * (2 / (1 - Rn)))

                if SigMaxZuln > (property1 / sf):
                    SigMaxZuln = (property1 / sf)

                if 0.5 * (SigMaxP + SigMinP) >= 0:
                    Rp = SigMinP / SigMaxP
                    if Rp == 1:
                        Rp = 1.0001
                    SigMaxZulp = df * (150 * (1.04 ** -x) * ((2 * (1 - 0.3 * Rp)) / (1.3 * (1 - Rp))))

                else:
                    Rp = SigMaxP / SigMinP
                    if Rp == 1:
                        Rp = 1.0001
                    SigMaxZulp = df * (150 * (1.04 ** -x) * (2 / (1 - Rp)))

                if SigMaxZulp > (property1 / sf):
                    SigMaxZulp = (property1 / sf)

                if abs(Tau) < abs(Tau2):
                    Rt = Tau / Tau2

                else:
                    Rt = Tau2 / Tau

                if Rt == 1:
                    Rt = 1.0001

                TauMaxZul = df * (((2 * (1 - 0.17 * Rt)) / (1.17 * (1 - Rt))) * y)

                if TauMaxZul > (property1 / sqrt(3)) / sf:
                    TauMaxZul = (property1 / sqrt(3)) / sf

                # Bottom

                if 0.5 * (SigMaxNb + SigMinNb) >= 0:
                    Rnb = SigMinNb / SigMaxNb
                    if Rnb == 1:
                        Rnb = 1.0001
                    SigMaxZulnb = df * (150 * (1.04 ** -x) * ((2 * (1 - 0.3 * Rnb)) / (1.3 * (1 - Rnb))))

                else:
                    Rnb = SigMaxNb / SigMinNb
                    if Rnb == 1:
                        Rnb = 1.0001
                    SigMaxZulnb = df * (150 * (1.04 ** -x) * (2 / (1 - Rnb)))

                if SigMaxZulnb > (property1 / sf):
                    SigMaxZulnb = (property1 / sf)

                if 0.5 * (SigMaxPb + SigMinPb) >= 0:
                    Rpb = SigMinPb / SigMaxPb
                    if Rpb == 1:
                        Rpb = 1.0001
                    SigMaxZulpb = df * (150 * (1.04 ** -x) * ((2 * (1 - 0.3 * Rpb)) / (1.3 * (1 - Rpb))))

                else:
                    Rpb = SigMaxPb / SigMinPb
                    if Rpb == 1:
                        Rpb = 1.0001
                    SigMaxZulpb = df * (150 * (1.04 ** -x) * (2 / (1 - Rpb)))

                if SigMaxZulpb > (property1 / sf):
                    SigMaxZulpb = (property1 / sf)

                if abs(Taub) < abs(Tau2b):
                    Rtb = Taub / Tau2b

                else:
                    Rtb = Tau2b / Taub

                if Rtb == 1:
                    Rtb = 1.0001

                TauMaxZulb = df * (((2 * (1 - 0.17 * Rtb)) / (1.17 * (1 - Rtb))) * y)

                if TauMaxZulb > (property1 / sqrt(3)) / sf:
                    TauMaxZulb = (property1 / sqrt(3)) / sf

                DOUn = max(abs(SigN), abs(SigN2)) / SigMaxZuln
                DOUp = max(abs(SigP), abs(SigP2)) / SigMaxZulp
                DOUt = max(abs(Tau), abs(Tau2)) / TauMaxZul
                DOUeqv = ((max(abs(SigP), abs(SigP2)) / (SigMaxZulp)) ** 2) + (
                        (max(abs(SigN), abs(SigN2)) / (SigMaxZuln)) ** 2) \
                         - (max(abs(SigN), abs(SigN2)) / SigMaxZuln) * (max(abs(SigP), abs(SigP2)) / SigMaxZulp) \
                         + (max(abs(Tau), abs(Tau2)) / TauMaxZul) ** 2

                DOUnb = max(abs(SigNb), abs(SigN2b)) / SigMaxZulnb
                DOUpb = max(abs(SigPb), abs(SigP2b)) / SigMaxZulpb
                DOUtb = max(abs(Taub), abs(Tau2b)) / TauMaxZulb
                DOUeqvb = ((max(abs(SigPb), abs(SigP2b)) / (SigMaxZulpb)) ** 2) \
                          + ((max(abs(SigNb), abs(SigN2b)) / (SigMaxZulnb)) ** 2) \
                          - (max(abs(SigNb), abs(SigN2b)) / SigMaxZulnb) * (max(abs(SigPb), abs(SigP2b)) / SigMaxZulpb) \
                          + (max(abs(Taub), abs(Tau2b)) / TauMaxZulb) ** 2

                if DOUn > douxxt_list1[counter]:
                    douxxt_list1[counter] = DOUn
                if DOUp > douyyt_list1[counter]:
                    douyyt_list1[counter] = DOUp
                if DOUt > douxyt_list1[counter]:
                    douxyt_list1[counter] = DOUt
                if DOUeqv > douEQVt_list1[counter]:
                    douEQVt_list1[counter] = DOUeqv
                if DOUnb > douxxb_list1[counter]:
                    douxxb_list1[counter] = DOUnb
                if DOUpb > douyyb_list1[counter]:
                    douyyb_list1[counter] = DOUpb
                if DOUtb > douxyb_list1[counter]:
                    douxyb_list1[counter] = DOUtb
                if DOUeqvb > douEQVb_list1[counter]:
                    douEQVb_list1[counter] = DOUeqvb

                douxxt_list = douxxt_list1
                douyyt_list = douyyt_list1
                douxyt_list = douxyt_list1
                douEQVt_list = douEQVt_list1
                douxxb_list = douxxb_list1
                douyyb_list = douyyb_list1
                douxyb_list = douxyb_list1
                douEQVb_list = douEQVb_list1

                # Bericht info
                if DOUeqv > crit:
                    bericht.write(str(ID) + "," + "DOUeqvTop" + "," + str(DOUeqv) + "," + str(SigN) + ","
                                  + str(SigN2) + "," + str(SigMaxZuln) + "," + str(SigP) + ","
                                  + str(SigP2) + "," + str(SigMaxZulp) + "," + str(Tau) + "," + str(Tau2) + ","
                                  + str(TauMaxZul) + "," + str(list_lf[counter11]) + "," + str(list_lf[counter21])
                                  + "\n")

                if DOUn > crit:
                    bericht.write(str(ID) + "," + "DOUnTop" + "," + str(DOUn) + "," + str(SigN) + ","
                                  + str(SigN2) + "," + str(SigMaxZuln) + ",,,,,,,"
                                  + str(list_lf[counter11]) + "," + str(list_lf[counter21])
                                  + "\n")

                if DOUp > crit:
                    bericht.write(str(ID) + "," + "DOUpTop" + ",,,," + str(DOUp) + "," + str(SigP) + ","
                                  + str(SigP2) + "," + str(SigMaxZulp) + ",,,,"
                                  + str(list_lf[counter11]) + "," + str(list_lf[counter21])
                                  + "\n")

                if DOUt > crit:
                    bericht.write(str(ID) + "," + "DOUtTop" + ",,,,,,," + str(DOUt) + "," + str(Tau) + ","
                                  + str(Tau2) + "," + str(TauMaxZul) + ","
                                  + str(list_lf[counter11]) + "," + str(list_lf[counter21])
                                  + "\n")

                if DOUeqvb > crit:
                    bericht.write(str(ID) + "," + "DOUeqvBot" + "," + str(DOUeqvb) + "," + str(SigNb) + ","
                                  + str(SigN2b) + "," + str(SigMaxZulnb) + "," + str(SigPb) + ","
                                  + str(SigP2b) + "," + str(SigMaxZulpb) + "," + str(Taub) + "," + str(Tau2b) + ","
                                  + str(TauMaxZulb) + "," + str(list_lf[counter11]) + "," + str(list_lf[counter21])
                                  + "\n")

                if DOUnb > crit:
                    bericht.write(str(ID) + "," + "DOUnBot" + "," + str(DOUnb) + "," + str(SigNb) + ","
                                  + str(SigN2b) + "," + str(SigMaxZulnb) + ",,,,,,,"
                                  + str(list_lf[counter11]) + "," + str(list_lf[counter21])
                                  + "\n")

                if DOUpb > crit:
                    bericht.write(str(ID) + "," + "DOUpBot" + ",,,," + str(DOUpb) + "," + str(SigPb) + ","
                                  + str(SigP2b) + "," + str(SigMaxZulpb) + ",,,,"
                                  + str(list_lf[counter11]) + "," + str(list_lf[counter21])
                                  + "\n")

                if DOUtb > crit:
                    bericht.write(str(ID) + "," + "DOUtBot" + ",,,,,,," + str(DOUtb) + "," + str(Taub) + ","
                                  + str(Tau2b) + "," + str(TauMaxZulb) + ","
                                  + str(list_lf[counter11]) + "," + str(list_lf[counter21])
                                  + "\n")

                counter += 1
                output1 = total_time = ((time.time() - start))
                output2 = round(output1, 1)

                if output2 < 60:
                    output3 = str(output2) + " " + "sek."
                    labelStat.config(text=f"Calculation in progress... {output3}")
                elif output2 >= 60:
                    output3 = str(round((output2 / 60), 1)) + " " + "min."
                    labelStat.config(text=f"Calculation in progress... {output3}")

                if function_def == "SH":
                    interface2.update()
                else:
                    interface.update()

            # writing end_file when comparison between file1 and file2 is done.
            # results Top
            result_sheet.write(a + "-1" + b + "  " + "1051" + b + "1,7040,1," + b + "DOUnTop" + b
                               + "9.9900002E+30,-9.9900002E+30,9.9900002E+30," + b + "11033,15033,19033,23033,0,0,0,0,0,0,"
                               + b + "0,0,0,0,0,0,0,0,0,0," + b + "0," + b + f"0,0,4,{EoK},0," + b + "1,0,1,0," + b)
            id_counter_xxt = 0
            for item in douxxt_list1:
                result_sheet.write(str(ID_list[id_counter_xxt]) + " " + str(item) + b)
                id_counter_xxt += 1
            result_sheet.write("-1,0.," + b)

            result_sheet.write("1,7041,1," + b + "DOUpTop" + b
                               + "9.9900002E+30,-9.9900002E+30,9.9900002E+30," + b + "11033,15033,19033,23033,0,0,0,0,0,0,"
                               + b + "0,0,0,0,0,0,0,0,0,0," + b + "0," + b + f"0,0,4,{EoK},0," + b + "1,0,1,0," + b)
            id_counter_yyt = 0
            for item in douyyt_list1:
                result_sheet.write(str(ID_list[id_counter_yyt]) + " " + str(item) + b)
                id_counter_yyt += 1
            result_sheet.write("-1,0.," + b)

            result_sheet.write("1,7042,1," + b + "DOUtTop" + b
                               + "9.9900002E+30,-9.9900002E+30,9.9900002E+30," + b + "11033,15033,19033,23033,0,0,0,0,0,0,"
                               + b + "0,0,0,0,0,0,0,0,0,0," + b + "0," + b + f"0,0,4,{EoK},0," + b + "1,0,1,0," + b)
            id_counter_xyt = 0
            for item in douxyt_list1:
                result_sheet.write(str(ID_list[id_counter_xyt]) + " " + str(item) + b)
                id_counter_xyt += 1
            result_sheet.write("-1,0.," + b)

            result_sheet.write("1,7043,1," + b + "DOUeqvTop" + b
                               + "9.9900002E+30,-9.9900002E+30,9.9900002E+30," + b + "11033,15033,19033,23033,0,0,0,0,0,0,"
                               + b + "0,0,0,0,0,0,0,0,0,0," + b + "0," + b + f"0,0,4,{EoK},0," + b + "1,0,1,0," + b)
            id_counter_EQVt = 0
            for item in douEQVt_list1:
                result_sheet.write(str(ID_list[id_counter_EQVt]) + " " + str(item) + b)
                id_counter_EQVt += 1
            result_sheet.write("-1,0.," + b)

            # results Bottom
            result_sheet.write("1,9040,1," + b + "DOUnBot" + b
                               + "9.9900002E+30,-9.9900002E+30,9.9900002E+30," + b + "13033,17033,21033,25033,0,0,0,0,0,0,"
                               + b + "0,0,0,0,0,0,0,0,0,0," + b + "0," + b + f"0,0,4,{EoK},0," + b + "1,0,1,0," + b)
            id_counter_xxb = 0
            for item in douxxb_list1:
                result_sheet.write(str(ID_list[id_counter_xxb]) + " " + str(item) + b)
                id_counter_xxb += 1
            result_sheet.write("-1,0.," + b)

            result_sheet.write("1,9041,1," + b + "DOUpBot" + b
                               + "9.9900002E+30,-9.9900002E+30,9.9900002E+30," + b + "13033,17033,21033,25033,0,0,0,0,0,0,"
                               + b + "0,0,0,0,0,0,0,0,0,0," + b + "0," + b + f"0,0,4,{EoK},0," + b + "1,0,1,0," + b)
            id_counter_yyb = 0
            for item in douyyb_list1:
                result_sheet.write(str(ID_list[id_counter_yyb]) + " " + str(item) + b)
                id_counter_yyb += 1
            result_sheet.write("-1,0.," + b)

            result_sheet.write("1,9042,1," + b + "DOUtBot" + b
                               + "9.9900002E+30,-9.9900002E+30,9.9900002E+30," + b + "13033,17033,21033,25033,0,0,0,0,0,0,"
                               + b + "0,0,0,0,0,0,0,0,0,0," + b + "0," + b + f"0,0,4,{EoK},0," + b + "1,0,1,0," + b)
            id_counter_xyb = 0
            for item in douxyb_list1:
                result_sheet.write(str(ID_list[id_counter_xyb]) + " " + str(item) + b)
                id_counter_xyb += 1
            result_sheet.write("-1,0.," + b)

            result_sheet.write("1,9043,1," + b + "DOUeqvBot" + b
                               + "9.9900002E+30,-9.9900002E+30,9.9900002E+30," + b + "13033,17033,21033,25033,0,0,0,0,0,0,"
                               + b + "0,0,0,0,0,0,0,0,0,0," + b + "0," + b + f"0,0,4,{EoK},0," + b + "1,0,1,0," + b)
            id_counter_EQVb = 0
            for item in douEQVb_list1:
                result_sheet.write(str(ID_list[id_counter_EQVb]) + " " + str(item) + b)
                id_counter_EQVb += 1

            # End of result file
            result_sheet.write("-1,0.," + b + a + "-1" + b + a + "-1" + b + "  " + "1056" + b + "1,"
                               + b + "shell_format" + b + "36,1," + b + "1613143822,1," + b + "1," + b
                               + "<NULL>" + b + a + "-1")
            result_sheet.close()

    BLUE = "\033[34m"  # Colour variable
    # math for solid
    if function_def == "SO":
        start = time.time()
        print("Starting Calculation...")
        file_list = []
        open_path = "C:\\Users\\raphi\\PycharmProjects\\pythonProject"  # copy your path here
        open_name = "Index.txt"
        open_file = open_path + open_name
        with open(open_file) as index:  # "Index.txt" file (contains names of files (file_list) to know what to compare)
            for string in index:  # reading index
                file_list += string.split()
            length_list = len(file_list)
            with open("lastfall0.txt") as laenge:  # getting lenght of "lastfall0.txt" file
                counter_laenge = 0
                for lines in laenge:
                    counter_laenge += 1
                douxx_list = [-9999999999990] * counter_laenge  # creates list with index == lenghts("lastfall") file
                douyy_list = [-9999999999990] * counter_laenge
                douzz_list = [-9999999999990] * counter_laenge
                douxy_list = [-9999999999990] * counter_laenge
                douxz_list = [-9999999999990] * counter_laenge
                douyz_list = [-9999999999990] * counter_laenge
                douEQV_list = [-9999999999990] * counter_laenge

            laenge.close()
            counter_compares = 0
            for i in range(0, length_list - 1):  # taking files to compare
                for j in range(i + 1, length_list):
                    # your path after (with open)
                    with open("C:\\Users\\raphi\\PycharmProjects\\pythonProject" + file_list[i]) as mr5, \
                            open("C:\\Users\\raphi\\PycharmProjects\\pythonProject" + file_list[j]) as mr6:
                        math_solid(mr5, mr6, douxx_list,
                                   douyy_list, douzz_list, douxy_list, douxz_list, douyz_list, douEQV_list)
                    counter_compares += 1
                    print(counter_compares)
            print(f"Total of {str(counter_compares)} comparisons between {length_list} files were made.")
            total_time = (time.time() - start)  # printing total time
            total_time_rounded = round(total_time, 1)
            print(f"Script (solid) finished. It took {float(total_time_rounded) / 60} minutes.")
            output = f"Script (solid) finished. Elapsed time = {float(total_time_rounded) / 60} minutes." \
                     f" Total of {str(counter_compares)} comparisons of {length_list} files."
            labelStat.config(text=output)

    # math for shell
    elif function_def == "SH":
        start = time.time()
        entryComp.config(text="wait...")
        file_list = []
        global bericht
        save_path = "C:\\Users\\raphi\\PycharmProjects\\pythonProject\\"
        fn1 = "bericht"
        complete_name1 = os.path.join(save_path, fn1)
        bericht = open(complete_name1 + ".txt", "w")
        bericht.write("ID,DOU,EQV,SIGn1,SIGn2,SIGn_zul,SIGp1,SIGp2,SIGp_zul,TAU1,TAU2,TAUzul,Nr_LF1,NR_LF2" + "\n")

        with open("Index.txt") as index:  # "Index.txt" file (contains names of files, to know what to compare)
            for string in index:  # reading index
                file_list += string.split()
            length_list = len(file_list)
            list_lf = []
            counter_lf = 1
            for i in range(0, length_list):
                list_lf.append(counter_lf)
                counter_lf += 1
            print(list_lf)

            with open("lastfall0.txt") as laenge:  # getting lenght of "lastfall0.txt" file
                counter_laenge = 0
                for lines in laenge:
                    counter_laenge += 1
                douxxt_list = [-9999999999990] * counter_laenge  # creates list with index == lenghts("lastfall") file
                douyyt_list = [-9999999999990] * counter_laenge
                douxyt_list = [-9999999999990] * counter_laenge
                douxxb_list = [-9999999999990] * counter_laenge
                douyyb_list = [-9999999999990] * counter_laenge
                douxyb_list = [-9999999999990] * counter_laenge
                douEQVt_list = [-9999999999990] * counter_laenge
                douEQVb_list = [-9999999999990] * counter_laenge
                counter1 = 0
                counter2 = 1

            laenge.close()
            counter_compares = 0
            for i in range(0, length_list - 1):  # looping through files
                for j in range(i + 1, length_list):
                    with open(file_list[i]) as mr5, \
                            open(file_list[j]) as mr6:

                        # calling the actual function
                        math_shell(mr5, mr6, douxxt_list, douyyt_list, douxyt_list, douxxb_list, douyyb_list,
                                   douxyb_list, douEQVt_list, douEQVb_list, list_lf, counter1, counter2)
                    if counter2 == length_list - 1:
                        counter1 += 1
                        counter2 = counter1

                    counter2 += 1
                    counter_compares += 1
                    total_time = (time.time() - start)
                    estimated_comp = int((length_list * (length_list - 1)) / 2)
                    entryComp.config(text=f"""{counter_compares}/{estimated_comp}""")
                    if function_def == "SH":
                        interface2.update()
                    else:
                        interface.update()
                    estimated_time_left = ((total_time / counter_compares) * estimated_comp) - (total_time)
                    print(f"Estimated time left {(round(float(estimated_time_left) / 60, 2))} min.")
            print(f"Total of {str(counter_compares)} comparisons between {length_list} files were made.")
            total_time = str((time.time() - start))  # printing total time
            print(f"Script (shell) finished. It took {float(total_time) / 60} minutes.")
            bericht.close()
            labelStat.config(text=f"Process finished successfully. "
                                  f"It took {round((float(total_time) / 60), 1)} minutes.")

    # in case of unknown/missing input.
    else:
        output4 = "Please check your inputs :)"
        labelStat.config(text=output4)


def interface_FKM(output_set_name, unit, norm):


    def call1(labelStat, output_set_name, entryCrit, labelWeldy, labelnorme, entryRm, entryFsig, entryFtau,
        entryNsig, entryKf, entryRmN, entryRsig, entryR_Z, entryK_V, entryK_S, entryK_Nle, entryA_m, entryBm,
        entryNreq, entryN_Dsig, entryN_D2sig, entryKsig, entryK2sig, entryN_Dtau, entryN_D2tau, entryKtau,
        entryK2tau, entryf2sig, entryf2tau, entryjF, entryUnit2, entryComp, interface):

        entryUnit = unit
        labelnorme = norm
        entryS1 = 100
        buttonSolve(labelStat, output_set_name, entryCrit, labelWeldy, entryUnit, labelnorme, entryRm, entryFsig, entryFtau,
        entryNsig, entryKf, entryRmN, entryRsig, entryR_Z, entryK_V, entryK_S, entryK_Nle, entryA_m, entryBm,
        entryNreq, entryN_Dsig, entryN_D2sig, entryKsig, entryK2sig, entryN_Dtau, entryN_D2tau, entryKtau,
        entryK2tau, entryf2sig, entryf2tau, entryjF, entryUnit2, entryS1, entryComp, interface)
    # Interface FKM
    interface = Tk("FKM")
    interface.title('Ingenis Auswertung')
    interface.geometry('1110x675')

    path1 = 'C:\\Users\\raphi\\Pictures\\Saved Pictures\\DK2.jpeg'
    # img1 = ImageTk.PhotoImage(Image.open(path1))
    # panel1 = tk.Label(interface, image=img1)
    # panel1.pack(side="bottom", fill="both", expand="yes")
    # R_m
    lableRm = Label(master=interface, bg='white', text='R_m:')
    lableRm.place(x=54, y=24, width=100, height=27)
    entryRm = Entry(master=interface, bg='white')
    entryRm.place(x=164, y=24, width=200, height=27)
    lableTab_Rm = Label(master=interface, bg="yellow", text="Tab. 4.2.1")
    lableTab_Rm.place(x=373, y=24, width=150, height=27)
    entryRm.insert(0, 200)
    # f_wsig
    lableFsig = Label(master=interface, bg='white', text='f_wsig:')
    lableFsig.place(x=54, y=64, width=100, height=27)
    entryFsig = Entry(master=interface, bg='white')
    entryFsig.place(x=164, y=64, width=200, height=27)
    lableTab_Fsig = Label(master=interface, bg="yellow", text="Tab. 4.2.1")
    lableTab_Fsig.place(x=373, y=64, width=150, height=27)
    entryFsig.insert(0, 0.3)
    # f_wtau
    lableFtau = Label(master=interface, bg='white', text='f_wtau:')
    lableFtau.place(x=54, y=104, width=100, height=27)
    entryFtau = Entry(master=interface, bg='white')
    entryFtau.place(x=164, y=104, width=200, height=27)
    lableTab_Ftau = Label(master=interface, bg="yellow", text="Tab. 4.2.1")
    lableTab_Ftau.place(x=373, y=104, width=150, height=27)
    entryFtau.insert(0, 0.577)
    # n_sig
    lableNsig = Label(master=interface, bg='white', text='n_sig, n_tau:')
    lableNsig.place(x=54, y=144, width=100, height=27)
    entryNsig = Entry(master=interface, bg='white')
    entryNsig.place(x=164, y=144, width=200, height=27)
    lableTab_Nsig = Label(master=interface, bg="yellow", text="Kap. 4.3.1.3.1")
    lableTab_Nsig.place(x=373, y=144, width=150, height=27)
    entryNsig.insert(0, 1.0)
    # Kf
    lableKf = Label(master=interface, bg='white', text='Kf:')
    lableKf.place(x=54, y=184, width=100, height=27)
    entryKf = Entry(master=interface, bg='white')
    entryKf.place(x=164, y=184, width=200, height=27)
    lableTab_Kf = Label(master=interface, bg="yellow", text="Kap. 4.3.1.2, Tab. 4.3.1")
    lableTab_Kf.place(x=373, y=184, width=150, height=27)
    entryKf.insert(0, 2.0)
    # R_mNmin
    lableRmN = Label(master=interface, bg='white', text='R_mNmin:')
    lableRmN.place(x=54, y=224, width=100, height=27)
    entryRmN = Entry(master=interface, bg='white')
    entryRmN.place(x=164, y=224, width=200, height=27)
    lableTab_RmN = Label(master=interface, bg="yellow", text="Tab. 4.3.5")
    lableTab_RmN.place(x=373, y=224, width=150, height=27)
    entryRmN.insert(0, 133.0)
    # a_Rsig
    lableRsig = Label(master=interface, bg='white', text='a_Rsig:')
    lableRsig.place(x=54, y=264, width=100, height=27)
    entryRsig = Entry(master=interface, bg='white')
    entryRsig.place(x=164, y=264, width=200, height=27)
    lableTab_Rsig = Label(master=interface, bg="yellow", text="Tab. 4.3.5")
    lableTab_Rsig.place(x=373, y=264, width=150, height=27)
    entryRsig.insert(0, 0.22)
    # R_z
    lableR_Z = Label(master=interface, bg='white', text='R_z:')
    lableR_Z.place(x=54, y=304, width=100, height=27)
    entryR_Z = Entry(master=interface, bg='white')
    entryR_Z.place(x=164, y=304, width=200, height=27)
    lableTab_R_Z = Label(master=interface, bg='yellow', text="Bauteil")
    lableTab_R_Z.place(x=373, y=304, width=150, height=27)
    entryR_Z.insert(0, 25)
    # K_V
    lableK_V = Label(master=interface, bg='white', text='K_V:')
    lableK_V.place(x=54, y=344, width=100, height=27)
    entryK_V = Entry(master=interface, bg='white')
    entryK_V.place(x=164, y=344, width=200, height=27)
    lableTab_K_V = Label(master=interface, bg="yellow", text="Kap. 4.3.3")
    lableTab_K_V.place(x=373, y=344, width=150, height=27)
    entryK_V.insert(0, 1.0)
    # KS
    lableK_S = Label(master=interface, bg='white', text='KS:')
    lableK_S.place(x=54, y=384, width=100, height=27)
    entryK_S = Entry(master=interface, bg='white')
    entryK_S.place(x=164, y=384, width=200, height=27)
    lableTab_K_S = Label(master=interface, bg="yellow", text="Kap. 4.3.4")
    lableTab_K_S.place(x=373, y=384, width=150, height=27)
    entryK_S.insert(0, 1.0)
    # K_NL,E
    lableK_Nle = Label(master=interface, bg='white', text='K_NL,E:')
    lableK_Nle.place(x=54, y=424, width=100, height=27)
    entryK_Nle = Entry(master=interface, bg='white')
    entryK_Nle.place(x=164, y=424, width=200, height=27)
    lableTab_K_Nle = Label(master=interface, bg="yellow", text="Kap. 4.3.5")
    lableTab_K_Nle.place(x=373, y=424, width=150, height=27)
    entryK_Nle.insert(0, 1.0)
    # a_m
    lableA_m = Label(master=interface, bg='white', text='a_m:')
    lableA_m.place(x=54, y=464, width=100, height=27)
    entryA_m = Entry(master=interface, bg='white')
    entryA_m.place(x=164, y=464, width=200, height=27)
    lableTab_A_m = Label(master=interface, bg="yellow", text="Tab. 4.4.1")
    lableTab_A_m.place(x=373, y=464, width=150, height=27)
    entryA_m.insert(0, 0.35)
    # Unit

    # second unit
    lableUnit2 = Label(master=interface, bg='pink', text='Knot (7) or Element (8)')
    lableUnit2.place(x=224, y=504, width=140, height=27)
    entryUnit2 = Entry(master=interface, bg='white', text="")
    entryUnit2.place(x=373, y=504, width=50, height=27)
    entryUnit2.insert(0, 8)
    # comparison stat
    entryComp = Label(master=interface, bg='white', text="")
    entryComp.place(x=904, y=544, width=50, height=27)
    # b_m
    lableBm = Label(master=interface, bg='white', text='b_m:')
    lableBm.place(x=584, y=24, width=100, height=27)
    entryBm = Entry(master=interface, bg='white')
    entryBm.place(x=694, y=24, width=200, height=27)
    lableTab_Bm = Label(master=interface, bg="yellow", text="Tab. 4.4.1")
    lableTab_Bm.place(x=903, y=24, width=150, height=27)
    entryBm.insert(0, - 0.1)
    # Nreq
    lableNreq = Label(master=interface, bg='white', text='Nreq:')
    lableNreq.place(x=584, y=64, width=100, height=27)
    entryNreq = Entry(master=interface, bg='white')
    entryNreq.place(x=694, y=64, width=200, height=27)
    lableTab_Nreq = Label(master=interface, bg="yellow", text="Benutzereingabe")
    lableTab_Nreq.place(x=903, y=64, width=150, height=27)
    entryNreq.insert(0, 10000000)
    # N_Dsig
    lableN_Dsig = Label(master=interface, bg='white', text='N_Dsig:')
    lableN_Dsig.place(x=584, y=104, width=100, height=27)
    entryN_Dsig = Entry(master=interface, bg='white')
    entryN_Dsig.place(x=694, y=104, width=200, height=27)
    lableTab_N_Dsig = Label(master=interface, bg="yellow", text="Tab. 4.4.3")
    lableTab_N_Dsig.place(x=903, y=104, width=150, height=27)
    entryN_Dsig.insert(0, 1000000)
    # N_DIIsig
    lableN_D2sig = Label(master=interface, bg='white', text='N_DIIsig:')
    lableN_D2sig.place(x=584, y=144, width=100, height=27)
    entryN_D2sig = Entry(master=interface, bg='white')
    entryN_D2sig.place(x=694, y=144, width=200, height=27)
    lableTab_N_D2sig = Label(master=interface, bg="yellow", text="Tab. 4.4.3")
    lableTab_N_D2sig.place(x=903, y=144, width=150, height=27)
    entryN_D2sig.insert(0, 100000000)
    # Ksig
    lableKsig = Label(master=interface, bg='white', text='Ksig:')
    lableKsig.place(x=584, y=184, width=100, height=27)
    entryKsig = Entry(master=interface, bg='white')
    entryKsig.place(x=694, y=184, width=200, height=27)
    lableTab_Ksig = Label(master=interface, bg="yellow", text="Tab. 4.4.3")
    lableTab_Ksig.place(x=903, y=184, width=150, height=27)
    entryKsig.insert(0, 5.0)
    # KIIsig
    lableK2sig = Label(master=interface, bg='white', text='KIIsig:')
    lableK2sig.place(x=584, y=224, width=100, height=27)
    entryK2sig = Entry(master=interface, bg='white')
    entryK2sig.place(x=694, y=224, width=200, height=27)
    lableTab_K2sig = Label(master=interface, bg="yellow", text="Tab. 4.4.3")
    lableTab_K2sig.place(x=903, y=224, width=150, height=27)
    entryK2sig.insert(0, 15.0)
    # N_Dtau
    lableN_Dtau = Label(master=interface, bg='white', text='N_Dtau:')
    lableN_Dtau.place(x=584, y=264, width=100, height=27)
    entryN_Dtau = Entry(master=interface, bg='white')
    entryN_Dtau.place(x=694, y=264, width=200, height=27)
    lableTab_N_Dtau = Label(master=interface, bg="yellow", text="Tab. 4.4.3")
    lableTab_N_Dtau.place(x=903, y=264, width=150, height=27)
    entryN_Dtau.insert(0, 1000000)
    # N_DIItau
    lableN_D2tau = Label(master=interface, bg='white', text='N_DIItau:')
    lableN_D2tau.place(x=584, y=304, width=100, height=27)
    entryN_D2tau = Entry(master=interface, bg='white')
    entryN_D2tau.place(x=694, y=304, width=200, height=27)
    lableTab_N_D2tau = Label(master=interface, bg="yellow", text="Tab. 4.4.3")
    lableTab_N_D2tau.place(x=903, y=304, width=150, height=27)
    entryN_D2tau.insert(0, 100000000)
    # Ktau
    lableKtau = Label(master=interface, bg='white', text='Ktau:')
    lableKtau.place(x=584, y=344, width=100, height=27)
    entryKtau = Entry(master=interface, bg='white')
    entryKtau.place(x=694, y=344, width=200, height=27)
    lableTab_Ktau = Label(master=interface, bg="yellow", text="Tab. 4.4.3")
    lableTab_Ktau.place(x=903, y=344, width=150, height=27)
    entryKtau.insert(0, 8.0)
    # KIItau
    lableK2tau = Label(master=interface, bg='white', text='KIItau:')
    lableK2tau.place(x=584, y=384, width=100, height=27)
    entryK2tau = Entry(master=interface, bg='white')
    entryK2tau.place(x=694, y=384, width=200, height=27)
    lableTab_K2tau = Label(master=interface, bg="yellow", text="Tab. 4.4.3")
    lableTab_K2tau.place(x=903, y=384, width=150, height=27)
    entryK2tau.insert(0, 25.0)
    # fIIsig
    lablef2sig = Label(master=interface, bg='white', text='fIIsig:')
    lablef2sig.place(x=584, y=424, width=100, height=27)
    entryf2sig = Entry(master=interface, bg='white')
    entryf2sig.place(x=694, y=424, width=200, height=27)
    lableTab_f2sig = Label(master=interface, bg="yellow", text="Tab. 4.4.3")
    lableTab_f2sig.place(x=903, y=424, width=150, height=27)
    entryf2sig.insert(0, 0.74)
    # fIItau
    lablef2tau = Label(master=interface, bg='white', text='fIItau:')
    lablef2tau.place(x=584, y=464, width=100, height=27)
    entryf2tau = Entry(master=interface, bg="white")
    entryf2tau.place(x=694, y=464, width=200, height=27)
    lableTab_f2tau = Label(master=interface, bg="yellow", text="Tab. 4.4.3")
    lableTab_f2tau.place(x=903, y=464, width=150, height=27)
    entryf2tau.insert(0, 0.83)
    # jF
    lablejF = Label(master=interface, bg='white', text='jF:')
    lablejF.place(x=584, y=504, width=100, height=27)
    entryjF = Entry(master=interface, bg='white')
    entryjF.place(x=694, y=504, width=200, height=27)
    lableTab_jF = Label(master=interface, bg="yellow", text="Tab. 4.5.1")
    lableTab_jF.place(x=903, y=504, width=150, height=27)
    entryjF.insert(0, 1.2)
    # DOU_Crit
    lableCrit = Label(master=interface, bg='pink', text='DOU crit')
    lableCrit.place(x=584, y=544, width=100, height=27)
    entryCrit = Entry(master=interface, bg='white')
    entryCrit.place(x=694, y=544, width=50, height=27)
    entryCrit.insert(0, 10)
    # button
    buttonsolve = Button(master=interface, bg='lightgreen', text='Start', command=lambda: call1(labelStat,
        output_set_name, float(entryCrit.get()), str(labelWeldy.get()), labelnorme, float(entryRm.get()),
        float(entryFsig.get()), float(entryFtau.get()), float(entryNsig.get()), float(entryKf.get()),
        float(entryRmN.get()), float(entryRsig.get()), float(entryR_Z.get()), float(entryK_V.get()),
        float(entryK_S.get()), float(entryK_Nle.get()), float(entryA_m.get()), float(entryBm.get()),
        float(entryNreq.get()), float(entryN_Dsig.get()), float(entryN_D2sig.get()), float(entryKsig.get()),
        float(entryK2sig.get()), float(entryN_Dtau.get()), float(entryN_D2tau.get()), float(entryKtau.get()),
        float(entryK2tau.get()), float(entryf2sig.get()), float(entryf2tau.get()), float(entryjF.get()),
        int(entryUnit2.get()), entryComp, interface))
    buttonsolve.place(x=903, y=624, width=150, height=27)
    # status
    lableStatus = Label(master=interface, bg='lightgreen', text='Status:')
    lableStatus.place(x=54, y=624, width=100, height=27)
    labelStat = Label(master=interface, bg='white', text="")
    labelStat.place(x=164, y=624, width=730, height=27)
    # weld
    labelWeld = Label(master=interface, bg='pink', text='Weld:')
    labelWeld.place(x=54, y=544, width=100, height=27)
    labelWeldy = Entry(master=interface, bg='white', text="")
    labelWeldy.place(x=164, y=544, width=50, height=27)
    labelWeldy.insert(0, "Yes")
    interface.mainloop()


def interface_DVS(output_set_name, unit, norm):


    def call(entryS1, entryComp, entryCrit, interface2):
        entryS1 = float(entryS1.get())
        entryCrit = float(entryCrit.get())


        labelWeldy = "YES"
        entryUnit = unit
        labelnorme = norm.upper()
        entryRm = 100
        entryFsig = 100
        entryFtau = 100
        entryNsig = 100
        entryKf = 100
        entryRmN = 100
        entryRsig = 100
        entryR_Z = 100
        entryK_V = 100
        entryK_S = 100
        entryK_Nle = 100
        entryA_m = 100
        entryBm = 100
        entryNreq = 100
        entryN_Dsig = 100
        entryN_D2sig = 100
        entryKsig = 100
        entryK2sig = 100
        entryN_Dtau = 100
        entryN_D2tau = 100
        entryKtau = 100
        entryK2tau = 100
        entryf2sig = 100
        entryf2tau = 100
        entryjF = 100
        entryUnit2 = "h"
        print("frog")
        buttonSolve(labelStat, output_set_name, entryCrit, labelWeldy, entryUnit, labelnorme, entryRm, entryFsig, entryFtau,
        entryNsig, entryKf, entryRmN, entryRsig, entryR_Z, entryK_V, entryK_S, entryK_Nle, entryA_m, entryBm,
        entryNreq, entryN_Dsig, entryN_D2sig, entryKsig, entryK2sig, entryN_Dtau, entryN_D2tau, entryKtau,
        entryK2tau, entryf2sig, entryf2tau, entryjF, entryUnit2, entryS1, entryComp, interface2)

    # interface DVS
    interface2 = Tk("DVS")
    interface2.title('Ingenis Auswertung')
    interface2.geometry('670x150')

    # DOU_Crit
    lableCrit = Label(master=interface2, bg='pink', text='DOU crit')
    lableCrit.place(x=54, y=40, width=100, height=27)
    entryCrit = Entry(master=interface2, bg='white')
    entryCrit.place(x=164, y=40, width=50, height=27)
    entryCrit.insert(0, 1)
    # status
    lableStatus = Label(master=interface2, bg='lightgreen', text='Status:')
    lableStatus.place(x=54, y=80, width=100, height=27)
    labelStat = Label(master=interface2, bg='white', text="")
    labelStat.place(x=164, y=80, width=300, height=27)
    # Sicherheitsfaktor
    lableS1 = Label(master=interface2, bg='pink', text='S1')
    lableS1.place(x=224, y=40, width=100, height=27)
    entryS1 = Entry(master=interface2, bg='white')
    entryS1.place(x=334, y=40, width=50, height=27)
    entryS1.insert(0, 1.15)

    # comparison stat
    entryComp = Label(master=interface2, bg='white', text="")
    entryComp.place(x=474, y=40, width=140, height=27)
    # button
    buttonsolve1 = Button(master=interface2, bg='lightgreen', text='Start', command=lambda: call(entryS1, entryComp,
                                                                                                 entryCrit, interface2))

    buttonsolve1.place(x=474, y=80, width=140, height=27)

    interface2.mainloop()

def interfaces():
    norm = str(labelnorme.get())
    output_set_name = str(labelOutpute.get())
    unit = str(entryunit.get()).upper()

    print(norm)
    interface1.destroy()

    if norm.upper() == "DVS":
        interface_DVS(output_set_name, unit, norm)
    elif norm.upper() == "FKM":
        interface_FKM(output_set_name, unit, norm)


global labelnorme
interface1 = Tk("Screenname")
interface1.title('Ingenis Auswertung')
interface1.geometry('460x190')
# output set name
labelOutput = Label(master=interface1, bg='pink', text='Output set name:')
labelOutput.place(x=54, y=40, width=140, height=27)
labelOutpute = Entry(master=interface1, bg='white', text="")
labelOutpute.place(x=204, y=40, width=200, height=27)
# norm
labelnorm = Label(master=interface1, bg='pink', text='Norm:')
labelnorm.place(x=54, y=80, width=140, height=27)
labelnorme = Entry(master=interface1, bg='white', text="")
labelnorme.place(x=204, y=80, width=50, height=27)
# labelnorme.insert(0, "DVS")
labelunit = Label(master=interface1, bg='pink', text='El. Type:')
labelunit.place(x=54, y=120, width=140, height=27)
entryunit = Entry(master=interface1, bg='white')
entryunit.place(x=204, y=120, width=50, height=27)
# button next
buttonnext = Button(master=interface1, bg='lightgreen', text='next', command=interfaces)
buttonnext.place(x=264, y=120, width=140, height=27)
print("hallo")
interface1.mainloop()
