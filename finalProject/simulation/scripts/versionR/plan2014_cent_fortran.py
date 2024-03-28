# import libraries
import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime

# args = sys.argv()
args = ["", "mac_loc", "historic", "full", "sq", "1", "0"]

if args[1] == "mac_loc":
    wd = "/Users/kylasemmendinger/Box/Plan_2014/plan_2014"
elif args[1] == "mac_ext":
    wd = "/Volumes/Seagate Backup Plus Drive/plan_2014"
elif args[1] == "linux":
    wd = "/home/kyla/Desktop"
elif args[1] == "hopper":
    wd = "/home/fs02/pmr82_0001/kts48/plan_2014"

# set working directory
os.chdir(wd)

ver = args[2]
season = args[3]
skill = args[4]
nseeds = int(args[5])
startcent = int(args[6])

# import plan 2014 functions
sys.path.insert(1, os.getcwd() + "/scripts/functions/")
import limits
from stlawLevels import stlawLevels

filelist = os.listdir(os.getcwd() + "/input/" + ver)

# for cent in range(startcent, len(filelist)):

#     for p in range(nseeds):

cent = 0
p = 0

print(filelist[cent] + " " + str(p + 1))

startTime = datetime.now()

# load input data
data = pd.read_table("input/" + ver + "/" + filelist[cent])

# load spin up data for first year in the century simulation
spinup = pd.read_table("input/spin_up/" + ver + "/" + filelist[cent])

# load short term forecast predictions (status quo)
sf = pd.read_table("input/short_forecast/" + ver + "/" + filelist[cent])

if ver == "historic":
    lf = pd.read_table(
        "input/long_forecast/" + ver + "/skill_" + skill + "_S" + str(p + 1) + ".txt"
    )
elif ver == "stochastic":
    centname = filelist[cent].split(".")[0]
    lf = pd.read_table(
        "input/long_forecast/"
        + ver
        + "/"
        + centname
        + "/skill_"
        + skill
        + "_S"
        + str(p + 1)
        + ".txt"
    )

# join input data, short forecast, and long forecast data
data = data.merge(sf, how="outer", on=["Sim", "Year", "Month", "QM"])
data = data.merge(lf, how="outer", on=["Sim", "QM"])

data.loc[:47, ["ontLevel", "ontFlow"]] = spinup

# set start iteration at 49 to allow for one year of spin up
s = 48

# 2970 cms-quarters is the conversion factor for converting flows to levels
conv = 2970

# -----------------------------------------------------------------------------
# plan 2014 simulation
# -----------------------------------------------------------------------------

sim_st = datetime.now()

for t in range(s, data.shape[0] - 48):
    # for t in range(s, 4176):

    # quarter month
    qm = data["QM"][t]

    # -------------------------------------------------------------------------
    # starting values for time step, t
    # -------------------------------------------------------------------------

    # ontario water level
    ontLevelStart = data["ontLevel"][t - 1]

    # kingston water level
    kingLevelStart = ontLevelStart - 0.03

    # average level of previous 48 quarter-months
    annavgLevel = np.mean(data["ontLevel"][(t - 48) : (t)])

    # moses-saunders release
    ontFlowPrev = data["ontFlow"][t - 1]

    # ice status
    iceIndPrev = data["iceInd"][t - 1]

    # -------------------------------------------------------------------------
    # short-term supply forecasts over next 4 quarter-months
    # -------------------------------------------------------------------------

    # ontario net total supply (ontario nbs + erie outflows)
    sfSupplyNTS = data.filter(like="ontNTS_QM").loc[t, :]
    nts = sfSupplyNTS[0] / 10

    # lac st. louis flows - lake ontario flows (ottawa river flows)
    sfSupplySLON = data.filter(like="slonFlow_QM").loc[t, :]

    # -------------------------------------------------------------------------
    # long-term supply forecasts
    # -------------------------------------------------------------------------

    # ontario basin supply
    lfSupply = data["forNTS"][t]
    lfInd = data["indicator"][t]
    lfCon = data["confidence"][t]

    # -------------------------------------------------------------------------
    # state indicators
    # -------------------------------------------------------------------------

    # ice status
    iceInd = data["iceInd"][t]

    # roughness coefficients
    r = data.loc[t, data.columns.str.endswith("R")]

    # true versus forecasted slon
    foreInd = 0
    if foreInd == 0:
        slonFlow = data["slonFlow_QM1"][t]
    elif foreInd == 1:
        slonFlow = data["stlouisontOut"][t]

    # true nts
    obsontNTS = data["ontNTS"][t]

    # flow, level, and flag if september levels are dangerously high
    if qm <= 32:

        # take the flow and level from the previous year
        qm32Flow = (
            data.loc[data["Year"] < data.loc[t, "Year"]]
            .loc[data["QM"] == 32]
            .iloc[0]["ontFlow"]
        )
        qm32Level = (
            data.loc[data["Year"] < data.loc[t, "Year"]]
            .loc[data["QM"] == 32]
            .iloc[0]["ontLevel"]
        )
        flowflag = 0

    elif qm > 32:

        # take the flow and level from the current year
        qm32Flow = (
            data.loc[data["Year"] == data.loc[t, "Year"]]
            .loc[data["QM"] == 32]
            .iloc[0]["ontFlow"]
        )
        qm32Level = (
            data.loc[data["Year"] == data.loc[t, "Year"]]
            .loc[data["QM"] == 32]
            .iloc[0]["ontLevel"]
        )

        if qm32Level > 74.8:
            flowflag = 1
        else:
            flowflag = 0

    # -------------------------------------------------------------------------
    # rule curve release regime
    # -------------------------------------------------------------------------

    # calculate rule curve release for each forecasted quarter-month (1 - 4)
    nforecasts = 4
    startLev = []
    startLev.append(ontLevelStart)
    endLev = []
    sfFlow = []
    sfpreprojFlow = []
    sfRegime = []

    for k in range(nforecasts):

        # function of levels and long-term forecast of supplies
        slope = 55.5823

        # set indicators
        ice = 0
        adj = 0.0014 * (2010 - 1985)
        epsolon = 0.0001

        # while loop and break variables
        flg = 1
        ct = 0
        lastflow = 0

        while flg == 1:

            # only exits loop once a convergence threshold (epsolon) is met or 10
            # iterations exceeded. adjust the preproject relationship by how much the
            # long-term supply forecast varies from average

            # pre-project flows
            preproj = slope * (startLev[k] - adj - 69.474) ** 1.5

            # above average supplies
            if lfSupply >= 7011:

                # set c1 coefficients based on how confident forecast is in wet
                if lfInd == 1 and lfCon == 3:
                    c1 = 260
                else:
                    c1 = 220

                # rule curve release
                flow = preproj + ((lfSupply - 7011) / (8552 - 7011)) ** 0.9 * c1

                # set rc flow regime
                if lfInd == 1 and lfCon == 3:
                    sy = "RC1+"
                else:
                    sy = "RC1"

            # below average supplies
            if lfSupply < 7011:

                # set c2 coefficient
                c2 = 60

                # rule curve release
                flow = preproj - ((7011 - lfSupply) / (7011 - 5717)) ** 1.0 * c2

                # set rc flow regime
                sy = "RC2"

            # adjust release for any ice
            release = round(flow - ice, 0)

            if abs(release - lastflow) <= epsolon:
                break

            # # calculate resulting water level
            # wl1 = startLev[k] + (sfSupplyNTS[k] / 10 - release) / conv
            # wl2 = wl1
            # wl1 = (startLev[k] + wl2) * 0.5
            # wl = round(wl1, 2)

            # stability check
            lastflow = release
            ct = ct + 1

            if ct == 10:
                break

        # try to keep ontario level up in dry periods
        if annavgLevel <= 74.6:

            # adjust release
            release = release - 20

            # set flow regime
            sy = sy + "-"

        sfFlow.append(release)
        sfpreprojFlow.append(preproj)
        sfRegime.append(sy)

        # compute water level change using forecasted supply and flow
        dif = round((sfSupplyNTS[k] / 10 - sfFlow[k]) / conv, 6)
        endLev.append(startLev[k] + dif)

        # update intial conditions
        if k < 3:
            startLev.append(endLev[k])

    # compute averaged quarter-monthly release
    ontFlow = round(sum(sfFlow) / nforecasts, 0)
    ontRegime = sfRegime[0]

    # -----------------------------------------------------------------------------
    # R+ Limit - QM 32 high level check
    # -----------------------------------------------------------------------------

    # from qm 32 september check comments in ECCC fortran code: if sep 1 lake
    # levels are dangerously high (above 75.0), begin adjusting rule curve flow
    # to target 74.8 by beginning of qm 47 and sustain through qm 48. reassess
    # each qm and modify the adjustment

    if qm >= 33 and flowflag == 1:

        if ontLevelStart > 74.80:

            if qm <= 46:
                flowadj = ((ontLevelStart - 74.80) * conv) / (46 - qm + 1)
            else:
                flowadj = ((ontLevelStart - 74.80) * conv) / (48 - qm + 1)

            # adjust rule curve flow
            ontFlow = ontFlow + flowadj

            # adjust rule curve flow regime
            ontRegime = "R+"

            # restrain flow to QM32 flow until after Labor Day for recreational boaters
            if qm == 33:
                ontFlow = min(ontFlow, qm32Flow)

            # this bit of code comes from the L limit to prevent unrealistically high flows
            if ontLevelStart <= 75.13:
                if ontFlow > (835 + 100 * (ontLevelStart - 74.70)):
                    ontFlow = 835 + 100 * (ontLevelStart - 74.70)
                    ontRegime = "L1"
            elif ontLevelStart <= 75.44:
                if ontFlow > (878 + 364.5 * (ontLevelStart - 75.13)):
                    ontFlow = 878 + 364.5 * (ontLevelStart - 75.13)
                    ontRegime = "L1"
            elif ontLevelStart <= 75.70:
                if ontFlow > 991:
                    ontFlow = 991
                    ontRegime = "L1"
            elif ontLevelStart <= 76.0:
                if ontFlow > 1070:
                    ontFlow = 1070
                    ontRegime = "L1"
            else:
                if ontFlow > 1150:
                    ontFlow = 1150
                    ontRegime = "L1"

            ontFlow = round(ontFlow, 0)

    # calculate resulting water level using forecasted supplies
    dif = round((nts - ontFlow) / conv, 6)
    ontLevel = ontLevelStart + dif
    # ontLevel = round(ontLevelStart + dif, 2)

    # -----------------------------------------------------------------------------
    # I Limit - ice forming limits
    # -----------------------------------------------------------------------------

    # maximum i-limit flow check. ice status of 0, 1, and 2 correspond to no ice,
    # stable ice formed, and unstable ice forming

    if iceInd == 2 or iceIndPrev == 2:
        iFlow = 623

    elif iceInd == 1 or (qm < 13 or qm > 47):

        # calculate release to keep long sault level above 71.8 m
        con1 = (kingLevelStart - 62.4) ** 2.2381
        con2 = ((kingLevelStart - 71.80) / r["lsdamR"]) ** 0.387
        iFlow = (22.9896 * con1 * con2) * 0.1
        iFlow = round(iFlow, 0)

        # this is in original fortran code, but was commented out in operation code
        if iceInd == 1:
            if iFlow > 943:
                iFlow = 943
        else:
            if iFlow > 991:
                iFlow = 991

    else:
        iFlow = 0

    # i-limit
    iLimFlow = iFlow
    iRegime = "I"

    # -----------------------------------------------------------------------------
    # L Limit - navigation and channel capacity limits
    # -----------------------------------------------------------------------------

    # maximum l-limit flow check - primarily based on level. applied during
    # the navigation season (qm 13 - qm 47) and during non-navigation season.
    # reference table b3 in compendium report

    lFlow = 0

    # navigation season
    if qm >= 13 and qm <= 47:

        lRegime = "LN"

        if ontLevel <= 74.22:
            lFlow = 595

        elif ontLevel <= 74.34:
            lFlow = 595 + 133.3 * (ontLevel - 74.22)

        elif ontLevel <= 74.54:
            lFlow = 611 + 910 * (ontLevel - 74.34)

        elif ontLevel <= 74.70:
            lFlow = 793 + 262.5 * (ontLevel - 74.54)

        elif ontLevel <= 75.13:
            lFlow = 835 + 100 * (ontLevel - 74.70)

        elif ontLevel <= 75.44:
            lFlow = 878 + 364.5 * (ontLevel - 75.13)

        elif ontLevel <= 75.70:
            lFlow = 991

        elif ontLevel <= 76:
            lFlow = 1020

        else:
            lFlow = 1070

    # non-navigation season
    else:
        lRegime = "LM"
        lFlow = 1150

    # channel capacity check
    lFlowCC = (747.2 * (ontLevel - 69.10) ** 1.47) / 10

    if lFlowCC < lFlow:
        lFlow = lFlowCC
        lRegime = "LC"

    # l-limit
    lLimFlow = round(lFlow, 0)
    lRegime = lRegime

    # -----------------------------------------------------------------------------
    # M Limit - low levels
    # -----------------------------------------------------------------------------

    # minimum m-limit flow check. minimum limit flows to balance low levels of
    # lake ontario and lac st. louis primarily for seaway navigation interests

    # # m-limit by quarter-month
    # qmLimFlow = np.hstack(
    #     [
    #         [595] * 4,
    #         [586] * 4,
    #         [578] * 4,
    #         [532] * 8,
    #         [538] * 4,
    #         [547] * 12,
    #         [561] * 8,
    #         [595] * 4,
    #     ]
    # )

    # mFlow = qmLimFlow[qm - 1]
    # slonFlow = slonFlow * 0.1

    # # stochastic version of M limit to prevent too low of flows
    # if version == "stochastic":
    #     if rcLevel < 74.20:
    #         mq = 770 - 2 * slonFlow

    #         if mq < mFlow:
    #             mFlow = round(mq, 0)

    # # historic version of M limit to prevent too low of flows
    # elif version == "historic":

    # compute crustal adjustment factor, fixed for year 2010
    # adj = 0.0014 * (2010 - 1985)
    # slope = 55.5823
    # mq = 0

    # this part borrowed from 58DD to prevent too low St. Louis levels
    if ontLevel > 74.20:
        mFlow = 680 - (slonFlow * 0.1)

    # elif ontLevel > 74.10 and ontLevel <= 74.20:
    # mq = 650 - slonFlow
    elif ontLevel > 74.00 and ontLevel <= 74.25:
        mFlow = 640 - (slonFlow * 0.1)

    # elif ontLevel > 74.00 and ontLevel <= 74.10:
    #     mFlow = 620 - slonFlow

    elif ontLevel > 73.60 and ontLevel <= 74.00:
        mFlow = 610 - (slonFlow * 0.1)

    else:
        mFlow1 = 577 - (slonFlow * 0.1)
        mFlow2 = slope * (ontLevel - adj - 69.474) ** 1.5
        mFlow = min(mFlow1, mFlow2)

    # m-limit
    mLimFlow = round(mFlow, 0)
    mRegime = "M"

    # -----------------------------------------------------------------------------
    # J Limit - stability check
    # -----------------------------------------------------------------------------

    # difference between rc flow and last week's actual flow
    flowdif = abs(ontFlow - ontFlowPrev)

    # flow change bounds
    jdn = 70
    jup = 70

    # increase upper j-limit if high lake ontario level and no ice
    if ontLevel > 75.20 and iceInd == 0 and iceIndPrev < 2:
        jup = 142

    # if flow difference is positive, check if maxJ applies
    if ontFlow >= ontFlowPrev:

        # upper J limit applies
        if flowdif > jup:
            jlim = ontFlowPrev + jup
            jmaxup = jlim
            jmin = 0
            jFlow = jlim

            if jup == 70:
                jRegime = "J+"
            elif jup == 142:
                jRegime = "JJ"

        # no jlim is applied, flow is RC flow
        else:
            jFlow = ontFlow
            jmaxup = 9999
            jmin = 0
            jRegime = ontRegime

    # if the flow difference is negative, check if minJ applies
    else:

        # lower J limit applies
        if flowdif > jdn:
            jlim = ontFlowPrev - 70
            jmaxup = 9999
            jmin = jlim
            jFlow = jlim
            jRegime = "J-"

        # no jlim is applied, flow is RC flow
        else:
            jFlow = ontFlow
            jmaxup = 9999
            jmin = 0
            jRegime = ontRegime

    # j-limit
    jLimFlow = round(jFlow, 0)
    jRegime = jRegime

    # this is either the J-limit (if applied) or the RC flow and regime
    maxLimFlow = jLimFlow
    maxLimRegime = jRegime

    # get the smallest of the maximum limits (L and I)
    maxLim = -9999

    if lLimFlow != 0:
        if maxLim < 0:
            maxLim = lLimFlow
            maxRegime = lRegime

    if iLimFlow != 0:
        if maxLim < 0 or iLimFlow < maxLim:
            maxLim = iLimFlow
            maxRegime = iRegime

    # compare rc flow or j limit with maximum limits (RC or J with L and I)
    if maxLim > 0 and maxLimFlow > maxLim:
        maxLimFlow = maxLim
        maxLimRegime = maxRegime

    # get the biggest of the minimum limits (M)
    minLimFlow = mLimFlow
    minLimRegime = mRegime

    # compare the maximum and minimum limits
    if maxLimFlow > minLimFlow:
        limFlow = maxLimFlow
        limRegime = maxLimRegime

    # if the limit reaches to this point, then take the minimum limit
    else:

        # if the M limit is greater than the smaller of the I/L limit, take the M limit
        if minLimFlow > maxLim:
            if minLimRegime == mRegime:
                limFlow = minLimFlow
                limRegime = minLimRegime
            else:
                if maxLim > minLimFlow:
                    limFlow = maxLim
                    limRegime = maxRegime
                else:
                    limFlow = minLimFlow
                    limRegime = mRegime
        else:
            limFlow = minLimFlow
            limRegime = minLimRegime

    # -------------------------------------------------------------------------
    # ontario and st. lawrence level and flow calculations
    # -------------------------------------------------------------------------

    # update ontFlow and ontRegime post limit check
    ontFlow = limFlow
    ontRegime = limRegime

    # -------------------------------------------------------------------------
    # F limit - downstream flooding balance
    # -------------------------------------------------------------------------

    stlouisFlow = ontFlow * 10 + slonFlow

    # calculate pointe claire level
    ptclaireLevel = round(16.57 + ((r["ptclaireR"] * stlouisFlow / 604) ** 0.58), 2)

    # determine "action level" to apply at pointe claire
    if ontLevelStart < 75.3:
        actionlev = 22.10
        c1 = 11523.848
    elif ontLevelStart < 75.37:
        actionlev = 22.20
        c1 = 11885.486
    elif ontLevelStart < 75.50:
        actionlev = 22.33
        c1 = 12362.610
    elif ontLevelStart < 75.60:
        actionlev = 22.40
        c1 = 12622.784
    else:
        actionlev = 22.48
        c1 = 12922.906

    # estimate flow required to maintain pointe claire below action level
    if ptclaireLevel > actionlev:
        fFlow = round((c1 / r["ptclaireR"] - slonFlow) / 10, 0)

        if fFlow < ontFlow:
            ontFlow = fFlow
            ontRegime = "F"

    # calculate final ontario water level after limits applied, this is true level using observed nts
    dif = round(((obsontNTS / 10) - ontFlow) / conv, 6)
    # dif = round((nts - ontFlow) / conv, 6)
    ontLevel = round(ontLevelStart + dif, 2)

    # run function to calculate levels along the st. lawrence river
    stlaw = stlawLevels(ontLevel, ontFlow, r, slonFlow)

    # save ontario output for next iteration
    data.at[t, "ontLevel"] = ontLevel
    data.at[t, "ontFlow"] = ontFlow
    data.at[t, "flowRegime"] = ontRegime
    data.at[t, list(stlaw.keys())] = list(stlaw.values())

# if ver == "historic":
#     np.savetxt(
#         "output/" + ver + "/skill_" + skill + "_seeds/S" + str(p + 1) + ".txt"
#     )
# elif ver == "stochastic":
#     np.savetxt(
#         "output/"
#         + ver
#         + "/skill_"
#         + skill
#         + "_seeds/"
#         + centname
#         + "_S"
#         + str(p + 1)
#         + ".txt"
#     )

sim_et = datetime.now()
sim_ct = (sim_et - sim_st).total_seconds() / 60
print(sim_ct)

data.to_csv("validation/python_validation_sq2.txt", sep="\t", index=False)
