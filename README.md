# 📰 News Aggregator - Multi-Scraper con Scrapy

Un proyecto de web scraping que agrega noticias de tres fuentes diferentes (**La Voz de Galicia**, **El País** y **Marca**) en un formato unificado utilizando Scrapy.

##  Objetivo del Proyecto

Demostrar el uso de diferentes técnicas de scraping (selectores CSS, XPath y mixtos) para extraer información de múltiples sitios web de noticias y consolidarla en un único archivo JSON.

##  Características

- **Tres spiders independientes**:
  - **La Voz de Galicia Spider**: Utiliza únicamente selectores CSS
  - **El País Spider**: Utiliza únicamente selectores XPath
  - **Marca Spider**: Combina selectores CSS y XPath

- **Extracción de datos (5 campos comunes)**:
  - Fuente (identificador del sitio web)
  - Título de la noticia
  - Fecha de publicación
  - URL del artículo
  - Body (texto del artículo)

- **Limpieza de datos**:
  - Eliminación de espacios en blanco innecesarios
  - Eliminación de saltos de línea (`\n`, `\r`)
  - Normalización de nombres de autores
  - Manejo de datos faltantes con valores por defecto

##  Requisitos

```bash
Python 3.8+
Scrapy 2.11+
```

## 🔧 Instalación

1. **Clonar el repositorio**:
```bash
git clone https://github.com/EnriqueJimenezMartinez/Aggregator_Scraper.git
cd Aggregator_Scraper
```

2. **Crear un entorno virtual (recomendado)**:
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows
```

3. **Instalar dependencias**:
```bash
pip install scrapy
```

##  Uso

### Ejecutar cada spider individualmente

Para generar el archivo `news_data.json` con todas las noticias de las tres fuentes:

```bash
# Navega al directorio del proyecto
cd news_aggregator

# 1. Ejecutar La Voz de Galicia (solo CSS)
scrapy crawl lavoz -o ../temp_lavoz.json

# 2. Ejecutar El País (solo XPath)
scrapy crawl elpais -o ../temp_elpais.json

# 3. Ejecutar Marca (mixto)
scrapy crawl marca -o ../temp_marca.json

# 4. Volver al directorio raíz y combinar los resultados
cd ..
python3 -c "
import json
lavoz = json.load(open('temp_lavoz.json', encoding='utf-8'))
elpais = json.load(open('temp_elpais.json', encoding='utf-8'))
marca = json.load(open('temp_marca.json', encoding='utf-8'))
all_news = lavoz + elpais + marca
json.dump(all_news, open('news_data.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
"

# 5. Limpiar archivos temporales
rm temp_*.json
```

##  Estructura del Proyecto

```
Aggregator_Scraper/
│
├── news_aggregator/              # Proyecto Scrapy
│   ├── __init__.py               # Inicializador del módulo
│   ├── items.py                  # Definición de items 
│   ├── middlewares.py            # Middlewares personalizados
│   ├── pipelines.py              # Pipelines de procesamiento
│   ├── settings.py               # Configuración del proyecto
│   └── spiders/                  # Directorio de spiders
│       ├── __init__.py
│       ├── lavoz.py              # Spider La Voz (CSS)
│       ├── elpais.py             # Spider El País (XPath)
│       └── marca.py              # Spider Marca (Mixto)
│
├── news_data.json                # Archivo de salida con los datos
├── .gitignore                    # Archivos ignorados por Git
└── README.md                     # Este archivo
```

##  Formato de Salida

Los datos se exportan en formato JSON con la siguiente estructura:

```json
{
  "source": "La Voz de Galicia",
  "title": "Título de la noticia",
  "date": "2026-01-30",
  "url": "https://www.lavozdegalicia.es/noticia/galicia/2026/01/30/ejemplo.html",
  "body": "Texto del artículo..."
}
```

##  Detalles Técnicos

### La Voz de Galicia Spider (CSS Selectors)
- **Técnica**: Selectores CSS exclusivamente
- **Datos extraídos**: Título, fecha, URL, body
- **Particularidades**: El título se obtiene del `<title>` del artículo

### El País Spider (XPath Selectors)
- **Técnica**: XPath exclusivamente
- **Datos extraídos**: Título, fecha, URL, body

### Marca Spider (Selectores Mixtos)
- **Técnica**: Combinación de CSS y XPath
- **Datos extraídos**: Título, fecha, URL, body
- **Particularidades**: Scraping de la portada principal de Marca

##  Configuración

El archivo `settings.py` incluye configuración responsable:

- **DOWNLOAD_DELAY**: 2 segundos entre peticiones
- **CONCURRENT_REQUESTS_PER_DOMAIN**: 1 petición por dominio a la vez



##  Licencia

Este proyecto es de código abierto y está disponible para fines educativos.

