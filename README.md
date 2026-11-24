# 💰 FinOps Cloud-Cost Optimisation Dashboard

A Python-based interactive dashboard to monitor, analyse, and optimise cloud spending across AWS and Microsoft Azure using simulated billing data.

## 📌 Project Overview

The FinOps Cloud-Cost Optimisation Dashboard helps users understand cloud expenditure, compare cloud providers, monitor monthly budgets, identify unusual spending patterns, and explore potential cost-saving opportunities.

This project uses simulated AWS and Azure billing datasets, so no active cloud accounts or paid cloud subscriptions are required.

## 🎯 Project Objectives

- Monitor AWS and Azure cloud spending in one dashboard.
- Compare cloud costs across services and providers.
- Analyse daily and monthly spending trends.
- Identify unusual cloud spending patterns.
- Monitor monthly cloud budgets and utilisation.
- Forecast estimated cloud spending for the next 30 days.
- Provide cloud cost optimisation recommendations.
- Estimate potential cloud savings.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Streamlit | Interactive dashboard |
| Pandas | Data processing and analysis |
| Plotly | Interactive visualisations |
| OpenPyXL | Excel report generation |

## ☁️ Cloud Providers & Services

### AWS
- EC2
- S3
- RDS
- Lambda
- EBS
- CloudWatch

### Microsoft Azure
- Virtual Machines
- Blob Storage
- Azure SQL Database
- Azure Functions
- Managed Disks
- Azure Monitor

## ✨ Dashboard Features

### 1. Overview
- Total cloud cost
- AWS and Azure spending
- Average daily cost
- Highest spending provider
- Total cloud services
- Daily cost trend
- Service-wise cost comparison

### 2. Cost Analysis
- Service cost summary
- Monthly cost comparison
- Month-over-month spending analysis
- Top 5 expensive cloud services
- AWS vs Azure spending distribution
- Cloud cost anomaly detection

### 3. Cost Optimization
- Service-specific optimisation recommendations
- Estimated savings for individual services
- Total potential cloud savings

### 4. Budget & Forecast
- Monthly AWS and Azure budget configuration
- Budget utilisation monitoring
- Budget alerts
- Estimated 30-day cloud cost forecasting

### 5. Reports & Downloads
- Filtered cloud cost CSV report
- Complete AWS and Azure CSV report
- Excel report with separate AWS, Azure, and summary sheets

## 📂 Project Structure

```text
finops-cloud-cost-dashboard/
│
├── app.py
├── data_generator.py
├── data_processor.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── aws_costs.csv
│   └── azure_costs.csv
│
└── .gitignore
```

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10 or above
- Visual Studio Code

### Step 1: Clone the repository

```bash
git clone <your-github-repository-url>
cd finops-cloud-cost-dashboard
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

### Step 3: Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the application

```bash
streamlit run app.py
```

The dashboard will open in your web browser.

## 📊 Data Source

This project uses simulated cloud billing data generated for AWS and Azure services.

The dataset contains:
- 90 days of sample billing records
- 6 services from each cloud provider
- Daily cost information
- Cloud provider and service details
- Cost values in USD

No AWS or Azure credentials are required.

## 🔮 Future Enhancements

- Integration with real AWS Cost Explorer data.
- Integration with Azure Cost Management APIs.
- Machine learning-based cost forecasting.
- Advanced anomaly detection.
- Automated cloud cost optimisation suggestions.
- Cloud budget notifications.

## 👩‍💻 Author

Developed as a Cloud FinOps and DevOps learning project.

---

**Note:** Cost forecasts, anomaly detection, and potential savings are based on simulated billing data and illustrative calculations. They should not be treated as actual cloud billing predictions or guaranteed savings.