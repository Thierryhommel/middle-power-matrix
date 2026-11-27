import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from data import (
    LANG_TEXT, BASE_COUNTRIES, BASE_ISO, BASE_REGIONS, DIMS, DIM_LABELS,
    STD_PERF, STD_DEP, CONS_PERF, CONS_DEP, MULTIPLIERS, DOCTRINES,
    INDICATORS_52, INDICATOR_SOURCES
)
from engine import run_simulation

st.set_page_config(page_title="Middle Power Matrix", page_icon="🌐", layout="wide")
st.markdown(
    "<style>#MainMenu {visibility: hidden;} header {visibility: hidden;} .stAppDeployButton {display: none;}</style>",
    unsafe_allow_html=True
)

# --- INITIALISATION DE L'ÉTAT DE SESSION ---
if "custom_active" not in st.session_state:
    st.session_state.custom_active = False
    st.session_state.custom_name = "Poland (Custom)"
    st.session_state.custom_iso = "POL"
    st.session_state.custom_region = "C. Europe"
    st.session_state.custom_std_p = np.full(9, 3.0)
    st.session_state.custom_std_d = np.full(9, 3.0)
    st.session_state.custom_cons_p = np.full(9, 2.8)
    st.session_state.custom_cons_d = np.full(9, 3.25)
    st.session_state.custom_mults = {k: 1.00 for k in MULTIPLIERS.keys()}

if "ind_editor_df" not in st.session_state:
    st.session_state.ind_editor_df = pd.DataFrame(
        INDICATORS_52,
        columns=["ID", "Dim", "Indicator", "Axis", "Weight", "Anchor_1", "Anchor_5", "Raw_Value"]
    )

# --- ASSEMBLAGE DU PANEL DE PAYS ---
countries, isos, regions = list(BASE_COUNTRIES), list(BASE_ISO), list(BASE_REGIONS)
std_p_mat, std_d_mat = STD_PERF.copy(), STD_DEP.copy()
cons_p_mat, cons_d_mat = CONS_PERF.copy(), CONS_DEP.copy()
mult_dict = {k: list(v) for k, v in MULTIPLIERS.items()}

if st.session_state.custom_active:
    countries.append(st.session_state.custom_name)
    isos.append(st.session_state.custom_iso)
    regions.append(st.session_state.custom_region)
    std_p_mat = np.vstack([std_p_mat, st.session_state.custom_std_p])
    std_d_mat = np.vstack([std_d_mat, st.session_state.custom_std_d])
    cons_p_mat = np.vstack([cons_p_mat, st.session_state.custom_cons_p])
    cons_d_mat = np.vstack([cons_d_mat, st.session_state.custom_cons_d])
    for k in mult_dict:
        mult_dict[k].append(st.session_state.custom_mults[k])

total_n = len(countries)

# --- SIDEBAR ÉPURÉE ---
with st.sidebar:
    lang_choice = st.radio("🌐 Language / Langue", ["EN", "FR"], horizontal=True, label_visibility="collapsed")
    T = LANG_TEXT[lang_choice]
    st.divider()

    st.subheader(T["sidebar_header"])
    scenario = st.selectbox(T["scenario_label"], list(mult_dict.keys()))
    severity = st.slider(T["severity_label"], 0.0, 2.0, 1.0, 0.25, format="%.2fx")
    selected_country = st.selectbox(
        T["country_label"],
        countries,
        index=total_n - 1 if st.session_state.custom_active else 0
    )

    st.divider()
    with st.expander(T["adv_model"], expanded=False):
        calib_mode = st.radio(T["calib_label"], ["Standard", "Conservative"], horizontal=True)
        doctrine = st.selectbox(T["doctrine_label"], list(DOCTRINES.keys()))
        horizon_opt = st.radio(T["horizon_label"], ["t=0", "t=12m"], horizontal=True)
        agg_opt = st.radio(T["agg_label"], ["Linear", "Non-Linear"], horizontal=True)

    with st.expander(T["adv_mitig"], expanded=False):
        mit_target = st.radio(T["mit_target"], ["Focus", "Global"], horizontal=True)
        mit_d4 = st.slider("⚡ Énergie (-Dep D4)", 0.0, 1.0, 0.0, 0.10, format="-%.2f")
        mit_d5 = st.slider("💻 Cloud/Tech (-Dep D5)", 0.0, 1.0, 0.0, 0.10, format="-%.2f")
        mit_d2 = st.slider("🏦 Fiscal (-Dep D2)", 0.0, 1.0, 0.0, 0.10, format="-%.2f")

is_12m = (horizon_opt == "t=12m")
is_nonlinear = (agg_opt == "Non-Linear")

# --- EXÉCUTION DU MOTEUR ---
df, base_p, base_d, post_p, post_d, adapt_factor, eff_severity = run_simulation(
    countries, isos, regions, std_p_mat, std_d_mat, cons_p_mat, cons_d_mat, mult_dict,
    calib_mode, scenario, severity, doctrine, is_12m, is_nonlinear,
    mit_target, selected_country, mit_d4, mit_d5, mit_d2
)

# --- EN-TÊTE & KPI COMPACTS ---
st.title(T["title"])
st.caption(T["subtitle"])

q1_pre = (df["Base_Regime"] == "Q1 Resilient").sum()
q1_post = (df["Post_Regime"] == "Q1 Resilient").sum()
q4_pre = (df["Base_Regime"] == "Q4 Critical").sum()
q4_post = (df["Post_Regime"] == "Q4 Critical").sum()
alerts_pre = df["Alerts_Base"].sum()
alerts_post = df["Alerts_Post"].sum()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric(T["kpi1"], f"{df['Base_Gap'].mean():+.2f}")
k2.metric(T["kpi2"], f"{df['Post_Gap'].mean():+.2f}", f"{df['Shift'].mean():+.2f}")
k3.metric(T["kpi3"], f"{q1_post}/{total_n}", f"{q1_post - q1_pre:+d}")
k4.metric(T["kpi4"], f"{q4_post}/{total_n}", f"{q4_post - q4_pre:+d}", delta_color="inverse")
k5.metric(T["kpi5"], f"{alerts_post}/{total_n * 9}", f"{alerts_post - alerts_pre:+d}", delta_color="inverse")

# --- SYNTHÈSE NARRATIVE REPLIABLE ---
with st.expander(T["summary_exp"], expanded=False):
    c_sum1, c_sum2 = st.columns(2)
    shifted_df = df[df["Regime_Shift"] != "Stable"]
    worst_row = df.sort_values("Shift").iloc[0]
    s_list = ", ".join([f"{r['Country']} ({r['Regime_Shift']})" for _, r in shifted_df.iterrows()]) or ("None" if lang_choice == "EN" else "Aucun")

    if lang_choice == "EN":
        c_sum1.info(
            f"**Panel ({scenario} @ {severity:.2f}x):** Mean margin **{df['Base_Gap'].mean():+.2f} → {df['Post_Gap'].mean():+.2f}** "
            f"({df['Shift'].mean():+.2f}). Quadrant shifts ({len(shifted_df)}): {s_list}. Sharpest drop: **{worst_row['Country']}** ({worst_row['Shift']:+.2f})."
        )
    else:
        c_sum1.info(
            f"**Panel ({scenario} @ {severity:.2f}x) :** Marge moyenne **{df['Base_Gap'].mean():+.2f} → {df['Post_Gap'].mean():+.2f}** "
            f"({df['Shift'].mean():+.2f}). Bascules ({len(shifted_df)}) : {s_list}. Plus forte baisse : **{worst_row['Country']}** ({worst_row['Shift']:+.2f})."
        )

    row_c = df[df["Country"] == selected_country].iloc[0]
    idx_c = countries.index(selected_country)
    d_shift = (post_p[idx_c] - post_d[idx_c]) - (base_p[idx_c] - base_d[idx_c])
    w_dim = DIM_LABELS[lang_choice][int(np.argmin(d_shift))]

    if lang_choice == "EN":
        c_sum2.success(
            f"**Focus {selected_country}:** Margin **{row_c['Base_Gap']:+.2f} → {row_c['Post_Gap']:+.2f}** (**{row_c['Shift']:+.2f}**). "
            f"Regime: **{row_c['Post_Regime']}**. Most exposed dimension: **{w_dim}**."
        )
    else:
        c_sum2.success(
            f"**Focus {selected_country} :** Marge **{row_c['Base_Gap']:+.2f} → {row_c['Post_Gap']:+.2f}** (**{row_c['Shift']:+.2f}**). "
            f"Régime : **{row_c['Post_Regime']}**. Dimension la plus exposée : **{w_dim}**."
        )

# --- ONGLETS ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(T["tabs"])

# TAB 1 : MATRICE STRATÉGIQUE SANS CHEVAUCHEMENT
with tab1:
    df["Plot_Label"] = df.apply(
        lambda r: r["Country"] if (r["Country"] == selected_country or r["Regime_Shift"] != "Stable" or severity == 0) else "",
        axis=1
    )
    fig = px.scatter(
        df, x="Post_Dep", y="Post_Perf", text="Plot_Label", hover_name="Country",
        hover_data={"Plot_Label": False, "Post_Gap": True, "Shift": True, "Regime_Shift": True},
        color="Post_Regime",
        color_discrete_map={
            "Q1 Resilient": "#16a34a",
            "Q2 Exposed": "#d97706",
            "Q3 Insulated Weak": "#2563eb",
            "Q4 Critical": "#dc2626"
        },
        range_x=[1.8, 5.1], range_y=[1.8, 4.6], height=540,
        title=f"{T['matrix_title']} — {scenario} ({severity:.2f}x)"
    )
    fig.add_shape(type="rect", x0=1.8, y0=3.0, x1=3.0, y1=4.6, fillcolor="rgba(22,163,74,0.06)", line_width=0, layer="below")
    fig.add_shape(type="rect", x0=3.0, y0=3.0, x1=5.1, y1=4.6, fillcolor="rgba(217,119,6,0.06)", line_width=0, layer="below")
    fig.add_shape(type="rect", x0=1.8, y0=1.8, x1=3.0, y1=3.0, fillcolor="rgba(37,99,235,0.06)", line_width=0, layer="below")
    fig.add_shape(type="rect", x0=3.0, y0=1.8, x1=5.1, y1=3.0, fillcolor="rgba(220,38,38,0.06)", line_width=0, layer="below")
    fig.add_annotation(x=1.85, y=4.52, text="<b>Q1 · RESILIENT</b>", showarrow=False, font=dict(size=11, color="#15803d"), xanchor="left")
    fig.add_annotation(x=5.05, y=4.52, text="<b>Q2 · EXPOSED</b>", showarrow=False, font=dict(size=11, color="#b45309"), xanchor="right")
    fig.add_annotation(x=1.85, y=1.88, text="<b>Q3 · INSULATED WEAK</b>", showarrow=False, font=dict(size=11, color="#1d4ed8"), xanchor="left")
    fig.add_annotation(x=5.05, y=1.88, text="<b>Q4 · CRITICAL</b>", showarrow=False, font=dict(size=11, color="#b91c1c"), xanchor="right")
    fig.add_hline(y=3.0, line_dash="dash", line_color="#94a3b8")
    fig.add_vline(x=3.0, line_dash="dash", line_color="#94a3b8")
    fig.update_traces(textposition="top center", marker=dict(size=12))
    st.plotly_chart(fig, use_container_width=True)

# TAB 2 : TABLEAU AVEC CODE COULEUR
with tab2:
    def color_regime(val):
        colors = {
            "Q1 Resilient": "background-color: #dcfce7; color: #166534; font-weight: bold;",
            "Q2 Exposed": "background-color: #fef3c7; color: #92400e;",
            "Q3 Insulated Weak": "background-color: #dbeafe; color: #1e40af;",
            "Q4 Critical": "background-color: #fee2e2; color: #991b1b; font-weight: bold;"
        }
        return colors.get(val, "")

    cols_show = ["Rank", "Country", "Region", "Post_Perf", "Post_Dep", "Post_Gap", "Shift", "Post_Regime", "Regime_Shift", "Alerts_Post"]
    styled_df = df[cols_show].style.map(color_regime, subset=["Post_Regime"]).format({
        "Post_Perf": "{:.2f}",
        "Post_Dep": "{:.2f}",
        "Post_Gap": "{:+.2f}",
        "Shift": "{:+.2f}"
    })
    st.dataframe(styled_df, use_container_width=True, hide_index=True, height=560)
    st.download_button(
        T["export_csv"],
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=f"MPM_{calib_mode}.csv",
        mime="text/csv"
    )

# TAB 3 : RADAR SIMPLIFIÉ
with tab3:
    idx = countries.index(selected_country)
    weights = DOCTRINES[doctrine]
    c_top1, c_top2 = st.columns([1.2, 1])
    radar_mode = c_top1.radio(T["radar_mode"], T["radar_opts"], horizontal=True)
    comp_country = c_top2.selectbox(T["comp_label"], [T["comp_none"]] + [c for c in countries if c != selected_country])
    has_comp = (comp_country != T["comp_none"])
    idx2 = countries.index(comp_country) if has_comp else None

    col_radar, col_table = st.columns([1.15, 1])
    with col_radar:
        labels = [f"{lbl} ({weights[i]*100:.0f}%)" for i, lbl in enumerate(DIM_LABELS[lang_choice])]
        theta = labels + [labels[0]]
        fig_radar = go.Figure()

        if radar_mode in [T["radar_opts"][1], T["radar_opts"][2]]:
            fig_radar.add_trace(go.Scatterpolar(
                r=list(base_p[idx]) + [base_p[idx][0]], theta=theta,
                name=f"{selected_country} Perf (Pre)", line=dict(color="#16a34a", width=1.5, dash="dash")
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=list(base_d[idx]) + [base_d[idx][0]], theta=theta,
                name=f"{selected_country} Dep (Pre)", line=dict(color="#dc2626", width=1.5, dash="dash")
            ))

        if radar_mode in [T["radar_opts"][0], T["radar_opts"][1]]:
            fig_radar.add_trace(go.Scatterpolar(
                r=list(post_p[idx]) + [post_p[idx][0]], theta=theta,
                name=f"{selected_country} Perf (Post)", line=dict(color="#15803d", width=3),
                fill="toself", fillcolor="rgba(21,128,61,0.12)"
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=list(post_d[idx]) + [post_d[idx][0]], theta=theta,
                name=f"{selected_country} Dep (Post)", line=dict(color="#b91c1c", width=3),
                fill="toself", fillcolor="rgba(185,28,28,0.12)"
            ))

        if has_comp:
            fig_radar.add_trace(go.Scatterpolar(
                r=list(post_p[idx2]) + [post_p[idx2][0]], theta=theta,
                name=f"{comp_country} Perf", line=dict(color="#2563eb", width=2.5, dash="dot")
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=list(post_d[idx2]) + [post_d[idx2][0]], theta=theta,
                name=f"{comp_country} Dep", line=dict(color="#d97706", width=2.5, dash="dot")
            ))

        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[1.0, 5.0])),
            height=460, margin=dict(l=40, r=40, t=30, b=40),
            legend=dict(orientation="h", y=-0.2)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_table:
        if has_comp:
            gap1 = post_p[idx] - post_d[idx]
            gap2 = post_p[idx2] - post_d[idx2]
            dim_df = pd.DataFrame({
                "Dimension": DIM_LABELS[lang_choice],
                selected_country: np.round(gap1, 2),
                comp_country: np.round(gap2, 2),
                "Diff": np.round(gap1 - gap2, 2)
            })
        else:
            dim_df = pd.DataFrame({
                "Dimension": DIM_LABELS[lang_choice],
                "Perf": np.round(post_p[idx], 2),
                "Dep": np.round(post_d[idx], 2),
                "Status": ["🚨 ALERT" if d >= 4.0 else "OK" for d in post_d[idx]]
            })
        st.dataframe(dim_df, use_container_width=True, hide_index=True, height=420)

# TAB 4 : NOUVEL ÉTAT PAR ÉTAPES (AVEC SAUVEGARDE PERSISTANTE DU FILTRE)
with tab4:
    st.subheader(T["custom_header"])
    st.markdown(f"**{T['custom_step1']}**")
    c1, c2, c3, c4, c5 = st.columns(5)
    new_name = c1.text_input("Name / Nom :", value=st.session_state.custom_name)
    new_iso = c2.text_input("ISO-3 :", value=st.session_state.custom_iso, max_chars=3).upper()
    new_region = c3.text_input("Region / Région :", value=st.session_state.custom_region)
    pen_perf = c4.number_input("Perf Haircut (-Δ) :", 0.0, 1.0, 0.20, 0.05)
    pen_dep = c5.number_input("Dep Premium (+Δ) :", 0.0, 1.0, 0.25, 0.05)

    st.markdown(f"**{T['custom_step2']}**")
    all_dims = sorted(st.session_state.ind_editor_df["Dim"].unique())
    dim_sel = st.multiselect("Filter Dimensions / Filtrer les dimensions :", all_dims, default=all_dims)

    subset_df = st.session_state.ind_editor_df[st.session_state.ind_editor_df["Dim"].isin(dim_sel)]
    edited_subset = st.data_editor(
        subset_df,
        use_container_width=True,
        hide_index=True,
        disabled=["ID", "Dim", "Indicator", "Axis", "Weight", "Anchor_1", "Anchor_5"],
        height=320,
        key="editor_widget"
    )
    st.session_state.ind_editor_df.update(edited_subset)
    full_edited = st.session_state.ind_editor_df.copy()

    norm_scores = np.clip(
        1.0 + 4.0 * (full_edited["Raw_Value"].values - full_edited["Anchor_1"].values) / (full_edited["Anchor_5"].values - full_edited["Anchor_1"].values),
        1.0, 5.0
    )
    full_edited["Score_1_5"] = np.round(norm_scores, 2)

    calc_std_p, calc_std_d = np.zeros(9), np.zeros(9)
    for d_i, d_code in enumerate(DIMS):
        sub_p = full_edited[(full_edited["Dim"] == d_code[:2]) & (full_edited["Axis"] == "Perf")]
        sub_d = full_edited[(full_edited["Dim"] == d_code[:2]) & (full_edited["Axis"] == "Dep")]
        calc_std_p[d_i] = np.average(sub_p["Score_1_5"], weights=sub_p["Weight"])
        calc_std_d[d_i] = np.average(sub_d["Score_1_5"], weights=sub_d["Weight"])

    st.markdown(f"**{T['custom_step3']}**")
    m_cols = st.columns(7)
    new_mults = {
        sc_key: m_cols[i].number_input(sc_key[:2], -1.0, 2.5, 1.00, 0.05, key=f"m_{i}")
        for i, sc_key in enumerate(MULTIPLIERS.keys())
    }

    b1, b2 = st.columns(2)
    if b1.button(T["btn_add"], type="primary"):
        st.session_state.custom_active = True
        st.session_state.custom_name = new_name
        st.session_state.custom_iso = new_iso
        st.session_state.custom_region = new_region
        st.session_state.custom_std_p = calc_std_p
        st.session_state.custom_std_d = calc_std_d
        st.session_state.custom_cons_p = np.clip(calc_std_p - pen_perf, 1.0, 5.0)
        st.session_state.custom_cons_d = np.clip(calc_std_d + pen_dep, 1.0, 5.0)
        st.session_state.custom_mults = new_mults
        st.rerun()

    if st.session_state.custom_active and b2.button(T["btn_rem"]):
        st.session_state.custom_active = False
        st.rerun()

# TAB 5 : CARTE MONDIALE
with tab5:
    st.subheader(T["map_header"])
    sim_state = st.radio("View / Affichage :", T["map_opts"], horizontal=True)
    regime_colors = {
        "Q1 Resilient": "#16a34a",
        "Q2 Exposed": "#d97706",
        "Q3 Insulated Weak": "#2563eb",
        "Q4 Critical": "#dc2626"
    }

    if sim_state == T["map_opts"][2]:
        fig_map = px.choropleth(
            df, locations="ISO", color="Regime_Shift", hover_name="Country",
            hover_data={"ISO": False, "Base_Regime": True, "Post_Regime": True, "Shift": True},
            color_discrete_map={
                "Stable": "#cbd5e1",
                "Q1 → Q2": "#f59e0b",
                "Q2 → Q4": "#dc2626",
                "Q1 → Q4": "#991b1b",
                "Q3 → Q4": "#ea580c"
            },
            projection="natural earth", height=520
        )
    else:
        col_r = "Post_Regime" if sim_state == T["map_opts"][0] else "Base_Regime"
        fig_map = px.choropleth(
            df, locations="ISO", color=col_r, hover_name="Country",
            hover_data={"ISO": False, "Post_Perf": True, "Post_Dep": True, "Post_Gap": True, "Shift": True},
            color_discrete_map=regime_colors,
            projection="natural earth", height=520
        )

    fig_map.update_geos(showcountries=True, countrycolor="#cbd5e1", showcoastlines=True, coastlinecolor="#94a3b8", fitbounds="locations")
    fig_map.update_layout(margin={"r": 0, "t": 10, "l": 0, "b": 0})
    st.plotly_chart(fig_map, use_container_width=True)

# TAB 6 : MÉTHODOLOGIE STRUCTURÉE
with tab6:
    if lang_choice == "EN":
        st.subheader("📖 Analytical Architecture (2026–2027)")
        st.markdown("""
        * **Q1 · Resilient Power ($P \ge 3.00, D < 3.00$):** High institutional/material capacity paired with low external chokepoint exposure.
        * **Q2 · Exposed Power ($P \ge 3.00, D \ge 3.00$):** Strong domestic capabilities offset by acute external dependencies.
        * **Q3 · Insulated Weak ($P < 3.00, D < 3.00$):** Limited global projection capacity, structurally insulated from external shocks.
        * **Q4 · Critical Vulnerability ($P < 3.00, D \ge 3.00$):** Severe structural fragility exposed to systemic compounding crises.
        """)
        with st.expander("📐 View Stress-Test Equations (Direct Shock, Spillover & Aggregation)"):
            st.markdown("""
            * **Shock Transmission:** $P'_{i,d} = \text{clip}(P_{i,d} - M_i \cdot \Delta P_{s,d} \cdot \alpha_{\text{eff}}, 1, 5)$ and $D'_{i,d} = \text{clip}(D_{i,d} + M_i \cdot \Delta D_{s,d} \cdot \alpha_{\text{eff}}, 1, 5)$.
            * **12-Month Adaptation (`t=12m`):** $\alpha_{\text{eff}} = \alpha \cdot [1 - \eta_s \cdot (\frac{P_{\text{adapt}} - 1}{4})]$, where $P_{\text{adapt}}$ aggregates `D1`, `D2`, `D7`, and `D8`.
            * **Spillover (`Dep > 4.50`):** Applies `+0.25 × max(0, max(D') - 4.50)` onto `D2` (Fiscal) and `D6` (Social).
            * **Non-Linear Aggregation:** Weighted Geometric Mean for $P$ and Quadratic Mean for $D$.
            """)
    else:
        st.subheader("📖 Architecture Analytique (2026–2027)")
        st.markdown("""
        * **Q1 · Puissance Résiliente ($P \ge 3.00, D < 3.00$) :** Capacités élevées combinées à une faible exposition aux goulets externes.
        * **Q2 · Puissance Exposée ($P \ge 3.00, D \ge 3.00$) :** Capacités internes solides mais vulnérables à des dépendances externes aiguës.
        * **Q3 · Puissance Faible Isolée ($P < 3.00, D < 3.00$) :** Capacité de projection limitée, faiblement exposée aux chocs mondiaux.
        * **Q4 · Vulnérabilité Critique ($P < 3.00, D \ge 3.00$) :** Fragilité structurelle majeure exposée aux crises cumulatives.
        """)
        with st.expander("📐 Voir les équations mathématiques (Stress-Test, Contagion & Agrégation)"):
            st.markdown("""
            * **Choc Direct :** $P'_{i,d} = \text{clip}(P_{i,d} - M_i \cdot \Delta P_{s,d} \cdot \alpha_{\text{eff}}, 1, 5)$ et $D'_{i,d} = \text{clip}(D_{i,d} + M_i \cdot \Delta D_{s,d} \cdot \alpha_{\text{eff}}, 1, 5)$.
            * **Boucle d'Adaptation (`t=12m`) :** $\alpha_{\text{eff}} = \alpha \cdot [1 - \eta_s \cdot (\frac{P_{\text{adapt}} - 1}{4})]$, où $P_{\text{adapt}}$ agrège `D1`, `D2`, `D7` et `D8`.
            * **Contagion (`Dep > 4.50`) :** Report de `+0.25 × max(0, max(D') - 4.50)` sur `D2` (Fiscal) et `D6` (Social).
            * **Agrégation Non-Linéaire :** Moyenne géométrique pondérée pour $P$ et moyenne quadratique pour $D$.
            """)

    st.divider()
    st.subheader("📚 52 Empirical Indicators & Sources" if lang_choice == "EN" else "📚 Référentiel des 52 Indicateurs & Sources")
    full_ind_df = pd.DataFrame(
        INDICATORS_52,
        columns=["ID", "Dim", "Indicator", "Axis", "Weight", "Anchor_1", "Anchor_5", "Mid_Anchor"]
    )
    full_ind_df["Source"] = full_ind_df["ID"].map(INDICATOR_SOURCES)
    full_ind_df["Weight"] = full_ind_df["Weight"].apply(lambda x: f"{x*100:.0f}%")

    col_f1, col_f2, col_f3 = st.columns([1.2, 1.0, 1.8])
    dim_filter = col_f1.multiselect("Dimension:", options=sorted(full_ind_df["Dim"].unique()), default=sorted(full_ind_df["Dim"].unique()))
    axis_filter = col_f2.multiselect("Axis / Axe:", options=["Perf", "Dep"], default=["Perf", "Dep"])
    search_q = col_f3.text_input("Search / Rechercher (ex. IMF, SIPRI, debt):")

    filtered_ind = full_ind_df[full_ind_df["Dim"].isin(dim_filter) & full_ind_df["Axis"].isin(axis_filter)]
    if search_q:
        search_blob = filtered_ind[["ID", "Indicator", "Source"]].astype(str).agg(" ".join, axis=1)
        filtered_ind = filtered_ind[search_blob.str.contains(search_q, case=False, na=False)]

    st.dataframe(
        filtered_ind[["ID", "Dim", "Axis", "Weight", "Indicator", "Anchor_1", "Mid_Anchor", "Anchor_5", "Source"]],
        use_container_width=True,
        hide_index=True,
        height=450
    )
    st.download_button(
        "📥 Export 52 Indicators (CSV)" if lang_choice == "EN" else "📥 Exporter les 52 Indicateurs (CSV)",
        data=filtered_ind.to_csv(index=False).encode("utf-8"),
        file_name="MPM_52_Indicators_and_Sources.csv",
        mime="text/csv"
    )
