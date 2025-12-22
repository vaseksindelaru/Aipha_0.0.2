# Aipha - Sistema de Trading Inteligente

Este repositorio contiene la implementación central del sistema Aipha, organizado en componentes funcionales que colaboran para transformar datos de mercado en decisiones de trading optimizadas.

## 🏗️ Arquitectura del Sistema

El sistema se divide en cuatro pilares fundamentales que operan de forma secuencial y coordinada:

### 1. Data Processor (Capa 2)
**Responsabilidad**: Adquisición y Persistencia.
- Descarga datos históricos de Binance Vision.
- Procesa y limpia archivos CSV/ZIP.
- Almacena los datos en una base de datos analítica local (**DuckDB**).
- *Documentación*: [data_processor/README.md](file:///home/vaclav/Aipha_0.0.2/data_processor/README.md)

### 2. Trading Manager (Capa 3)
**Responsabilidad**: Lógica de Ejecución y Estrategia.
- Implementa detectores de señales basados en patrones de velas y volumen.
- Utiliza el **Triple Barrier Method** con ATR para definir objetivos de salida (TP/SL).
- Transforma los datos crudos en eventos accionables con etiquetas de rendimiento.
- *Documentación*: [trading_manager/README.md](file:///home/vaclav/Aipha_0.0.2/trading_manager/README.md)

### 3. Oracle (Capa 4)
**Responsabilidad**: Inteligencia y Filtrado.
- Utiliza modelos de **Machine Learning** (Random Forest) para validar señales.
- Extrae características avanzadas (features) de cada evento detectado.
- Filtra las señales de baja probabilidad, aumentando significativamente el Win Rate del sistema.
- *Documentación*: [oracle/README.md](file:///home/vaclav/Aipha_0.0.2/oracle/README.md)

### 4. Data Postprocessor (Capa 5)
**Responsabilidad**: Auto-Mejora y Adaptación.
- Realiza análisis post-mortem de los trades ejecutados.
- Identifica "ruido" de mercado y ajusta dinámicamente la sensibilidad de las barreras.
- Cierra el bucle de retroalimentación para que el sistema aprenda de sus errores en tiempo real.
- *Documentación*: [data_postprocessor/README.md](file:///home/vaclav/Aipha_0.0.2/data_postprocessor/README.md)

---

## 🔄 Flujo de Trabajo Integrado

1.  **Adquisición**: El `Data Processor` puebla la base de datos con velas históricas.
2.  **Detección**: El `Trading Manager` identifica oportunidades (Velas Clave).
3.  **Validación**: El `Oracle` analiza la oportunidad y decide si es apta para operar.
4.  **Ejecución**: Se simula el trade con barreras dinámicas de ATR.
5.  **Aprendizaje**: El `Data Postprocessor` evalúa el resultado y ajusta los multiplicadores para futuras señales.

## 🚀 Próximos Pasos: Capa 1
Esta estructura consolidada sirve como base para la implementación de la **Capa 1**, que se encargará de la orquestación de alto nivel, gestión de memoria y reglas de evolución del sistema completo.

---
*Aipha - Hacia un sistema de trading autónomo y auto-mejorable.*
# Aipha_0.0.2
