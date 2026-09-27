# Tarea: dashboard interactivo con Dash — paquete de trabajo

## Qué contiene esta carpeta

| Archivo | Qué es |
|---|---|
| `TAREA_Dashboard_Dash.md` | **El enunciado.** Léelo completo antes de empezar. |
| `airline_data.csv` | El conjunto de datos que debes usar: muestra de vuelos 1987-2020 (27.000 filas, 33 aerolíneas). |
| `dashboard.py` | **Plantilla de partida** con 3 `TODO` marcados. Es el archivo que debes completar. |


## Qué necesitas antes de empezar

1. **Python 3.12** y un editor (VS Code).
2. Una cuenta de **GitHub**.
3. Una cuenta en la plataforma de despliegue (**Render**), creada con **la misma cuenta de GitHub**.

## Qué debes entregar

**Solo la URL pública** del dashboard ya publicado. Nada más: no se entregan
capturas, ni PDF, ni el repositorio.

## Comprueba esto antes de enviar la URL

- [ ] Abre el enlace en una **ventana de incógnito** (sin tu sesión): debe cargar sin pedir login.
- [ ] Escribe `2010` en el campo del año: deben dibujarse los cinco gráficos.
- [ ] Borra el contenido del campo: el tablero **no** debe mostrar una pantalla de error.
- [ ] La primera visita puede tardar unos 40 segundos, porque el plan gratuito
      "duerme" la aplicación. Es normal.

## Puesta en marcha en tu equipo

```powershell
# 1. Entorno virtual e instalacion de librerias
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install dash pandas plotly

# 2. Ejecutar el dashboard (abre http://127.0.0.1:8050; se detiene con Ctrl+C)
.\.venv\Scripts\python.exe dashboard.py
```

En macOS o Linux el interprete del entorno es `.venv/bin/python`.

## Subir el proyecto a GitHub

El despliegue se conecta a tu repositorio, asi que el codigo tiene que estar alli.
El repositorio es un medio para publicar, **no** es parte de la entrega.

```powershell
git init
git add -A
git commit -m "Dashboard Dash de retrasos de vuelos"
git remote add origin https://github.com/<tu-usuario>/<tu-repositorio>.git
git branch -M main
git push -u origin main
```

> Antes de subir, comprueba con `git ls-files` que **no** aparece `.venv/` y que
> **si** aparece `airline_data.csv`.

## Orden de trabajo recomendado

1. Lee el enunciado completo (los requisitos `RF1`-`RF10` son la lista de comprobación).
2. Completa los `TODO` de `dashboard.py` y pruébalo en local.
3. Crea los archivos de despliegue que pide el enunciado (secciones 6.3 a 6.6).
4. Sube todo a un repositorio de GitHub (comandos de arriba).
5. Despliega y publica el dashboard.
6. Envía **la URL**.
