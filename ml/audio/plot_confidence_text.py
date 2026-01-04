import csv

LOG_FILE = "monitor_logs.csv"
BAR_WIDTH = 40

def plot():
    print("\n📊 Confidence Over Time (Text Graph)\n")

    with open(LOG_FILE) as f:
        reader = csv.DictReader(f)
        for row in reader:
            conf = float(row["confidence"])
            bars = int(conf * BAR_WIDTH)
            bar = "█" * bars
            print(f"{row['timestamp']} | {bar} {conf:.3f}")

if __name__ == "__main__":
    plot()
