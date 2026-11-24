import pandas as pd
import random
from datetime import datetime, timedelta
import os

random.seed(42)

# Generate 90 days of sample cloud billing data
end_date = datetime.today().date()
start_date = end_date - timedelta(days=89)

dates = [
    start_date + timedelta(days=i)
    for i in range(90)
]

cloud_services = {
    "AWS": [
        "EC2",
        "S3",
        "RDS",
        "Lambda",
        "EBS",
        "CloudWatch"
    ],
    "Azure": [
        "Virtual Machines",
        "Blob Storage",
        "Azure SQL Database",
        "Azure Functions",
        "Managed Disks",
        "Azure Monitor"
    ]
}

def generate_cloud_data(provider):
    records = []

    for date in dates:
        for service in cloud_services[provider]:

            base_cost = random.uniform(20, 150)
            daily_variation = random.uniform(0.8, 1.2)

            cost = round(base_cost * daily_variation, 2)

            records.append({
                "date": date,
                "cloud_provider": provider,
                "service": service,
                "cost": cost,
                "currency": "USD"
            })

    return pd.DataFrame(records)


# Generate AWS and Azure datasets
aws_data = generate_cloud_data("AWS")
azure_data = generate_cloud_data("Azure")

# Create data folder if it does not exist
os.makedirs("data", exist_ok=True)

# Save CSV files
aws_data.to_csv("data/aws_costs.csv", index=False)
azure_data.to_csv("data/azure_costs.csv", index=False)

print("Sample cloud billing data generated successfully!")
print(f"AWS records: {len(aws_data)}")
print(f"Azure records: {len(azure_data)}")
print("CSV files saved inside the data folder.")
