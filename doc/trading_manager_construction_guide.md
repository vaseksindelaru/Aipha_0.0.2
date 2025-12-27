# Guía de Construcción: Trading Manager

Esta guía detalla el proceso técnico para construir y extender el **Trading Manager** de Aipha, enfocándose en la modularidad y la integración con los datos del Data Processor.

## 1. Filosofía de Diseño
El Trading Manager se basa en la separación de responsabilidades:
- **Detectores**: Solo identifican "cuándo" mirar el mercado.
- **Etiquetadores**: Solo evalúan "qué pasó" después de mirar.
- **Estrategias**: Unen ambos mundos.

---

## 2. Implementación de Detectores
Los detectores deben ser clases con métodos estáticos o funciones puras que acepten un DataFrame de Pandas y devuelvan el mismo DataFrame con columnas de señales.

### Ejemplo: `key_candle_detector.py`
La lógica fundamental es el uso de **percentiles móviles** para el volumen. Esto permite que el detector se adapte a diferentes regímenes de mercado (alta o baja volatilidad).

```python
# Lógica clave:
df['volume_threshold'] = df['Volume'].rolling(window=50).apply(lambda x: np.percentile(x, 80))
is_key = (df['Volume'] >= df['volume_threshold']) & (body_pct <= 30)
```

---

## 3. Implementación de Etiquetadores (Potential Capture)
El etiquetado es crucial para el entrenamiento de modelos de ML. Usamos el **Triple Barrier Method** simplificado.

### El uso del ATR
En lugar de usar porcentajes fijos (ej: 1%), usamos el **ATR (Average True Range)**.
- **TP**: `Precio + (ATR * Factor_TP)`
- **SL**: `Precio - (ATR * Factor_SL)`

Esto asegura que los objetivos sean realistas según la volatilidad del momento. Si el mercado está "loco", las barreras se alejan; si está tranquilo, se acercan.

---

## 4. Integración con Data Processor (DuckDB)
Para que el Trading Manager sea funcional, debe consumir datos del Data Processor. La conexión se realiza mediante `duckdb`:

```python
import duckdb
conn = duckdb.connect('data_processor/data/aipha_data.duckdb')
df = conn.execute("SELECT * FROM btc_1h_data").df()
```

---

## 5. Flujo de Trabajo para Nuevas Estrategias
Para crear una nueva estrategia en esta capa:

1.  **Definir el Bloque**: Crea un nuevo archivo en `building_blocks/detectors/` si necesitas una nueva señal.
2.  **Configurar el Labeler**: Ajusta los factores de TP/SL en `potential_capture_engine.py`.
3.  **Ensamblar**: Crea un script en `strategies/` que importe tus bloques y ejecute el análisis.
4.  **Validar**: Usa el Win Rate y la distribución de etiquetas para iterar sobre los parámetros.

---

## 6. Próximos Pasos en el Desarrollo
- **Posicion Sizers**: Implementar lógica para decidir cuánto capital arriesgar por señal.
- **Detectores ML**: Incorporar modelos de Scikit-Learn o LightGBM como detectores de señales.
- **Backtesting Avanzado**: Integrar con librerías como `VectorBT` para análisis de drawdown y Sharpe Ratio.
