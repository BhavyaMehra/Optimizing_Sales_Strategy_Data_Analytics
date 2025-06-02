# Optimizing Sales Strategies – Data Analyst Certification Project

This project was completed as part of the **Data Analyst Certification on DataCamp**, simulating a real-world business scenario. It analyzes sales data for a company selling **pens and printers**, with the goal of identifying the **most effective sales strategy** to boost revenue and optimize resource allocation.

---

## Project Overview

The company currently uses three sales strategies:

| Sales Strategy     | Description                              | Avg. Call Time |
|--------------------|------------------------------------------|----------------|
| **Email**          | Only email communication                 | 0 mins         |
| **Call**           | Only phone call outreach                 | 30 mins        |
| **Email + Call**   | Email followed by a phone call           | 10 mins        |

Management seeks to scale the most effective strategy across regions, reduce inefficiencies, and improve targeting.

---

## Objectives

- **Identify** which strategy yields the highest **Revenue per Customer**
- **Uncover** regional trends to inform where marketing should focus
- **Design** a simple metric to monitor sales performance
- **Support** decisions with clear, actionable insights

---

## Techniques Used

- **Data Cleaning & Validation** (handled missing values, standardized strategy labels)
- **Exploratory Data Analysis** using `pandas`, `matplotlib`, and `seaborn`
- **Group-by Aggregation** for strategy and region comparisons
- **Custom KPI Definition**: Revenue per Customer
- **Data Visualization** to communicate trends

---

## Key Findings

| Strategy        | Revenue Share | Revenue per Customer | Avg. Call Time |
|----------------|----------------|-----------------------|----------------|
| **Email**       | 50%            | $97                   | 0 mins         |
| **Call**        | 33%            | $50                   | 30 mins        |
| **Email + Call**| 17%            | $171                  | 10 mins        |

- **Email + Call** had the **highest revenue efficiency** despite fewer customers.
- **Email-only** led in volume but had declining efficiency.
- **Call-only** had the lowest revenue per customer and the highest time cost.
- **67% of total revenue** came from just 7 states (e.g., CA, TX, NY) – indicating **regional concentration**.

---

## Final Recommendations

- **Scale** Email + Call strategy for **high-value customers**
- ✉**Enhance** Email campaigns (personalization, timing, content)
- **Target** top 7 states with focused campaigns
- **Reduce** reliance on Call-only outreach due to low ROI
- **Track** Revenue per Customer as the primary performance metric

---

## Tools & Technologies

- **Python**: `pandas`, `matplotlib`, `seaborn`
- **Jupyter Notebook**
- **Microsoft PowerPoint** (for presentation)
