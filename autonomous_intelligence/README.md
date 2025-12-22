# GUÍA PARA CONSTRUIR CAPA 1 EN AIPHA_0.0.2

## 📋 TABLA DE CONTENIDOS
1. [Estado Actual del Proyecto](#estado-actual)
2. [Arquitectura de Capa 1](#arquitectura-capa-1)
3. [Plan de Implementación (Fases)](#plan-implementacion)
4. [Especificaciones Técnicas](#especificaciones)
5. [Roadmap de Evolución a Largo Plazo](#roadmap-futuro)

---

## 🔍 ESTADO ACTUAL DEL PROYECTO {#estado-actual}

### Capas Implementadas (SÓLIDAS ✅)
| Capa | Nombre | Estado | Responsabilidad |
|------|--------|--------|-----------------|
| 2 | Data Processor | ✅ COMPLETA | Adquisición y persistencia (DuckDB) |
| 3 | Trading Manager | ✅ COMPLETA | Detección de señales + etiquetado (ATR) |
| 4 | Oracle | ✅ COMPLETA | Filtrado con ML (Random Forest) |
| 5 | Data Postprocessor | ✅ COMPLETA | Auto-mejora de barreras (adaptativo) |

### Capa 1 (PENDIENTE ⏳)
- **Actual**: NO EXISTE
- **Necesaria para**: Orquestación inteligente, memoria persistente, auto-proposición de cambios
- **Impacto**: Sin Capa 1, el sistema no puede mejorar autónomamente

---

## 🏛️ ARQUITECTURA DE CAPA 1 {#arquitectura-capa-1}

### Visión General
```text
┌─────────────────────────────────────────────┐
│      CAPA 1: INTELIGENCIA AUTÓNOMA          │
│   (Orquestación + Memoria + Auto-Mejora)    │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────┐  ┌──────────────┐       │
│  │   MEMORIA    │  │  EVALUADOR   │       │
│  │ (Historial   │  │   (Score     │       │
│  │  + Estado)   │  │    Cambios)  │       │
│  └──────────────┘  └──────────────┘       │
│         ▲                ▲                  │
│         │                │                  │
│  ┌──────────────────────────────┐         │
│  │   ORQUESTADOR CENTRAL         │         │
│  │  (Controla flujo global)      │         │
│  └──────────────────────────────┘         │
│         ▲                ▲                  │
│         │                │                  │
│  ┌──────────────┐  ┌──────────────┐       │
│  │   PROPOSER   │  │  APROBADOR   │       │
│  │  (Sugiere    │  │  (Valida     │       │
│  │   cambios)   │  │   cambios)   │       │
│  └──────────────┘  └──────────────┘       │
│                                             │
└─────────────────────────────────────────────┘
         ▼ (EJECUTA)
    [CAPA 2-5: Sistema Existente]
```

### Componentes Principales

#### 1️⃣ Memory Manager (`memory_manager.py`)
**Función**: Persistencia de estado y decisiones.
**Archivos persistentes**:
- `action_history.jsonl`: Historial atómico de todas las acciones.
- `system_state.json`: Estado actual del sistema.
- `performance_metrics.json`: Métricas de rendimiento por período.

#### 2️⃣ Change Proposer (`change_proposer.py`)
**Función**: Sugiere mejoras basadas en métricas.
**Lógica**:
- Analiza tendencias de rendimiento.
- Genera propuestas de cambio (parámetros, features, modelos).
- Proporciona justificación cuantitativa.

#### 3️⃣ Change Evaluator (`change_evaluator.py`)
**Función**: Califica propuestas antes de aplicarlas.
**Criterios de scoring (0.0-1.0)**:
- **Factibilidad** (0.3): ¿Técnicamente posible? ¿Sin romper dependencias?
- **Impacto** (0.4): ¿Mejora métricas principales?
- **Riesgo** (0.3): ¿Puede causar regresión?

**Umbral de aprobación**: Score ≥ 0.70

#### 4️⃣ Central Orchestrator (`orchestrator.py`)
**Función**: Dirección central del ciclo de mejora.
**Flujo**:
1. Recolectar métricas de Capa 2-5.
2. Proposer sugiere cambios.
3. Evaluator puntúa.
4. Si score ≥ 0.70 → APROBAR automáticamente.
5. Si score < 0.70 → RECHAZAR + registrar razón.
6. Memory Manager persiste todo.
7. Volver a 1 (próximo ciclo).

---

## 📅 PLAN DE IMPLEMENTACIÓN {#plan-implementacion}

### FASE 1A: Memory Manager (1-2 semanas)
**Objetivo**: Persistencia confiable del estado.

### FASE 1B: Change Proposer (2 semanas)
**Objetivo**: Sugerir cambios automáticamente.

### FASE 1C: Change Evaluator (2 semanas)
**Objetivo**: Puntuar propuestas automáticamente.

### FASE 1D: Central Orchestrator (2-3 semanas)
**Objetivo**: Unir todo en un ciclo automático.

---

## 🎯 ESPECIFICACIONES TÉCNICAS {#especificaciones}

### Estructura de Directorios Capa 1
```text
autonomous_intelligence/
├── core/
│   ├── __init__.py
│   ├── memory_manager.py        ✅ FASE 1A
│   ├── change_proposer.py       ✅ FASE 1B
│   ├── change_evaluator.py      ✅ FASE 1C
│   └── orchestrator.py          ✅ FASE 1D
├── memory/  # Almacenamiento persistente
│   ├── action_history.jsonl     (append-only)
│   ├── system_state.json
│   └── performance_metrics.json
└── tests/
    ├── test_memory_manager.py
    ├── test_change_proposer.py
    ├── test_change_evaluator.py
    └── test_orchestrator.py
```

---

## 🚀 ROADMAP DE EVOLUCIÓN {#roadmap-futuro}

### CORTO PLAZO (3-6 meses)
**Objetivo**: Ciclo autónomo funcional.

### MEDIANO PLAZO (6-12 meses)
**Objetivo**: Auto-mejora inteligente con contexto.

### LARGO PLAZO (12+ meses)
**Objetivo**: Aipha Completamente Autónoma.
