import yaml
import tabulate

# Load YAML file
with open('report.yaml') as file:
    data = yaml.load(file, Loader=yaml.FullLoader)

# Extract the relevant information
report = data['report']
summary = report['summary']
vulnerabilities = report['vulnerabilities']

# Format as a table in Markdown
header = ["Vulnerability ID", "Resource", "Installed Version", "Fixed Version", "Severity", "Score", "Title"]
table = []

for vulnerability in vulnerabilities:
    row = [
        vulnerability.get('vulnerabilityID', ""),
        vulnerability.get('resource', ""),
        vulnerability.get('installedVersion', ""),
        vulnerability.get('fixedVersion', ""),
        vulnerability.get('severity', ""),
        vulnerability.get('score', ""),
        vulnerability.get('title', ""),
    ]
    table.append(row)

markdown_table = tabulate.tabulate(table, headers=header, tablefmt="pipe")

print(markdown_table)

