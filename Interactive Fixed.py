import streamlit as st
import pandas as pd

# Page configuration (must be the first Streamlit call)
st.set_page_config(page_title="Interactive Slider Model", layout="wide")

# Global CSS for responsive layout and moderate text sizes
st.markdown(
    """
    <style>
      /* Limit container width and padding */
      .block-container {
        max-width: 95% !important;
        padding: 1rem !important;
      }
      /* Base font size for all Streamlit text */
      html, body, [class*="css"] {
        font-size: 16px !important;
      }
      /* Slider tick and tooltip sizes */
      .stSlider span {
        font-size: 14px !important;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("Interactive Slider Model: Revenue & Profit")
st.markdown("Adjust parameters on the left and save or reset scenarios on the right.")

# Initialize saved scenarios in session state
if "saved_scenarios" not in st.session_state:
    st.session_state.saved_scenarios = []

# Function to compute metrics
def compute_metrics(base_price, base_volume, base_cost, fixed_cost,
                    price_change, volume_change, cost_change):
    new_price = base_price * (1 + price_change / 100)
    new_volume = base_volume * (1 + volume_change / 100)
    new_cost = base_cost * (1 + cost_change / 100)
    revenue = new_price * new_volume
    variable_cost = new_cost * new_volume
    profit = revenue - variable_cost - fixed_cost
    return {
        "New Price": new_price,
        "New Volume": new_volume,
        "New Cost": new_cost,
        "Revenue": revenue,
        "Variable Cost": variable_cost,
        "Profit": profit
    }

# Layout: left column for inputs, right for outputs & saved scenarios
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Inputs & Reset/Save")
    # Custom labels at moderate size
    st.markdown("<div style='font-size:16px; font-weight:bold;'>Base Price per Unit</div>", unsafe_allow_html=True)
    base_price = st.number_input(
        "Base Price per Unit", min_value=0.0, value=10.0, step=1.0,
        format="%.0f", key="base_price", label_visibility="hidden"
    )

    st.markdown("<div style='font-size:16px; font-weight:bold;'>Base Volume</div>", unsafe_allow_html=True)
    base_volume = st.number_input(
        "Base Volume", min_value=0.0, value=1000.0, step=10.0,
        format="%.0f", key="base_volume", label_visibility="hidden"
    )

    st.markdown("<div style='font-size:16px; font-weight:bold;'>Base Cost per Unit</div>", unsafe_allow_html=True)
    base_cost = st.number_input(
        "Base Cost per Unit", min_value=0.0, value=8.0, step=1.0,
        format="%.0f", key="base_cost", label_visibility="hidden"
    )

    st.markdown("<div style='font-size:16px; font-weight:bold;'>Fixed Cost</div>", unsafe_allow_html=True)
    fixed_cost = st.number_input(
        "Fixed Cost", min_value=0.0, value=1000.0, step=10.0,
        format="%.0f", key="fixed_cost", label_visibility="hidden"
    )

    st.markdown("<div style='font-size:16px; font-weight:bold;'>Price change (%)</div>", unsafe_allow_html=True)
    price_change = st.slider(
        "Price change (%)", -50, 50, 0, 1,
        key="price_change", label_visibility="hidden"
    )

    st.markdown("<div style='font-size:16px; font-weight:bold;'>Volume change (%)</div>", unsafe_allow_html=True)
    volume_change = st.slider(
        "Volume change (%)", -50, 50, 0, 1,
        key="volume_change", label_visibility="hidden"
    )

    st.markdown("<div style='font-size:16px; font-weight:bold;'>Cost change (%)</div>", unsafe_allow_html=True)
    cost_change = st.slider(
        "Cost change (%)", -50, 50, 0, 1,
        key="cost_change", label_visibility="hidden"
    )

    # Compute current scenario metrics
    metrics_input = compute_metrics(
        base_price, base_volume, base_cost, fixed_cost,
        price_change, volume_change, cost_change
    )

    # Action buttons
    btn_save, btn_reset = st.columns(2)
    with btn_save:
        if st.button("Save This Scenario"):
            st.session_state.saved_scenarios.append(metrics_input)
            st.success("Scenario saved!")
    with btn_reset:
        if st.button("Reset"):
            st.session_state.saved_scenarios = []
            st.success("Saved scenarios cleared!")

with col2:
    st.subheader("Calculated Outputs")
    display = metrics_input
    # Formatting helper
    def fmt(metric, val):
        if metric in ["New Price", "New Cost", "Revenue", "Variable Cost", "Profit"]:
            return f"${val:,.0f}"
        if metric.endswith("Volume"):
            return f"{val:,.0f}"
        return val

    # Build HTML table at 50% width
    html = '<div style="overflow-x:auto;"><table style="width:50%;border-collapse:collapse;font-size:16px;">'
    html += '<tr><th style="text-align:left;padding:6px;">Metric</th><th style="text-align:right;padding:6px;">Value</th></tr>'
    for metric, val in display.items():
        html += f'<tr><td style="font-weight:bold;padding:6px;">{metric}</td><td style="text-align:right;padding:6px;">{fmt(metric, val)}</td></tr>'
    html += '</table></div>'
    st.markdown(html, unsafe_allow_html=True)

    st.subheader("Saved Scenarios")
    if st.session_state.saved_scenarios:
        saved_df = pd.DataFrame(st.session_state.saved_scenarios)
        for col in saved_df.columns:
            if col in ["New Price", "New Cost", "Revenue", "Variable Cost", "Profit"]:
                saved_df[col] = saved_df[col].map(lambda x: f"${x:,.0f}")
            elif col.endswith("Volume"):
                saved_df[col] = saved_df[col].map(lambda x: f"{x:,.0f}")
        html_saved = '<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:16px;">'
        html_saved += '<tr>' + ''.join(f'<th style="padding:6px;border:1px solid #ddd;text-align:center;">{col}</th>' for col in saved_df.columns) + '</tr>'
        for idx, row in saved_df.iterrows():
            style = 'font-weight:bold;' if idx == 0 else ''
            html_saved += f'<tr style="{style}">' + ''.join(
                f'<td style="padding:6px;border:1px solid #ddd;text-align:center;">{row[col]}</td>' for col in saved_df.columns
            ) + '</tr>'
        html_saved += '</table></div>'
        st.markdown(html_saved, unsafe_allow_html=True)
    else:
        st.info("No scenarios saved yet. Use the left panel to save your first scenario.")

st.markdown("---")
