import streamlit as st
import pandas as pd
import plotly.express as px
import io

from data_processor import load_cloud_data

# Page configuration
st.set_page_config(
    page_title="FinOps Cloud-Cost Optimisation Dashboard",
    page_icon="💰",
    layout="wide"
)

# Load data
data = load_cloud_data()

# Dashboard title
st.title("💰 FinOps Cloud-Cost Optimisation Dashboard")
st.caption("Monitor, analyse and optimise cloud spending.")

st.divider()

# Sidebar filters
st.sidebar.header("Dashboard Filters")

providers = ["All", "AWS", "Azure"]

selected_provider = st.sidebar.selectbox(
    "Select Cloud Provider",
    providers
)

# Filter data

# Date Range Filter
st.sidebar.subheader("📅 Date Range Filter")

min_date = data["date"].min().date()
max_date = data["date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply provider filter
if selected_provider == "All":
    filtered_data = data.copy()
else:
    filtered_data = data[
        data["cloud_provider"] == selected_provider
    ].copy()

# Apply date filter
if len(selected_dates) == 2:

    start_date, end_date = selected_dates

    filtered_data = filtered_data[
        (filtered_data["date"].dt.date >= start_date) &
        (filtered_data["date"].dt.date <= end_date)
    ]


# Calculate costs
total_cost = filtered_data["cost"].sum()

aws_cost = filtered_data[
    filtered_data["cloud_provider"] == "AWS"
]["cost"].sum()

azure_cost = filtered_data[
    filtered_data["cloud_provider"] == "Azure"
]["cost"].sum()

# Additional KPI calculations

number_of_days = filtered_data["date"].nunique()

average_daily_cost = (
    total_cost / number_of_days
    if number_of_days > 0 else 0
)

highest_spending_provider = (
    "N/A" if filtered_data.empty
    else "AWS" if aws_cost >= azure_cost
    else "Azure"
)

total_services = filtered_data["service"].nunique()

# Dashboard Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "📈 Cost Analysis",
    "💡 Optimization",
    "💰 Budget & Forecast"
])

with tab1:
    # KPI metrics
    st.subheader("💰 Cloud Cost Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.metric(
                label="🌐 Total Cloud Cost",
                value=f"${total_cost:,.2f}"
            )
            st.caption("Combined AWS + Azure spending")

    with col2:
        with st.container(border=True):
            st.metric(
                label="🟠 AWS Cost",
                value=f"${aws_cost:,.2f}"
            )
            st.caption("Amazon Web Services spending")

    with col3:
        with st.container(border=True):
            st.metric(
                label="🔵 Azure Cost",
                value=f"${azure_cost:,.2f}"
            )
            st.caption("Microsoft Azure spending")


    # Additional KPI Cards

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.metric(
                label="📅 Average Daily Cost",
                value=f"${average_daily_cost:,.2f}"
            )
            st.caption("Average cloud spending per day")

    with col2:
        with st.container(border=True):
            st.metric(
                label="🏆 Highest Spending Provider",
                value=highest_spending_provider
            )
            st.caption("Cloud provider with higher spending")

    with col3:
        with st.container(border=True):
            st.metric(
                label="⚙️ Total Cloud Services",
                value=total_services
            )
            st.caption("Number of services monitored")

    st.divider()



    # Daily cost trend
    st.subheader("📈 Daily Cloud Cost Trend")

    daily_cost = (
        filtered_data.groupby(
            ["date", "cloud_provider"]
        )["cost"]
        .sum()
        .reset_index()
    )


    fig_daily = px.line(
        daily_cost,
        x="date",
        y="cost",
        color="cloud_provider",
        markers=True,
        title="Daily Cloud Spending Trend",
        color_discrete_map={
            "AWS": "#FF9900",
            "Azure": "#0078D4"
        },
        labels={
            "date": "Date",
            "cost": "Cost (USD)",
            "cloud_provider": "Cloud Provider"
        },
        template="plotly_white"
    )

    fig_daily.update_layout(
        hovermode="x unified",
        legend_title="Cloud Provider",
        title_x=0.02,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_daily,
        use_container_width=True
    )


    # Service-wise cost
    st.subheader("📊 Service-wise Cloud Cost")

    service_cost = (
        filtered_data.groupby(
            ["service", "cloud_provider"]
        )["cost"]
        .sum()
        .reset_index()
    )


    fig_service = px.bar(
        service_cost,
        x="service",
        y="cost",
        color="cloud_provider",
        barmode="group",
        text_auto=".2s",
        title="Cloud Service Spending Comparison",
        color_discrete_map={
            "AWS": "#FF9900",
            "Azure": "#0078D4"
        },
        labels={
            "service": "Cloud Service",
            "cost": "Total Cost (USD)",
            "cloud_provider": "Cloud Provider"
        },
        template="plotly_white"
    )

    fig_service.update_layout(
        title_x=0.02,
        legend_title="Cloud Provider",
        xaxis_title="Cloud Service",
        yaxis_title="Total Cost (USD)",
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_service,
        use_container_width=True
    )

with tab2:

    # Service Cost Summary
    st.divider()
    st.subheader("📋 Service Cost Summary")

    service_summary = (
        filtered_data.groupby(
            ["cloud_provider", "service"]
        )
        .agg(
            Total_Cost=("cost", "sum"),
            Average_Daily_Cost=("cost", "mean"),
            Total_Records=("cost", "count")
        )
        .reset_index()
    )

    service_summary["Total_Cost"] = service_summary["Total_Cost"].round(2)
    service_summary["Average_Daily_Cost"] = service_summary["Average_Daily_Cost"].round(2)

    service_summary = service_summary.sort_values(
        by="Total_Cost",
        ascending=False
    )

    st.dataframe(
        service_summary,
        use_container_width=True,
        hide_index=True
    )


    # Monthly Cost Comparison
    st.divider()
    st.subheader("📅 Monthly Cost Comparison")

    monthly_comparison = filtered_data.copy()

    monthly_comparison["month"] = (
        monthly_comparison["date"].dt.to_period("M")
    )

    monthly_summary = (
        monthly_comparison.groupby(
            ["month", "cloud_provider"]
        )["cost"]
        .sum()
        .reset_index()
    )

    monthly_summary["month"] = (
        monthly_summary["month"].astype(str)
    )


    fig_monthly = px.bar(
        monthly_summary,
        x="month",
        y="cost",
        color="cloud_provider",
        barmode="group",
        title="Monthly Cloud Spending Comparison",
        labels={
            "month": "Month",
            "cost": "Total Cost (USD)",
            "cloud_provider": "Cloud Provider"
        },
        color_discrete_map={
            "AWS": "#FF9900",
            "Azure": "#0078D4"
        },
        template="plotly_white"
    )


    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )

    # Month-over-month summary
    months = sorted(monthly_comparison["month"].unique())

    if len(months) >= 2:

        current_month = months[-1]
        previous_month = months[-2]

        current_cost = monthly_comparison[
            monthly_comparison["month"] == current_month
        ]["cost"].sum()

        previous_cost = monthly_comparison[
            monthly_comparison["month"] == previous_month
        ]["cost"].sum()

        change = current_cost - previous_cost

        if previous_cost > 0:
            percentage_change = (change / previous_cost) * 100

            st.metric(
                "Overall Month-over-Month Change",
                f"{percentage_change:+.2f}%",
                delta=f"${change:+,.2f}"
            )
    else:
        st.info("At least two months of data are required.")


    # Top 5 Expensive Cloud Services
    st.divider()
    st.subheader("🏆 Top 5 Expensive Cloud Services")

    top_services = (
        filtered_data.groupby(
            ["cloud_provider", "service"]
        )["cost"]
        .sum()
        .reset_index()
        .sort_values("cost", ascending=False)
        .head(5)
    )


    fig_top_services = px.bar(
        top_services,
        x="cost",
        y="service",
        color="cloud_provider",
        orientation="h",
        text="cost",
        title="Top 5 Services by Total Spending",
        labels={
            "cost": "Total Cost (USD)",
            "service": "Cloud Service",
            "cloud_provider": "Cloud Provider"
        },
        color_discrete_map={
            "AWS": "#FF9900",
            "Azure": "#0078D4"
        },
        template="plotly_white"
    )


    fig_top_services.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig_top_services,
        use_container_width=True
    )

    st.dataframe(
        top_services,
        use_container_width=True,
        hide_index=True
    )

    # Provider comparison
    st.subheader("☁️ AWS vs Azure Cost Comparison")

    provider_cost = (
        data.groupby("cloud_provider")["cost"]
        .sum()
        .reset_index()
    )


    fig_provider = px.pie(
        provider_cost,
        names="cloud_provider",
        values="cost",
        hole=0.55,
        color="cloud_provider",
        color_discrete_map={
            "AWS": "#FF9900",
            "Azure": "#0078D4"
        },
        title="AWS vs Azure Spending Distribution",
        template="plotly_white"
    )

    fig_provider.update_traces(
        textinfo="label+percent",
        textposition="outside",
        hole=0.55
    )

    fig_provider.update_layout(
        title_x=0.02,
        legend_title="Cloud Provider",
        margin=dict(l=30, r=30, t=60, b=30)
    )

    st.plotly_chart(
        fig_provider,
        use_container_width=True
    )



    # Anomaly Detection
    st.divider()
    st.subheader("🚨 Cloud Cost Anomaly Detection")

    # Calculate daily cost for each cloud provider
    daily_provider_cost = (
        data.groupby(["date", "cloud_provider"])["cost"]
        .sum()
        .reset_index()
    )

    # Calculate anomaly threshold separately for each provider
    anomalies = []

    for provider in daily_provider_cost["cloud_provider"].unique():

        provider_data = daily_provider_cost[
            daily_provider_cost["cloud_provider"] == provider
        ].copy()

        average_cost = provider_data["cost"].mean()
        std_cost = provider_data["cost"].std()

        threshold = average_cost + (2 * std_cost)

        provider_anomalies = provider_data[
            provider_data["cost"] > threshold
        ].copy()

        anomalies.append(provider_anomalies)

    if anomalies:
        anomaly_data = pd.concat(anomalies, ignore_index=True)

        if not anomaly_data.empty:
            st.warning("Unexpected cloud cost increases detected!")

            st.dataframe(
                anomaly_data,
                use_container_width=True
            )
        else:
            st.success("No unusual cloud cost increases detected.")

# Tab 4 - Budget & Forecast
with tab4:
    # Cloud Cost Forecasting
    st.divider()
    st.subheader("🔮 Cloud Cost Forecasting")

    forecast_data = filtered_data.copy()

    forecast_data["date"] = pd.to_datetime(
        forecast_data["date"]
    )

    forecast_daily = (
        forecast_data.groupby(
            ["date", "cloud_provider"]
        )["cost"]
        .sum()
        .reset_index()
    )

    forecast_results = []

    for provider in ["AWS", "Azure"]:

        provider_data = forecast_daily[
            forecast_daily["cloud_provider"] == provider
        ].sort_values("date")

        if len(provider_data) < 7:
            continue

        # Average daily cost of last 30 days
        average_daily_cost = provider_data.tail(30)["cost"].mean()

        last_date = provider_data["date"].max()

        for day in range(1, 31):

            forecast_results.append({
                "date": last_date + pd.Timedelta(days=day),
                "cloud_provider": provider,
                "cost": round(average_daily_cost, 2)
            })

    forecast_df = pd.DataFrame(forecast_results)


    if not forecast_df.empty:

        fig_forecast = px.line(
            forecast_df,
            x="date",
            y="cost",
            color="cloud_provider",
            title="Estimated Daily Cloud Cost - Next 30 Days",
            labels={
                "date": "Forecast Date",
                "cost": "Estimated Daily Cost (USD)",
                "cloud_provider": "Cloud Provider"
            },
            color_discrete_map={
                "AWS": "#FF9900",
                "Azure": "#0078D4"
            },
            template="plotly_white"
        )

        st.plotly_chart(
            fig_forecast,
            use_container_width=True
        )

        forecast_summary = (
            forecast_df.groupby("cloud_provider")["cost"]
            .sum()
            .reset_index()
        )


        forecast_summary = (
            forecast_df.groupby("cloud_provider")["cost"]
            .sum()
            .reset_index()
        )

        forecast_summary.rename(
            columns={"cost": "Estimated 30-Day Cost"},
            inplace=True
        )

        st.write("Estimated Cloud Spending for Next 30 Days")

        st.dataframe(
            forecast_summary,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("Not enough historical data for forecasting.")

    # Monthly Budget Monitoring
    st.divider()
    st.subheader("💰 Monthly Budget Monitoring")

    # Select current month data
    current_month = pd.Timestamp.today().to_period("M")

    monthly_data = data[
        pd.to_datetime(data["date"]).dt.to_period("M") == current_month
    ]

    # Budget settings
    col1, col2 = st.columns(2)

    with col1:
        aws_budget = st.number_input(
            "AWS Monthly Budget (USD)",
            min_value=100,
            value=3000,
            step=1000
        )

    with col2:
        azure_budget = st.number_input(
            "Azure Monthly Budget (USD)",
            min_value=100,
            value=3000,
            step=1000
        )

    # Calculate monthly costs
    aws_monthly_cost = monthly_data[
        monthly_data["cloud_provider"] == "AWS"
    ]["cost"].sum()

    azure_monthly_cost = monthly_data[
        monthly_data["cloud_provider"] == "Azure"
    ]["cost"].sum()

    total_monthly_cost = aws_monthly_cost + azure_monthly_cost
    total_budget = aws_budget + azure_budget


    # Display budget utilization
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🟠 AWS Monthly Cost", f"${aws_monthly_cost:,.2f}")
        aws_percentage = aws_monthly_cost / aws_budget * 100
        st.markdown(
            f"""
            <div style="background:#eeeeee; border-radius:10px; height:12px;">
                <div style="width:{min(aws_percentage, 100):.1f}%;
                            background:#FF9900; height:12px;
                            border-radius:10px;"></div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.caption(f"Budget used: {aws_percentage:.1f}%")

    with col2:
        st.metric("🔵 Azure Monthly Cost", f"${azure_monthly_cost:,.2f}")
        azure_percentage = azure_monthly_cost / azure_budget * 100
        st.markdown(
            f"""
            <div style="background:#eeeeee; border-radius:10px; height:12px;">
                <div style="width:{min(azure_percentage, 100):.1f}%;
                            background:#0078D4; height:12px;
                            border-radius:10px;"></div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.caption(f"Budget used: {azure_percentage:.1f}%")

    with col3:
        st.metric("Combined Monthly Cost", f"${total_monthly_cost:,.2f}")
        combined_percentage = total_monthly_cost / total_budget * 100
        st.progress(min(combined_percentage / 100, 1.0))
        st.caption(f"Budget used: {combined_percentage:.1f}%")

    # Budget alerts
    if aws_monthly_cost > aws_budget:
        st.error("AWS monthly budget exceeded!")

    if azure_monthly_cost > azure_budget:
        st.error("Azure monthly budget exceeded!")

    if total_monthly_cost > total_budget:
        st.error("Combined cloud budget exceeded!")
    else:
        st.success("Cloud spending is within the combined budget.")

# Tab 3- Optimization
with tab3:
    # Cost Optimization Recommendations
    st.divider()
    st.subheader("💡 Cost Optimization Recommendations")

    recommendations = {
        "EC2": "Review unused EC2 instances and consider right-sizing.",
        "S3": "Review storage usage and consider cheaper storage tiers.",
        "RDS": "Review database instance sizes and remove unused databases.",
        "Lambda": "Optimize function memory and execution time.",
        "EBS": "Identify and review unattached EBS volumes.",
        "CloudWatch": "Review log retention periods to reduce storage costs.",
        "Virtual Machines": "Review VM utilization and consider right-sizing.",
        "Blob Storage": "Consider cool or archive tiers for infrequently accessed data.",
        "Azure SQL Database": "Review database performance tiers and sizing.",
        "Azure Functions": "Optimize function execution and hosting plans.",
        "Managed Disks": "Review unused disks and disk performance tiers.",
        "Azure Monitor": "Review log retention and monitoring data volume."
    }
    # Total potential savings calculation
    total_potential_savings = (
        filtered_data["cost"].sum() * 0.10
    )

    st.metric(
        label="💰 Total Potential Cloud Savings",
        value=f"${total_potential_savings:,.2f}",
        help="Illustrative savings estimate based on 10% of filtered cloud spending."
    )

    for provider in ["AWS", "Azure"]:

        st.markdown(f"#### ☁️ {provider}")

        provider_data = filtered_data[
            filtered_data["cloud_provider"] == provider
        ]

        if provider_data.empty:
            st.info(f"No {provider} data available for this filter.")
            continue

        service_summary = (
            provider_data.groupby("service")["cost"]
            .sum()
            .sort_values(ascending=False)
        )

        for service, cost in service_summary.items():

            with st.expander(f"{service} — ${cost:,.2f}"):

                st.write(
                    recommendations.get(
                        service,
                        "Review service usage and optimize spending."
                    )
                )
                            # Estimated potential savings
                estimated_savings = cost * 0.10

                st.metric(
                    label="Estimated Potential Savings (10%)",
                    value=f"${estimated_savings:,.2f}"
                )

                st.caption(
                    "Recommendation based on service category, "
                    "not actual resource utilization."
                )

# Data table
st.subheader("📋 Cloud Billing Records")

st.dataframe(
    filtered_data.sort_values("date", ascending=False),
    use_container_width=True
)


# Download Cloud Cost Reports
st.divider()
st.subheader("📥 Download Cloud Cost Reports")

col1, col2 = st.columns(2)

with col1:
    csv_data = filtered_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered Cloud Report",
        data=csv_data,
        file_name="cloud_cost_report.csv",
        mime="text/csv"
    )

with col2:
    complete_csv = data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Complete AWS + Azure Report",
        data=complete_csv,
        file_name="aws_azure_complete_report.csv",
        mime="text/csv"
    )
# Excel Report Generation
excel_buffer = io.BytesIO()

with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:

    filtered_data[
        filtered_data["cloud_provider"] == "AWS"
    ].to_excel(writer, sheet_name="AWS Costs", index=False)

    filtered_data[
        filtered_data["cloud_provider"] == "Azure"
    ].to_excel(writer, sheet_name="Azure Costs", index=False)

    cloud_summary = (
        filtered_data.groupby("cloud_provider")["cost"]
        .agg(["sum", "mean", "count"])
        .reset_index()
    )

    cloud_summary.columns = [
        "Cloud Provider",
        "Total Cost (USD)",
        "Average Cost (USD)",
        "Number of Records"
    ]

    cloud_summary.to_excel(
        writer,
        sheet_name="Cloud Cost Summary",
        index=False
    )

st.download_button(
    label="📊 Download Excel Cloud Report",
    data=excel_buffer.getvalue(),
    file_name="finops_cloud_cost_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Footer
st.caption(
    "Note: This dashboard uses simulated AWS and Azure billing data."
)
