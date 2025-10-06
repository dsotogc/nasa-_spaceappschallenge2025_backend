# NASA Space Apps Challenge 2025 — Backend

Este repositorio contiene la parte de **backend** del proyecto para la NASA Space Apps Challenge 2025. Su propósito es procesar datos, ofrecer cálculos y servir una API para que el frontend consuma los resultados.

---

## 🧰 Tecnologías utilizadas

- Python  
- FastAPI (u otro framework de API que hayas usado)  
- Uvicorn (o similar para servidor ASGI)  

---

## 🎯 Funcionalidad principal

La API backend está diseñada para:

- Recibir coordenadas geográficas (latitud, longitud) o zonas de interés desde el frontend.  
- Obtener datos satelitales o atmosféricos (por ejemplo niveles de NO₂ u otros contaminantes)  
- Realizar cálculos / transformaciones para estimar moléculas por cm², concentraciones, etc.  
- Devolver la información procesada en formato JSON para que el frontend la visualice en mapas, gráficos u otros componentes.

Un endpoint destacado podría ser algo como:

GET /api/atmosfera?lat={lat}&lon={lon}

donde la respuesta incluiría el valor estimado, unidades, posibles intervalos de confianza, etc.

---

## 🚀 Instrucciones de ejecución (modo local / desarrollo)

1. Clona este repositorio:

   ```bash
   git clone https://github.com/dsotogc/nasa-_spaceappschallenge2025_backend.git
   cd nasa-_spaceappschallenge2025_backend
Crea un entorno virtual e instala dependencias:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload
Esto levantará el servidor en http://127.0.0.1:8000 (o el puerto que hayas configurado).


📐 Ejemplo de petición / respuesta
Request:

GET /api/atmosfera?lat=40.4168&lon=-3.7038
Respuesta esperada (ejemplo):


{
  "lat": 40.4168,
  "lon": -3.7038,
  "no2_molecules_per_cm2": 1.23e16,
  "unidad": "moléculas/cm²",
  "timestamp": "2025-10-06T12:34:56Z"
}

📁 Integración con frontend
El frontend (repositorio aparte) consumirá los endpoints de esta API para mostrar datos en mapas, gráficos u otros componentes UI. 

🤝 Colaboradores y equipo
dsotogc
rasitoo

📝 Licencia
MIT License.
