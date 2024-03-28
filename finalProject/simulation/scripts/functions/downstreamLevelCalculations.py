# -----------------------------------------------------------------------------

# calculate resulting water levels at various locations along the st. lawrence
# river.

# -----------------------------------------------------------------------------

import pandas as pd
import numpy as np

data = pd.read_csv("/Users/kylasemmendinger/Box/Plan_2014/svm/hydro_data.csv")
data = data.dropna().astype("float64")
# df = data.loc[:, ['Sim', 'QM', 'Month', 'Year', 'ontLevel', 'ontFlow']]

for i in range(data.shape[0]):

    release = data.loc[i, "ontFlow"]
    ontarioLevel = data.loc[i, "ontLevel"]
    kingstonLevel = ontarioLevel - 0.03
    difLev = kingstonLevel - 62.40

    ogdensburgLevel = kingstonLevel - data.loc[i, "ogdensburgR"] * pow(
        release / (6.328 * pow(difLev, 2.0925)), (1 / 0.4103)
    )
    cardinalLevel = kingstonLevel - data.loc[i, "cardinalR"] * pow(
        release / (1.94908 * pow(difLev, 2.3981)), (1 / 0.4169)
    )
    iroquoishwLevel = kingstonLevel - data.loc[i, "iroquoishwR"] * pow(
        release / (2.36495 * pow(difLev, 2.2886)), (1 / 0.4158)
    )
    iroquoistwLevel = kingstonLevel - data.loc[i, "iroquoistwR"] * pow(
        release / (2.42291 * pow(difLev, 2.2721)), (1 / 0.4118)
    )

    alexbayLev = kingstonLev - 0.39 * (kingstonLev - odgensburgLev)

    iroquoishwLev = kingstonLev - (
        r["iroquoishwR"] * (ontFlow / (24.2291 * (difLev ** 2.2721))) ** (1 / 0.4118)
    )
    morrisburgLev = kingstonLev - (
        r["morrisburgR"] * (ontFlow / (23.9537 * (difLev ** 2.2450))) ** (1 / 0.3999)
    )
    longsaultLev = kingstonLev - (
        r["lsdamR"] * (ontFlow / (22.9896 * (difLev ** 2.2381))) ** (1 / 0.3870)
    )
    saunderhwLev = kingstonLev - (
        r["saundershwR"] * (ontFlow / (21.603 * (difLev ** 2.2586))) ** (1 / 0.3749)
    )
    saundersitwLev = 44.50 + 0.006338 * (r["saunderstwR"] * ontFlow) ** 0.7158
    cornwallLev = 45.00 + 0.0756 * (r["cornwallR"] * ontFlow) ** 0.364
    summerstownLev = 46.10 + 0.0109 * (r["summerstownR"] * ontFlow) ** 0.451
    ptclaireLev = 16.57 + ((r["ptclaireR"] * stlouisFlow / 604) ** 0.58)


def stlawLevels(
    ontLevel,  # final ontario level
    ontFlow,  # final ontario release
    r,  # roughness coefficients
    slonFlow,  # slon to calculate st. louis flow
):

    ontFlow = ontFlow * 10
    kingstonLev = ontLevel - 0.03
    difLev = kingstonLev - 62.40
    stlouisFlow = ontFlow + slonFlow

    odgensburgLev = kingstonLev - (
        r["ogdensburgR"] * (ontFlow / (63.280 * (difLev ** 2.0925))) ** (1 / 0.4103)
    )
    alexbayLev = kingstonLev - 0.39 * (kingstonLev - odgensburgLev)
    cardinalLev = kingstonLev - (
        r["cardinalR"] * (ontFlow / (19.4908 * (difLev ** 2.3981))) ** (1 / 0.4169)
    )
    iroquoishwLev = kingstonLev - (
        r["iroquoishwR"] * (ontFlow / (24.2291 * (difLev ** 2.2721))) ** (1 / 0.4118)
    )
    morrisburgLev = kingstonLev - (
        r["morrisburgR"] * (ontFlow / (23.9537 * (difLev ** 2.2450))) ** (1 / 0.3999)
    )
    longsaultLev = kingstonLev - (
        r["lsdamR"] * (ontFlow / (22.9896 * (difLev ** 2.2381))) ** (1 / 0.3870)
    )
    saunderhwLev = kingstonLev - (
        r["saundershwR"] * (ontFlow / (21.603 * (difLev ** 2.2586))) ** (1 / 0.3749)
    )
    saundersitwLev = 44.50 + 0.006338 * (r["saunderstwR"] * ontFlow) ** 0.7158
    cornwallLev = 45.00 + 0.0756 * (r["cornwallR"] * ontFlow) ** 0.364
    summerstownLev = 46.10 + 0.0109 * (r["summerstownR"] * ontFlow) ** 0.451
    ptclaireLev = 16.57 + ((r["ptclaireR"] * stlouisFlow / 604) ** 0.58)

    levels = {
        "kingstonLevel": kingstonLev,
        "odgensburgLevel": odgensburgLev,
        "alexbayLevel": alexbayLev,
        "cardinalLevel": cardinalLev,
        "iroquoishwLevel": iroquoishwLev,
        "morrisburgLevel": morrisburgLev,
        "longsaultLevel": longsaultLev,
        "saunderhwLevel": saunderhwLev,
        "saundersitwLevel": saundersitwLev,
        "cornwallLevel": cornwallLev,
        "summerstownLevel": summerstownLev,
        "stlouisFlow": stlouisFlow,
        "ptclaireLevel": ptclaireLev,
    }

    return levels
