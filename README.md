# 📊 E-Commerce Sales Analysis & Dashboard

A complete end-to-end analytics project analyzing 10,000+ retail transactions to identify revenue drivers, customer lifetime value, delivery impact, and discount effectiveness. Production-ready with interactive dashboard, comprehensive KPIs, and business insights.

🧠 Problem Statement

In the current data-driven ecommerce ecosystem, businesses struggle to transform large volumes of transactional data into meaningful strategic insights. This project addresses the need to evaluate customer purchase behavior, revenue trends, and product performance to help businesses optimize marketing, inventory, and customer engagement strategies.

*⭐ Project Highlight:* Achieved 20% profit improvement recommendations through data-driven decision making.

---

## 🎯 Objective

Analyze retail transaction data to:
- ✅ Identify revenue drivers and high-value customer segments
- ✅ Calculate Customer Lifetime Value (CLV) and retention metrics
- ✅ Measure impact of delivery delays on customer retention
- ✅ Evaluate discount strategy effectiveness
- ✅ Provide actionable business insights with quantified ROI

---

## 📊 Dataset

*Source:* Superstore Sales Dataset (Kaggle)  
*Size:* 10,000+ transactions | 21 columns | 4 years of data  
*Time Period:* Jan 2014 - Dec 2017  

*Key Columns:*
- Order & Shipping: Order Date, Ship Date, Delivery Days
- Financial: Sales, Profit, Discount, Quantity
- Geography: Region, State, City
- Product: Category, Sub-Category, Product Name
- Customer: Customer ID, Customer Segment

---

## 🛠️ Tools & Technologies

| Component | Technology |
|-----------|-----------|
| *Data Processing* | Python 3.9+, Pandas, NumPy |
| *Visualization* | Seaborn, Matplotlib, Plotly |
| *Dashboard* | Streamlit |
| *Analysis* | Scikit-learn, Statistical methods |
| *Environment* | Jupyter Notebook, VS Code |

---

## 📁 Project Structure


Ecommerce-Analytics/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
│
├── data/
│   ├── raw/
│   │   └── superstore.csv             # Original dataset
│   └── processed/
│       ├── superstore_cleaned.csv     # Cleaned data with features
│       └── kpis.csv                   # Calculated KPIs
│
├── notebooks/
│   ├── 01_data_cleaning_and_features.ipynb  # Phase 2-3: Data prep & engineering
│   └── 02_eda_and_kpis.ipynb               # Phase 4-5: EDA & KPI analysis
│
├── dashboard/
│   └── app.py                         # Phase 6: Interactive Streamlit dashboard
│
├── reports/
│   ├── business_insights.md           # Phase 7: Strategic insights & recommendations
│   └── *.png                          # EDA visualizations
│
└── scripts/
    └── [future] Scheduled analysis jobs


---

## 🚀 Quick Start

### 1️⃣ *Installation*

bash
# Clone repository
git clone https://github.com/yourusername/Ecommerce-Analytics.git
cd Ecommerce-Analytics

# Create virtual environment (optional but recommended)
python -m venv env
source env/Scripts/activate  # Windows
# or
source env/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt


### 2️⃣ *Run Data Processing*

bash
jupyter notebook notebooks/01_data_cleaning_and_features.ipynb
# Execute all cells to:
# - Clean data (handle missing values, duplicates, outliers)
# - Create engineered features
# - Save cleaned data to data/processed/


### 3️⃣ *Run EDA & KPI Analysis*

bash
jupyter notebook notebooks/02_eda_and_kpis.ipynb
# Execute all cells to:
# - Answer all mandatory analysis questions
# - Generate visualizations (saved to reports/)
# - Calculate 11 key performance indicators


### 4️⃣ *Launch Interactive Dashboard*

bash
cd dashboard
streamlit run app.py


Dashboard will open at: http://localhost:8501

---

## 👥 Author
*Veenashree B*  
💼 [LinkedIn Profile](https://www.linkedin.com/in/veenashree-b-20a69329a/)
🐙 [GitHub Profile](https://github.com/Veenashree-B)
