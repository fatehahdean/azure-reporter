# Azure Cloud Assessment Reporter

A Python tool that connects to a live Microsoft Azure subscription and generates a professional HTML assessment report for client delivery.

## What it does
- Connects to Azure using CLI credentials
- Audits all resource groups for tagging compliance
- Inventories all resources by type and location
- Flags governance risks in red
- Generates a formatted HTML report ready for client presentation

## Why it matters
Cloud advisory engagements require clear, client-ready deliverables. This tool automates the assessment phase by turning raw Azure data into an executive-ready report that highlights governance gaps and recommendations.

<img width="1470" height="956" alt="Screenshot 2026-07-01 at 1 11 57 AM" src="https://github.com/user-attachments/assets/695d99bc-df5c-443d-9633-c721152bf65d" />
<img width="1470" height="956" alt="Screenshot 2026-07-01 at 1 11 29 AM" src="https://github.com/user-attachments/assets/2185cc93-9206-4e2b-8f95-c5badb118546" />

## Technologies used
- Python 3.13
- Azure SDK (azure-identity, azure-mgmt-resource)
- HTML/CSS for report generation
- Azure CLI

## How to run
1. Install dependencies: `pip3 install azure-identity azure-mgmt-resource`
2. Login: `az login`
3. Run: `python3 azure_reporter.py`
4. Open the generated .html file in your browser
