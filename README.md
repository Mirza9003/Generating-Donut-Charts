# Generating Donut Charts (Publication-Quality)

This repository provides **reproducible Python code** for generating **publication-quality donut (ring) charts** used in environmental modeling and machine-learning–based spatial analysis.

The workflow was developed to support **Flood Susceptibility Mapping (FSM)** studies, where class-wise area proportions (Very Low → Very High) must be visualized clearly and consistently across models.

---

## 📊 Example Output

<p align="center">
  <img src="FIGURE 6 UPDATED.png" width="900">
</p>

**Figure.** Flood susceptibility maps (left) and corresponding class-wise area distributions (right) for Iowa generated using three machine-learning models:
**(a)** XGBoost, **(b)** LightGBM, and **(c)** Histogram Gradient Boosting (HGB).  
FSM classes are categorized as **Very Low, Low, Moderate, High, and Very High**.

---

## 🧠 Features

- Publication-ready **donut charts** (high-resolution, journal compliant)
- Consistent **color scheme** across models and figures
- Inside-ring percentage labels with adaptive contrast
- Supports **single plots** and **multi-panel layouts**
- Designed for **environmental, hydrologic, and GeoAI studies**

---

## 🗂 Repository Structure

```text
.
├── donut_charts.py        # Main script to generate donut charts
├── FIGURE 6 UPDATED.png   # Example output figure (used in README)
└── README.md              # Project documentation

