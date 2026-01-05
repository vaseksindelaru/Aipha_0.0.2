# 🦅 Aipha v2.1: Autonomous Trading System

> **Estado:** ✅ RENTABLE (Win Rate 56.12%) | 🛡️ HARDENED | 🧠 SELF-IMPROVING

Aipha es un sistema de trading algorítmico autónomo diseñado para **auto-mejorarse**. Utiliza un bucle de retroalimentación cerrado donde un Orquestador (IA) analiza métricas de trading, genera propuestas de cambio de código/configuración, las evalúa y las aplica de forma atómica.

---

## 🚀 Características Clave (v2.1)

- **Estrategia Ganadora:** "Trend Following" con barreras asimétricas (TP 1.0 / SL 2.0).
- **Core Reforzado (`HardenedOrchestrator`):** Resistente a fallos, con manejo de señales (SIGUSR1/SIGUSR2) y colas de prioridad.
- **CLI Avanzado:** Interfaz completa para monitoreo, diagnóstico y control manual (`aipha status`, `aipha dashboard`).
- **Memoria Persistente:** Sistema de logs y estado en JSONL que sobrevive a reinicios.
- **Seguridad Atómica:** Los cambios de código se prueban y pueden revertirse automáticamente si fallan.

---

## 🛠️ Instalación y Uso

### Requisitos
- Python 3.10+
- Entorno Linux/Unix

### Comandos Principales

1. **Ver Estado del Sistema**
   ```bash
   aipha status
   ```

2. **Ejecutar un Ciclo de Mejora**
   ```bash
   aipha cycle run
   ```

3. **Panel de Control en Tiempo Real**
   ```bash
   aipha dashboard
   ```

4. **Diagnóstico de Salud**
   ```bash
   aipha brain health
   ```

---

## 📂 Estructura del Proyecto

- **`core/`**: El cerebro del sistema (`orchestrator_hardened.py`, `context_sentinel.py`).
- **`trading_manager/`**: Lógica de mercado (`proof_strategy.py`, detectores).
- **`aiphalab/`**: Herramientas de interfaz y CLI.
- **`memory/`**: Base de datos persistente (Configuración, Historial, Métricas).

---

## 📊 Rendimiento Actual
- **Estrategia:** Continuación de Tendencia (Trend Following)
- **Win Rate:** 56.12%
- **Gestión de Riesgo:** Asimetría Defensiva (SL amplio para evitar ruido).

---

## 📜 Documentación Adicional
- [Resumen Final v2.1](./RESUMEN_FINAL_COMPLETO_AIPHA_v2_1.md) - Detalles del hito de rentabilidad.
- [Arquitectura](./ARCHITECTURE.md) - Diseño técnico del sistema.
- [Guía CLI](./GUIA_CLI_PANEL_CONTROL.md) - Manual completo de comandos.
