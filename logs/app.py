import datetime
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

def analyze_logs(log_entries):
    db_errors = []
    web_errors = []
    high_cpu_usage = False
    network_latency = False
    memory_leak = False
    high_request_rate = False
    security_breach = False

    for log in log_entries:
        try:
            timestamp, log_level, component, message = log
            
            if 'DBServer' in component and ('timeout' in message.lower() or 'connection' in message.lower()):
                db_errors.append(log)
            if 'WebServer' in component:
                if 'CPU usage' in message and 'high' in message:
                    high_cpu_usage = True
                if 'network latency' in message and 'high' in message:
                    network_latency = True
                if 'memory leak' in message.lower():
                    memory_leak = True
                if 'high request rate' in message.lower():
                    high_request_rate = True
            if 'Security' in component and ('unauthorized access' in message.lower() or 'multiple failed login' in message.lower()):
                security_breach = True
        except Exception as e:
            print(f"Error processing log entry: {e}")

    root_cause_analysis, possible_correlation, recommendation = None, None, None

    if db_errors:
        root_cause_analysis = "DBServer errors detected: Possible connection issues or timeouts."
        possible_correlation = "Increased server load may have led to slow responses and connection timeouts."
        recommendation = "Optimize database queries and implement connection pooling."
    elif high_cpu_usage:
        root_cause_analysis = "High CPU usage detected: Server is experiencing performance bottlenecks."
        possible_correlation = "Increased web traffic might be causing excessive CPU usage."
        recommendation = "Optimize server workload distribution and scale resources accordingly."
    elif network_latency:
        root_cause_analysis = "High network latency detected: Possible network bottlenecks."
        possible_correlation = "Network congestion or slow server response may be affecting performance."
        recommendation = "Optimize network infrastructure to reduce latency."
    elif memory_leak:
        root_cause_analysis = "Memory leak detected: Application may not be releasing memory properly."
        possible_correlation = "Long-running processes could be consuming excessive memory."
        recommendation = "Perform memory profiling and optimize resource management."
    elif high_request_rate:
        root_cause_analysis = "High request rate detected: Possible DDoS attack or increased traffic."
        possible_correlation = "A surge in user requests might be overwhelming the server."
        recommendation = "Implement rate limiting and caching mechanisms."
    elif security_breach:
        root_cause_analysis = "Security breach detected: Unauthorized access attempts logged."
        possible_correlation = "Multiple failed login attempts may indicate a brute-force attack."
        recommendation = "Enforce stronger authentication mechanisms and monitor access logs."
    
    return root_cause_analysis, possible_correlation, recommendation

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data or 'logs' not in data:
            return jsonify({"error": "Invalid JSON input"}), 400

        log_entries = data['logs']
        parsed_logs = []
        for log in log_entries:
            timestamp = datetime.datetime.strptime(log['timestamp'], "%Y-%m-%d %H:%M:%S")
            parsed_logs.append((timestamp, log['log_level'], log['component'], log['message']))
        
        root_cause_analysis, possible_correlation, recommendation = analyze_logs(parsed_logs)
        return jsonify({
            "root_cause_analysis": root_cause_analysis,
            "possible_correlation": possible_correlation,
            "recommendation": recommendation
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
