import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import json

# Must be the first Streamlit command
st.set_page_config(
    page_title="ProphetReal | World Edition v3.5",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Obsidian & Gold Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    .stApp { background-color: #0d0f12; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: #d4af37 !important; }
    div.stMetric > div { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(212, 175, 55, 0.2); border-radius: 12px; padding: 20px; }
    .stButton > button { background: linear-gradient(135deg, #d4af37, #aa8c2c); color: #000; font-weight: bold; border: none; border-radius: 8px; width: 100%; transition: 0.3s; }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(212, 175, 55, 0.4); }
    [data-testid="stSidebar"] { background-color: #15181d; border-right: 1px solid rgba(212, 175, 55, 0.1); }
    .roi-card { background: rgba(212, 175, 55, 0.05); border: 1px dashed #d4af37; border-radius: 10px; padding: 15px; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000"

st.sidebar.title("💎 ProphetReal")
st.sidebar.markdown("---")
market_region = st.sidebar.selectbox("Market Engine", ["India (INR)", "Global (USD)"])

st.title(f"🌍 ProphetReal : {market_region} Property Intelligence")
st.markdown("### Advanced Predictive Engine & ROI Analytics")

tab1, tab2 = st.tabs(["🎯 Valuation Engine", "⚖️ Renovation ROI Simulator"])

with tab1:
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.subheader("Property Specifications")
        with st.form("spec_form"):
            if market_region == "India (INR)":
                bhk = st.number_input("BHK", 1, 10, 3)
                sqft = st.number_input("Sqft Area", 350.0, 10000.0, 1500.0)
                bathrooms = st.number_input("Bathrooms", 1, 6, 2)
                balconies = st.number_input("Balconies", 0, 5, 2)
                city_tier = st.selectbox("City Tier", ["Tier 1 (Metro)", "Tier 2", "Tier 3"])
                location_type = st.selectbox("Location Type", ["City Center", "Suburbs", "Outskirts", "Tech Park"])
                furnishing = st.selectbox("Furnishing", ["Unfurnished", "Semi-Furnished", "Fully Furnished"])
                age = st.number_input("Property Age (Years)", 0, 50, 5)
                backup = st.selectbox("Power Backup", ["Yes", "No"])
                security = st.selectbox("Gated Security", ["Yes", "No"])
                parking = st.number_input("Parking Spaces", 0, 4, 1)
                metro_dist = st.slider("Distance to Metro (km)", 0.0, 20.0, 1.5)
                clubhouse = st.selectbox("Clubhouse Access", ["Yes", "No"])
                
                payload = {
                    "BHK": bhk, "SqftArea": sqft, "Bathrooms": bathrooms, "Balconies": balconies,
                    "CityTier": city_tier, "LocationType": location_type, "Furnishing": furnishing,
                    "PropertyAge": age, "PowerBackup": backup, "GatedSecurity": security,
                    "ParkingSpaces": parking, "MetroDistance": metro_dist, "Clubhouse": clubhouse
                }
                endpoint = "/predict/india"
                currency_symbol = "₹"
            else:
                lot_area = st.number_input("Lot Area (sq ft)", 1000.0, 100000.0, 5000.0)
                gr_liv_area = st.number_input("Living Area (sq ft)", 500.0, 10000.0, 1500.0)
                overall_qual = st.slider("Overall Quality (1-10)", 1, 10, 6)
                overall_cond = st.slider("Overall Condition (1-10)", 1, 10, 5)
                year_built = st.number_input("Year Built", 1900, 2025, 2010)
                full_bath = st.number_input("Full Baths", 1, 6, 2)
                half_bath = st.number_input("Half Baths", 0, 4, 0)
                garage_cars = st.number_input("Garage Cars", 0, 6, 2)
                neighborhood = st.selectbox("Neighborhood", ["UrbanCenter", "SuburbanGreen", "RuralPlain", "LuxuryHeights"])
                kitchen_qual = st.selectbox("Kitchen Quality", ["Fa", "TA", "Gd", "Ex"])
                smart_home = st.selectbox("Smart Home Features", ["Yes", "No"])
                basement = st.number_input("Basement Area (sq ft)", 0.0, 5000.0, 0.0)
                eco = st.selectbox("Eco Certified", ["Yes", "No"])
                
                payload = {
                    "LotArea": lot_area, "OverallQual": overall_qual, "OverallCond": overall_cond,
                    "YearBuilt": year_built, "GrLivArea": gr_liv_area, "FullBath": full_bath,
                    "HalfBath": half_bath, "GarageCars": garage_cars, "Neighborhood": neighborhood,
                    "KitchenQual": kitchen_qual, "SmartHome": smart_home, "BasementArea": basement,
                    "EcoCertified": eco
                }
                endpoint = "/predict/global"
                currency_symbol = "$"
                
            submit = st.form_submit_button("Generate Valuation")

    with col2:
        st.subheader("Intelligence Output")
        if submit:
            with st.spinner("Sentinel AI analyzing market trends..."):
                try:
                    res = requests.post(f"{API_URL}{endpoint}", json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        price = data['predicted_price']
                        
                        # Formatting
                        if data['currency'] == "INR":
                            display_price = f"₹{price/10000000:.2f} Cr" if price >= 10000000 else f"₹{price/100000:.2f} L"
                        else:
                            display_price = f"${price:,.0f}"
                        
                        st.metric(label=f"Predicted Valuation", value=display_price)
                        
                        # Importance Chart
                        imp_data = data['importance']
                        fig = go.Figure(go.Bar(
                            x=list(imp_data.values()),
                            y=list(imp_data.keys()),
                            orientation='h',
                            marker_color='#d4af37'
                        ))
                        fig.update_layout(
                            title="Feature Impact Breakdown",
                            height=300,
                            margin=dict(l=20, r=20, t=40, b=20),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color="#e0e0e0")
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        st.markdown("### 🤖 Sentinel Insights")
                        for insight in data['insights']:
                            st.info(f"💡 {insight}")
                    else:
                        st.error(f"API Error: {res.status_code}")
                except Exception as e:
                    st.error(f"Connection Failed: {e}")
        else:
            st.info("👈 Enter property details and launch the agent to see analysis.")

with tab2:
    st.subheader("Strategize Your Upgrades")
    st.markdown("Select potential renovations to see how they impact your property's market value.")
    
    if 'last_payload' not in st.session_state:
        st.warning("Please run a valuation in Tab 1 first to load base property data.")
    else:
        base_payload = st.session_state['last_payload']
        base_price = st.session_state['last_price']
        
        col_a, col_b = st.columns([1, 1])
        
        with col_a:
            st.markdown("#### Potential Upgrades")
            if market_region == "India (INR)":
                upgrade_security = st.checkbox("Add Gated Security (CCTV/Guard)")
                upgrade_furnishing = st.checkbox("Convert to Fully Furnished")
                upgrade_backup = st.checkbox("Install 24/7 Power Backup")
                
                # Create modified payload
                mod_payload = base_payload.copy()
                if upgrade_security: mod_payload["GatedSecurity"] = "Yes"
                if upgrade_furnishing: mod_payload["Furnishing"] = "Fully Furnished"
                if upgrade_backup: mod_payload["PowerBackup"] = "Yes"
                sim_endpoint = "/predict/india"
            else:
                upgrade_smart = st.checkbox("Install Full Smart Home System")
                upgrade_eco = st.checkbox("Obtain Eco-Certification")
                upgrade_qual = st.slider("Improve Overall Quality to:", int(base_payload["OverallQual"]), 10, int(base_payload["OverallQual"]))
                
                mod_payload = base_payload.copy()
                if upgrade_smart: mod_payload["SmartHome"] = "Yes"
                if upgrade_eco: mod_payload["EcoCertified"] = "Yes"
                mod_payload["OverallQual"] = upgrade_qual
                sim_endpoint = "/predict/global"

            if st.button("Simulate ROI"):
                try:
                    res = requests.post(f"{API_URL}{sim_endpoint}", json=mod_payload)
                    if res.status_code == 200:
                        new_price = res.json()['predicted_price']
                        delta = new_price - base_price
                        
                        st.session_state['sim_price'] = new_price
                        st.session_state['sim_delta'] = delta
                    else:
                        st.error("Simulation failed.")
                except Exception as e:
                    st.error(f"Error: {e}")

        with col_b:
            if 'sim_price' in st.session_state:
                st.markdown("#### Simulation Results")
                delta = st.session_state['sim_delta']
                
                if market_region == "India (INR)":
                    display_delta = f"₹{delta/100000:.2f} L"
                else:
                    display_delta = f"${delta:,.0f}"
                
                st.metric("Estimated Value Increase", value=display_delta, delta=display_delta)
                
                # ROI Gauge
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = st.session_state['sim_price'],
                    title = {'text': "New Valuation"},
                    gauge = {
                        'axis': {'range': [None, base_price * 1.5]},
                        'bar': {'color': "#d4af37"},
                        'steps': [
                            {'range': [0, base_price], 'color': "rgba(255,255,255,0.1)"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': base_price
                        }
                    }
                ))
                fig_gauge.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#e0e0e0"))
                st.plotly_chart(fig_gauge, use_container_width=True)
                
                st.markdown(f"""
                <div class='roi-card'>
                    <strong>Sentinel Advisory:</strong> 
                    Based on market trends, these upgrades could potentially yield a { (delta/base_price)*100 :.1f}% 
                    increase in property equity.
                </div>
                """, unsafe_allow_html=True)

# Save session state for ROI simulator
if submit and 'data' in locals():
    st.session_state['last_payload'] = payload
    st.session_state['last_price'] = data['predicted_price']

st.sidebar.markdown("---")
st.sidebar.caption("ProphetReal v3.5 | World Edition")
st.sidebar.caption("© 2026 Property Intelligence Systems")
