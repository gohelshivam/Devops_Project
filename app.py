import os
import socket
import datetime
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Server start hone ka time record karna
START_TIME = datetime.datetime.now(datetime.timezone.utc)
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_ENV = os.getenv("FLASK_ENV", "production")

@app.route("/")
def home():
    """Main homepage - dashboard render karta hai"""
    hostname = socket.gethostname()
    uptime = str(datetime.datetime.now(datetime.timezone.utc) - START_TIME).split(".")[0]
    return render_template(
        "index.html",
        hostname=hostname,
        version=APP_VERSION,
        environment=APP_ENV,
        uptime=uptime,
        deployed_at=START_TIME.strftime("%Y-%m-%d %H:%M:%S UTC")
    )

@app.route("/health")
def health_check():
    """
    AWS Application Load Balancer (ALB) aur Docker HEALTHCHECK
    is endpoint ko check karke batate hain server healthy hai ya nahi.
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "version": APP_VERSION,
        "hostname": socket.gethostname()
    }), 200

@app.route("/api/info")
def info():
    """API endpoint deployment metadata provide karta hai"""
    return jsonify({
        "app_name": "DevOps Cloud Web Application",
        "version": APP_VERSION,
        "environment": APP_ENV,
        "hostname": socket.gethostname(),
        "uptime": str(datetime.datetime.now(datetime.timezone.utc) - START_TIME).split(".")[0],
        "deployed_at": START_TIME.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "tech_stack": [
            "Python / Flask",
            "Docker / Docker Hub",
            "GitHub Actions CI/CD",
            "AWS EC2 & ALB",
            "DuckDNS / Route 53",
            "AWS CloudWatch"
        ]
    }), 200

if __name__ == "__main__":
    # Local running ke liye port 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
