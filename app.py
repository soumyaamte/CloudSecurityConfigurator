from flask import Flask, request, render_template
import json

app = Flask(__name__)

def analyze_security(config):
    issues = []
    for resource in config.get("resources", []):
        name = resource.get("name", "Unknown Resource")
        
        if "password" in resource and "weak" in resource["password"].lower():
            issues.append({
                "issue": "Weak Password",
                "name": name,
                "description": "The password for this resource is weak and can be easily compromised.",
                "recommendation": "Use a strong password with at least 12 characters, including uppercase, lowercase, numbers, and symbols."
            })
        
        if not resource.get("encryption", True):
            issues.append({
                "issue": "Encryption Disabled",
                "name": name,
                "description": "This resource does not have encryption enabled, which makes it vulnerable to data breaches.",
                "recommendation": "Enable encryption to protect sensitive data."
            })
        
        if "open_ports" in resource and resource["open_ports"]:
            issues.append({
                "issue": "Open Ports Detected",
                "name": name,
                "description": f"The following ports are open: {', '.join(map(str, resource['open_ports']))}. Open ports increase the attack surface and can be exploited.",
                "recommendation": "Close unnecessary ports and use firewall rules to restrict access."
            })
    
    return issues

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file uploaded", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    try:
        config = json.load(file)
    except json.JSONDecodeError:
        return "Invalid JSON format", 400
    
    issues = analyze_security(config)
    report_data = {
        "total_resources": len(config.get("resources", [])),
        "total_issues": len(issues),
        "issues": issues
    }
    
    return render_template("report.html", report=report_data)

if __name__ == '__main__':
    app.run(debug=True)
