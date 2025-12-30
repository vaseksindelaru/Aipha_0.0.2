# 🚨 CRISIS RESPONSE PROTOCOL - Win Rate 30% Recovery

## SITUACIÓN CRÍTICA
```
Win Rate actual: 30% (CRÍTICO)
Problema: Sistema no está ganando suficientemente
Solución: Ajustar confidence_threshold para mayor sensibilidad
```

## SOLUCIÓN INMEDIATA

### Paso 1: Crear Propuesta de Cambio
```bash
aipha proposal create \
  --component orchestrator \
  --parameter confidence_threshold \
  --new-value "0.65" \
  --reason "Aumentar sensibilidad para operaciones en crisis"
```

**Output Esperado:**
```
✅ PROPUESTA CREADA
  ID: PROP_MANUAL_XXXXXXXX
  Componente: orchestrator
  Parámetro: confidence_threshold
  Nuevo Valor: 0.65
  Estado: PENDING_EVALUATION

💡 Siguiente paso: aipha proposal evaluate PROP_MANUAL_XXXXXXXX
```

**Captura el ID** (ej: `PROP_MANUAL_04E00882`) para los siguientes pasos.

### Paso 2: Evaluar Propuesta
```bash
aipha proposal evaluate PROP_MANUAL_XXXXXXXX
```

**Output Esperado:**
```
🔍 Evaluando propuesta...

📊 EVALUACIÓN COMPLETADA
Propuesta: PROP_MANUAL_XXXXXXXX
Score: 0.87 / 1.00
Estado: ✅ APROBADO

Evaluación:
- Impacto (30%): 0.90
- Dificultad (20%): 0.80
- Riesgo (30%): 0.85
- Complejidad (20%): 0.90
Score Total: 0.87 -> APROBADO

💡 Siguiente paso: aipha proposal apply PROP_MANUAL_XXXXXXXX
```

### Paso 3: Aplicar Propuesta con Protocolo Atómico
```bash
aipha proposal apply PROP_MANUAL_XXXXXXXX
```

**Output Esperado:**
```
🚀 Aplicando propuesta: PROP_MANUAL_XXXXXXXX
  Componente: orchestrator
  Parámetro: confidence_threshold
  Nuevo Valor: 0.65

[1/4] 💾 BACKUP
  Creando copia de seguridad del estado actual...
  ✅ Backup creado

[2/4] 📝 DIFF
  Preparando cambio: confidence_threshold = 0.65
  Anterior: 0.75
  Nuevo:    0.65
  ✅ Diff preparado

[3/4] 🧪 TEST
  Validando cambios...
  ✓ Tipo: válido (numérico)
  ✅ Validaciones pasadas

[4/4] ✅ COMMIT
  Consolidando cambios...
  ✅ Cambios consolidados

============================================================
✅ PROTOCOLO ATÓMICO COMPLETADO
============================================================

Propuesta PROP_MANUAL_XXXXXXXX ha sido aplicada exitosamente.
  • Componente: orchestrator
  • Parámetro: confidence_threshold
  • Anterior: 0.75
  • Nuevo: 0.65
  • Razón: Aumentar sensibilidad para operaciones en crisis

✨ Sistema actualizado y seguro
```

## VERIFICACIÓN DEL CAMBIO

### Ver todas las propuestas
```bash
aipha proposal list
```

Verás una tabla con:
- ID: PROP_MANUAL_XXXXXXXX
- Componente: orchestrator
- Parámetro: confidence_threshold
- Nuevo Valor: 0.65
- Estado: APPLIED
- Score: 0.87

### Verificar en el config
```bash
cat memory/aipha_config.json | grep -A 5 "orchestrator"
```

Debe mostrar:
```json
"orchestrator": {
  "confidence_threshold": "0.65"
}
```

## OPCIONES DE VALORES PARA TUNING

| confidence_threshold | Impacto | Riesgo | Uso |
|----------------------|---------|--------|-----|
| 0.95+ | Muy bajo | Muy bajo | Solo operaciones ultra seguras |
| 0.75-0.90 | Bajo | Bajo | Estándar (actual: 0.75) |
| 0.65-0.75 | Moderado | Moderado | Crisis LIGERA |
| 0.50-0.65 | Alto | Moderado | Crisis GRAVE (0.65) |
| < 0.50 | Muy Alto | Alto | EMERGENCIA (uso con cuidado) |

## OTROS PARÁMETROS PARA AJUSTAR

Si confidence_threshold no es suficiente, prueba:

```bash
# Aumentar ATR factor para más oportunidades
aipha proposal create \
  --component Trading \
  --parameter atr_period \
  --new-value "10" \
  --reason "Reducir período para mayor sensibilidad"

# Reducir threshold de volumen
aipha proposal create \
  --component Trading \
  --parameter volume_percentile_threshold \
  --new-value "80" \
  --reason "Permitir más volúmenes"

# Ajustar Oracle threshold
aipha proposal create \
  --component Oracle \
  --parameter confidence_threshold \
  --new-value "0.65" \
  --reason "Mayor senibilidad del modelo"
```

## PROTOCOLO ATÓMICO EXPLICADO

```
💾 BACKUP: Copia de seguridad antes de cambiar
  └─ Archivo: memory/.backup_PROP_MANUAL_XXXX.json

📝 DIFF: Aplica el cambio propuesto
  └─ Muestra valores anteriores vs nuevos

🧪 TEST: Valida que el cambio es válido
  └─ Verifica tipo, rango, integridad

✅ COMMIT: Guarda cambios en memory/aipha_config.json
  └─ Si algo falla, automáticamente ROLLBACK

🔄 ROLLBACK (automático si algo falla):
  └─ Restaura backup si tests fallan
```

## MONITOREO POST-CAMBIO

Después de aplicar:

1. Monitorear Win Rate
2. Ver health status
   ```bash
   aipha brain health
   ```

3. Ver diagnóstico si hay problemas
   ```bash
   aipha brain diagnose
   ```

4. Generar propuestas de mejora adicionales
   ```bash
   aipha brain propose
   ```

## ROLLBACK (Si necesitas revertir)

Si el cambio empeora el sistema:

```bash
# Usa el backup que se creó automáticamente
cp memory/.backup_PROP_MANUAL_XXXXXXXX.json memory/aipha_config.json

# O crea una nueva propuesta para revertir
aipha proposal create \
  --component orchestrator \
  --parameter confidence_threshold \
  --new-value "0.75" \
  --reason "Revertir cambio de crisis"
```

## COMBINACIÓN RECOMENDADA PARA CRISIS

Para recuperación de Win Rate 30% → 50%+:

```bash
# 1. Aumentar sensibilidad del orchestrator
aipha proposal create --component orchestrator --parameter confidence_threshold --new-value "0.65" --reason "Crisis L1"

# 2. Aumentar sensibilidad del oracle
aipha proposal create --component Oracle --parameter confidence_threshold --new-value "0.65" --reason "Crisis L1"

# 3. Reducir período ATR
aipha proposal create --component Trading --parameter atr_period --new-value "10" --reason "Crisis L1"

# 4. Evaluar y aplicar todas
aipha proposal evaluate PROP_MANUAL_XXXX1
aipha proposal evaluate PROP_MANUAL_XXXX2
aipha proposal evaluate PROP_MANUAL_XXXX3

aipha proposal apply PROP_MANUAL_XXXX1
aipha proposal apply PROP_MANUAL_XXXX2
aipha proposal apply PROP_MANUAL_XXXX3
```

## STATUS DEL SISTEMA DESPUÉS

```
✅ Propuestas creadas: 1+
✅ Evaluadas: score 0.87+
✅ Aplicadas: protocolo atómico completado
✅ Backup: seguro
✅ Config actualizado: memory/aipha_config.json
✅ Historial: registrado en action_history.jsonl

Sistema listo para testing con nuevos parámetros
```

---

**Versión**: Crisis Response v1  
**Fecha**: 2024-12-30  
**Status**: 🚨 IMPLEMENTADO PARA EMERGENCIAS
