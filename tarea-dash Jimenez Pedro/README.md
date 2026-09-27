# Dashboard de retrasos de vuelos — Pedro Jiménez

**URL pública:** *(se agrega cuando el servicio en Render quede Live)*

Tablero interactivo para el área de operaciones de una aerolínea. Permite elegir un año y ver el **retraso promedio en minutos** por aerolínea y por mes, separado en cinco causas: transportista (*carrier*), clima, sistema aéreo nacional (NAS), seguridad y aeronave tardía (*late aircraft*).

Pensado para que la dirección consulte los datos desde el navegador, sin instalar nada.

## Tabla de componentes

| `id` | Qué grafica | Bloque del layout |
| --- | --- | --- |
| `input-year` | Campo numérico del año (valor inicial 2010) | Encabezado, junto al título |
| `carrier-plot` | Promedio de `CarrierDelay` (minutos) por mes y aerolínea | Fila 1, columna izquierda |
| `weather-plot` | Promedio de `WeatherDelay` (minutos) por mes y aerolínea | Fila 1, columna derecha |
| `nas-plot` | Promedio de `NASDelay` (minutos) por mes y aerolínea | Fila 2, columna izquierda |
| `security-plot` | Promedio de `SecurityDelay` (minutos) por mes y aerolínea | Fila 2, columna derecha |
| `late-plot` | Promedio de `LateAircraftDelay` (minutos) por mes y aerolínea | Fila 3, ancho completo |

Un único callback recibe el año y actualiza las cinco figuras.

## Cómo ejecutarlo en local

Requisitos: Python 3.12.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python dashboard.py
```

Abre [http://127.0.0.1:8050](http://127.0.0.1:8050). Detén el servidor con `Ctrl+C`.

Pruebas rápidas:

- Deja el año en `2010`: deben dibujarse los cinco gráficos.
- Borra el campo: el tablero muestra un aviso y **no** debe caerse.

## Estructura del proyecto

```text
tarea-dash Jimenez Pedro/
├── dashboard.py          # Aplicación Dash (layout, compute_info, callback, WSGI)
├── airline_data.csv      # Muestra de vuelos 1987–2020
├── requirements.txt      # Dependencias, incluye gunicorn
├── Procfile              # Comando de arranque tipo Heroku
├── render.yaml           # Blueprint de Render (plan gratuito)
├── .python-version       # Python 3.12 en el servidor
├── .gitignore            # Excluye .venv/ y basura de Python
└── README.md             # Esta documentación
```

## Datos

- **Fuente:** muestra del conjunto *Airline Reporting Carrier On-Time Performance* (curso de analítica de datos).
- **Archivo:** `airline_data.csv` (repositorio; se lee con ruta relativa al módulo).
- **Tamaño:** unas 27.000 filas, años 1987–2020, 33 aerolíneas.
- **Columnas usadas:** `Year`, `Month`, `Reporting_Airline`, `CarrierDelay`, `WeatherDelay`, `NASDelay`, `SecurityDelay`, `LateAircraftDelay`.
- **Transformación:** se filtra por año y se calcula el promedio de cada causa agrupando por mes y aerolínea. No se imputan valores faltantes: pandas omite `NaN` al promediar.

## Decisiones de diseño

- **Gráfico de líneas:** el eje temporal es el mes (1–12); cada aerolínea es una serie. Así se ve la estacionalidad y se comparan operadores.
- **Colores:** paleta cualitativa `Dark24` de Plotly, con muchas categorías distinguibles. No se usa rojo/verde como único criterio.
- **Distribución:** dos filas de dos gráficos y una tercera con el de aeronave tardía, en tarjetas con `display: flex`, para que quepan en pantalla de escritorio sin una columna interminable.
- **Robustez:** si el año está vacío, no es numérico o no hay datos, se muestran figuras vacías con un mensaje claro.

## Despliegue

La plataforma recomendada es **Render** (plan gratuito). El repositorio incluye `render.yaml` y `Procfile`.

1. Sube este proyecto a GitHub (incluye `airline_data.csv`; no subas `.venv/`).
2. En Render: *New → Blueprint* y aplica el archivo, o crea un Web Service con:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn dashboard:server --bind 0.0.0.0:$PORT`
   - Instance: Free
3. La primera visita puede tardar unos 40 segundos si el servicio estaba dormido.

## Autoría

Pedro Jiménez — septiembre 2026.
