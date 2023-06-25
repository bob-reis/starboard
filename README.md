# SCA: Aquasecurity Starboard para Analise de Kubernetes

# Sobre o Projeto

A Starboard é uma ferramenta que podemos classificar como SCA no contexto DevSecOps, ele tenta integrar ferramentas de segurança heterogêneas incorporando suas saídas aos CRDs do Kubernetes (definições de recursos personalizados) e, a partir daí, tornando os relatórios de segurança acessíveis por meio da API do Kubernetes. Dessa forma, podemos encontrar e visualizar os riscos relacionados a diferentes recursos  do Kubernetes.

# Starboard fornece:

- Varredura automatizada de vulnerabilidades para cargas de trabalho do Kubernetes.
- Auditorias de configuração automatizadas para recursos do Kubernetes com regras predefinidas ou políticas personalizadas do Open Policy Agent (OPA).
- Escaneamento automatizado de infraestruturas e verificações de conformidade com CIS Benchmarks publicados pelo Center for Internet Security (CIS).
- Relatório de conformidade automatizado - NSA, CISA Kubernetes Hardening Kubernetes Guidance v1.0
- Resultados do teste de penetração para um cluster Kubernetes.
- Definições de recursos personalizados e um módulo Go para trabalhar e integrar uma variedade de verificadores de segurança.
- O plug-in Octant e a extensão Lens que disponibilizam relatórios de segurança por meio de interfaces familiares do Kubernetes.

Links Importantes

Projeto
https://github.com/aquasecurity/starboard
Documentação
https://aquasecurity.github.io/starboard/v0.15.12/



Instalação no Cluster

```
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/starboard/v0.15.12/deploy/static/starboard.yaml
```

Será criado o namespace starboard-system e você deverá encontrar os seguintes pods

```
kubectl get pods -n starboard-system

NAME                                        READY   STATUS    RESTARTS   AGE
scan-vulnerabilityreport-55778d48f9-9hs9s   1/1     Running   0          19s
scan-vulnerabilityreport-6467cdd4b5-thc45   1/1     Running   0          19s
scan-vulnerabilityreport-66cb785fb-gs8q8    1/1     Running   0          49s
scan-vulnerabilityreport-688b5b46c8-tb8lk   1/1     Running   0          19s
scan-vulnerabilityreport-7998b888ff-sr2s4   1/1     Running   0          19s
scan-vulnerabilityreport-ffff5867b-qpqtv    1/1     Running   0          19s
starboard-operator-fb4fbd59b-rtlvb          1/1     Running   0          8m57s
```


Como Utilizar

Varios recursos serão criados e você poderá verificar com o seguinte comando
```
kubectl api-resources --api-group aquasecurity.github.io
```

O Starboard Operator irá verificar continuamente e automaticamente e gerar relatórios de vulnerabilidade para todos os workloads em seu cluster. Você não precisa iniciar manualmente as varreduras de vulnerabilidade. 

Voce pode listar os relatorios gerados com o comando
```
kubectl get vulnerabilityreports -n <namespace>
```

Provavelmente você terá diversos replicasets, voce pode listar os replicasets ativos com o seguinte comando
```
kubectl get rs -n <namespace>|grep -v " 0"
```

E para ler um destes relatórios você poderá usar o comando
```
kubectl get vulnerabilityreports <report-name> -n <namespace> -o yaml > report.yaml
```


Convertendo o Resultado para formato Markdown

Você pode converter este resultado para o formato markdown (md) e torna-lo disponivel no seu código para analise e gestão.

Os Passos:
Crie um script em pythn que faz a conversão
```
vi convert.py
```

```
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
```

Considerando que você já tem o python instalado na máquina
Instale o venv
```
apt-get install python3-venv
```

Crie o ambiente virtual
```
python3 -m venv vuln-analisys
```

Ative o ambiente virtual
```
source vuln-analisys/bin/activate
```

Instale as dependencias
```
pip install pyyaml
pip install tabulate
```

Execute o script
```
python convert.py > report.md
```
