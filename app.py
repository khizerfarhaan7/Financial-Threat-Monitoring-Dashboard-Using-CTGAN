
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Financial Threat Monitoring Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# --------------------------------
# MATPLOTLIB STYLE
# --------------------------------
plt.style.use('dark_background')

# --------------------------------
# CUSTOM CSS
# --------------------------------
st.markdown("""
<style>

.main {
    background: linear-gradient(
        135deg,
        #0B1020,
        #111827,
        #0F172A
    );
}

h1, h2, h3, h4 {
    color: white;
}

.stMetric {
    background: linear-gradient(
        145deg,
        #1E1E1E,
        #252836
    );

    padding: 18px;

    border-radius: 14px;

    border: 1px solid #2F3545;

    box-shadow: 0 0 12px rgba(
        77,
        150,
        255,
        0.15
    );
}

.block-container {
    padding-top: 2rem;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

.stButton>button {

    background: linear-gradient(
        90deg,
        #4D96FF,
        #6C63FF
    );

    color: white;

    border: none;

    border-radius: 12px;

    height: 50px;

    width: 220px;

    font-size: 16px;

    font-weight: bold;
}

.stButton>button:hover {

    transform: scale(1.03);

    transition: 0.3s ease;

    box-shadow: 0 0 15px rgba(
        108,
        99,
        255,
        0.5
    );
}

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# LOAD MODEL
# --------------------------------
model = joblib.load(
    "fraud_analysis_model.pkl"
)

# --------------------------------
# SIDEBAR
# --------------------------------
st.sidebar.title("🛡️ System Overview")

st.sidebar.markdown("""
## Financial Risk Intelligence

This platform provides:

• 📊 Transaction Monitoring
• 🤖 AI-Based Risk analysis
• 🧬 Synthetic Fraud Analysis
• 📈 Interactive Data Insights

---

### Core Features

✅ Fraud Identification  
✅ Risk Classification  
✅ AI-Powered Analytics  
✅ Report Generation  
✅ CSV Export Support  

---
""")

# --------------------------------
# MAIN TITLE
# --------------------------------
st.title("🛡️ Financial Threat Monitoring Dashboard")

st.markdown("""
Upload transaction datasets and identify potentially suspicious financial activities using AI-driven fraud analysis.
""")

st.success(
    "✅ System Ready for Transaction Risk Analysis"
)

# --------------------------------
# FILE UPLOADER
# --------------------------------
uploaded_file = st.file_uploader(
    "📂 Upload Transaction Dataset",
    type=["csv"]
)

# --------------------------------
# PROCESS FILE
# --------------------------------
if uploaded_file is not None:

    # Read CSV
    data = pd.read_csv(uploaded_file)

    # --------------------------------
    # REMOVE CLASS COLUMN IF EXISTS
    # --------------------------------
    if 'Class' in data.columns:
        data = data.drop('Class', axis=1)

    # --------------------------------
    # DATASET PREVIEW
    # --------------------------------
    st.subheader("📋 Dataset Preview")

    st.dataframe(
        data.head(),
        use_container_width=True
    )

    st.info(
        f"Dataset contains {data.shape[0]} records and {data.shape[1]} features."
    )

    # --------------------------------
    # RUN MODEL
    # --------------------------------
    if st.button("🚀 Run Analysis"):

        try:

            # --------------------------------
            # INPUT ARRAY
            # --------------------------------
            input_array = data.values

            # --------------------------------
            # PREDICTIONS
            # --------------------------------
            predictions = model.predict(input_array)

            probabilities = model.predict_proba(
                input_array
            )[:,1]

            # --------------------------------
            # RESULTS
            # --------------------------------
            results = pd.DataFrame({

                'Transaction_ID': range(
                    1,
                    len(predictions)+1
                ),

                'Risk_Score (%)': (
                    probabilities * 100
                ).round(2)

            })

            results['Status'] = predictions

            results['Status'] = results[
                'Status'
            ].map({
                0: 'Normal',
                1: 'Fraud'
            })

            # --------------------------------
            # RISK LEVEL
            # --------------------------------
            def risk_level(prob):

                if prob < 30:
                    return "🟢 Low"

                elif prob < 70:
                    return "🟠 Medium"

                else:
                    return "🔴 High"

            results['Risk_Level'] = results[
                'Risk_Score (%)'
            ].apply(risk_level)

            # --------------------------------
            # METRICS
            # --------------------------------
            fraud_count = (
                results['Status'] == 'Fraud'
            ).sum()

            normal_count = (
                results['Status'] == 'Normal'
            ).sum()

            total_transactions = len(results)

            fraud_percentage = (
                fraud_count / total_transactions
            ) * 100

            avg_probability = results[
                'Risk_Score (%)'
            ].mean()

            # --------------------------------
            # SUMMARY METRICS
            # --------------------------------
            st.subheader("📊 Risk Analysis Summary")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Total Transactions",
                total_transactions
            )

            col2.metric(
                "Fraud Cases",
                fraud_count
            )

            col3.metric(
                "Fraud Ratio",
                f"{fraud_percentage:.2f}%"
            )

            col4.metric(
                "Average Risk Score",
                f"{avg_probability:.2f}%"
            )

            # --------------------------------
            # ALERT
            # --------------------------------
            if fraud_count > 0:

                st.error(
                    f"🚨 ALERT: {fraud_count} suspicious transactions identified."
                )

            else:

                st.success(
                    "✅ No suspicious transactions detected."
                )

            # --------------------------------
            # SIDE BY SIDE CHARTS
            # --------------------------------
            st.subheader("📈 Transaction Insights")

            chart1, chart2 = st.columns(2)

            # --------------------------------
            # DONUT CHART
            # --------------------------------
            with chart1:

                fig1, ax1 = plt.subplots(
                    figsize=(6,6)
                )

                wedges, texts, autotexts = ax1.pie(
                    [normal_count, fraud_count],
                    labels=['Legitimate', 'Fraudulent'],
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=['#6C8EF5', '#FF6B81'],
                    wedgeprops={
                        'width':0.45,
                        'edgecolor':'white'
                    },
                    textprops={
                        'fontsize': 11,
                        'color':'white'
                    }
                )

                ax1.set_title(
                    "Fraud Activity Overview",
                    fontsize=14
                )

                st.pyplot(fig1)

                plt.close(fig1)

            # --------------------------------
            # BAR CHART
            # --------------------------------
            with chart2:

                risk_counts = results[
                    'Risk_Level'
                ].value_counts()

                fig2, ax2 = plt.subplots(
                    figsize=(7,6)
                )

                ax2.bar(
                    risk_counts.index,
                    risk_counts.values,
                    color=[
                        '#4D96FF',
                        '#FFD93D',
                        '#FF6B6B'
                    ]
                )

                ax2.set_title(
                    "Risk Level Analysis",
                    fontsize=14
                )

                ax2.set_xlabel(
                    "Risk Category"
                )

                ax2.set_ylabel(
                    "Number of Transactions"
                )

                st.pyplot(fig2)

                plt.close(fig2)

            # --------------------------------
            # FRAUD TRANSACTIONS
            # --------------------------------
            st.subheader("🚨 Flagged Transactions")

            suspicious = results[
                results['Status'] == 'Fraud'
            ]

            if len(suspicious) > 0:

                st.dataframe(
                    suspicious,
                    use_container_width=True
                )

            else:

                st.info(
                    "No flagged transactions found."
                )

            # --------------------------------
            # FULL RESULTS
            # --------------------------------
            st.subheader("📝 Complete Analysis Results")

            st.dataframe(
                results,
                use_container_width=True
            )

            # --------------------------------
            # DOWNLOAD BUTTON
            # --------------------------------
            csv = results.to_csv(index=False)

            st.download_button(
                label="⬇️ Download Analysis Report",
                data=csv,
                file_name='transaction_analysis_results.csv',
                mime='text/csv'
            )

            # --------------------------------
            # FOOTER
            # --------------------------------
            st.markdown(
                """
                <hr>
                <center>
                AI-Based Financial Risk Monitoring System
                </center>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:

            st.error(
                f"❌ Error Processing File: {e}"
            )
