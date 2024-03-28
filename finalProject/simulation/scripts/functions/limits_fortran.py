import pandas as pd
import numpy as np

# 2970 cms-quarters is the conversion factor for converting flows to levels
conv = 2970

# ---------------------------------------------------------------------------

# from qm 32 september check comments in ECCC fortran code: if sep 1 lake
# levels are dangerously high (above 75.0), begin adjusting rule curve flow
# to target 74.8 by beginning of qm 47 and sustain through qm 48. reassess
# each qm and modify the adjustment

# ---------------------------------------------------------------------------


def limitQM32(
    qm,  # quarter month
    nts,  # short forecasted nts for level calc
    startLevel,  # starting water level
    rcLevel,  # water level from rule curve flow
    rcFlow,  # rule curve flow
    rcRegime,  # rule curve flow regime
    qm32Flow,  # previous flow from qm 32
    flowflag,  # flow adjuster indicator (0 or 1)
):

    if qm >= 32 and flowflag == 1:

        if startLevel > 74.80:

            if qm <= 46:
                flowadj = ((startLevel - 74.80) * conv) / (46 - qm + 1)
            else:
                flowadj = ((startLevel - 74.80) * conv) / (48 - qm + 1)

            # adjust rule curve flow
            rcFlow = rcFlow + flowadj

            if qm == 33:
                rcFlow = min(rcFlow, qm32Flow)

            # adjust rule curve flow
            rcFlow = round(rcFlow, 0)

            # calculate resulting water level
            nts = nts / 10
            dif1 = round((nts - rcFlow) / conv, 6)
            rcLevel = round(startLevel + dif1, 2)

            # adjust rule curve flow regime
            rcRegime = "R+"

    return [rcLevel, rcFlow, rcRegime]


# -----------------------------------------------------------------------------

# maximum i-limit flow check. ice status of 0, 1, and 2 correspond to no ice,
# stable ice formed, and unstable ice forming

# -----------------------------------------------------------------------------


def limitMaxI(
    qm,  # quarter month
    iceInd,  # ice status at qm
    iceIndPrev,  # ice status at previous qm
    rcLevel,  # water level from rc regime
    kingLevel,  # previous kingston level
    longsaultR,  # roughness coefficient for long sault
):

    if iceInd == 2 or iceIndPrev == 2:
        iFlow = 623

    elif iceInd == 1 or (qm < 13 or qm > 47):

        # calculate release to keep long sault level above 71.8 m
        con1 = (kingLevel - 62.4) ** 2.2381
        con2 = ((kingLevel - 71.80) / longsaultR) ** 0.387
        qx = (22.9896 * con1 * con2) * 0.1
        iFlow = round(qx, 0)

        # this is in original fortran code, but was commented out in operation code
        if iceInd == 1:
            if iFlow > 943:
                iFlow = 943
        else:
            if iFlow > 991:
                iFlow = 991

    else:
        iFlow = 0


# -----------------------------------------------------------------------------

# maximum l-limit flow check - primarily based on level. applied during
# the navigation season (qm 13 - qm 47) and during non-navigation season.
# reference table b3 in compendium report

# -----------------------------------------------------------------------------


def limitMaxL(qm, rcLevel):  # quarter month  # water level from rc regime

    lFlow = 0

    # navigation season
    if qm >= 13 and qm <= 47:

        lRegime = "LN"

        if rcLevel <= 74.22:
            lFlow = 595

        elif rcLevel <= 74.34:
            lFlow = 595 + 133.3 * (rcLevel - 74.22)

        elif rcLevel <= 74.54:
            lFlow = 611 + 910 * (rcLevel - 74.34)

        elif rcLevel <= 74.70:
            lFlow = 793 + 262.5 * (rcLevel - 74.54)

        elif rcLevel <= 75.13:
            lFlow = 835 + 100 * (rcLevel - 74.70)

        elif rcLevel <= 75.44:
            lFlow = 878 + 364.5 * (rcLevel - 75.13)

        elif rcLevel <= 75.70:
            lFlow = 991

        elif rcLevel <= 76:
            lFlow = 1020

        else:
            lFlow = 1070

    # non-navigation season
    else:
        lRegime = "LM"
        lFlow = 1150

    # channel capacity check
    lFlow1 = lFlow
    lFlow2 = (747.2 * (rcLevel - 69.10) ** 1.47) / 10

    if lFlow2 < lFlow1:
        lFlow = lFlow2
        lRegime = "LC"

    lFlow = round(lFlow, 0)

    return [lFlow, lRegime]


# -----------------------------------------------------------------------------

# minimum m-limit flow check. minimum limit flows to balance low levels of
# lake ontario and lac st. louis primarily for seaway navigation interests

# -----------------------------------------------------------------------------


def limitMinM(
    qm,  # quarter month
    rcLevel,  # water level from rc regime
    slonFlow,  # lac st. louis - st. lawrence flows
    version,  # historic or stochastic
):

    # m-limit by quarter-month
    qmLimFlow = np.hstack(
        [
            [595] * 4,
            [586] * 4,
            [578] * 4,
            [532] * 8,
            [538] * 4,
            [547] * 12,
            [561] * 8,
            [595] * 4,
        ]
    )
    mFlow = qmLimFlow[qm - 1]
    slonFlow = slonFlow * 0.1

    # stochastic version of M limit to prevent too low of flows
    if version == "stochastic":
        if rcLevel < 74.20:
            mq = 770 - 2 * slonFlow

            if mq < mFlow:
                mFlow = round(mq, 0)

    # historic version of M limit to prevent too low of flows
    elif version == "historic":

        # compute crustal adjustment factor, fixed for year 2010
        adj = 0.0014 * (2010 - 1985)
        slope = 55.5823
        mq = 0

        # this part borrowed from 58DD to prevent too low St. Louis levels
        if rcLevel > 74.20:
            mq = 680 - slonFlow

        elif rcLevel > 74.10 and rcLevel <= 74.20:
            mq = 650 - slonFlow

        elif rcLevel > 74.00 and rcLevel <= 74.10:
            mq = 620 - slonFlow

        elif rcLevel > 73.60 and rcLevel <= 74.00:
            mq = 610 - slonFlow

        else:
            mq1 = 577 - slonFlow
            mq2 = slope * (rcLevel - adj - 69.474) ** 1.5
            mq = min(mq1, mq2)

        mFlow = round(mq, 0)

    return mFlow


# -----------------------------------------------------------------------------

# j-limit stability flow check. adjusts large changes between flow for coming
# week and actual flow last week. can be min or max limit.

# -----------------------------------------------------------------------------


def limitMinMaxJ(
    rcFlow,  # rule curve flow
    rcLevel,  # rule curve level
    ontFlowPrev,  # flow from previous qm
    iceInd,  # ice status at qm
    iceIndPrev,  # ice status at previous qm
    rcRegime,  # rule curve regime
):

    # difference between rc flow and last week's actual flow
    flowdif = abs(rcFlow - ontFlowPrev)

    # flow change bounds
    jdn = 70
    jup = 70

    # increase upper j-limit if high lake ontario level and no ice
    if rcLevel > 75.20 and iceInd == 0 and iceIndPrev < 2:
        jup = 142

    # if flow difference is positive, check if maxJ applies
    if rcFlow >= ontFlowPrev:

        # upper J limit applies
        if flowdif > jup:
            jlim = ontFlowPrev + jup
            jmaxup = jlim
            jmin = 0
            jFlow = jlim

            if jup == 70:
                jRegime = "J+"
            else:
                jRegime = "JJ"

        # no jlim is applied, flow is RC flow
        else:
            jFlow = rcFlow
            jmaxup = 9999
            jmin = 0
            jRegime = rcRegime

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
            jFlow = rcFlow
            jmaxup = 9999
            jmin = 0
            jRegime = rcRegime

    return [jFlow, jRegime]


# -----------------------------------------------------------------------------

# f-limit levels check. calculate lac st. louis flow at levels at pt. claire
# to determine if downstream flooding needs to be mitigated

# -----------------------------------------------------------------------------


def limitMaxLevF(
    startLevel,  # previous ontario level
    ontFlow,  # flow after I, L, J, and M limit check
    ontRegime,  # flow regime
    # foreInd, # forecast indicator
    slonFlow,  # lac st. louis - st. lawrence flows
    ptclaireR,  # roughness coefficient for pt. claire
):

    stlouisFlow = ontFlow * 10 + slonFlow

    # calculate pointe claire level
    ptclaireLevel = round(16.57 + ((ptclaireR * stlouisFlow / 604) ** 0.58), 2)

    # determine "action level" to apply at pointe claire
    if startLevel < 75.3:
        actionlev = 22.10
        c1 = 11523.848
    elif startLevel < 75.37:
        actionlev = 22.20
        c1 = 11885.486
    elif startLevel < 75.50:
        actionlev = 22.33
        c1 = 12362.610
    elif startLevel < 75.60:
        actionlev = 22.40
        c1 = 12622.784
    else:
        actionlev = 22.48
        c1 = 12922.906

    # estimate flow required to maintain pointe claire below action level
    if ptclaireLevel > actionlev:
        fFlow = round((c1 / ptclaireR - slonFlow) / 10, 0)

        if fFlow < ontFlow:
            ontFlow = fFlow
            ontRegime = "F"

    return [ontFlow, ontRegime]
