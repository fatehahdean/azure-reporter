from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
import subprocess
import json
from datetime import datetime

# Get subscription
result = subprocess.run(['az', 'account', 'show'], capture_output=True, text=True)
account = json.loads(result.stdout)
subscription_id = account['id']
subscription_name = account['name']

print(f"Connected to: {subscription_name}")
print("Running assessment...")

credential = AzureCliCredential()
resource_client = ResourceManagementClient(credential, subscription_id)

# Collect all resources
resources = []
for resource in resource_client.resources.list():
    resources.append({
        'name': resource.name,
        'type': resource.type,
        'location': resource.location,
        'resource_group': resource.id.split('/')[4]
    })

# Check resource groups for tags
rg_findings = []
for rg in resource_client.resource_groups.list():
    tags = rg.tags or {}
    rg_findings.append({
        'name': rg.name,
        'location': rg.location,
        'tagged': bool(tags),
        'tag_count': len(tags)
    })

# Summary counts
total_resources = len(resources)
total_rgs = len(rg_findings)
untagged_rgs = len([r for r in rg_findings if not r['tagged']])
resource_types = {}
for r in resources:
    t = r['type']
    resource_types[t] = resource_types.get(t, 0) + 1

# Generate HTML report
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
report_date = datetime.now().strftime("%B %d, %Y")

html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Azure Cloud Assessment Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; color: #333; }}
        h1 {{ color: #0078d4; }}
        h2 {{ color: #0078d4; border-bottom: 1px solid #0078d4; padding-bottom: 5px; }}
        .summary-box {{ background: #f0f8ff; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .warning {{ color: #d83b01; font-weight: bold; }}
        .ok {{ color: #107c10; font-weight: bold; }}
        table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
        th {{ background: #0078d4; color: white; padding: 8px; text-align: left; }}
        td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background: #f5f5f5; }}
        .footer {{ margin-top: 40px; font-size: 12px; color: #666; }}
    </style>
</head>
<body>
    <h1>Azure Cloud Assessment Report</h1>
    <p><strong>Subscription:</strong> {subscription_name}</p>
    <p><strong>Generated:</strong> {report_date} at {timestamp}</p>
    <p><strong>Prepared by:</strong> Fatehah Burhannudin</p>

    <h2>Executive Summary</h2>
    <div class="summary-box">
        <p>Total Resources: <strong>{total_resources}</strong></p>
        <p>Total Resource Groups: <strong>{total_rgs}</strong></p>
        <p>Untagged Resource Groups: <strong class="{'warning' if untagged_rgs > 0 else 'ok'}">{untagged_rgs}</strong></p>
        <p>Governance Risk: <strong class="{'warning' if untagged_rgs > 0 else 'ok'}">{'HIGH - Missing tags detected' if untagged_rgs > 0 else 'LOW - All resource groups tagged'}</strong></p>
    </div>

    <h2>Resource Group Compliance</h2>
    <table>
        <tr><th>Resource Group</th><th>Location</th><th>Tags</th><th>Status</th></tr>
"""

for rg in rg_findings:
    status = '<span class="ok">OK</span>' if rg['tagged'] else '<span class="warning">WARNING - No tags</span>'
    html += f"        <tr><td>{rg['name']}</td><td>{rg['location']}</td><td>{rg['tag_count']}</td><td>{status}</td></tr>\n"

html += """    </table>

    <h2>Resource Inventory</h2>
    <table>
        <tr><th>Resource Name</th><th>Type</th><th>Location</th><th>Resource Group</th></tr>
"""

for r in resources:
    html += f"        <tr><td>{r['name']}</td><td>{r['type']}</td><td>{r['location']}</td><td>{r['resource_group']}</td></tr>\n"

html += """    </table>

    <h2>Resource Type Breakdown</h2>
    <table>
        <tr><th>Resource Type</th><th>Count</th></tr>
"""

for rtype, count in sorted(resource_types.items(), key=lambda x: x[1], reverse=True):
    html += f"        <tr><td>{rtype}</td><td>{count}</td></tr>\n"

html += f"""    </table>

    <h2>Recommendations</h2>
    <ul>
        <li>{'<span class="warning">Apply tags to all resource groups to enable cost tracking and governance</span>' if untagged_rgs > 0 else '<span class="ok">Tagging compliance is good — maintain this standard</span>'}</li>
        <li>Review resource inventory regularly to identify unused or forgotten resources</li>
        <li>Implement Azure Policy to enforce tagging on all new resources</li>
        <li>Consider Azure Cost Management dashboards for ongoing FinOps visibility</li>
    </ul>

    <div class="footer">
        <p>This report was generated automatically using the Azure SDK for Python.</p>
        <p>Generated on {timestamp}</p>
    </div>
</body>
</html>"""

# Save report
filename = f"azure_report_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
with open(filename, 'w') as f:
    f.write(html)

print(f"\nReport saved: {filename}")
print(f"Total resources found: {total_resources}")
print(f"Untagged resource groups: {untagged_rgs}")
print("\nOpen the HTML file in your browser to view the full report.")
