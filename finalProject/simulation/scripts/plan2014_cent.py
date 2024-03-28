# import libraries
import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime

# args = sys.argv
args = ["", "mac_loc", "historic", "full", "0.1", "100", "0"]

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

if season == "full":
    exp = "_full"
elif season != "full":
    exp = "_" + season

os.makedirs("output/" + ver + "/skill_" + skill + "_seeds" + exp, exist_ok=True)

# import plan 2014 functions
sys.path.insert(1, os.getcwd() + "/scripts/functions/")
import limits
from stlawLevels import stlawLevels

filelist = os.listdir(os.getcwd() + "/input/" + ver)

for cent in range(startcent, len(filelist)):

    for p in range(nseeds):

        print(filelist[cent] + " " + str(p))

        startTime = datetime.now()

        # load input data
        data = pd.read_table("input/" + ver + "/" + filelist[cent])

        # load spin up data for first year in the century simulation
        spinup = pd.read_table("input/spin_up/" + ver + "/" + filelist[cent])

        # load short term forecast predictions (status quo)
        sf = pd.read_table("input/short_forecast/" + ver + "/" + filelist[cent])

        if ver == "historic":
            lf = pd.read_table(
                "input/long_forecast/"
                + ver
                + "/skill_"
                + skill
                + exp
                + "_S"
                + str(p + 1)
                + ".txt"
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
                + exp
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

                    # calculate resulting water level
                    wl1 = startLev[k] + (sfSupplyNTS[k] / 10 - release) / conv
                    wl2 = wl1
                    wl1 = (startLev[k] + wl2) * 0.5
                    wl = round(wl1, 2)

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
                dif1 = round((sfSupplyNTS[k] / 10 - sfFlow[k]) / conv, 6)
                endLev.append(startLev[k] + dif1)

                # update intial conditions
                if k < 3:
                    startLev.append(endLev[k])

            # compute averaged quarter-monthly release
            ontFlow = round(sum(sfFlow) / nforecasts, 0)
            dif1 = round((sfSupplyNTS[0] / 10 - ontFlow) / conv, 6)
            # ontLevel = ontLevelStart + dif1
            ontLevel = round(ontLevelStart + dif1, 2)
            ontRegime = sfRegime[0]

            # -----------------------------------------------------------------------------
            # limit check
            # -----------------------------------------------------------------------------

            # qm 32 - high level check
            ontLevel, ontFlow, ontRegime = limits.limitQM32(
                qm=qm,
                nts=sfSupplyNTS[0],
                startLevel=ontLevelStart,
                rcLevel=ontLevel,
                rcFlow=ontFlow,
                rcRegime=ontRegime,
                qm32Flow=qm32Flow,
                flowflag=flowflag,
            )

            # i-limit
            iLimFlow = limits.limitMaxI(
                qm=qm,
                iceInd=iceInd,
                iceIndPrev=iceIndPrev,
                rcLevel=ontLevel,
                kingLevel=kingLevelStart,
                longsaultR=r["lsdamR"],
            )
            iRegime = "I"

            # l-limit
            lLimFlow, lRegime = limits.limitMaxL(qm=qm, rcLevel=ontLevel)

            # m-limit
            mLimFlow = limits.limitMinM(
                qm=qm, rcLevel=ontLevel, slonFlow=slonFlow, version=ver
            )
            mRegime = "M"

            # j-limit
            jLimFlow, jRegime = limits.limitMinMaxJ(
                rcFlow=ontFlow,
                rcLevel=ontLevel,
                rcRegime=ontRegime,
                ontFlowPrev=ontFlowPrev,
                iceInd=iceInd,
                iceIndPrev=iceIndPrev,
            )

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

            # run F limit
            ontFlow, ontRegime = limits.limitMaxLevF(
                startLevel=ontLevelStart,
                ontFlow=ontFlow,
                ontRegime=ontRegime,
                slonFlow=slonFlow,
                ptclaireR=r["ptclaireR"],
            )

            # calculate final ontario water level after limits applied, this is true level using observed nts
            dif2 = round(((obsontNTS / 10) - ontFlow) / conv, 6)
            ontLevel = round(ontLevelStart + dif2, 2)

            # run function to calculate levels along the st. lawrence river
            stlaw = stlawLevels(ontLevel, ontFlow, r, slonFlow)

            # save ontario output for next iteration
            data.at[t, "ontLevel"] = ontLevel
            data.at[t, "ontFlow"] = ontFlow
            data.at[t, "flowRegime"] = ontRegime
            data.at[t, list(stlaw.keys())] = list(stlaw.values())

        if ver == "historic":
            data.to_csv(
                "output/"
                + ver
                + "/skill_"
                + skill
                + "_seeds"
                + exp
                + "/S"
                + str(p + 1)
                + ".txt",
                sep="\t",
                index=False,
            )

        elif ver == "stochastic":
            data.to_csv(
                "output/"
                + ver
                + "/skill_"
                + skill
                + "_seeds/"
                + centname
                + "_S"
                + str(p + 1)
                + ".txt",
                sep="\t",
                index=False,
            )

        sim_et = datetime.now()
        sim_ct = (sim_et - sim_st).total_seconds() / 60
        print(sim_ct)
