import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

# =========================================================
# PAGE
# =========================================================
st.set_page_config(
    page_title="PJMW Energy Forecast",
    page_icon="",
    layout="wide"
)

# =========================================================
# PROFESSIONAL UI
# =========================================================
st.markdown("""
<style>

.stApp {
    background: #F3F6F8;
    color: #172033;
}

/* ================= HEADER ================= */

.hero {
    background: linear-gradient(135deg, #0B1F33, #176B87);
    padding: 30px 34px;
    border-radius: 20px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 10px 28px rgba(11,31,51,.18);
}

.hero h1 {
    color: white !important;
    font-size: 40px;
    margin: 0;
    font-weight: 800;
}

.hero p {
    color: #D9EEF2 !important;
    font-size: 16px;
    margin-top: 8px;
}

/* ================= SIDEBAR ================= */

[data-testid="stSidebar"] {
    background: #0B1F33;
}

[data-testid="stSidebar"] label {
    color: white !important;
}

[data-testid="stSidebar"] p {
    color: #D9E6EF !important;
}

[data-testid="stSidebar"] h2 {
    color: white !important;
}

/* ================= MODEL SELECTBOX ================= */

/* ================= SELECTBOX ================= */

/* Selectbox box */
[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #B8C7D3 !important;
    border-radius: 10px !important;
    color: #172033 !important;
}

/* Selected model text */
[data-testid="stSidebar"] div[data-baseweb="select"] div {
    color: #172033 !important;
}

/* Text inside selectbox */
[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #172033 !important;
}

/* Input text */
[data-testid="stSidebar"] div[data-baseweb="select"] input {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
}

/* Dropdown arrow */
[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill: #176B87 !important;
}

/* Dropdown menu */
div[data-baseweb="popover"] {
    background: #FFFFFF !important;
}

/* Dropdown options */
div[data-baseweb="popover"] li {
    background: #FFFFFF !important;
    color: #172033 !important;
}

/* Option text */
div[data-baseweb="popover"] li span {
    color: #172033 !important;
}

/* Hover option */
div[data-baseweb="popover"] li:hover {
    background: #E7F3F5 !important;
    color: #0B1F33 !important;
}

[data-testid="stSidebar"] {
    background: #0B1F33;
}

[data-testid="stSidebar"] label {
    color: white !important;
}

[data-testid="stSidebar"] p {
    color: #D9E6EF !important;
}
/* ================= GENERAL TEXT ================= */

h1, h2, h3, h4 {
    color: #0B1F33 !important;
}

p {
    color: #405465;
}

/* ================= DATASET CARDS ================= */

.card {
    background: #FFFFFF;
    border: 1px solid #D8E1E8;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 5px 16px rgba(11,31,51,.06);
    transition: .25s;
}

.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 9px 22px rgba(11,31,51,.11);
}

.card-title {
    color: #607080 !important;
    font-size: 13px;
    font-weight: 600;
}

.card-value {
    color: #0B1F33 !important;
    font-size: 27px;
    font-weight: 800;
    margin-top: 5px;
}

.card-text {
    color: #607080 !important;
    font-size: 12px;
}


/* ================= MODEL CARD ================= */

.model-card {
    background: #E7F3F5;
    border-left: 5px solid #176B87;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
}

.model-name {
    color: #0B1F33 !important;
    font-size: 26px;
    font-weight: 800;
}

.model-description {
    color: #405465 !important;
    margin-top: 6px;
}

/* ================= KPI CARDS ================= */

.kpi {
    color: white;
    padding: 21px;
    border-radius: 17px;
    min-height: 125px;
    box-shadow: 0 7px 20px rgba(11,31,51,.13);
    transition: .25s;
}

.kpi:hover {
    transform: translateY(-4px);
}

.kpi-title {
    color: white !important;
    font-size: 13px;
    font-weight: 600;
}

.kpi-value {
    color: white !important;
    font-size: 29px;
    font-weight: 800;
    margin-top: 7px;
}

.kpi-info {
    color: white !important;
    font-size: 12px;
    opacity: .88;
}

.blue {
    background: #176B87;
}

.gold {
    background: #B77900;
}

.green {
    background: #16805C;
}

.navy {
    background: #244A68;
}

/* ================= INSIGHT CARDS ================= */

.insight {
    padding: 22px;
    border-radius: 14px;
    margin-bottom: 18px;
    min-height: 125px;
    border: 1px solid;
}

.insight.peak {
    background: #E8F3F8;
    border-color: #B7D7E2;
    border-left: 5px solid #176B87;
}

.insight.average {
    background: #E8F5EF;
    border-color: #B8DDCE;
    border-left: 5px solid #16805C;
}

.insight.minimum {
    background: #FFF5DD;
    border-color: #E8D19A;
    border-left: 5px solid #B77900;
}

.insight.range {
    background: #FBEAEA;
    border-color: #E6C2C2;
    border-left: 5px solid #B42318;
}

.insight-title {
    font-size: 16px;
    font-weight: 700;
    color: #0B1F33 !important;
}

.insight-value {
    font-size: 25px;
    font-weight: 800;
    color: #172033 !important;
    margin: 10px 0;
}

.insight-text {
    font-size: 14px;
    color: #526273 !important;
    line-height: 1.5;
}

.insight-text b {
    color: #172033 !important;
}

/* ================= BUTTON ================= */

.stButton > button {
    background: #2A9D8F !important;
    color: white !important;
    border: none !important;
    border-radius: 10px;
    font-weight: 700;
}

.stButton > button:hover {
    background: #21867A !important;
}

/* ================= DOWNLOAD ================= */

.stDownloadButton > button {
    background: white !important;
    color: #176B87 !important;
    border: 1px solid #176B87 !important;
    border-radius: 10px;
    font-weight: 700;
}

.stDownloadButton > button:hover {
    background: #E7F3F5 !important;
}

/* ================= TABS ================= */

button[data-baseweb="tab"] {
    color: #526273 !important;
    font-weight: 600;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #176B87 !important;
}

/* ================= FOOTER ================= */

.footer {
    text-align: center;
    color: #607080 !important;
    padding: 30px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD MODELS
# =========================================================

@st.cache_resource
def load_bundle():

    path = (
        Path(__file__).parent
        / "deployment"
        / "models.joblib"
    )

    if not path.exists():
        st.error(
            "models.joblib was not found inside deployment folder."
        )
        st.stop()

    return joblib.load(path)


bundle = load_bundle()

models = bundle["models"]

if "XGBoost" not in models:
    st.error(
        "The loaded model bundle does not contain XGBoost. "
        "Re-run the notebook's XGBoost-only export cell and ensure "
        "deployment/models.joblib points to the newly exported file."
    )
    st.stop()

history = bundle["history"].copy()

history["Datetime"] = pd.to_datetime(
    history["Datetime"]
)

history = history.sort_values("Datetime")

history_series = (
    history
    .set_index("Datetime")["PJMW_MW"]
)

features = bundle["features"]

holidays = bundle.get(
    "holidays",
    pd.DatetimeIndex([])
)


# =========================================================
# MODEL DESCRIPTIONS
# =========================================================

model_info = {

    "XGBoost":
        "Gradient boosting using calendar information and historical demand lags.",

    "CatBoost":
        "Boosting model using calendar, lag and rolling demand features.",

    "Random Forest":
        "Ensemble of decision trees for learning complex demand patterns.",

    "LightGBM":
        "Fast gradient boosting using calendar and cyclical time features.",

    "Prophet":
        "Time-series model designed to capture trend and seasonal patterns.",

    "SARIMA":
        "Statistical time-series model designed for seasonal demand forecasting."
}


# =========================================================
# XGBOOST
# =========================================================

def xgb_forecast(model, future):

    hist = history_series.copy()
    result = []

    for dt in future:

        row = pd.DataFrame([{
            "Hour": dt.hour,
            "DOW": dt.dayofweek,
            "Month": dt.month,
            "Year": dt.year,
            "Lag_1": hist.iloc[-1],
            "Lag_24": hist.iloc[-24],
            "Lag_168": hist.iloc[-168]
        }])

        pred = float(
            model.predict(
                row[features["XGBoost"]]
            )[0]
        )

        pred = max(pred, 0)

        result.append(pred)
        hist.loc[dt] = pred

    return result


# =========================================================
# CATBOOST / RANDOM FOREST
# =========================================================

def tree_forecast(model, future):

    hist = history_series.copy()
    result = []

    for dt in future:

        dow = dt.dayofweek

        row = pd.DataFrame([{

            "Hour": dt.hour,
            "DayOfWeek": dow,
            "DayOfMonth": dt.day,
            "Month": dt.month,
            "Quarter": dt.quarter,
            "WeekOfYear": dt.isocalendar().week,
            "Year": dt.year,
            "IsWeekend": int(dow >= 5),
            "IsHoliday": int(
                dt.normalize() in holidays
            ),

            "Lag_1": hist.iloc[-1],
            "Lag_2": hist.iloc[-2],
            "Lag_3": hist.iloc[-3],
            "Lag_24": hist.iloc[-24],
            "Lag_48": hist.iloc[-48],
            "Lag_72": hist.iloc[-72],
            "Lag_168": hist.iloc[-168],

            "RollingMean_24": hist.iloc[-24:].mean(),
            "RollingStd_24": hist.iloc[-24:].std(),
            "RollingMean_168": hist.iloc[-168:].mean(),
            "RollingStd_168": hist.iloc[-168:].std()

        }])

        pred = float(
            model.predict(
                row[features["TreeModels"]]
            )[0]
        )

        pred = max(pred, 0)

        result.append(pred)
        hist.loc[dt] = pred

    return result


# =========================================================
# LIGHTGBM
# =========================================================

def lightgbm_forecast(model, future):

    x = pd.DataFrame({
        "Datetime": future
    })

    x["Hour"] = x.Datetime.dt.hour
    x["DOW"] = x.Datetime.dt.dayofweek
    x["Month"] = x.Datetime.dt.month
    x["Year"] = x.Datetime.dt.year

    x["Hour_sin"] = np.sin(
        2 * np.pi * x.Hour / 24
    )

    x["Hour_cos"] = np.cos(
        2 * np.pi * x.Hour / 24
    )

    x["DOW_sin"] = np.sin(
        2 * np.pi * x.DOW / 7
    )

    x["DOW_cos"] = np.cos(
        2 * np.pi * x.DOW / 7
    )

    x["Month_sin"] = np.sin(
        2 * np.pi * x.Month / 12
    )

    x["Month_cos"] = np.cos(
        2 * np.pi * x.Month / 12
    )

    return np.maximum(
        model.predict(
            x[features["LightGBM"]]
        ),
        0
    )


# =========================================================
# GENERATE FORECAST
# =========================================================

def generate_forecast(model_name, days):

    future = pd.date_range(
        start=(
            history_series.index[-1]
            + pd.Timedelta(hours=1)
        ),
        periods=days * 24,
        freq="h"
    )

    model = models[model_name]

    if model_name == "XGBoost":

        prediction = xgb_forecast(
            model,
            future
        )

    elif model_name in [
        "CatBoost",
        "Random Forest"
    ]:

        prediction = tree_forecast(
            model,
            future
        )

    elif model_name == "LightGBM":

        prediction = lightgbm_forecast(
            model,
            future
        )

    elif model_name == "Prophet":

        prediction = model.predict(
            pd.DataFrame({
                "ds": future
            })
        )["yhat"].clip(
            lower=0
        ).values

    elif model_name == "SARIMA":

        prediction = model.get_forecast(
            steps=len(future)
        ).predicted_mean.clip(
            lower=0
        ).values

    return pd.DataFrame({
        "Datetime": future,
        "Predicted_MW": prediction
    })


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero">

<h1>⚡ PJMW Energy Forecast</h1>

<p>
Hourly electricity demand forecasting using
machine learning and time-series models.
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## Forecast Controls")

st.sidebar.write(
    "Select a model and forecast period."
)

model_name = st.sidebar.selectbox(
    "Forecasting Model",
    ["XGBoost"]
)

days = st.sidebar.select_slider(
    "Forecast Period",
    options=[1, 3, 7, 14, 30],
    value=7
)

st.sidebar.markdown("---")

st.sidebar.write(
    f"**Selected Model:** {model_name}"
)

st.sidebar.write(
    f"**Forecast Period:** {days} day(s)"
)

st.sidebar.write(
    f"**Forecast Points:** {days * 24:,} hours"
)

generate = st.sidebar.button(
    "Generate Forecast",
    use_container_width=True
)


# =========================================================
# DATASET OVERVIEW
# =========================================================

st.subheader("Dataset Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(
        f"""
        <div class="card">
        <div class="card-title">
        Historical Records
        </div>

        <div class="card-value">
        {len(history):,}
        </div>

        <div class="card-text">
        Hourly observations
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:

    st.markdown(
        f"""
        <div class="card">
        <div class="card-title">
        Latest Demand
        </div>

        <div class="card-value">
        {history_series.iloc[-1]:,.0f} MW
        </div>

        <div class="card-text">
        Latest recorded demand
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:

    st.markdown(
        f"""
        <div class="card">
        <div class="card-title">
        Average Demand
        </div>

        <div class="card-value">
        {history_series.mean():,.0f} MW
        </div>

        <div class="card-text">
        Historical average
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:

    st.markdown(
        f"""
        <div class="card">
        <div class="card-title">
        Available Models
        </div>

        <div class="card-value">
        {len(models)}
        </div>

        <div class="card-text">
        Forecasting models
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.caption(
    f"Historical period: "
    f"{history_series.index.min():%d %b %Y}"
    f" → "
    f"{history_series.index.max():%d %b %Y %H:%M}"
)


# =========================================================
# SELECTED MODEL
# =========================================================

st.subheader("Selected Forecasting Model")

st.markdown(
    f"""
    <div class="model-card">

    <div class="model-name">
    {model_name}
    </div>

    <div class="model-description">
    {model_info.get(
        model_name,
        "Forecasting model"
    )}
    </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# GENERATE FORECAST
# =========================================================

if generate:

    with st.spinner(
        f"Generating {model_name} forecast..."
    ):

        forecast = generate_forecast(
            model_name,
            days
        )

    st.success(
        f"Forecast generated successfully "
        f"for the next {days} day(s)."
    )

    # =====================================================
    # CALCULATIONS
    # =====================================================

    average = forecast[
        "Predicted_MW"
    ].mean()

    peak_index = forecast[
        "Predicted_MW"
    ].idxmax()

    minimum_index = forecast[
        "Predicted_MW"
    ].idxmin()

    peak = forecast.loc[
        peak_index,
        "Predicted_MW"
    ]

    minimum = forecast.loc[
        minimum_index,
        "Predicted_MW"
    ]

    peak_time = forecast.loc[
        peak_index,
        "Datetime"
    ]

    minimum_time = forecast.loc[
        minimum_index,
        "Datetime"
    ]

    demand_range = peak - minimum


    # =====================================================
    # KPI CARDS
    # =====================================================

    st.subheader("Forecast Summary")

    k1, k2, k3, k4 = st.columns(4)

    with k1:

        st.markdown(
            f"""
            <div class="kpi blue">

            <div class="kpi-title">
            Average Demand
            </div>

            <div class="kpi-value">
            {average:,.0f} MW
            </div>

            <div class="kpi-info">
            Expected average
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with k2:

        st.markdown(
            f"""
            <div class="kpi gold">

            <div class="kpi-title">
            Peak Demand
            </div>

            <div class="kpi-value">
            {peak:,.0f} MW
            </div>

            <div class="kpi-info">
            {peak_time:%d %b %H:%M}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with k3:

        st.markdown(
            f"""
            <div class="kpi green">

            <div class="kpi-title">
            Minimum Demand
            </div>

            <div class="kpi-value">
            {minimum:,.0f} MW
            </div>

            <div class="kpi-info">
            {minimum_time:%d %b %H:%M}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with k4:

        st.markdown(
            f"""
            <div class="kpi navy">

            <div class="kpi-title">
            Forecast Points
            </div>

            <div class="kpi-value">
            {len(forecast):,}
            </div>

            <div class="kpi-info">
            Hourly predictions
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # TABS
    # =====================================================

    tab1, tab2, tab3 = st.tabs([
        "📈 Forecast Chart",
        "💡 Forecast Insights",
        "📋 Hourly Data"
    ])


    # =====================================================
    # CHART
    # =====================================================

    with tab1:

        st.markdown(
            "### Hourly Electricity Demand"
        )

        chart = forecast.set_index(
            "Datetime"
        )[["Predicted_MW"]]

        st.line_chart(
            chart,
            height=450
        )

        st.caption(
            "Predicted electricity demand for "
            "each future hour."
        )


    # =====================================================
    # INSIGHTS
    # =====================================================

    with tab2:

        st.markdown(
            "### Forecast Insights"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                f"""
                <div class="insight peak">

                <div class="insight-title">
                🔥 Peak Demand
                </div>

                <div class="insight-value">
                {peak:,.0f} MW
                </div>

                <div class="insight-text">
                Expected around
                <b>
                {peak_time:%d %B %Y at %H:%M}
                </b>
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="insight average">

                <div class="insight-title">
                📊 Average Demand
                </div>

                <div class="insight-value">
                {average:,.0f} MW
                </div>

                <div class="insight-text">
                Expected average consumption
                during the forecast period.
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                f"""
                <div class="insight minimum">

                <div class="insight-title">
                📉 Minimum Demand
                </div>

                <div class="insight-value">
                {minimum:,.0f} MW
                </div>

                <div class="insight-text">
                Expected around
                <b>
                {minimum_time:%d %B %Y at %H:%M}
                </b>
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="insight range">

                <div class="insight-title">
                📈 Demand Range
                </div>

                <div class="insight-value">
                {demand_range:,.0f} MW
                </div>

                <div class="insight-text">
                Difference between peak
                and minimum demand.
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    # =====================================================
    # HOURLY DATA
    # =====================================================

    with tab3:

        st.markdown(
            "### Hourly Forecast Data"
        )

        display = forecast.copy()

        display["Datetime"] = display[
            "Datetime"
        ].dt.strftime(
            "%d %b %Y %H:%M"
        )

        display["Predicted_MW"] = display[
            "Predicted_MW"
        ].round(2)

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True,
            height=500
        )

        st.markdown("#### Download Results")

        csv = forecast.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Forecast Data",
            data=csv,
            file_name=(
                f"{model_name.replace(' ', '_')}_"
                f"{days}_day_forecast.csv"
            ),
            mime="text/csv",
            use_container_width=True
        )


# =========================================================
# INITIAL SCREEN
# =========================================================

else:

    st.markdown("---")

    st.markdown(
        """
        <div class="card">

        <h2>Ready to Forecast?</h2>

        <p>
        Select a forecasting model and prediction
        period from the sidebar.
        </p>

        <p>
        Click <b>Generate Forecast</b> to view
        hourly predictions, demand insights,
        charts and downloadable forecast data.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

    <b>PJMW Hourly Energy Forecast</b>

    <br>

    Machine Learning • Time-Series Forecasting • Streamlit

    </div>
    """,
    unsafe_allow_html=True
)