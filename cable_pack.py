import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("🔌 Cable Packing in a Circular Duct")

# Sidebar Inputs
duct_diameter = st.number_input("Enter the Duct Diameter (mm)", min_value=10, value=60)
cable_diameter = st.number_input("Enter the Cable Diameter (mm)", min_value=1.0, value=6.0)
gap = st.number_input("Enter the Gap Between Cables (mm)", min_value=0.0, value=1.0)

# Derived values
duct_radius = duct_diameter / 2
cable_radius = cable_diameter / 2
spacing = cable_diameter + gap

# Packing logic
cables = []
y = -duct_radius + cable_radius
while y <= duct_radius - cable_radius:
    x = -duct_radius + cable_radius
    while x <= duct_radius - cable_radius:
        if np.sqrt(x**2 + y**2) + cable_radius <= duct_radius:
            cables.append((x, y))
        x += spacing
    y += spacing

# Area Calculations
cable_area = len(cables) * np.pi * (cable_radius ** 2)
duct_area = np.pi * (duct_radius ** 2)
utilization = (cable_area / duct_area) * 100

# Results
st.subheader("📊 Packing Summary")
st.write(f"**Number of Cables**: {len(cables)}")
st.write(f"**Total Cable Area**: {cable_area:.2f} mm²")
st.write(f"**Duct Area**: {duct_area:.2f} mm²")
st.write(f"**Utilization**: {utilization:.2f}%")

if utilization <= 40:
    st.success("✅ Cable utilization is under the 40% limit.")
else:
    st.error("⚠️ Cable area must be ≤ 40% of the duct's internal cross-sectional area.")

# Plotting
fig, ax = plt.subplots(figsize=(6, 6))
duct_circle = plt.Circle((0, 0), duct_radius, color='black', fill=False, linewidth=1, label=f"Duct {duct_diameter} mm")
ax.add_patch(duct_circle)

for (x, y) in cables:
    cable_circle = plt.Circle((x, y), cable_radius, color='orange', fill=True)
    ax.add_patch(cable_circle)

summary_text = (
    f"Cables: {len(cables)}\n"
    f"Utilization: {utilization:.2f}%"
)
box_color = 'lightgreen' if utilization <= 40 else 'lightcoral'
ax.text(-duct_radius, duct_radius + 5, summary_text, fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle="round", facecolor=box_color, edgecolor='gray'))

ax.set_aspect('equal')
ax.set_xlim(-duct_radius - 10, duct_radius + 10)
ax.set_ylim(-duct_radius - 10, duct_radius + 10)
ax.set_title("Cable Packing Layout")
ax.axis('off')

st.pyplot(fig)
