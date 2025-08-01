# Customer-Sales-Analyzer
"A complete Python-powered Sales Analyzer that cleans messy data, visualizes trends, and uncovers business insights using Pandas"
# 🛒 Sales Analyzer by Ibraheem

This is a complete end-to-end sales data analyzer project created in Python using `pandas` (not available now `matplotlib`, and `seaborn` but...Soon). It performs data cleaning, analysis, and insights extraction on messy or real-world e-commerce data.

---

## 📦 Features

### ✅ Phase 1: Cleaning

- Standardized `OrderDate` into consistent `datetime` format.
- Converted `Amount` to `float`, removed `$` and handled missing values.
- Fixed inconsistent category names, payment methods, and location strings.
- Filled empty values logically:
  - Removed rows with missing amount or date.
  - Replaced blank cities (`''`) with `"Unknown"`.

---

### ✅ Phase 2: Exploratory Analysis

#### 📊 Basic Metrics:
- **Total Revenue**
- **Average Order Value**
- **Number of Orders per City**

#### 📈 Trends:
- **Orders Per Day**
- **Sales Per Category**
- **Top Paying Customers**

#### 🧠 Insights:
- **Most Used Payment Methods**
- **Most Popular Product Categories**

---

### ✅ Phase 3: Advanced Analysis

#### 🔍 Notes & Coupon Extraction:
- Extracted all coupon codes using regex (supports multiple codes like `"A50, B25"`).
- Counted how many orders had coupons applied.

#### 🧮 Custom Columns:
- **Order Weekday**
- **Order Value Label**: 
  - `Low` (< 50),
  - `Medium` (50–100),
  - `High` (> 100)

---

### ✅ Phase 4: Growth & Statistics

- **Month-over-Month (MoM) Growth** using `pct_change()` or `diff()`
- **Correlation** between `Quantity` and `Revenue`
- Descriptive stats: `mean`, `median`, `std`, `percentiles`

---

### ✅ Phase 5: Advanced Features

- **Crosstab**: Product vs. Order Status
- **Rolling Average** (e.g., 3-day revenue trend)
- **Customer Segmentation** using Quartiles (Q1–Q4)

---

## 📂 Project Structure

```bash
sales_analyzer/
│
├── sales_analyzer.ipynb     # Main Jupyter notebook
├── sales_data.csv           # Cleaned or original data file
├── requirements.txt         # Python packages
└── README.md                # Project overview (this file)
