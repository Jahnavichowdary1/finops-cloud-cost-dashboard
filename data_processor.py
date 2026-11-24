import pandas as pd

def load_cloud_data():

    # Load AWS data
    aws_data = pd.read_csv("data/aws_costs.csv")

    # Load Azure data
    azure_data = pd.read_csv("data/azure_costs.csv")

    # Combine both datasets
    combined_data = pd.concat(
        [aws_data, azure_data],
        ignore_index=True
    )

    # Convert date column
    combined_data["date"] = pd.to_datetime(
        combined_data["date"]
    )

    return combined_data


def get_cloud_summary(data):

    summary = data.groupby("cloud_provider")["cost"].sum()

    return summary


# Test the data processing
if __name__ == "__main__":

    data = load_cloud_data()

    print("Multi-Cloud Data Loaded Successfully!")
    print("-------------------------------------")

    print("Total Records:", len(data))

    print("\nCloud Provider Summary:")
    print(get_cloud_summary(data))

    print("\nAvailable Services:")
    print(data["service"].unique())
