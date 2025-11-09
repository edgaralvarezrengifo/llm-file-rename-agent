# llm-file-rename-agent

🧠 Agente de Renombramiento Automatizado de Archivos
Caso de Uso — Proyecto de Grado: Implementación de agentes de IA con LLMs locales en entornos seguros

## 🧩 Descripción General

Este repositorio implementa un sistema multiagente local para el renombramiento automatizado de archivos basado en su contenido.
El sistema utiliza AutoGen Studio para la coordinación entre agentes y Ollama como motor local de modelos de lenguaje (LLMs).

El flujo cuenta con dos agentes cooperativos:

🧩 Agente Analizador → procesa y comprende el contenido del archivo.

🧠 Agente Renombrador → genera un nuevo nombre descriptivo de acuerdo al contenido analizado.

Este caso de uso hace parte del proyecto de grado "Implementación de agentes de IA con LLMs locales en entornos seguros", orientado a la automatización de procesos académico-administrativos dentro de la universidad.

## 🧱 Componentes Principales
Componente	Función	Tecnología
Ollama	Motor local de ejecución de modelos LLM.	Ollama

AutoGen Studio	Framework para crear y orquestar agentes cooperativos.	AutoGen Studio

Python	Implementación de la lógica multiagente.	3.11+
Docker Compose	Despliegue y orquestación local de contenedores.	v2+
🧩 Flujo de Trabajo

El usuario coloca un archivo en el directorio /data/input.

El Agente Analizador lee el contenido y genera una descripción semántica.

El Agente Renombrador recibe la descripción y propone un nuevo nombre para el archivo.

El archivo se renombra y se guarda en /data/output.

Todo el proceso se ejecuta de manera local, sin conexión a la nube.

## 📁 Estructura del Proyecto
agent-renombramiento-local/
├── docker-compose.yml
├── Dockerfile
├── agents/
│   ├── analyzer_agent.py
│   ├── rename_agent.py
│   └── __init__.py
├── main.py
├── requirements.txt
├── data/
│   ├── input/
│   └── output/
└── README.md

## 🧰 Requisitos del Sistema

Docker y Docker Compose instalados.

8 GB RAM mínimo (recomendado 16 GB).

Ollama descargará el modelo mistral automáticamente.

## ▶️ Instrucciones de uso

1. Clonar el repositorio:
```bash
git clone https://github.com/<usuario>/agent-renombramiento-local.git
cd agent-renombramiento-local

2. Construir y levantar los servicios:
```bash
docker compose up -d --build


3. Verificar los contenedores:

docker ps


4. Ver logs del agente:

docker logs -f auto-rename-agent


5. Colocar archivos a procesar en:

/data/input/

🔐 Consideraciones de Privacidad

Todo el procesamiento se realiza en entornos locales.

Ningún archivo ni descripción se envía a servidores externos.

El sistema cumple con políticas de seguridad institucional y protección de datos.

📚 Referencias

Ollama Documentation

AutoGen Studio Docs

Python Official Docs

Docker Compose Reference

⚙️ Arquitectura del Sistema
```mermaid
flowchart LR
    A["Archivo original (PDF, TXT, DOCX)"] --> B["Agente Analizador"]
    B -->|Descripción semántica| C["Agente Renombrador"]
    C --> D["Archivo renombrado y guardado en /data/output"]
