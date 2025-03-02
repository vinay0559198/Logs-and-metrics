from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Define threshold ranges for normal system performance
THRESHOLDS = {
    "CPU Usage (%)": (0, 80),  
    "Memory Usage (MB)": (0, 1600),  
    "Disk I/O (IOPS)": (0, 400),  
    "Network Latency (ms)": (0, 300),  
    "Throughput (Requests/sec)": (50, 500)  
}

# Recommendations based on detected issues
RECOMMENDATIONS = {
    "High CPU Usage": "Optimize workload, reduce background processes, and scale CPU resources.",
    "High Memory Usage": "Check for memory leaks, optimize memory allocation, and increase RAM if necessary.",
    "High Disk I/O": "Optimize database queries, consider SSDs, and reduce unnecessary disk writes.",
    "High Network Latency": "Check network bandwidth, optimize API calls, and use Content Delivery Networks (CDNs).",
    "Low Throughput": "Optimize request handling, scale infrastructure, and reduce bottlenecks.",
    "None": "Monitor system regularly for performance issues."
}

def detect_anomalies(data):
    """Detects anomalies in input metrics"""
    anomalies = {}
    anomaly_detected = False

    for metric, value in data.items():
        min_val, max_val = THRESHOLDS.get(metric, (None, None))
        if min_val is not None and max_val is not None:
            anomalies[metric] = not (min_val <= value <= max_val)
            if anomalies[metric]:  
                anomaly_detected = True

    return anomalies, anomaly_detected

def root_cause_analysis(anomalies):
    """Determines the root cause of detected anomalies"""
    if not any(anomalies.values()):
        return "None"
    
    causes = []
    if anomalies.get("CPU Usage (%)"):
        causes.append("High CPU Usage")
    if anomalies.get("Memory Usage (MB)"):
        causes.append("High Memory Usage")
    if anomalies.get("Disk I/O (IOPS)"):
        causes.append("High Disk I/O")
    if anomalies.get("Network Latency (ms)"):
        causes.append("High Network Latency")
    if anomalies.get("Throughput (Requests/sec)"):
        causes.append("Low Throughput")
    
    return ", ".join(causes)

def generate_recommendations(root_cause):
    """Provides recommendations based on root cause"""
    if root_cause == "None":
        return [RECOMMENDATIONS["None"]]
    
    causes = root_cause.split(", ")
    return [RECOMMENDATIONS.get(cause, "No specific recommendation available.") for cause in causes]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Get input values from form
            data = {
                "CPU Usage (%)": float(request.form["cpu"]),
                "Memory Usage (MB)": float(request.form["memory"]),
                "Disk I/O (IOPS)": float(request.form["disk_io"]),
                "Network Latency (ms)": float(request.form["network_latency"]),
                "Throughput (Requests/sec)": float(request.form["throughput"])
            }

            # Perform anomaly detection
            anomalies, anomaly_detected = detect_anomalies(data)

            # Determine root cause
            root_cause = root_cause_analysis(anomalies)

            # Generate recommendations
            recommendations = generate_recommendations(root_cause)

            return render_template("index.html", data=data, anomalies=anomalies, root_cause=root_cause, recommendations=recommendations)

        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")

if __name__ == "__main__":
    app.run()
