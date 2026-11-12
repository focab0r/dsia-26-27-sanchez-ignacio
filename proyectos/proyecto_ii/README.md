# Predicción de ozono en Madrid a partir de la meteorología

Proyecto II — Automatización e integración de servicios. Este repositorio es la base del Trabajo Final (Proyecto III).

El proyecto predice la concentración media diaria de ozono (O₃) en Madrid a partir de variables meteorológicas. Combina dos piezas:

1. Un **modelo de regresión lineal de scikit-learn**, entrenado con datos abiertos del Ayuntamiento de Madrid.
2. Un **modelo de lenguaje accedido por API**, que convierte una descripción del tiempo en lenguaje natural ("mañana 34 grados, soleado, casi sin viento") en las variables numéricas que necesita el modelo de regresión.

## Limitaciones conocidas

Tres puntos importantes del estado actual, todos previstos como mejora en el Proyecto III:

- **El preprocesamiento es muy lento.** La carga y transformación de los datos de origen (`--load`) tarda mucho. Se implementó así por falta de tiempo; la optimización prevista apunta a hacerlo hasta unas 600 veces más rápido.
- **La carga de datos es manual y algo compleja.** `--load` necesita que los CSV anuales estén ya descargados del portal y colocados en dos carpetas distintas, una para calidad del aire y otra para meteorología. En el futuro, el propio pipeline descargará esos ficheros con peticiones HTTP (`requests`) al portal de datos abiertos.
- **El ajuste del modelo es moderado: R² ≈ 0,54.** La meteorología explica algo más de la mitad de la variación del ozono diario. Es el resultado actual, no el definitivo: se trabajará en mejorarlo.

## Dominio y datos

**Motivación.** El ozono troposférico se forma con radiación solar y calor, por lo que su relación con la meteorología es directa y razonablemente lineal. Eso lo hace un buen objetivo para una regresión lineal, y permite un producto sencillo de explicar: estimar el ozono de un día a partir de su previsión del tiempo.

**Origen.** [Portal de datos abiertos del Ayuntamiento de Madrid](https://datos.madrid.es):

| Conjunto de datos | Uso en el proyecto |
| --- | --- |
| [Calidad del aire. Datos diarios](https://datos.madrid.es/dataset/201410-0-calidad-aire-diario) | Variable objetivo: ozono (magnitud 14) |
| [Datos meteorológicos. Datos diarios desde 2019](https://datos.madrid.es/dataset/300351-0-meteorologicos-diarios) | Variables predictoras |
| [Calidad del aire. Estaciones de control](https://datos.madrid.es/dataset/212629-0-estaciones-control-aire) | Códigos y ubicación de las estaciones |
| [Datos meteorológicos. Estaciones de control](https://datos.madrid.es/dataset/300360-0-meteorologicos-estaciones) | Códigos y ubicación de las estaciones |

**Formato de origen.** Cada fila es una estación, una magnitud y un mes, con los días en columnas (`D01`…`D31`) y un indicador de validez por día (`V01`…`V31`).

**Variables predictoras** (medias diarias):

| Código | Variable | Unidad |
| --- | --- | --- |
| 81 | Velocidad del viento | m/s |
| 82 | Dirección del viento | grados |
| 83 | Temperatura | °C |
| 86 | Humedad relativa | % |
| 87 | Presión barométrica | mb |
| 88 | Radiación solar | W/m² |
| 89 | Precipitación | l/m² |

### Preprocesamiento

- **Se elimina el día 31** de todos los meses.
- **Los valores nulos se rellenan con la media entre estaciones.** No todas las estaciones miden las mismas variables, así que hay muchos huecos. Cada uno se sustituye por la media de esa magnitud entre todas las estaciones que sí tienen valor ese mismo día, mes y año. Con este criterio se rellenan todos los nulos.
- **El dataset final tiene unas 35.000 filas** y se guarda en `data/training_data.csv`.

## Instalación

El proyecto usa [uv](https://docs.astral.sh/uv/) para gestionar el entorno y las dependencias:

```bash
uv sync
```

Después, copia la plantilla `.env.example` como `.env` (este último nunca se sube a Git) y rellena sus claves:

```bash
cp .env.example .env
```

```bash
FOUNDRY_API_KEY=<KEY>
FOUNDRY_AGENT_ENDPOINT=<URL>
FOUNDRY_API_VERSION=<VERSION>
```

| Variable | Descripción |
| --- | --- |
| `FOUNDRY_API_KEY` | Clave de API del proyecto de Foundry |
| `FOUNDRY_AGENT_ENDPOINT` | URL del agente |
| `FOUNDRY_API_VERSION` | Versión de la API (`v1`) |

## Uso

Todo el pipeline se maneja desde el módulo `proyecto_ii.cli`:

```bash
uv run python -m proyecto_ii.cli -h
```

```text
usage: cli.py [-h] [-l] [-t] [-p PREDICT] [-a ASK_AGENT]
```

| Opción | Qué hace |
| --- | --- |
| `-h`, `--help` | Muestra la ayuda. |
| `-l`, `--load` | Lee los CSV anuales de las dos carpetas de datos (calidad del aire y meteorología), los procesa y genera el CSV de entrenamiento. Requiere haber descargado antes los ficheros, y es el paso lento (ver "Limitaciones conocidas"). |
| `-t`, `--train` | Entrena el modelo de regresión con el CSV generado y lo guarda. |
| `-p FICHERO`, `--predict FICHERO` | Predice el ozono a partir de un CSV con las variables meteorológicas. |
| `-a "TEXTO"`, `--ask-agent "TEXTO"` | Envía una descripción del tiempo al agente de IA, que genera los valores del CSV, y devuelve la predicción. |

Flujo habitual:

```bash
uv run python -m proyecto_ii.cli --load                  # 1. preparar los datos
uv run python -m proyecto_ii.cli --train                 # 2. entrenar el modelo
uv run python -m proyecto_ii.cli --predict entrada.csv   # 3a. predecir desde un CSV
uv run python -m proyecto_ii.cli --ask-agent "Fecha: 2026-07-15. Temperatura media de 27 grados, viento flojo del noreste, humedad del 35 %, presión de 942 mb, despejado y sin lluvia."   # 3b. predecir desde texto
```

Formato del CSV de entrada para `--predict` (una fila por día, una columna por variable):

```csv
81,82,83,86,87,88,89
0.69,16.0,11.6,51.0,950.5,82.3,0.05
```


## Modelo scikit-learn

- **Tipo:** regresión lineal (`LinearRegression`).
- **Objetivo:** concentración media diaria de ozono, en µg/m³.
- **Entradas:** las siete variables meteorológicas de la tabla anterior.
- **Persistencia:** el modelo entrenado se guarda con `joblib` en `data/model.joblib`.
- **Evaluación:** los datos se dividen en un 80 % para entrenamiento y un 20 % para prueba.
- **Métrica actual:** R² ≈ 0,54.

## Cliente de IA

- **Proveedor:** Microsoft Foundry.
- **Modelo:** GPT-4o, desplegado como agente con un prompt de sistema propio.
- **Tarea:** generación de texto (chat) para extracción de datos estructurados.
- **Para qué se usa:** crea la entrada del modelo de regresión. Recibe una frase con la fecha y la descripción del tiempo, y devuelve un JSON con las siete variables meteorológicas.

**Por qué Foundry y no Hugging Face.** La Inference API de Hugging Face es de pago: desde octubre de 2026 las cuentas gratuitas ya no incluyen créditos de inferencia. Como el enunciado admite otro proveedor de API documentado, se ha optado por Microsoft Foundry.

**El prompt del agente.** Define las siete variables y sus unidades, e indica al modelo que:

- extraiga solo lo que el usuario ha dicho, con cifras o con descripciones cualitativas de una tabla de conversión ("soleado", "viento flojo", "sin lluvia"…);
- convierta unidades cuando haga falta (km/h a m/s, hPa a mb) y promedie máxima y mínima de temperatura;
- nunca invente un valor: si falta alguna variable, devuelve siempre el mismo tipo de error indicando cuáles faltan;
- responda únicamente con JSON.

Respuesta cuando todas las variables están informadas:

```json
{"status": "ok", "data": {"81": 1.0, "82": 45, "83": 27, "86": 35, "87": 942, "88": 300, "89": 0}}
```

Respuesta cuando falta alguna:

```json
{"status": "error", "error": {"type": "MISSING_FIELDS", "message": "82,86,87,89"}}
```

### Modo mock

Si el texto enviado contiene la cadena `[mock]` en cualquier posición, el cliente no consulta a ninguna IA y devuelve un valor fijo de prueba. Permite ejecutar el pipeline sin credenciales ni coste:

```bash
uv run python -m proyecto_ii.cli --ask-agent "[mock] cualquier texto"
```

## Logs

El pipeline escribe en consola y en `logs/log_AAAA-MM-DD.log`, con el formato `fecha nivel: mensaje`. La configuración está en `logging.conf`, en la raíz del proyecto. El repositorio incluye un log de ejemplo en `logs/`.

## Tests

El proyecto incluye 5 tests con pytest, repartidos en `tests/test_model.py` y `tests/test_preprocess.py`. Cubren la carga de datos, el entrenamiento del modelo y partes del preprocesamiento, con los datos de ejemplo de `tests/data/`.

```bash
uv run pytest
```

## Estructura del proyecto

```text
├── .env                         # credenciales (no se sube a Git)
├── .env.example                 # plantilla del .env
├── data
│   ├── model.joblib             # modelo entrenado
│   └── training_data.csv        # CSV final con el que se entrena el modelo
├── logging.conf                 # configuración de logging
├── logs
│   └── log_2026-11-12.log       # log de ejemplo
├── pyproject.toml
├── README.md
├── src
│   └── proyecto_ii
│       ├── __init__.py
│       ├── agent.py             # cliente del agente de IA (incluye el modo mock)
│       ├── cli.py               # punto de entrada y opciones de línea de comandos
│       ├── loader.py            # lectura de los ficheros de origen
│       ├── model.py             # entrenamiento y predicción
│       └── preprocess.py        # limpieza y transformación de los datos
├── tests
│   ├── data                     # datos que necesitan los tests
│   │   ├── calidad.csv
│   │   └── prediction.csv
│   ├── test_model.py
│   └── test_preprocess.py
└── uv.lock
```

## Uso de IA en el desarrollo

Ver [`AI_USAGE.md`](AI_USAGE.md).

## Continuidad hacia el Proyecto III

Sobre esta base, el Proyecto III añadirá:

- integración continua y mayor robustez;
- la descarga automática de los datos mediante peticiones HTTP (`requests`) al portal de datos abiertos, en lugar de la descarga manual a dos carpetas;
- un preprocesamiento mucho más rápido;
- un modelo con mejor ajuste.