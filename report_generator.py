import matplotlib.pyplot as plt
from datetime import datetime
from email_alert import send_email
from analyzer import load_data, calculate_metrics


DATA_PATH = "../data/incidents.csv"
REPORT_PATH = "../output/sla_report.txt"
CHART_PATH = "../output/incident_trend.png"


def generate_report(metrics):
    report = f"""
SLA INCIDENT REPORT
Generated: {datetime.now()}

Total Resolved Incidents: {metrics['total_incidents']}
SLA Breaches: {metrics['breaches']}
Breach Percentage: {metrics['breach_percent']}%
MTTR (Hours): {metrics['mttr']}
"""

    with open(REPORT_PATH, "w") as f:
        f.write(report)

    return report


def generate_chart(df):
    df["created_time"] = df["created_time"].dt.date
    trend = df.groupby("created_time").size()

    plt.figure()
    trend.plot(kind="line")
    plt.title("Daily Incident Trend")
    plt.xlabel("Date")
    plt.ylabel("Incident Count")
    plt.savefig(CHART_PATH)
    plt.close()


def main():
    df = load_data(DATA_PATH)
    metrics = calculate_metrics(df)

    report_text = generate_report(metrics)
    generate_chart(metrics["dataframe"])

    # Send alert if SLA breach > 20%
    if metrics["breach_percent"] > 20:
        send_email(
            subject="⚠ SLA Breach Alert",
            body=report_text
        )

    print("Report generated successfully.")


if __name__ == "__main__":
    main()
