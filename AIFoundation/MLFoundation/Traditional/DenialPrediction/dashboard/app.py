"""
Healthcare Denial Prediction Dashboard
Streamlit application for real-time monitoring and analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import json
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Streamlit page
st.set_page_config(
    page_title="Healthcare Denial Prediction Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = st.secrets.get("API_BASE_URL", "http://localhost:8000")
API_TOKEN = st.secrets.get("API_TOKEN", "demo_token_123")

class DashboardAPI:
    """API client for dashboard"""
    
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {token}"}
    
    def predict_claim(self, claim_data: dict) -> dict:
        """Make prediction API call"""
        try:
            response = requests.post(
                f"{self.base_url}/predict",
                json=claim_data,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"API call failed: {e}")
            raise
    
    def get_model_performance(self) -> dict:
        """Get model performance metrics"""
        try:
            response = requests.get(
                f"{self.base_url}/model/performance",
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Performance API call failed: {e}")
            raise
    
    def health_check(self) -> dict:
        """Check API health"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}

# Initialize API client
api = DashboardAPI(API_BASE_URL, API_TOKEN)

# ============================================================================
# DASHBOARD LAYOUT
# ============================================================================

def main():
    """Main dashboard application"""
    
    st.title("🏥 Healthcare Denial Prediction Dashboard")
    st.markdown("Real-time prediction and analysis of healthcare claim denials")
    
    # Check API health
    health_status = api.health_check()
    if health_status.get("status") != "healthy":
        st.error(f"⚠️ API is not healthy: {health_status.get('error', 'Unknown error')}")
        st.warning("Some features may not work properly. Please check the API server.")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Single Claim Prediction", "Batch Analysis", "Model Performance", "Risk Analytics"]
    )
    
    if page == "Single Claim Prediction":
        single_claim_page()
    elif page == "Batch Analysis":
        batch_analysis_page()
    elif page == "Model Performance":
        model_performance_page()
    elif page == "Risk Analytics":
        risk_analytics_page()

def single_claim_page():
    """Single claim prediction page"""
    st.header("Single Claim Prediction")
    
    # Create input form
    with st.form("claim_prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            claim_id = st.text_input("Claim ID", value="CLM_001")
            provider_id = st.text_input("Provider ID", value="PROV_123")
            payer_id = st.text_input("Payer ID", value="PAY_456")
            patient_id = st.text_input("Patient ID", value="PAT_789")
            claim_amount = st.number_input("Claim Amount ($)", min_value=0.0, value=1500.0)
            
        with col2:
            patient_age = st.number_input("Patient Age", min_value=0, max_value=120, value=45)
            patient_gender = st.selectbox("Patient Gender", ["M", "F"])
            service_date = st.date_input("Service Date", datetime.now().date())
            place_of_service = st.text_input("Place of Service", value="11")
            authorization_number = st.text_input("Authorization Number (optional)", value="")
        
        # CPT and ICD codes
        cpt_codes = st.text_input("CPT Codes (comma-separated)", value="99213,90834").split(",")
        icd_codes = st.text_input("ICD Codes (comma-separated)", value="F32.9,Z00.00").split(",")
        modifiers = st.text_input("Modifiers (comma-separated)", value="").split(",") if st.text_input("Modifiers (comma-separated)", value="") else []
        
        submitted = st.form_submit_button("Predict Denial Risk")
        
        if submitted:
            # Prepare claim data
            claim_data = {
                "claim_id": claim_id,
                "provider_id": provider_id,
                "payer_id": payer_id,
                "patient_id": patient_id,
                "cpt_codes": [code.strip() for code in cpt_codes if code.strip()],
                "icd_codes": [code.strip() for code in icd_codes if code.strip()],
                "claim_amount": claim_amount,
                "service_date": service_date.isoformat(),
                "patient_age": patient_age,
                "patient_gender": patient_gender,
                "authorization_number": authorization_number if authorization_number else None,
                "modifiers": [mod.strip() for mod in modifiers if mod.strip()],
                "place_of_service": place_of_service
            }
            
            try:
                # Make prediction
                with st.spinner("Making prediction..."):
                    result = api.predict_claim(claim_data)
                
                # Display results
                display_prediction_results(result)
                
            except Exception as e:
                st.error(f"Prediction failed: {str(e)}")

def display_prediction_results(result: dict):
    """Display prediction results"""
    
    # Main metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        denial_prob = result["denial_probability"]
        st.metric(
            "Denial Probability",
            f"{denial_prob:.1%}",
            delta=f"{denial_prob - 0.15:.1%}" if denial_prob > 0.15 else None
        )
    
    with col2:
        risk_level = result["risk_level"]
        risk_color = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}
        st.metric("Risk Level", f"{risk_color.get(risk_level, '⚪')} {risk_level}")
    
    with col3:
        st.metric("Model Version", result["model_version"])
    
    # Risk gauge chart
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = denial_prob * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Denial Risk %"},
        delta = {'reference': 15},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig_gauge.update_layout(height=300)
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Risk factors
    st.subheader("Top Risk Factors")
    if result["top_risk_factors"]:
        risk_df = pd.DataFrame(result["top_risk_factors"])
        
        fig_factors = px.bar(
            risk_df,
            x="magnitude",
            y="factor",
            color="impact",
            orientation="h",
            title="Risk Factor Contributions"
        )
        fig_factors.update_layout(height=300)
        st.plotly_chart(fig_factors, use_container_width=True)
    
    # Recommendations
    st.subheader("Recommended Actions")
    for i, action in enumerate(result["recommended_actions"], 1):
        st.write(f"{i}. {action}")

def batch_analysis_page():
    """Batch analysis page"""
    st.header("Batch Claim Analysis")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Claims CSV",
        type=["csv"],
        help="Upload a CSV file with claim data for batch analysis"
    )
    
    if uploaded_file is not None:
        try:
            # Read CSV
            df = pd.read_csv(uploaded_file)
            st.write(f"Loaded {len(df)} claims")
            st.dataframe(df.head())
            
            if st.button("Analyze Claims"):
                # Process batch prediction
                with st.spinner("Processing claims..."):
                    results = process_batch_claims(df)
                
                # Display batch results
                display_batch_results(results)
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

def process_batch_claims(df: pd.DataFrame) -> pd.DataFrame:
    """Process batch claims (simulated)"""
    # In a real implementation, this would call the batch API
    # For now, simulate results
    results = []
    
    for _, row in df.iterrows():
        # Simulate prediction
        denial_prob = np.random.beta(2, 8)  # Skewed toward lower probabilities
        risk_level = "HIGH" if denial_prob > 0.7 else "MEDIUM" if denial_prob > 0.4 else "LOW"
        
        results.append({
            "claim_id": row.get("claim_id", f"CLM_{len(results)}"),
            "denial_probability": denial_prob,
            "risk_level": risk_level,
            "claim_amount": row.get("claim_amount", 1000),
            "provider_id": row.get("provider_id", "PROV_001")
        })
    
    return pd.DataFrame(results)

def display_batch_results(results_df: pd.DataFrame):
    """Display batch analysis results"""
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Claims", len(results_df))
    
    with col2:
        high_risk_count = len(results_df[results_df["risk_level"] == "HIGH"])
        st.metric("High Risk Claims", high_risk_count)
    
    with col3:
        avg_risk = results_df["denial_probability"].mean()
        st.metric("Average Risk", f"{avg_risk:.1%}")
    
    with col4:
        total_amount = results_df["claim_amount"].sum()
        st.metric("Total Amount at Risk", f"${total_amount:,.0f}")
    
    # Risk distribution
    fig_hist = px.histogram(
        results_df,
        x="denial_probability",
        nbins=20,
        title="Risk Distribution",
        labels={"denial_probability": "Denial Probability", "count": "Number of Claims"}
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Risk by provider
    provider_risk = results_df.groupby("provider_id")["denial_probability"].mean().reset_index()
    fig_provider = px.bar(
        provider_risk,
        x="provider_id",
        y="denial_probability",
        title="Average Risk by Provider"
    )
    st.plotly_chart(fig_provider, use_container_width=True)
    
    # Detailed results table
    st.subheader("Detailed Results")
    st.dataframe(results_df.sort_values("denial_probability", ascending=False))

def model_performance_page():
    """Model performance monitoring page"""
    st.header("Model Performance Dashboard")
    
    try:
        # Get performance metrics
        performance = api.get_model_performance()
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Predictions", performance.get("total_predictions", 0))
        
        with col2:
            actual_rate = performance.get("actual_denial_rate", 0)
            st.metric("Actual Denial Rate", f"{actual_rate:.1%}")
        
        with col3:
            pred_rate = performance.get("avg_predicted_probability", 0)
            st.metric("Predicted Rate", f"{pred_rate:.1%}")
        
        with col4:
            feedback_coverage = performance.get("feedback_coverage", 0)
            st.metric("Feedback Coverage", f"{feedback_coverage:.1%}")
        
        # Generate sample performance charts
        generate_performance_charts()
        
    except Exception as e:
        st.error(f"Error loading performance data: {str(e)}")

def generate_performance_charts():
    """Generate sample performance monitoring charts"""
    
    # Sample data for demonstration
    dates = pd.date_range(start="2024-01-01", periods=30, freq="D")
    
    # Model accuracy over time
    accuracy_data = pd.DataFrame({
        "date": dates,
        "accuracy": np.random.normal(0.85, 0.03, 30),
        "auc": np.random.normal(0.88, 0.02, 30)
    })
    
    fig_performance = go.Figure()
    fig_performance.add_trace(go.Scatter(
        x=accuracy_data["date"],
        y=accuracy_data["accuracy"],
        mode="lines+markers",
        name="Accuracy",
        line=dict(color="blue")
    ))
    fig_performance.add_trace(go.Scatter(
        x=accuracy_data["date"],
        y=accuracy_data["auc"],
        mode="lines+markers",
        name="AUC",
        line=dict(color="red")
    ))
    
    fig_performance.update_layout(
        title="Model Performance Over Time",
        xaxis_title="Date",
        yaxis_title="Score",
        height=400
    )
    st.plotly_chart(fig_performance, use_container_width=True)
    
    # Prediction calibration
    prob_bins = np.arange(0, 1.1, 0.1)
    actual_rates = np.random.uniform(0.05, 0.95, len(prob_bins)-1)
    
    fig_calibration = go.Figure()
    fig_calibration.add_trace(go.Scatter(
        x=prob_bins[:-1] + 0.05,
        y=actual_rates,
        mode="markers+lines",
        name="Actual",
        line=dict(color="blue")
    ))
    fig_calibration.add_trace(go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode="lines",
        name="Perfect Calibration",
        line=dict(color="red", dash="dash")
    ))
    
    fig_calibration.update_layout(
        title="Model Calibration",
        xaxis_title="Predicted Probability",
        yaxis_title="Actual Rate",
        height=400
    )
    st.plotly_chart(fig_calibration, use_container_width=True)

def risk_analytics_page():
    """Risk analytics and insights page"""
    st.header("Risk Analytics & Insights")
    
    # Generate sample analytics data
    generate_risk_analytics()

def generate_risk_analytics():
    """Generate risk analytics dashboard"""
    
    # Sample data
    providers = [f"PROV_{i:03d}" for i in range(1, 21)]
    payers = ["Medicare", "Medicaid", "Aetna", "BCBS", "UnitedHealth"]
    
    # Provider risk analysis
    provider_data = pd.DataFrame({
        "provider_id": providers,
        "denial_rate": np.random.beta(2, 8, len(providers)),
        "claim_volume": np.random.poisson(100, len(providers)),
        "avg_amount": np.random.normal(2000, 500, len(providers))
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_provider_risk = px.scatter(
            provider_data,
            x="claim_volume",
            y="denial_rate",
            size="avg_amount",
            hover_data=["provider_id"],
            title="Provider Risk Analysis"
        )
        st.plotly_chart(fig_provider_risk, use_container_width=True)
    
    with col2:
        # Top risk providers
        top_risk = provider_data.nlargest(5, "denial_rate")
        fig_top_risk = px.bar(
            top_risk,
            x="denial_rate",
            y="provider_id",
            orientation="h",
            title="Highest Risk Providers"
        )
        st.plotly_chart(fig_top_risk, use_container_width=True)
    
    # Payer analysis
    payer_data = pd.DataFrame({
        "payer": payers,
        "denial_rate": np.random.beta(2, 6, len(payers)),
        "avg_days_to_pay": np.random.poisson(25, len(payers))
    })
    
    fig_payer = px.bar(
        payer_data,
        x="payer",
        y="denial_rate",
        title="Denial Rates by Payer"
    )
    st.plotly_chart(fig_payer, use_container_width=True)

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

def sidebar_config():
    """Sidebar configuration and settings"""
    st.sidebar.title("Configuration")
    
    # API settings
    st.sidebar.subheader("API Settings")
    api_url = st.sidebar.text_input("API URL", value=API_BASE_URL)
    api_token = st.sidebar.text_input("API Token", value=API_TOKEN, type="password")
    
    # Refresh settings
    st.sidebar.subheader("Refresh Settings")
    auto_refresh = st.sidebar.checkbox("Auto Refresh", value=False)
    refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 30, 300, 60)
    
    # Theme settings
    st.sidebar.subheader("Theme")
    theme = st.sidebar.selectbox("Theme", ["Light", "Dark"])
    
    return {
        "api_url": api_url,
        "api_token": api_token,
        "auto_refresh": auto_refresh,
        "refresh_interval": refresh_interval,
        "theme": theme
    }

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Configure sidebar
    config = sidebar_config()
    
    # Update API client with new settings
    global api
    api = DashboardAPI(config["api_url"], config["api_token"])
    
    # Run main dashboard
    main() 