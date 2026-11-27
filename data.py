import numpy as np

LANG_TEXT = {
    "EN": {
        "title": "🌐 Middle Power Matrix — Stress-Test Simulator",
        "subtitle": "Structural autonomy, critical bottlenecks (D1–D9), and systemic crisis trajectories (2026–2027).",
        "sidebar_header": "⚙️ Core Parameters",
        "scenario_label": "Crisis Scenario:",
        "severity_label": "Shock Severity:",
        "country_label": "Country Focus:",
        "adv_model": "🧠 Model & Calibration",
        "adv_mitig": "🛡️ Mitigation Policies",
        "calib_label": "Calibration:",
        "doctrine_label": "Weighting Doctrine:",
        "horizon_label": "Time Horizon:",
        "agg_label": "Aggregation:",
        "mit_target": "Target:",
        "kpi1": "Baseline Margin",
        "kpi2": "Post-Shock Margin",
        "kpi3": "Resilient (Q1)",
        "kpi4": "Critical (Q4)",
        "kpi5": "Alerts (Dep >= 4.0)",
        "summary_exp": "📝 Read Dynamic Impact Summary",
        "tabs": [
            "📊 Strategic Matrix",
            "📋 Ranking Table",
            "🔍 Country Radar",
            "➕ Custom State",
            "🗺️ World Map",
            "📖 Methodology"
        ],
        "matrix_title": "Post-Shock Strategic Positioning",
        "export_csv": "📥 Export CSV",
        "diag_header": "Dimensional Profile",
        "radar_mode": "Display:",
        "radar_opts": ["Post-Shock Only", "Overlay (Pre vs Post)", "Pre-Shock Only"],
        "comp_label": "⚔️ Compare with:",
        "comp_none": "None",
        "custom_header": "Integrate a Custom 17th State (52 Indicators)",
        "custom_step1": "1. Identity & Calibration Penalties",
        "custom_step2": "2. Edit 52 Empirical Indicators",
        "custom_step3": "3. Scenario Exposure Multipliers (S1–S7)",
        "btn_add": "🚀 Integrate State",
        "btn_rem": "🗑️ Remove Custom State",
        "map_header": "Geopolitical Regime Mapping",
        "map_opts": ["Post-Shock", "Pre-Shock", "Quadrant Shifts"],
    },
    "FR": {
        "title": "🌐 Middle Power Matrix — Simulateur de Stress-Test",
        "subtitle": "Autonomie structurelle, goulets d'étranglement (D1–D9) et trajectoires de crises (2026–2027).",
        "sidebar_header": "⚙️ Paramètres Principaux",
        "scenario_label": "Scénario de Crise :",
        "severity_label": "Sévérité du Choc :",
        "country_label": "Focus Pays :",
        "adv_model": "🧠 Modèle & Calibration",
        "adv_mitig": "🛡️ Politiques d'Atténuation",
        "calib_label": "Calibration :",
        "doctrine_label": "Doctrine de Pondération :",
        "horizon_label": "Horizon Temporel :",
        "agg_label": "Agrégation :",
        "mit_target": "Cible :",
        "kpi1": "Marge Pré-Choc",
        "kpi2": "Marge Post-Choc",
        "kpi3": "Résilients (Q1)",
        "kpi4": "Critiques (Q4)",
        "kpi5": "Alertes (Dep >= 4.0)",
        "summary_exp": "📝 Lire la synthèse narrative des changements",
        "tabs": [
            "📊 Matrice Stratégique",
            "📋 Classement",
            "🔍 Radar Pays",
            "➕ Nouvel État",
            "🗺️ Carte Mondiale",
            "📖 Méthodologie"
        ],
        "matrix_title": "Positionnement Stratégique Post-Choc",
        "export_csv": "📥 Exporter CSV",
        "diag_header": "Profil Dimensionnel",
        "radar_mode": "Affichage :",
        "radar_opts": ["Post-Choc Uniquement", "Superposition (Pré vs Post)", "Pré-Choc Uniquement"],
        "comp_label": "⚔️ Comparer avec :",
        "comp_none": "Aucun",
        "custom_header": "Intégrer un 17e État Personnalisé (52 Indicateurs)",
        "custom_step1": "1. Identité & Pénalités de Calibration",
        "custom_step2": "2. Édition des 52 Indicateurs Empiriques",
        "custom_step3": "3. Multiplicateurs d'Exposition aux Scénarios (S1–S7)",
        "btn_add": "🚀 Intégrer ce pays",
        "btn_rem": "🗑️ Retirer le pays",
        "map_header": "Cartographie des Régimes Géopolitiques",
        "map_opts": ["Post-Choc", "Pré-Choc", "Bascules de Quadrant"],
    }
}

BASE_COUNTRIES = [
    "France", "United Kingdom", "Canada", "Australia", "Germany", "Italy",
    "South Korea", "Japan", "Brazil", "Indonesia", "India", "Saudi Arabia",
    "Turkiye", "Morocco", "Mexico", "Pakistan"
]

BASE_ISO = [
    "FRA", "GBR", "CAN", "AUS", "DEU", "ITA",
    "KOR", "JPN", "BRA", "IDN", "IND", "SAU",
    "TUR", "MAR", "MEX", "PAK"
]

BASE_REGIONS = [
    "W. Europe", "W. Europe", "N. America", "Indo-Pacific", "C. Europe", "S. Europe",
    "E. Asia", "E. Asia", "S. America", "SE Asia", "S. Asia", "Middle East",
    "Eurasia", "N. Africa", "N. America", "S. Asia"
]

DIMS = ["D1_Gov", "D2_Fisc", "D3_Def", "D4_Ener", "D5_Tech", "D6_Soc", "D7_Infr", "D8_Dipl", "D9_Clim"]

DIM_LABELS = {
    "EN": [
        "D1 · Governance", "D2 · Fiscal", "D3 · Hard Power", "D4 · Energy",
        "D5 · Tech & Cyber", "D6 · Society", "D7 · Infra", "D8 · Diplomacy", "D9 · Climate"
    ],
    "FR": [
        "D1 · Gouvernance", "D2 · Fiscal", "D3 · Défense", "D4 · Énergie",
        "D5 · Tech & Cyber", "D6 · Société", "D7 · Infra", "D8 · Diplomatie", "D9 · Climat"
    ]
}

STD_PERF = np.array([
    [4.10, 3.25, 4.35, 3.90, 3.85, 3.70, 4.30, 4.45, 4.00],
    [4.05, 3.35, 4.25, 3.60, 3.95, 3.55, 4.15, 4.40, 3.85],
    [4.15, 3.65, 2.75, 4.45, 3.55, 3.85, 3.70, 3.90, 4.15],
    [4.25, 3.85, 3.25, 4.35, 3.30, 4.05, 3.70, 3.90, 3.80],
    [4.25, 3.85, 3.40, 2.95, 4.15, 3.75, 4.15, 4.20, 3.90],
    [3.65, 3.05, 3.85, 3.40, 3.70, 3.40, 4.05, 4.10, 3.75],
    [3.95, 3.85, 4.15, 2.35, 4.75, 3.30, 4.30, 3.60, 2.95],
    [4.05, 3.30, 3.85, 2.50, 4.35, 3.60, 4.45, 4.10, 3.15],
    [3.10, 3.05, 3.20, 4.25, 2.95, 3.00, 3.05, 3.75, 4.30],
    [3.15, 3.45, 2.95, 3.85, 2.75, 3.40, 3.05, 3.60, 3.10],
    [3.55, 3.40, 3.80, 2.75, 3.45, 3.20, 3.45, 3.85, 2.45],
    [3.35, 3.95, 3.20, 4.75, 2.85, 3.30, 3.80, 3.70, 2.15],
    [2.85, 2.75, 4.05, 2.55, 3.15, 2.95, 3.65, 3.95, 3.05],
    [3.15, 3.00, 2.95, 2.85, 2.65, 2.90, 3.30, 3.55, 2.50],
    [2.85, 3.30, 2.55, 3.15, 3.25, 3.15, 3.15, 3.30, 3.00],
    [2.45, 2.15, 3.25, 2.25, 2.25, 2.50, 2.35, 2.75, 2.15],
])

STD_DEP = np.array([
    [2.30, 3.85, 2.40, 2.65, 4.10, 3.05, 2.25, 2.15, 2.55],
    [2.25, 3.85, 2.55, 3.10, 4.05, 3.05, 2.35, 2.15, 2.90],
    [2.15, 3.45, 4.05, 2.10, 3.90, 2.85, 2.70, 2.55, 2.25],
    [2.10, 2.65, 3.90, 4.10, 4.15, 2.40, 2.95, 2.50, 2.75],
    [2.25, 2.55, 3.85, 4.25, 4.10, 2.95, 2.65, 2.35, 2.60],
    [2.85, 4.35, 2.75, 4.15, 3.95, 3.25, 2.65, 2.35, 3.15],
    [2.45, 2.65, 3.95, 4.65, 4.35, 3.55, 2.40, 3.15, 3.90],
    [2.25, 4.15, 3.80, 4.70, 3.70, 3.55, 2.35, 2.55, 4.25],
    [3.35, 3.85, 2.55, 2.40, 3.90, 3.60, 3.45, 2.50, 3.05],
    [3.25, 3.40, 3.30, 3.15, 3.90, 3.15, 3.55, 2.70, 3.60],
    [2.85, 3.65, 3.20, 4.15, 3.40, 3.35, 3.10, 2.80, 4.10],
    [3.20, 3.15, 4.20, 3.85, 4.15, 3.10, 2.95, 2.85, 4.45],
    [3.45, 4.35, 3.30, 4.30, 3.85, 3.80, 3.15, 3.40, 3.55],
    [3.10, 3.60, 3.50, 4.35, 3.95, 3.55, 3.15, 2.90, 4.30],
    [3.70, 3.60, 4.10, 3.65, 4.25, 3.55, 3.50, 3.45, 3.60],
    [4.15, 4.65, 3.85, 4.45, 4.30, 4.10, 4.05, 3.90, 4.55],
])

CONS_PERF = np.array([
    [3.75, 2.90, 4.20, 3.75, 3.65, 3.30, 4.15, 4.30, 3.85],
    [3.80, 3.05, 4.05, 3.45, 3.80, 3.25, 4.00, 4.25, 3.70],
    [3.95, 3.35, 2.60, 4.25, 3.35, 3.55, 3.50, 3.75, 3.95],
    [4.05, 3.60, 3.10, 4.15, 3.05, 3.80, 3.55, 3.75, 3.60],
    [3.95, 3.55, 3.15, 2.75, 3.85, 3.40, 3.85, 3.95, 3.70],
    [3.40, 2.75, 3.70, 3.25, 3.50, 3.10, 3.90, 3.95, 3.55],
    [3.70, 3.60, 4.00, 2.20, 4.55, 2.95, 4.15, 3.40, 2.75],
    [3.85, 2.95, 3.70, 2.35, 4.15, 3.35, 4.30, 3.95, 2.95],
    [2.85, 2.80, 3.05, 4.10, 2.75, 2.75, 2.85, 3.55, 4.15],
    [2.90, 3.15, 2.80, 3.65, 2.55, 3.15, 2.85, 3.45, 2.90],
    [3.30, 3.15, 3.65, 2.60, 3.30, 3.00, 3.30, 3.70, 2.35],
    [3.05, 3.65, 3.00, 4.55, 2.65, 2.95, 3.60, 3.50, 1.95],
    [2.50, 2.40, 3.85, 2.40, 2.95, 2.65, 3.45, 3.75, 2.85],
    [2.90, 2.75, 2.80, 2.70, 2.50, 2.65, 3.15, 3.40, 2.35],
    [2.60, 3.05, 2.40, 2.95, 3.05, 2.90, 2.95, 3.15, 2.85],
    [2.15, 1.90, 3.05, 2.05, 2.05, 2.20, 2.15, 2.55, 1.95],
])

CONS_DEP = np.array([
    [2.85, 4.35, 2.60, 2.85, 4.35, 3.60, 2.45, 2.35, 2.80],
    [2.65, 4.30, 2.80, 3.40, 4.35, 3.50, 2.55, 2.35, 3.15],
    [2.45, 4.00, 4.30, 2.35, 4.20, 3.25, 3.00, 2.80, 2.50],
    [2.30, 2.90, 4.15, 4.35, 4.40, 2.65, 3.15, 2.70, 3.00],
    [2.65, 3.05, 4.15, 4.50, 4.35, 3.45, 3.00, 2.65, 2.85],
    [3.15, 4.65, 2.95, 4.35, 4.20, 3.60, 2.85, 2.55, 3.45],
    [2.75, 2.95, 4.20, 4.85, 4.60, 4.05, 2.60, 3.40, 4.15],
    [2.45, 4.45, 4.10, 4.90, 4.00, 3.85, 2.55, 2.75, 4.50],
    [3.65, 4.15, 2.70, 2.60, 4.15, 3.90, 3.65, 2.70, 3.30],
    [3.55, 3.85, 3.50, 3.45, 4.20, 3.45, 3.80, 2.90, 4.05],
    [3.05, 4.00, 3.35, 4.40, 3.60, 3.55, 3.25, 2.95, 4.45],
    [3.55, 3.60, 4.45, 4.15, 4.40, 3.55, 3.25, 3.15, 4.75],
    [3.85, 4.65, 3.55, 4.55, 4.10, 4.15, 3.35, 3.65, 3.85],
    [3.35, 3.95, 3.70, 4.55, 4.20, 3.85, 3.35, 3.10, 4.60],
    [4.05, 3.90, 4.30, 3.95, 4.50, 3.85, 3.75, 3.65, 3.85],
    [4.45, 4.85, 4.10, 4.70, 4.55, 4.40, 4.30, 4.15, 4.80],
])

MULTIPLIERS = {
    "S1: Maritime Chokepoint Closure": [1.15, 1.10, -0.30, -0.30, 1.35, 1.25, 1.55, 1.50, -0.15, 0.95, 1.35, 1.65, 1.35, 1.35, 0.65, 1.40],
    "S2: Tech Decoupling & Chip Freeze": [1.10, 1.15, 1.05, 1.15, 1.40, 1.10, 1.75, 1.35, 0.95, 1.15, 1.10, 1.10, 1.15, 0.95, 1.25, 0.95],
    "S3: Sovereign Debt & Capital Flight": [1.35, 1.40, 1.30, 0.95, 1.05, 1.45, 1.05, 1.25, 1.40, 1.35, 1.25, 1.15, 1.45, 1.30, 1.30, 1.45],
    "S4: Bilateral Tariff Fragmentation": [1.15, 1.15, 1.55, 1.45, 1.55, 1.15, 1.40, 1.20, 1.15, 1.05, 1.05, 0.95, 1.15, 1.05, 1.60, 1.10],
    "S5: Compound Climate & CBAM": [0.95, 0.95, 0.75, 1.05, 0.90, 1.05, 1.05, 1.15, 1.35, 1.40, 1.50, 1.45, 1.25, 1.50, 1.15, 1.45],
    "S6: EU / Eurozone Collapse": [1.50, 1.20, 0.70, 0.65, 1.60, 1.55, 0.85, 0.80, 0.90, 0.80, 0.85, 0.85, 1.30, 1.40, 0.65, 1.00],
    "S7: Data Center Cyber-Catastrophe": [1.20, 1.50, 1.35, 1.30, 1.25, 1.20, 1.35, 1.25, 1.05, 1.10, 1.15, 1.25, 1.05, 1.05, 1.15, 1.15],
}

SHOCK_VECTORS = {
    "S1: Maritime Chokepoint Closure": (
        np.array([0.05, 0.15, 0.05, 0.35, 0.10, 0.10, 0.15, 0.05, 0.10]),
        np.array([0.05, 0.20, 0.05, 0.65, 0.15, 0.15, 0.20, 0.05, 0.15])
    ),
    "S2: Tech Decoupling & Chip Freeze": (
        np.array([0.05, 0.10, 0.10, 0.05, 0.45, 0.05, 0.10, 0.05, 0.00]),
        np.array([0.05, 0.15, 0.15, 0.10, 0.70, 0.05, 0.15, 0.10, 0.00])
    ),
    "S3: Sovereign Debt & Capital Flight": (
        np.array([0.10, 0.45, 0.05, 0.05, 0.05, 0.15, 0.10, 0.05, 0.05]),
        np.array([0.10, 0.70, 0.05, 0.05, 0.05, 0.25, 0.10, 0.05, 0.05])
    ),
    "S4: Bilateral Tariff Fragmentation": (
        np.array([0.05, 0.15, 0.05, 0.10, 0.30, 0.10, 0.10, 0.10, 0.05]),
        np.array([0.05, 0.20, 0.05, 0.15, 0.50, 0.15, 0.15, 0.15, 0.10])
    ),
    "S5: Compound Climate & CBAM": (
        np.array([0.05, 0.15, 0.00, 0.15, 0.05, 0.15, 0.10, 0.05, 0.45]),
        np.array([0.05, 0.20, 0.00, 0.20, 0.10, 0.20, 0.15, 0.05, 0.70])
    ),
    "S6: EU / Eurozone Collapse": (
        np.array([0.15, 0.40, 0.05, 0.10, 0.15, 0.15, 0.10, 0.20, 0.05]),
        np.array([0.20, 0.60, 0.05, 0.15, 0.20, 0.20, 0.15, 0.25, 0.05])
    ),
    "S7: Data Center Cyber-Catastrophe": (
        np.array([0.20, 0.25, 0.10, 0.10, 0.45, 0.10, 0.30, 0.05, 0.05]),
        np.array([0.25, 0.35, 0.15, 0.15, 0.75, 0.15, 0.40, 0.05, 0.05])
    ),
}

DOCTRINES = {
    "1. Balanced (Equal 1/9)": np.ones(9) / 9.0,
    "2. Realpolitik / Security": np.array([0.10, 0.08, 0.25, 0.22, 0.07, 0.05, 0.05, 0.05, 0.13]),
    "3. Geo-Economic / Supply": np.array([0.08, 0.22, 0.04, 0.10, 0.25, 0.04, 0.15, 0.08, 0.04]),
    "4. Sustainability / Ecology": np.array([0.10, 0.05, 0.02, 0.22, 0.04, 0.18, 0.08, 0.03, 0.28]),
}

SCENARIO_ELASTICITY = {
    "S1: Maritime Chokepoint Closure": 0.40,
    "S2: Tech Decoupling & Chip Freeze": 0.08,
    "S3: Sovereign Debt & Capital Flight": 0.35,
    "S4: Bilateral Tariff Fragmentation": 0.35,
    "S5: Compound Climate & CBAM": 0.25,
    "S6: EU / Eurozone Collapse": 0.25,
    "S7: Data Center Cyber-Catastrophe": 0.45,
}

INDICATORS_52 = [
    ("IND-01", "D1", "Regulatory Quality & Rule of Law (WGI/WJP)", "Perf", 0.20, 0.30, 0.90, 0.60),
    ("IND-02", "D1", "Tax-to-GDP & Revenue Mobilization (% GDP)", "Perf", 0.20, 10.0, 38.0, 22.0),
    ("IND-03", "D1", "Digital Public Infrastructure (UN EGDI)", "Perf", 0.15, 0.40, 0.95, 0.68),
    ("IND-04", "D1", "Bureaucratic & Crisis Execution [1-5]", "Perf", 0.15, 1.00, 5.00, 3.00),
    ("IND-05", "D1", "Parliamentary / Coalition Gridlock [1-5]", "Dep", 0.15, 1.00, 5.00, 3.00),
    ("IND-06", "D1", "Off-Balance-Sheet & SOE Contingent Risk (% GDP)", "Dep", 0.15, 5.00, 40.0, 18.0),
    ("IND-07", "D2", "FX Reserves Import Cover (Months)", "Perf", 0.20, 2.00, 14.0, 6.00),
    ("IND-08", "D2", "Primary Fiscal Balance (% GDP)", "Perf", 0.15, -5.0, 1.50, -1.5),
    ("IND-09", "D2", "Monetary Credibility & Central Bank Depth [1-5]", "Perf", 0.15, 1.00, 5.00, 3.00),
    ("IND-10", "D2", "Gross Public Debt-to-GDP Ratio (% GDP)", "Dep", 0.20, 35.0, 140.0, 75.0),
    ("IND-11", "D2", "Debt-Service-to-Revenue (% Revenue)", "Dep", 0.15, 5.00, 35.0, 15.0),
    ("IND-12", "D2", "Non-Resident Debt & Private FX Leverage (%)", "Dep", 0.15, 10.0, 50.0, 30.0),
    ("IND-13", "D3", "Defense Industrial Localization Ratio (%)", "Perf", 0.20, 15.0, 85.0, 50.0),
    ("IND-14", "D3", "Force Projection & Strategic Deterrence [1-5]", "Perf", 0.20, 1.00, 5.00, 3.00),
    ("IND-15", "D3", "Defense R&D & Spending (% GDP)", "Perf", 0.15, 0.50, 4.50, 2.00),
    ("IND-16", "D3", "External Nuclear / Security Umbrella Reliance [1-5]", "Dep", 0.20, 1.00, 5.00, 3.00),
    ("IND-17", "D3", "Foreign Tier-1 Weapons & C4ISR Import Share (%)", "Dep", 0.15, 10.0, 85.0, 45.0),
    ("IND-18", "D3", "Internal Security & Border Attrition Drag [1-5]", "Dep", 0.10, 1.00, 5.00, 3.00),
    ("IND-19", "D4", "Domestic Primary Energy & Low-Carbon Base (%)", "Perf", 0.20, 15.0, 100.0, 50.0),
    ("IND-20", "D4", "Upstream Critical Minerals & Swing Capacity [1-5]", "Perf", 0.15, 1.00, 5.00, 3.00),
    ("IND-21", "D4", "Strategic Petroleum & Gas Storage Buffer (Days)", "Perf", 0.15, 15.0, 120.0, 60.0),
    ("IND-22", "D4", "Net Hydrocarbon & Refined Fuel Import Share (%)", "Dep", 0.20, 0.00, 85.0, 40.0),
    ("IND-23", "D4", "Maritime Chokepoint Transit Concentration (%)", "Dep", 0.15, 5.00, 70.0, 30.0),
    ("IND-24", "D4", "Midstream Refining & Grid Cost Pass-Through [1-5]", "Dep", 0.15, 1.00, 5.00, 3.00),
    ("IND-25", "D5", "R&D Intensity (% GDP)", "Perf", 0.20, 0.50, 4.50, 2.00),
    ("IND-26", "D5", "Semiconductor Fab & Capital Goods Share [1-5]", "Perf", 0.15, 1.00, 5.00, 3.00),
    ("IND-27", "D5", "Sovereign Cloud & National Cyber Defense [1-5]", "Perf", 0.15, 1.00, 5.00, 3.00),
    ("IND-28", "D5", "Non-Domestic Hyperscale Cloud Concentration (%)", "Dep", 0.20, 20.0, 75.0, 50.0),
    ("IND-29", "D5", "East Asian Advanced Foundry & Tool Reliance (%)", "Dep", 0.15, 15.0, 85.0, 55.0),
    ("IND-30", "D5", "Export & Intermediate Input Concentration (% Top-1)", "Dep", 0.15, 15.0, 70.0, 35.0),
    ("IND-31", "D6", "Working-Age Demographic Momentum [1-5]", "Perf", 0.20, 1.00, 5.00, 3.00),
    ("IND-32", "D6", "Human Capital, STEM & Healthcare Resilience [1-5]", "Perf", 0.20, 1.00, 5.00, 3.00),
    ("IND-33", "D6", "Institutional Trust & Social Buffer [1-5]", "Perf", 0.20, 1.00, 5.00, 3.00),
    ("IND-34", "D6", "Household Debt-Service & Cost-of-Living (% Inc.)", "Dep", 0.20, 50.0, 160.0, 100.0),
    ("IND-35", "D6", "Youth Unemployment & Informal Labor (%)", "Dep", 0.20, 8.00, 30.0, 18.0),
    ("IND-36", "D7", "Port, Rail & Logistics Throughput (LPI 2.2 to 4.3)", "Perf", 0.25, 2.20, 4.30, 3.25),
    ("IND-37", "D7", "Grid Redundancy & Telecom Backbone [1-5]", "Perf", 0.25, 1.00, 5.00, 3.00),
    ("IND-38", "D7", "Subsea Cable & Maritime Corridor Chokepoints [1-5]", "Dep", 0.25, 1.00, 5.00, 3.00),
    ("IND-39", "D7", "Data Center Geographic & Grid Centralization (%)", "Dep", 0.25, 15.0, 75.0, 40.0),
    ("IND-40", "D8", "Global Diplomatic Network & G20/EU Seat [1-5]", "Perf", 0.20, 1.00, 5.00, 3.00),
    ("IND-41", "D8", "Multi-Alignment & Trade Bloc Diversification [1-5]", "Perf", 0.15, 1.00, 5.00, 3.00),
    ("IND-42", "D8", "Development Finance & Soft-Power Projection [1-5]", "Perf", 0.15, 1.00, 5.00, 3.00),
    ("IND-43", "D8", "Asymmetric Coercion & Sanctions Exposure [1-5]", "Dep", 0.20, 1.00, 5.00, 3.00),
    ("IND-44", "D8", "Alliance Entanglement & Treaty Overstretch [1-5]", "Dep", 0.15, 1.00, 5.00, 3.00),
    ("IND-45", "D8", "Regional Contagion & Neighbor Instability [1-5]", "Dep", 0.15, 1.00, 5.00, 3.00),
    ("IND-46", "D9", "Calorie-Based Food & Grain Self-Sufficiency (%)", "Perf", 0.20, 30.0, 120.0, 75.0),
    ("IND-47", "D9", "Renewable Freshwater Buffer (m3/cap/yr)", "Perf", 0.15, 500.0, 10000.0, 2500.0),
    ("IND-48", "D9", "Climate Adaptation & Low-Carbon Readiness [1-5]", "Perf", 0.15, 1.00, 5.00, 3.00),
    ("IND-49", "D9", "Staple Food & Fertilizer (NPK) Import Reliance (%)", "Dep", 0.15, 0.00, 70.0, 35.0),
    ("IND-50", "D9", "Drought, Monsoon & Hydro-Basin Volatility [1-5]", "Dep", 0.15, 1.00, 5.00, 3.00),
    ("IND-51", "D9", "Coastal Desalination & Heatwave Grid Fragility [1-5]", "Dep", 0.10, 1.00, 5.00, 3.00),
    ("IND-52", "D9", "EU CBAM & Carbon Tariff Export Exposure (%)", "Dep", 0.10, 2.00, 25.0, 10.0),
]

INDICATOR_SOURCES = {
    "IND-01": "World Bank — Worldwide Governance Indicators (WGI) & WJP Rule of Law",
    "IND-02": "IMF — Government Finance Statistics (GFS) & OECD Revenue Statistics",
    "IND-03": "UN (UNDESA) — E-Government Development Index (EGDI) & World Bank GTMI",
    "IND-04": "World Bank — WGI (Government Effectiveness) & OECD Government at a Glance",
    "IND-05": "Inter-Parliamentary Union (IPU) — Parline Global Data & Constitutional Records",
    "IND-06": "IMF — Fiscal Monitor & Article IV Consultation Reports",
    "IND-07": "IMF — International Financial Statistics (IFS) & National Central Banks",
    "IND-08": "IMF — World Economic Outlook (WEO) Database",
    "IND-09": "Bank for International Settlements (BIS) & IMF AREAER",
    "IND-10": "IMF — World Economic Outlook (WEO) & Eurostat (EU Member States)",
    "IND-11": "IMF — GFS, World Bank IDS & National Treasury Yield Curves",
    "IND-12": "BIS — Debt Securities Statistics & IMF Sovereign Debt Investor Base",
    "IND-13": "SIPRI — Arms Industry Database & National Ministries of Defense",
    "IND-14": "UN — Register of Conventional Arms (UNROCA) & IAEA Safeguards",
    "IND-15": "NATO — Defence Expenditure Reports, EDA & National Budgets",
    "IND-16": "UN — Treaty Series (UNTS) & Bilateral Mutual Defense Treaties",
    "IND-17": "SIPRI — Arms Transfers Database",
    "IND-18": "UNODC — Global Study on Homicide & Uppsala Conflict Data Program (UCDP)",
    "IND-19": "International Energy Agency (IEA) — World Energy Balances & IRENA",
    "IND-20": "US Geological Survey (USGS) — Mineral Commodity Summaries & OPEC",
    "IND-21": "IEA — Oil Stocks of IEA Countries & Gas Infrastructure Europe (GIE)",
    "IND-22": "IEA — Energy Statistics Data Browser & UN Comtrade",
    "IND-23": "US Energy Information Administration (EIA) — Chokepoints & UNCTAD",
    "IND-24": "IEA — Energy Prices & Eurostat Electricity Price Statistics",
    "IND-25": "UNESCO Institute for Statistics (UIS), OECD (MSTI) & WIPO",
    "IND-26": "UN Comtrade (HS 8541/8542/8486) & OECD TiVA Database",
    "IND-27": "International Telecommunication Union (ITU) — Global Cybersecurity Index",
    "IND-28": "National Competition Authorities (Ofcom, ADLC) & DORA/CTP Regulators",
    "IND-29": "UN Comtrade — Bilateral Trade Flows & OECD Trade in Value Added (TiVA)",
    "IND-30": "UNCTAD — Merchandise Trade Concentration Index & WTO",
    "IND-31": "UN (UNDESA) — World Population Prospects",
    "IND-32": "UNDP — Human Development Index (HDI), WHO & OECD (PISA)",
    "IND-33": "OECD — Trust in Government & International Labour Organization (ILO)",
    "IND-34": "BIS — Credit to the Non-Financial Sector & IMF IFS (CPI)",
    "IND-35": "International Labour Organization (ILO) — ILOSTAT",
    "IND-36": "World Bank — Logistics Performance Index (LPI) & UNCTAD (LSCI)",
    "IND-37": "World Bank — Enterprise Surveys & ENTSO-E / Energy Regulators",
    "IND-38": "ITU — Global Connectivity Report & Maritime Transport Authorities",
    "IND-39": "IEA — Electricity & Data Centres Report & TSO Grid Operators",
    "IND-40": "UN — Protocol and Liaison Service & Ministries of Foreign Affairs",
    "IND-41": "World Trade Organization (WTO) — Regional Trade Agreements Database",
    "IND-42": "OECD — Official Development Assistance (ODA/DAC) & UNESCO",
    "IND-43": "UN — Consolidated Sanctions List, Council of the EU & US OFAC",
    "IND-44": "UN — Treaty Series (UNTS) & Official Overseas Deployment Budgets",
    "IND-45": "UNHCR — Refugee Data Finder & UCDP Conflict Encyclopedia",
    "IND-46": "FAO — FAOSTAT (Food Balance Sheets)",
    "IND-47": "FAO — AQUASTAT",
    "IND-48": "UNFCCC — National Greenhouse Gas Inventories & IEA (CO2 Emissions)",
    "IND-49": "FAO — FAOSTAT (Trade) & UN Comtrade (Fertilizers)",
    "IND-50": "World Meteorological Organization (WMO) & FAO (Agricultural Stress Index)",
    "IND-51": "UN-Water & IEA (Cooling & Power Grid Reports)",
    "IND-52": "European Commission — CBAM & Eurostat (Comext)",
}
