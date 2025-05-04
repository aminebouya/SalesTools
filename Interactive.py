import streamlit as st
import pandas as pd

# Page configuration (must be the first Streamlit command)
st.set_page_config(page_title="Interactive Slider Model", layout="wide")

# --- Authentication ---
PASSWORD = "PVS101"  # Set your desired password
# Prompt for password in sidebar
st.sidebar.header("Login")
password_input = st.sidebar.text_input("Password", type="password")
if password_input != PASSWORD:
    st.sidebar.error("Invalid password")
    st.stop()

# Global CSS for larger text and inputs
st.markdown(
    """
    <style>
    html, body, [class*=\"css\"] {
        font-size: 20px !important;
    }
    /* Enlarge slider and input labels */
    .stSlider label, .stNumberInput label {
        font-size: 20px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Interactive Slider Model: Revenue & Profit")
st.markdown("Adjust parameters on the left and save scenarios for comparison on the right.")

# Initialize saved scenarios
if "saved_scenarios" not in st.session_state:
    st.session_state.saved_scenarios = []

# Computation function
def compute_metrics(base_price, base_volume, base_cost, fixed_cost,
                    price_change, volume_change, cost_change):
    new_price = base_price * (1 + price_change / 100)
    new_volume = base_volume * (1 + volume_change / 100)
    new_cost = base_cost * (1 + cost_change / 100)
    revenue = new_price * new_volume
    variable_cost = new_cost * new_volume
    profit = revenue - variable_cost - fixed_cost
    return {
        "Base Price": base_price,
        "Base Volume": base_volume,
        "Base Cost": base_cost,
        "Fixed Cost": fixed_cost,
        "Price Change %": price_change,
        "Volume Change %": volume_change,
        "Cost Change %": cost_change,
        "New Price": new_price,
        "New Volume": new_volume,
        "New Cost": new_cost,
        "Revenue": revenue,
        "Variable Cost": variable_cost,
        "Profit": profit
    }

# Layout: two columns
col1, col2 = st.columns([1, 3])

# Metrics to hide from outputs
base_metrics = ["Base Price", "Base Volume", "Base Cost", "Fixed Cost"]

with col1:
    st.header("Inputs & Save")
    # Base parameter inputs
    base_price = st.number_input("Base Price per Unit", min_value=0.0, value=10.0, step=0.1, format="%.2f")
    base_volume = st.number_input("Base Volume", min_value=0.0, value=1000.0, step=10.0, format="%.2f")
    base_cost = st.number_input("Base Cost per Unit", min_value=0.0, value=8.0, step=0.1, format="%.2f")
    fixed_cost = st.number_input("Fixed Cost", min_value=0.0, value=1000.0, step=10.0, format="%.2f")

    # Integer percentage sliders
    price_change = st.slider("Price change (%)", -50, 50, 0, step=1)
    volume_change = st.slider("Volume change (%)", -50, 50, 0, step=1)
    cost_change = st.slider("Cost change (%)", -50, 50, 0, step=1)

    # Compute current scenario
    current = compute_metrics(base_price, base_volume, base_cost, fixed_cost,
                              price_change, volume_change, cost_change)
    # Save button
    if st.button("Save This Scenario"):
        st.session_state.saved_scenarios.append(current)
        st.success("Scenario saved!")

with col2:
    st.subheader("Calculated Outputs")
    # Prepare display: exclude base & percent metrics
    display = {k: v for k, v in current.items() if k not in base_metrics and not k.endswith("%")}
    df_display = pd.DataFrame.from_dict(display, orient='index', columns=['Value'])

    # Formatting
    def fmt_val(metric, val):
        if metric in ["New Price", "New Cost", "Revenue", "Variable Cost", "Profit"]:
            return f"${val:,.2f}"
        if metric.endswith("Volume"):
            return f"{val:,.2f}"
        return val

    df_display['Value'] = [fmt_val(idx, v) for idx, v in df_display['Value'].items()]
    st.table(df_display)

    st.subheader("Comparison of Saved Scenarios")
    if st.session_state.saved_scenarios:
        saved = pd.DataFrame(st.session_state.saved_scenarios)
        saved = saved.drop(columns=base_metrics)
        for col in saved.columns:
            if col in ["New Price", "New Cost", "Revenue", "Variable Cost", "Profit"]:
                saved[col] = saved[col].map(lambda x: f"${x:,.2f}")
            elif col.endswith("%"):
                saved[col] = saved[col].map(lambda x: f"{x}%")
            elif col.endswith("Volume"):
                saved[col] = saved[col].map(lambda x: f"{x:,.2f}")
        saved.index = range(1, len(saved)+1)
        st.table(saved)
    else:
        st.info("No scenarios saved yet. Use the left panel to save your first scenario.")

st.markdown("---")
