import numpy as np
import pandas as pd
from data import DOCTRINES, SHOCK_VECTORS, SCENARIO_ELASTICITY


def classify_regime(perf: float, dep: float) -> str:
    if perf >= 3.0 and dep < 3.0:
        return "Q1 Resilient"
    elif perf >= 3.0 and dep >= 3.0:
        return "Q2 Exposed"
    elif perf < 3.0 and dep < 3.0:
        return "Q3 Insulated Weak"
    return "Q4 Critical"


def run_simulation(
    countries, isos, regions, std_p, std_d, cons_p, cons_d, mult_dict,
    calib_mode, scenario, severity, doctrine, is_12m, is_nonlinear,
    mit_target, selected_country, mit_d4, mit_d5, mit_d2
):
    total_n = len(countries)
    base_p = (std_p if calib_mode == "Standard" else cons_p).copy()
    base_d = (std_d if calib_mode == "Standard" else cons_d).copy()

    m_rows = [countries.index(selected_country)] if mit_target == "Focus" else list(range(total_n))
    for r_i in m_rows:
        base_d[r_i, 3] = max(1.0, base_d[r_i, 3] - mit_d4)
        base_d[r_i, 4] = max(1.0, base_d[r_i, 4] - mit_d5)
        base_d[r_i, 1] = max(1.0, base_d[r_i, 1] - mit_d2)

    weights = DOCTRINES[doctrine]
    mults = np.array(mult_dict[scenario])[:, None]
    d_perf, d_dep = SHOCK_VECTORS[scenario]

    if is_12m:
        eta_m = SCENARIO_ELASTICITY.get(scenario, 0.25)
        adapt_score = 0.35 * base_p[:, 0] + 0.25 * base_p[:, 1] + 0.20 * base_p[:, 6] + 0.20 * base_p[:, 7]
        adapt_factor = 1.0 - eta_m * ((adapt_score - 1.0) / 4.0)
        eff_severity = (severity * adapt_factor)[:, None]
    else:
        adapt_factor = np.ones(total_n)
        eff_severity = np.full((total_n, 1), severity)

    post_p = np.clip(base_p - mults * d_perf * eff_severity, 1.0, 5.0)
    post_d = np.clip(base_d + mults * d_dep * eff_severity, 1.0, 5.0)

    for r_i in m_rows:
        post_d[r_i, 3] = max(1.0, post_d[r_i, 3] - mit_d4 * 0.5)
        post_d[r_i, 4] = max(1.0, post_d[r_i, 4] - mit_d5 * 0.5)
        post_d[r_i, 1] = max(1.0, post_d[r_i, 1] - mit_d2 * 0.5)

    spillover = 0.25 * np.maximum(0, post_d - 4.50).max(axis=1)
    post_d[:, 1] = np.clip(post_d[:, 1] + spillover, 1.0, 5.0)
    post_d[:, 5] = np.clip(post_d[:, 5] + spillover, 1.0, 5.0)

    if is_nonlinear:
        agg_base_p = np.prod(base_p ** weights, axis=1)
        agg_post_p = np.prod(post_p ** weights, axis=1)
        agg_base_d = np.sqrt((base_d ** 2) @ weights)
        agg_post_d = np.sqrt((post_d ** 2) @ weights)
    else:
        agg_base_p = base_p @ weights
        agg_post_p = post_p @ weights
        agg_base_d = base_d @ weights
        agg_post_d = post_d @ weights

    base_regimes = [classify_regime(p, d) for p, d in zip(agg_base_p, agg_base_d)]
    post_regimes = [classify_regime(p, d) for p, d in zip(agg_post_p, agg_post_d)]
    shift_labels = [
        f"{b.split()[0]} -> {p.split()[0]}" if b != p else "Stable"
        for b, p in zip(base_regimes, post_regimes)
    ]

    df = pd.DataFrame({
        "Country": countries,
        "ISO": isos,
        "Region": regions,
        "Base_Perf": np.round(agg_base_p, 2),
        "Base_Dep": np.round(agg_base_d, 2),
        "Base_Gap": np.round(agg_base_p - agg_base_d, 2),
        "Base_Regime": base_regimes,
        "Alerts_Base": (base_d >= 4.0).sum(axis=1),
        "Post_Perf": np.round(agg_post_p, 2),
        "Post_Dep": np.round(agg_post_d, 2),
        "Post_Gap": np.round(agg_post_p - agg_post_d, 2),
        "Shift": np.round((agg_post_p - agg_post_d) - (agg_base_p - agg_base_d), 2),
        "Post_Regime": post_regimes,
        "Regime_Shift": shift_labels,
        "Alerts_Post": (post_d >= 4.0).sum(axis=1)
    }).sort_values(by="Post_Gap", ascending=False).reset_index(drop=True)
    df.insert(0, "Rank", range(1, total_n + 1))

    return df, base_p, base_d, post_p, post_d, adapt_factor, eff_severity
