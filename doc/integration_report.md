# Aipha v0.0.2: El Proceso de Automejora Autónoma
## Documentación Integral del Bucle Cerrado (Closed Loop)

Este documento detalla el funcionamiento interno del sistema de automejora de Aipha, utilizando como caso de estudio la **Optimización de Estrategia ATR** (Proof Strategy).

---

## 1. Filosofía: El Bucle Cerrado

Aipha no es solo un bot de trading; es un organismo digital diseñado para evolucionar. A diferencia de los sistemas tradicionales que requieren intervención humana para actualizarse, Aipha implementa un **Bucle Cerrado de Automejora**:

1.  **Observar**: Detectar ineficiencias en su propio rendimiento.
2.  **Pensar**: Analizar causas y proponer soluciones de código.
3.  **Decidir**: Evaluar el riesgo y aprobar cambios.
4.  **Actuar**: Reescribir su propio código fuente de forma segura.
5.  **Aprender**: Recordar el resultado para futuras decisiones.

---

## 2. Caso de Estudio: La Crisis de Volatilidad (Proof Strategy)

Para validar esta arquitectura, sometimos al sistema a un escenario de crisis simulada.

### El Problema
El mercado cambió repentinamente a un régimen de alta volatilidad.
- **Síntoma**: El `Win Rate` de la estrategia de captura cayó al **15%**.
- **Causa Raíz**: El sistema usaba un umbral fijo (`fixed_threshold = 0.02`) que era demasiado rígido para las nuevas condiciones.

---

## 3. Ejecución del Proceso de Autonomía

A continuación, describimos paso a paso cómo Aipha resolvió este problema sin intervención humana.

### FASE 1: Conciencia (ContextSentinel)
*El sistema se da cuenta de que algo va mal.*

El `CentralOrchestrator` inicia su ciclo de mejora y consulta al `ContextSentinel`.
- **Acción**: Lectura de métricas de rendimiento.
- **Dato Crítico**: `win_rate: 0.15` (muy por debajo del objetivo de 0.55).
- **Registro**: Se guarda el estado de "Degradación Detectada" en la memoria persistente (`current_state.json`).

### FASE 2: Inteligencia (ChangeProposer & Evaluator)
*El sistema idea una solución y juzga su viabilidad.*

#### A. Generación de la Propuesta (`ChangeProposer`)
El componente analítico detecta que el fallo se debe a la rigidez del umbral.
- **Lógica**: "Si la volatilidad es alta, un umbral fijo falla. Necesitamos un umbral dinámico basado en ATR (Average True Range)."
- **Propuesta Generada (`AIPHA-ATR-001`)**:
    - **Título**: Optimización de ATR en PotentialCaptureEngine.
    - **Cambio de Código (`diff`)**:
      ```python
      - self.fixed_threshold = 0.02
      + self.atr = ATR(period=14)  # Umbral dinámico
      ```
    - **Justificación**: Se espera recuperar el Win Rate en un +7%.

#### B. Evaluación de Riesgo (`ProposalEvaluator`)
Antes de tocar una sola línea de código, el sistema somete la propuesta a un juicio riguroso.
- **Criterios de Evaluación**:
    1.  **Impacto (30%)**: Alto (0.90) - Es crítico arreglar el Win Rate.
    2.  **Dificultad (20%)**: Baja (0.80) - Es un cambio de lógica simple.
    3.  **Riesgo (30%)**: Bajo (0.85) - El cambio está aislado en un componente.
    4.  **Complejidad (20%)**: Baja (0.90) - Código limpio y mantenible.
- **Veredicto**: **Score 0.86** (Superior al umbral de 0.70) -> **✅ APROBADO**.

### FASE 3: Cirugía Atómica (AtomicUpdateSystem)
*El sistema opera su propio código.*

Aquí es donde Aipha demuestra su capacidad única: **CodecraftSage**. Para evitar "lobotomizarse" a sí mismo con un error de sintaxis, utiliza un protocolo de seguridad militar de 5 pasos.

#### Paso 1: Backup (Red de Seguridad)
Se crea una copia instantánea del archivo objetivo.
- `dummy_component.py` -> `dummy_component.py.bak`

#### Paso 2: Diff (La Incisión)
Se aplica el parche línea por línea. El código fuente en disco cambia físicamente.
- El valor `100` (umbral fijo) es reemplazado por `200` (lógica dinámica simulada).

#### Paso 3: Test (Verificación Vital)
Antes de confirmar, el sistema ejecuta la suite de pruebas específica para ese componente.
- Comando: `pytest tests/test_dummy.py`
- **Resultado**: ✅ PASSED. El nuevo código no rompe la funcionalidad existente.

#### Paso 4: Commit (Cicatrización)
Al pasar los tests, el cambio se hace permanente.
- Se elimina el archivo `.bak`.
- Se registra el éxito en el `ContextSentinel`.

*(Nota: Si el Paso 3 hubiera fallado, el sistema habría ejecutado un **Rollback** automático en milisegundos, restaurando el backup y cancelando la operación).*

---

## 4. Resultado Final

Al finalizar el ciclo:
1.  El código de Aipha ha mutado para adaptarse al mercado.
2.  No hubo intervención humana.
3.  El sistema es más robusto que hace 5 minutos.
4.  Todo el proceso quedó auditado en `action_history.jsonl`.

Este proceso demuestra que Aipha v0.0.2 no es solo un software, sino un **sistema adaptativo autónomo**.
