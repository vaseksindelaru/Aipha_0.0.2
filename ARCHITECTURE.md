# Aipha v2.1 - Arquitectura del Sistema Autónomo de 5 Capas

> **Estado:** ✅ RENTABLE | 🛡️ HARDENED | 🧹 CLEAN
> **Win Rate:** 56.12% (Trend Following)

---

## 🏛️ Las 5 Capas Fundamentales (v2.1)

### 🚀 CAPA 1: VELOCIDAD (Core)
**Archivo Maestro**: `core/orchestrator_hardened.py`

- **HardenedOrchestrator**: Cerebro central resistente a fallos.
- **ExecutionQueue**: Cola de prioridad (Usuario > Sistema).
- **Signal Handlers**: Interrupciones seguras (SIGUSR1/SIGUSR2).
- **Health Checks**: Monitoreo continuo de integridad.

### 🔐 CAPA 2: SEGURIDAD (Atomicidad)
**Archivo**: `core/atomic_update_system.py`

- **Actualizaciones ACID**: Backup -> Diff -> Test -> Commit -> Rollback.
- **Validación Pydantic**: `core/config_validators.py` asegura integridad de parámetros.
- **Quarantine Manager**: Aísla componentes defectuosos automáticamente.

### 🛡️ CAPA 3: ESTRATEGIA (Trading)
**Archivos**: `trading_manager/strategies/proof_strategy.py`, `potential_capture_engine.py`

- **Lógica**: Trend Following (Continuación).
- **Gestión de Riesgo**: Triple Barrier Method Asimétrico (SL 2.0 / TP 1.0).
- **Detectores**: Velas clave + Filtro de Tendencia (EMA 200).

### 💚 CAPA 4: CONSCIENCIA (Memoria)
**Archivo**: `core/context_sentinel.py`

- **Memoria Persistente**: JSONL (Append-only) para historial de acciones.
- **Estado Global**: `memory/current_state.json`.
- **Configuración Viva**: `memory/aipha_config.json`.

### 🧠 CAPA 5: INTELIGENCIA (LLM)
**Archivos**: `core/llm_client.py`, `core/llm_assistant.py`

- **Modelo**: Qwen 2.5 Coder 32B.
- **Función**: Diagnóstico profundo, generación de propuestas complejas y análisis de causa raíz.
- **Integración**: Vía CLI (`aipha brain diagnose`) y Orquestador.

---

## 🎛️ Interface de Línea de Comandos (CLI)

El sistema se controla totalmente desde la terminal:

| Comando | Descripción |
|---------|-------------|
| `aipha status` | Ver métricas vitales (Win Rate, Drawdown) |
| `aipha dashboard` | Panel de control en tiempo real |
| `aipha cycle run` | Ejecutar ciclo de automejora manual |
| `aipha brain diagnose` | Solicitar análisis del LLM |
| `aipha proposal create` | Inyectar propuesta manual |

---

## 🔄 El Ciclo de Automejora (Hardened Loop)

1.  **Recolección**: El Orquestador lee métricas de `proof_strategy.py`.
2.  **Análisis**: El LLM o heurísticas detectan anomalías (ej: Win Rate < 50%).
3.  **Propuesta**: Se genera un cambio (ej: "Cambiar a Trend Following").
4.  **Evaluación**: Se simula el impacto y riesgo.
5.  **Ejecución Atómica**: Se aplica el cambio con rollback automático si fallan los tests.
6.  **Veredicto**: Se mide el impacto real en el siguiente ciclo (Hito 5).

---

## 📂 Estructura del Proyecto (Limpia)

```
Aipha_0.0.2/
├── core/                    # El Cerebro Blindado
│   ├── orchestrator_hardened.py
│   ├── context_sentinel.py
│   ├── atomic_update_system.py
│   ├── llm_assistant.py
│   └── ...
├── trading_manager/         # El Músculo
│   ├── strategies/proof_strategy.py
│   └── building_blocks/...
├── aiphalab/                # La Voz (CLI)
│   ├── cli.py
│   └── dashboard.py
├── memory/                  # La Memoria
│   ├── aipha_config.json    # Configuración Ganadora
│   └── ...
└── life_cycle.py            # El Corazón (Loop principal)
```

---

*Documentación actualizada para Aipha v2.1*
