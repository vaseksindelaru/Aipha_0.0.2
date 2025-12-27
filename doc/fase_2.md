# Aipha v0.0.2 - Guía de Estudio: FASE 2 (ChangeProposer & Evaluator)

En esta fase, dotamos a Aipha de **Capacidad Analítica**. Si la Fase 1 fue la "Memoria", la Fase 2 es el "Pensamiento" antes de la acción.

---

## 🧠 ¿Qué sucede en la Fase 2?

El sistema ahora puede generar propuestas de cambio basadas en datos y evaluarlas mediante un sistema de scoring ponderado.

### 1. ChangeProposer (El Proponente)
Su función es analizar el estado del sistema y proponer mejoras. En esta fase inicial, hemos implementado una propuesta fundamental: **La Optimización de ATR**.

- **Propuesta**: Reemplazar el umbral fijo de detección por un ATR (Average True Range) dinámico.
- **Justificación**: El mercado es volátil; un umbral fijo se queda obsoleto rápidamente.

### 2. ProposalEvaluator (El Juez)
No todos los cambios son buenos. El Evaluador puntúa cada propuesta del 0.0 al 1.0 basándose en:
- **Impacto (30%)**: ¿Cuánto mejorará el Win Rate?
- **Dificultad (20%)**: ¿Es fácil de programar?
- **Riesgo (30%)**: ¿Puede causar pérdidas inesperadas?
- **Complejidad (20%)**: ¿Qué tan difícil es de mantener?

> [!IMPORTANT]
> Solo las propuestas con un **Score >= 0.70** son aprobadas para su implementación.

---

## 🛠️ Componentes Técnicos

### ChangeProposal (La Estructura)
Cada propuesta es un objeto inmutable que contiene:
- `proposal_id`: Identificador único.
- `diff_content`: El cambio exacto de código propuesto.
- `test_plan`: Cómo verificar que el cambio funciona.
- `metrics`: Impacto esperado (ej: +7% Win Rate).

### Registro en Memoria
Ambos componentes utilizan el `ContextSentinel` (Fase 1) para dejar rastro:
- El Proposer registra `PROPOSAL_GENERATED`.
- El Evaluator registra `PROPOSAL_EVALUATED`.

---

## 🧪 Verificación de la Fase 2

Hemos validado esta fase con una suite de pruebas que garantiza que la lógica de decisión es sólida.

**Ejecutar Pruebas:**
```bash
pytest tests/test_phase_2.py -v
```

**Resultados:**
- Generación correcta de propuestas ATR.
- Cálculo preciso del score de evaluación.
- Persistencia de decisiones en el historial de acciones.

---

## 🚀 Siguiente Paso: FASE 3 (CodecraftSage)

Ahora que Aipha puede **proponer** y **aprobar** cambios, el siguiente paso es **implementarlos automáticamente** en el código fuente usando el protocolo atómico.

---
*Aipha v0.0.2 - El sistema que piensa antes de actuar.*
