import streamlit as st
import pandas as pd

# Page configuration (must be first Streamlit call)
st.set_page_config(page_title="Interactive Slider Model", layout="wide")

# Global CSS for responsive layout and larger text
st.markdown(
    """
    <style>
      .block-container {
        max-width: 95% !important;
        padding: 1rem !important;
      }
      html, body, [class*="css"] {
        font-size: 28px !important;
      }
      .stSlider span {
        font-size: 32px !important;
      }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Interactive Slider Model: Revenue & Profit")
st.markdown("Adjust parameters on the left and save or reset scenarios on the right.")

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
        "New Price": new_price,
        "New Volume": new_volume,
        "New Cost": new_cost,
        "Revenue": revenue,
        "Variable Cost": variable_cost,
        "Profit": profit
    }

# Layout: inputs (left) and outputs & saved scenarios (right)
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Inputs & Reset/Save")

    # Base Price per Unit
    st.markdown("<div style='font-size:26px; font-weight:bold;'>Base Price per Unit</div>", unsafe_allow_html=True)
    base_price = st.number_input(
        "Base Price per Unit", 0.0, 1e6, 10.0, 1.0,
        format="%.0f", key="base_price", label_visibility="hidden"
    )

    # Base Volume
    st.markdown("<div style='font-size:26px; font-weight:bold;'>Base Volume</div>", unsafe_allow_html=True)
    base_volume = st.number_input(
        "Base Volume", 0.0, 1e6, 1000.0, 10.0,
        format="%.0f", key="base_volume", label_visibility="hidden"
    )

    # Base Cost per Unit
    st.markdown("<div style='font-size:26px; font-weight:bold;'>Base Cost per Unit</div>", unsafe_allow_html=True)
    base_cost = st.number_input(
        "Base Cost per Unit", 0.0, 1e6, 8.0, 1.0,
        format="%.0f", key="base_cost", label_visibility="hidden"
    )

    # Fixed Cost
    st.markdown("<div style='font-size:26px; font-weight:bold;'>Fixed Cost</div>", unsafe_allow_html=True)
    fixed_cost = st.number_input(
        "Fixed Cost", 0.0, 1e6, 1000.0, 10.0,
        format="%.0f", key="fixed_cost", label_visibility="hidden"
    )

    # Price change (%) slider
    st.markdown("<div style='font-size:26px; font-weight:bold;'>Price change (%)</div>", unsafe_allow_html=True)
    price_change = st.slider(
        "Price change (%)", -50, 50, 0, 1,
        key="price_change", label_visibility="hidden"
    )

    # Volume change (%) slider
    st.markdown("<div style='font-size:26px; font-weight:bold;'>Volume change (%)</div>", unsafe_allow_html=True)
    volume_change = st.slider(
        "Volume change (%)", -50, 50, 0, 1,
        key="volume_change", label_visibility="hidden"
    )

    # Cost change (%) slider
    st.markdown("<div style='font-size:26px; font-weight:bold;'>Cost change (%)</div>", unsafe_allow_html=True)
    cost_change = st.slider(
        "Cost change (%)", -50, 50, 0, 1,
        key="cost_change", label_visibility="hidden"
    )

    # Compute metrics based on inputs
    metrics_input = compute_metrics(
        base_price, base_volume, base_cost, fixed_cost,
        price_change, volume_change, cost_change
    )

    # Buttons: Save and Reset
    btn1, btn2 = st.columns(2)
    with btn1:
        if st.button("Save This Scenario"):
            st.session_state.saved_scenarios.append(metrics_input)
            st.success("Scenario saved!")
    with btn2:
        if st.button("Reset"):
            st.session_state.saved_scenarios = []
            st.success("Saved scenarios cleared!")

with col2:
    st.subheader("Calculated Outputs")
    display = metrics_input
    def fmt(metric, val):
        if metric in ["New Price", "New Cost", "Revenue", "Variable Cost", "Profit"]:
            return f"${val:,.0f}"
        if metric.endswith("Volume"):
            return f"{val:,.0f}"
        return val

    # Table at half width
    html = (
        '<div style="overflow-x:auto;">'
        '<table style="width:50%;border-collapse:collapse;font-size:26px;">'
    )
    html += (
        '<tr><th style="text-align:left;padding:8px;">Metric</th>'
        '<th style="text-align:right;padding:8px;">Value</th></tr>'
    )
    for metric, val in display.items():
        html += (
            f'<tr><td style="font-weight:bold;padding:8px;">{metric}</td>'
            f'<td style="text-align:right;padding:8px;">{fmt(metric, val)}</td></tr>'
        )
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
        # Render HTML table for saved scenarios
        html_saved = (
            '<div style="overflow-x:auto;">'
            '<table style="width:100%;border-collapse:collapse;font-size:26px;">'
        )
        html_saved += '<tr>'
        for col in saved_df.columns:
            html_saved += (
                f'<th style="padding:8px;border:1px solid #ddd;text-align:center;">{col}</th>'
            )
        html_saved += '</tr>'
        for idx, row in saved_df.iterrows():
            style = 'font-weight:bold;' if idx == 0 else ''
            html_saved += f'<tr style="{style}">'
            for col in saved_df.columns:
                html_saved += (
                    f'<td style="padding:8px;border:1px solid #ddd;text-align:center;">{row[col]}</td>'
                )
            html_saved += '</tr>'
        html_saved += '</table></div>'
        st.markdown(html_saved, unsafe_allow_html=True)
    else:
        st.info("No scenarios saved yet. Use the left panel to save your first scenario.")

st.markdown("---")
