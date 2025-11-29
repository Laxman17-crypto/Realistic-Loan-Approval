import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from io import BytesIO

st.set_page_config(layout="wide", page_title="Loan Approval — Optimized Dashboard", page_icon="💳")

# -----------------------
# Configuration / Constants
# -----------------------
MAX_RAW_ROWS = 2000       # show only first N rows in the raw-data tab
HEATMAP_SAMPLE = 3000    # rows to use when drawing heatmap
PCA_SAMPLE = 5000        # rows to use for PCA
SCATTER_MAX = 10000      # max rows for scatter
HIGH_CARD_THRESHOLD = 50 # don't allow categorical charts above this many unique values

# -----------------------
# Caching helpers
# -----------------------
@st.cache_data
def load_data(path_or_buf):
    try:
        df = pd.read_csv(path_or_buf)
        # small cleaning: strip names
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        return None

@st.cache_data
def numeric_columns(df):
    return df.select_dtypes(include=[np.number]).columns.tolist()

@st.cache_data
def categorical_columns(df):
    return df.select_dtypes(include=["object", "category"]).columns.tolist()

@st.cache_data
def sample_for_heatmap(df, n=HEATMAP_SAMPLE):
    if df.shape[0] <= n:
        return df
    return df.sample(n, random_state=42)

@st.cache_data
def sample_for_pca(df, n=PCA_SAMPLE):
    if df.shape[0] <= n:
        return df
    return df.sample(n, random_state=42)

@st.cache_data
def sample_for_scatter(df, n=SCATTER_MAX):
    if df.shape[0] <= n:
        return df
    return df.sample(n, random_state=42)

# -----------------------
# Utility
# -----------------------
def download_link(df):
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer

# -----------------------
# App Sidebar: load + filters
# -----------------------
st.sidebar.title("Data & Settings")
uploaded=None
if uploaded is None:
    DEFAULT_PATH = "data/Loan_approval_data_2025.csv"
    df = load_data(DEFAULT_PATH)
else:
    df = load_data(uploaded)

if df is None:
    st.sidebar.error("No data found. Please upload a CSV or place it at /mnt/data/Loan_approval_data_2025.csv")
    st.stop()

# quick dtype convert for date-like strings
for col in df.columns:
    if col.lower().find("date") != -1 or col.lower().find("time") != -1:
        try:
            df[col] = pd.to_datetime(df[col])
        except Exception:
            pass

st.sidebar.markdown(f"**Rows:** {df.shape[0]}  —  **Cols:** {df.shape[1]}")

# Performance mode toggle (recommended)
perf_mode = st.sidebar.checkbox("Performance mode (fast, uses sampling)", value=True)

# Build light weight filters (only for low-cardinality columns)
st.sidebar.subheader("Quick filters")
filters = {}
for col in df.columns:
    if df[col].dtype == 'object' and df[col].nunique() <= 30:
        vals = st.sidebar.multiselect(f"{col}", options=sorted(df[col].dropna().unique()), default=list(sorted(df[col].dropna().unique())))
        filters[col] = vals
    elif np.issubdtype(df[col].dtype, np.number):
        minv, maxv = float(df[col].min()), float(df[col].max())
        rng = st.sidebar.slider(f"{col}", min_value=minv, max_value=maxv, value=(minv, maxv))
        filters[col] = rng

# Apply filters (safely)
df_filtered = df.copy()
for col, val in filters.items():
    if col in df.columns:
        if isinstance(val, list):
            if len(val) > 0:
                df_filtered = df_filtered[df_filtered[col].isin(val)]
        elif isinstance(val, tuple) and len(val) == 2:
            df_filtered = df_filtered[(df_filtered[col] >= val[0]) & (df_filtered[col] <= val[1])]

# Derived lists
num_cols = numeric_columns(df_filtered)
cat_cols = categorical_columns(df_filtered)

# -----------------------
# Main layout with tabs (lazy content inside each tab)
# -----------------------
st.title("💳 Loan Approval — Optimized Dashboard")

tabs = st.tabs(["📊 Overview", "📈 Time / Trends", "📉 Distribution & Stats", "🔁 Relationships", "🧭 Dimensionality", "📋 Raw Data"])

# --- Tab 1: Overview ---
with tabs[0]:
    st.header("Overview & Key Metrics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if 'LoanAmount' in df_filtered.columns and pd.api.types.is_numeric_dtype(df_filtered['LoanAmount']):
            st.metric("Avg Loan Amount", f"{df_filtered['LoanAmount'].mean():.2f}")
        else:
            st.metric("Rows", df_filtered.shape[0])
    with col2:
        if 'ApplicantIncome' in df_filtered.columns and pd.api.types.is_numeric_dtype(df_filtered['ApplicantIncome']):
            st.metric("Avg Applicant Income", f"{df_filtered['ApplicantIncome'].mean():.2f}")
        else:
            st.metric("Columns", df_filtered.shape[1])
    with col3:
        if 'Loan_Status' in df_filtered.columns:
            vc = df_filtered['Loan_Status'].value_counts()
            top_label = vc.idxmax() if not vc.empty else "N/A"
            st.metric("Top Loan Status", f"{top_label}")
        else:
            st.metric("Unique Categories", len(cat_cols))
    with col4:
        st.metric("Missing values", int(df_filtered.isna().sum().sum()))

    st.markdown("---")
    colA, colB = st.columns([2,3])
    with colA:
        # Safe categorical pie: skip high-cardinality
        safe_cats = [c for c in cat_cols if df_filtered[c].nunique() <= HIGH_CARD_THRESHOLD]
        if len(safe_cats) == 0:
            st.info("No low-cardinality categorical column available for pie. Avoid columns like customer_id.")
        else:
            pick_cat = st.selectbox("Pick categorical for pie", options=safe_cats)
            fig = px.pie(df_filtered, names=pick_cat, title=f'{pick_cat} Breakdown', hole=0.3)
            st.plotly_chart(fig, use_container_width=True)
    with colB:
        if len(num_cols) >= 1:
            pick_num = st.selectbox("Metric for bar", options=num_cols, index=0)
            # Aggregate by a safe categorical if available, otherwise show histogram
            if 'Loan_Status' in df_filtered.columns and df_filtered['Loan_Status'].nunique() <= HIGH_CARD_THRESHOLD:
                agg = df_filtered.groupby('Loan_Status')[pick_num].mean().reset_index()
                fig = px.bar(agg, x='Loan_Status', y=pick_num, title=f'Average {pick_num} by Loan Status')
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig = px.histogram(df_filtered, x=pick_num, nbins=30, title=f'Distribution: {pick_num}')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No numeric columns available for metrics.")

# --- Tab 2: Time / Trends ---
with tabs[1]:
    st.header("Time series & trend analysis")
    date_cols = [c for c in df.columns if np.issubdtype(df[c].dtype, np.datetime64)]
    if len(date_cols) == 0:
        st.info("No date-like columns detected. Upload data with a date column or convert one to datetime.")
    else:
        dcol = st.selectbox("Date column", options=date_cols)
        if len(num_cols) == 0:
            st.info("No numeric column to trend.")
        else:
            value_col = st.selectbox("Value to trend (numeric)", options=num_cols)
            freq = st.selectbox("Aggregation", options=["D","W","M","Q","Y"], index=2)
            ts = df_filtered[[dcol, value_col]].dropna().set_index(dcol).sort_index()
            # smoothing: if data is huge, downsample by resampling first or sampling
            try:
                ts_agg = ts.resample(freq).mean()
            except Exception:
                ts_agg = ts
            fig = px.line(ts_agg, x=ts_agg.index, y=value_col, title=f'{value_col} over time ({freq})')
            st.plotly_chart(fig, use_container_width=True)

            window = st.slider("Rolling window (periods)", 1, 60, 3)
            ts_roll = ts_agg.rolling(window).mean()
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=ts_agg.index, y=ts_agg[value_col], name='Original'))
            fig2.add_trace(go.Scatter(x=ts_roll.index, y=ts_roll[value_col], name=f'Rolling({window})'))
            st.plotly_chart(fig2, use_container_width=True)

# --- Tab 3: Distribution & Stats ---
with tabs[2]:
    st.header("Distributions, outliers & summary stats")
    if len(num_cols) == 0:
        st.write("No numeric columns detected.")
    else:
        pick = st.selectbox("Numeric column", options=num_cols)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Histogram + Rug")
            # histogram uses full filtered df but Plotly handles it efficiently
            fig = px.histogram(df_filtered, x=pick, nbins=40, marginal='rug', title=f'Histogram: {pick}')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.subheader("Box / Violin (sampled)")
            data_for_box = df_filtered[pick].dropna()
            # limit size for plotting
            if perf_mode and data_for_box.shape[0] > 10000:
                data_for_box = data_for_box.sample(10000, random_state=42)
            fig = go.Figure()
            fig.add_trace(go.Box(y=data_for_box, name='Box'))
            fig.add_trace(go.Violin(y=data_for_box, name='Violin', box_visible=True, meanline_visible=True))
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("Summary statistics")
        st.dataframe(df_filtered[num_cols].describe().T)

        st.markdown("---")
        st.subheader("Outliers (IQR method)")
        Q1 = df_filtered[pick].quantile(0.25)
        Q3 = df_filtered[pick].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df_filtered[(df_filtered[pick] < (Q1 - 1.5 * IQR)) | (df_filtered[pick] > (Q3 + 1.5 * IQR))]
        st.write(f"Outliers detected: {outliers.shape[0]}")
        if not outliers.empty:
            st.dataframe(outliers.head(100))

# --- Tab 4: Relationships ---
with tabs[3]:
    st.header("Relationships, correlations & categorical comparisons")
    col1, col2 = st.columns([2,3])

    with col1:
        st.subheader("Correlation matrix (numeric)")
        if len(num_cols) >= 2:
            # sample before correlation if huge
            corr_df = df_filtered[num_cols].dropna()
            if perf_mode and corr_df.shape[0] > HEATMAP_SAMPLE:
                corr_df = sample_for_heatmap(corr_df)
            corr = corr_df.corr()
            fig, ax = plt.subplots(figsize=(8,6))
            sns.heatmap(corr, annot=True, fmt='.2f', cmap='vlag', ax=ax)
            st.pyplot(fig)
        else:
            st.write("Need at least 2 numeric columns for correlation")

    with col2:
        st.subheader("Scatter / bubble (sampled)")
        if len(num_cols) >= 2:
            x = st.selectbox("X axis", options=num_cols, index=0)
            y = st.selectbox("Y axis", options=num_cols, index=1)
            size = st.selectbox("Size (optional)", options=[None]+num_cols)
            color = st.selectbox("Color (categorical)", options=[None]+cat_cols)

            plot_df = df_filtered[[x,y] + ([size] if size else []) + ([color] if color else [])].dropna()
            if perf_mode and plot_df.shape[0] > SCATTER_MAX:
                plot_df = sample_for_scatter(plot_df)
            fig = px.scatter(plot_df, x=x, y=y, size=size if size else None, color=color if color else None, hover_data=list(plot_df.columns), title=f'{y} vs {x}')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Need numeric columns to draw scatter")

    st.markdown("---")
    st.subheader("Categorical cross-tabs & stacked bars (safe)")
    safe_cat_cols = [c for c in cat_cols if df_filtered[c].nunique() <= HIGH_CARD_THRESHOLD]
    if len(safe_cat_cols) >= 2:
        a = st.selectbox("Category A", options=safe_cat_cols, index=0)
        b = st.selectbox("Category B", options=safe_cat_cols, index=1)
        ct = pd.crosstab(df_filtered[a], df_filtered[b], normalize='index')
        fig = px.bar(ct, barmode='stack', title=f'Stacked bar: {a} by {b}')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No two low-cardinality categorical columns found for cross-tab. Avoid customer_id or other high-card columns.")

# --- Tab 5: Dimensionality & Advanced ---
with tabs[4]:
    st.header("PCA & advanced projections")
    if len(num_cols) < 2:
        st.write("Need at least 2 numeric columns for PCA")
    else:
        n_components = st.slider("PCA components", 2, min(6, len(num_cols)), 2)
        X_full = df_filtered[num_cols].dropna()
        if perf_mode and X_full.shape[0] > PCA_SAMPLE:
            X = sample_for_pca(X_full)
        else:
            X = X_full
        if X.shape[0] < 2:
            st.write("Not enough rows for PCA after filtering/sampling.")
        else:
            scaler = StandardScaler()
            Xs = scaler.fit_transform(X.values)
            pca = PCA(n_components=n_components)
            Z = pca.fit_transform(Xs)
            pca_df = pd.DataFrame(Z, columns=[f'PC{i+1}' for i in range(Z.shape[1])])

            color = 'Loan_Status' if 'Loan_Status' in df_filtered.columns and df_filtered['Loan_Status'].nunique() <= HIGH_CARD_THRESHOLD else None
            if color:
                # align indices: attempt to join using index
                pca_df = pca_df.set_index(X.index)
                merged = pca_df.join(df_filtered[color])
                fig = px.scatter(merged.reset_index(), x='PC1', y='PC2', color=color, title='PCA (PC1 vs PC2)')
            else:
                fig = px.scatter(pca_df, x='PC1', y='PC2', title='PCA (PC1 vs PC2)')
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("Explained variance ratio (first components)")
            ev = pca.explained_variance_ratio_
            st.bar_chart(ev)

# --- Tab 6: Raw Data ---
with tabs[5]:
    st.header("Raw & Download")
    st.write(f"Showing first {min(MAX_RAW_ROWS, df_filtered.shape[0])} rows (to avoid browser overload)")
    st.dataframe(df_filtered.head(MAX_RAW_ROWS))
    buf = download_link(df_filtered)
    st.download_button("Download filtered CSV", data=buf, file_name="loan_filtered.csv", mime="text/csv")

    st.markdown("---")
    st.write("If you want finance-specific charts (candlestick / OHLC), upload time-series data with Date/Open/High/Low/Close/Volume columns. Performance mode will still sample large series.")

# Footer
st.markdown("---")
st.caption("Optimized: sampling + caching + safe guardrails to prevent UI freezes. Adjust sampling constants at the top of the script if needed.")
