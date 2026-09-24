import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from sqlalchemy import create_engine

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Bank Customer Churn Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🏦 Bank Customer Churn & Retention Analytics")
st.markdown(
    "Interactive executive dashboard examining customer churn drivers across demographics, credit tiers, and product usage using **SQL Server** and **Streamlit**."
)
st.markdown("---")

# -----------------------------------------------------------------------------
# 2. Database Connection & Data Querying (SQL Server)
# -----------------------------------------------------------------------------
SERVER = "localhost"
DATABASE = "BankChurnDB"
DRIVER = "ODBC Driver 17 for SQL Server"


@st.cache_data(ttl=600)
def load_data():
    connection_string = (
        f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver={DRIVER}&trusted_connection=yes"
    )
    engine = create_engine(connection_string)
    query = "SELECT * FROM bank_churn"
    df = pd.read_sql_query(query, engine)
    return df


try:
    df = load_data()
except Exception as e:
    st.error(f"Failed to connect to SQL Server database: {e}")
    st.stop()

# -----------------------------------------------------------------------------
# 3. Sidebar Filters
# -----------------------------------------------------------------------------
st.sidebar.header("🔍 Filter Dashboard")

# Geography Filter
geographies = sorted(df["geography"].unique().tolist())
selected_geo = st.sidebar.multiselect(
    "Geography", options=geographies, default=geographies
)

# Gender Filter
genders = sorted(df["gender"].unique().tolist())
selected_gender = st.sidebar.multiselect(
    "Gender", options=genders, default=genders
)

# Active Status Filter
active_statuses = sorted(df["is_active_member_label"].unique().tolist())
selected_active = st.sidebar.multiselect(
    "Member Status", options=active_statuses, default=active_statuses
)

# Filter Dataframe based on selections
filtered_df = df[
    (df["geography"].isin(selected_geo))
    & (df["gender"].isin(selected_gender))
    & (df["is_active_member_label"].isin(selected_active))
]

if filtered_df.empty:
    st.warning("No records found matching current filter selection.")
    st.stop()

# -----------------------------------------------------------------------------
# 4. Key Performance Indicators (KPIs)
# -----------------------------------------------------------------------------
total_customers = len(filtered_df)
churned_customers = filtered_df["exited"].sum()
churn_rate = (
    (churned_customers / total_customers * 100) if total_customers > 0 else 0
)
total_balance_at_risk = filtered_df[filtered_df["exited"] == 1][
    "balance"
].sum()
avg_credit_score = filtered_df["credit_score"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churn Rate", f"{churn_rate:.1f}%")
col3.metric("Balance at Risk", f"${total_balance_at_risk:,.2f}")
col4.metric("Avg Credit Score", f"{avg_credit_score:.0f}")

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. Visualizations Section
# -----------------------------------------------------------------------------
sns.set_theme(style="whitegrid")

row1_col1, row1_col2 = st.columns(2)

# Churn Rate by Age Group
with row1_col1:
    age_order = ["< 30", "30-39", "40-49", "50-59", "60+"]
    age_churn = (
        filtered_df.groupby("age_group", observed=False)["exited"]
        .mean()
        .reindex(age_order)
        * 100
    ).reset_index()

    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.barplot(
        data=age_churn,
        x="age_group",
        y="exited",
        palette="Reds_d",
        ax=ax1,
    )
    ax1.set_title("Churn Rate by Age Group", fontsize=13, fontweight="bold", pad=12)
    ax1.set_ylabel("Churn Rate (%)")
    ax1.set_xlabel("Age Group")
    ax1.set_ylim(0, max(age_churn["exited"].max() * 1.15, 10))
    for p in ax1.patches:
        height = p.get_height()
        if not pd.isna(height) and height > 0:
            ax1.annotate(
                f"{height:.1f}%",
                (p.get_x() + p.get_width() / 2.0, height),
                ha="center",
                va="bottom",
                fontsize=9,
                xytext=(0, 3),
                textcoords="offset points",
            )
    fig1.tight_layout()
    st.pyplot(fig1)

# Churn by Number of Products
with row1_col2:
    prod_churn = (
        filtered_df.groupby("num_of_products")["exited"].mean() * 100
    ).reset_index()

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.barplot(
        data=prod_churn,
        x="num_of_products",
        y="exited",
        palette="Blues_d",
        ax=ax2,
    )
    ax2.set_title("Churn Rate by Number of Products", fontsize=13, fontweight="bold", pad=12)
    ax2.set_ylabel("Churn Rate (%)")
    ax2.set_xlabel("Number of Products")
    ax2.set_ylim(0, 115)
    for p in ax2.patches:
        height = p.get_height()
        if not pd.isna(height) and height > 0:
            ax2.annotate(
                f"{height:.1f}%",
                (p.get_x() + p.get_width() / 2.0, height),
                ha="center",
                va="bottom",
                fontsize=9,
                xytext=(0, 3),
                textcoords="offset points",
            )
    fig2.tight_layout()
    st.pyplot(fig2)

row2_col1, row2_col2 = st.columns(2)

# Credit Tier Distribution vs Churn
with row2_col1:
    credit_order = [
        "Poor (< 580)",
        "Fair (580-669)",
        "Good (670-739)",
        "Very Good (740-799)",
        "Excellent (800+)",
    ]

    fig3, ax3 = plt.subplots(figsize=(6, 4))
    sns.countplot(
        data=filtered_df,
        x="credit_tier",
        hue="churn_status",
        order=credit_order,
        palette={"Retained": "#2ecc71", "Churned": "#e74c3c"},
        ax=ax3,
    )
    ax3.set_title("Churn Count by Credit Tier", fontsize=13, fontweight="bold", pad=12)
    ax3.set_ylabel("Customer Count")
    ax3.set_xlabel("Credit Tier")
    plt.xticks(rotation=20, ha="right")
    ax3.legend(title="")
    fig3.tight_layout()
    st.pyplot(fig3)

# Balance Distribution (Retained vs Churned)
with row2_col2:
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    sns.kdeplot(
        data=filtered_df,
        x="balance",
        hue="churn_status",
        common_norm=False,
        fill=True,
        clip=(0, None),
        palette={"Retained": "#2ecc71", "Churned": "#e74c3c"},
        ax=ax4,
    )
    ax4.set_title("Account Balance Distribution", fontsize=13, fontweight="bold", pad=12)
    ax4.set_ylabel("Density")
    ax4.set_xlabel("Account Balance ($)")
    fig4.tight_layout()
    st.pyplot(fig4)

# -----------------------------------------------------------------------------
# 6. Dataset Inspector
# -----------------------------------------------------------------------------
st.markdown("---")
with st.expander("📋 View Filtered Dataset"):
    st.dataframe(filtered_df, use_container_width=True)