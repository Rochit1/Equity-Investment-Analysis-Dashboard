# 📊 Equity Investment Analysis Dashboard

![image alt](https://github.com/Rochit1/Equity-Investment-Analysis-Dashboard/blob/db92db1657563481321770596869f688935f05ee/Screenshots/Executive%20Overview.png)

An interactive Power BI dashboard built to analyze publicly listed Indian companies across the Energy and Metal sectors. The dashboard transforms raw financial data into meaningful business insights through interactive visualizations, DAX calculations, peer benchmarking, and a custom investment scoring model.

---

# 🚀 Project Overview

This project was inspired by my exposure to equity markets during my internship at Arihant Capital. To deepen my understanding of financial analysis and business intelligence, I developed an end-to-end Power BI dashboard that enables users to explore company fundamentals, compare sector performance, analyze peer groups, and identify investment opportunities using publicly available financial data.

The dashboard follows a complete analytical workflow—from executive summaries to detailed company analysis and finally actionable business insights.

---

# 🎯 Business Objectives

- Analyze financial performance across Energy and Metal sector companies.
- Compare sector-level financial metrics.
- Evaluate individual company fundamentals.
- Perform peer-to-peer valuation comparison.
- Build an investment screener using custom scoring metrics.
- Present financial insights through an interactive dashboard.

---

# 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| **Power BI** | Dashboard Development |
| **Power Query** | Data Cleaning & Transformation |
| **DAX** | Business Logic & Financial Measures |
| **Excel** | Data Collection & Preparation |
| **NSE India** | Financial Data Source |
| **Screener.in** | Company Financial Metrics |
| **Python** | Optional data validation & cleaning layer |

---

# 📂 Dashboard Pages

## 📄 Page 1 – Executive Overview

Provides a high-level snapshot of the Energy and Metal sectors.

### Features
- Executive KPI Cards
- Market Capitalization Analysis
- Revenue & Profit Overview
- Average PE & ROE
- Sector Distribution
- Interactive Navigation

![Executive Overview](Screenshots/Executive%20Overview.png)

---

## 📄 Page 2 – Sector Analysis

Compares the overall financial performance of both sectors.

### Features
- Revenue Comparison
- Net Profit Comparison
- Return on Equity (ROE)
- Debt-to-Equity Ratio
- Dividend Yield
- PE Ratio Comparison

![Sector Analysis](Screenshots/Sector%20Analysis.png)

---

## 📄 Page 3 – Company Deep Dive

Allows users to explore a selected company in detail.

### Features
- Company Profile
- Revenue & Profit Trends
- Financial KPI Cards
- Ownership Breakdown
- Dynamic Peer Comparison
- Company-Level Analysis

![Company Deep Dive](Screenshots/Company%20Deep%20Dive.png)

---

## 📄 Page 4 – Investment Screener

Ranks companies using a custom investment scoring framework.

### Features
- Overall Investment Score
- Quality Score
- Value Score
- Growth Score
- Company Ranking
- Conditional Formatting

![Investment Screener](Screenshots/Investment%20Screener.png)

---

## 📄 Page 5 – Financial Health

Assesses bankruptcy/distress risk for each company using the Altman Z-Score model.

### Features
- Company Selector
- Z-Score Components (X1-X5)
- Final Z-Score & Health Status (Safe/Grey/Distress)
- Market Cap vs Debt Comparison
- Z-Score by Company
- Peer Comparison on Z-Score

![Key Insights](Screenshots/Financial%20Health.png)

---

## 📄 Page 6 – Key Insights

Summarizes the major findings from the dashboard.

### Features
- Sector Scale Analysis
- Profitability Insights
- Valuation Observations
- Top Ranked Companies
- Business Summary & Conclusions

![Key Insights](Screenshots/Key%20Insights.png)

---

# 📊 Key Financial Metrics

The dashboard analyzes multiple financial indicators including:

- Market Capitalization
- Revenue
- Net Profit
- Price-to-Earnings (PE) Ratio
- Return on Equity (ROE)
- Earnings Per Share (EPS)
- Dividend Yield
- Debt-to-Equity Ratio
- Promoter Holding
- FII Holding
- Overall Investment Score
- Altman Z-Score & Financial Health Status

---

🐍 Optional Python Data Preparation Layer

Alongside the Power BI dashboard, this project includes a small, optional Python-based data validation and cleaning layer in the python/ folder. It reads the same source workbook the dashboard uses, validates and cleans every sheet (missing values, duplicates, missing key columns, implausible negative figures), and writes standardized CSV output — demonstrating a pathway toward automated data preparation.

This does not make the dashboard real-time or live. The dashboard continues to use a fixed, historical data snapshot, exactly as described above. The Python layer is a standalone, on-demand script — see python/README.md for full details on what it does, how to run it, and how it could support periodic automated refresh in the future.

---

# 📈 DAX Concepts Used

This project utilizes several DAX concepts to build dynamic and interactive reports.

- CALCULATE()
- FILTER()
- DIVIDE()
- SWITCH()
- VAR
- SELECTEDVALUE()
- REMOVEFILTERS()
- TREATAS()
- SUMX()

---

# 💼 Business Questions Answered

This dashboard helps answer questions such as:

- Which sector performs better financially?
- Which companies generate the highest revenue and profit?
- Which companies appear undervalued based on PE ratio?
- How does a selected company compare with its peers?
- Which companies rank highest using quality, value, and growth metrics?
- What are the key insights derived from the analyzed dataset?

---

# ✨ Key Features

- Interactive Dashboard Navigation
- Dynamic Company & Sector Selection
- Executive KPI Dashboard
- Sector-wise Financial Analysis
- Company Deep Dive
- Dynamic Peer Comparison
- Investment Screener
- Business Insights & Recommendations
- Professional Dashboard Design
- Storytelling with Financial Data

---

# 📁 Project Structure

```
Equity-Investment-Analysis-Dashboard
│
├── Dashboard
│   └── Equity Investment Dashboard.pbix
│
├── Dataset
│   └── Equity Investment Dataset.xlsx
│
├── python
│   ├── data_cleaning.py
│   ├── data_pipeline.py
│   ├── data_source_optional.py
│   ├── requirements.txt
│   └── README.md
│
├── Screenshots
│   ├── Executive Overview.png
│   ├── Sector Analysis.png
│   ├── Company Deep Dive.png
│   ├── Investment Screener.png
│   ├── Financial Health.png
│   └── Key Insights.png
│
├── README.md
├── LICENSE
└── .gitignore
```

---

# 📚 Data Sources

Financial data was collected from publicly available sources:

- NSE India
- Screener.in

> **Disclaimer:** This dashboard has been developed solely for educational, analytical, and portfolio purposes. It should not be considered investment advice.

---

# 🎓 Skills Demonstrated

- Power BI Dashboard Development
- Data Modeling
- Power Query (ETL)
- DAX Programming
- Financial Analysis
- Business Intelligence
- KPI Design
- Interactive Report Development
- Data Visualization
- Investment Research
- Storytelling with Data

---

# 👨‍💻 Author

**Rochit Surana**
**Ishika Chhajed**

---

## ⭐ If you found this project interesting, consider giving it a star!
