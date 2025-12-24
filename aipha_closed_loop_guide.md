# Aipha v0.0.2: El Concepto de Bucle Cerrado (Closed Loop)

El mayor problema de los sistemas de trading tradicionales es que los resultados se pierden y no hay retroalimentación automática. Aipha v0.0.2 resuelve esto mediante la **Capa 1: Autonomous Intelligence**, que cierra el bucle de ejecución.

## 🔁 La Solución: Bucle Cerrado

A diferencia de un sistema lineal, Aipha utiliza sus propios resultados para mejorar su configuración futura sin intervención humana.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                    EJECUCIÓN DEL SISTEMA                             │
└──────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
            ┌─────────────────────────────────────┐
            │  Capa 2: DESCARGA DATOS             │
            │  Binance → DuckDB                   │
            └─────────────────────────────────────┘
                              │
                              ▼
            ┌─────────────────────────────────────┐
            │  Capa 3: DETECTA SEÑALES            │
            │  (Trading Manager)                  │
            └─────────────────────────────────────┘
                              │
                              ▼
            ┌─────────────────────────────────────┐
            │  Capa 4: FILTRA CON ORACLE          │
            │  (Machine Learning)                 │
            └─────────────────────────────────────┘
                              │
                              ▼
            ┌─────────────────────────────────────┐
            │  Capa 5: ADAPTA BARRERAS            │
            │  (Post-procesamiento)               │
            └─────────────────────────────────────┘
                              │
                              ▼
         ╔════════════════════════════════════════╗
         ║  CAPA 1: CIERRA EL BUCLE ✅           ║
         ╚════════════════════════════════════════╝
```

---

## 🎯 Los 5 Pasos para Cerrar el Bucle

### PASO 1️⃣: Registrar Métricas (Memory Manager)
**¿Por qué?** Sin registro, no hay historial. Sin historial, no hay análisis.
El sistema guarda cada Win Rate, Sharpe Ratio y Drawdown en `performance_metrics.json`.

### PASO 2️⃣: Detectar Tendencias (Change Proposer)
**¿Por qué?** Necesitamos convertir números en decisiones.
El `ChangeProposer` analiza las últimas métricas (ej. los últimos 7 días vs los 7 anteriores). Si detecta una mejora o degradación significativa, genera una **Propuesta de Cambio** (ej. "Aumentar el umbral de confianza del Oráculo").

### PASO 3️⃣: Evaluar Riesgo (Change Evaluator)
**¿Por qué?** No todos los cambios son seguros.
Cada propuesta recibe un score basado en:
- **Factibilidad (30%)**: ¿Es fácil de aplicar?
- **Impacto (40%)**: ¿Cuánto mejorará el sistema?
- **Riesgo (30%)**: ¿Qué puede salir mal?
Solo los cambios con un score > 0.70 son aprobados.

### PASO 4️⃣: Aplicar Cambio (Config Manager)
**¿Por qué?** La evaluación debe traducirse en acción real.
1. Se crea un **BACKUP** de la configuración actual.
2. Se actualiza el archivo `aipha_config.json`.
3. Se recarga la configuración en memoria para que el sistema la use inmediatamente.

### PASO 5️⃣: Monitorear Resultado (Feedback Loop)
**¿Por qué?** ¿El cambio realmente ayudó o empeoró las cosas?
En el siguiente ciclo, el sistema compara los resultados nuevos con los anteriores.
- **Si mejoró**: El cambio se consolida.
- **Si empeoró**: Se ejecuta un **ROLLBACK** automático al backup anterior.

---

## 📊 Comparación: Bucle Abierto vs. Cerrado

| Aspecto | Bucle Abierto (Tradicional) | Bucle Cerrado (Aipha) |
|---------|---------------------------|----------------------|
| **Memoria** | ❌ Ninguna (se olvida) | ✅ Persistente (historial) |
| **Aprendizaje** | ❌ Manual / Imposible | ✅ Automático |
| **Cambios** | ❌ Requiere programador | ✅ Autónomos |
| **Mejora** | ❌ Accidental | ✅ Intencional y Medida |
| **Degradación** | ❌ No detectada | ✅ Auto-revertida |

---

## 📈 Conclusión: Evolución, no solo Ejecución

Con la Capa 1, Aipha deja de ser una tubería lineal y se convierte en un **Sistema Reflexivo**.

**ANTES (Lineal)**:
`Datos → Análisis → Resultados → [OLVIDO]`

**DESPUÉS (Cerrado)**:
`Datos → Análisis → Resultados → [MEMORIA] → [APRENDIZAJE] → [MEJORA] → [SIGUIENTE CICLO MEJOR]`

El bucle se cierra cuando los resultados de hoy alimentan las decisiones de mañana, **automáticamente**.
