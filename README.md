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
