# ⚡ QUICK REFERENCE - Aipha v2.0 Super Cerebro

## Setup (30 segundos)
```bash
# 1. Crear .env con tu API key de HuggingFace
echo "AIPHA_BRAIN_KEY=hf_YOUR_TOKEN_HERE" > .env

# 2. Verificar instalación
python3 test_final.py

# 3. ¡Listo! Usar comandos brain
aipha brain test-connection
```

## Comandos Disponibles

### 🔍 Verificación Rápida
```bash
aipha brain test-connection
# Output: Qwen 2.5 Coder 32B conectado ✅
```

### 🏥 Ver Salud del Sistema
```bash
aipha brain health
# Output: Tabla con estado de componentes
```

### 🧠 Diagnóstico Profundo
```bash
# Básico (rápido)
aipha brain diagnose

# Detallado (con evidencia citada)
aipha brain diagnose --detailed
```

### 💡 Generar Propuestas
```bash
aipha brain propose
# Output: Sugerencias de optimización automáticas
```

## Archivos Importantes

| Archivo | Propósito |
|---------|-----------|
| `.env` | Configuración (AIPHA_BRAIN_KEY) |
| `memory/aipha_config.json` | Configuración del sistema |
| `memory/current_state.json` | Estado actual |
| `memory/health_events.jsonl` | Historial de eventos |
| `memory/quarantine.jsonl` | Parámetros en cuarentena |

## Documentación

- **README.md** → Introducción general
- **ARCHITECTURE.md** → Detalles técnicos de 5 capas
- **RESUMEN_EJECUTIVO.md** → Guía para usuarios
- **IMPLEMENTATION_COMPLETE.md** → Status de implementación
- **FINAL_STATUS.md** → Estado técnico detallado

## Troubleshooting

### Error: "AIPHA_BRAIN_KEY no configurada"
```bash
echo "AIPHA_BRAIN_KEY=hf_YOUR_TOKEN" > .env
```

### Error: "No se puede conectar a LLM"
```bash
# Verificar token HuggingFace en .env
cat .env

# Verificar conexión
aipha brain test-connection
```

### Comando lento (>10 segundos)
```bash
# Normal: 3-5 segundos (incluye LLM)
# Si tarda más, puede ser issue de red o API
```

## Performance

| Comando | Tiempo |
|---------|--------|
| test-connection | <1s |
| health | ~2s |
| diagnose | ~3-5s |
| propose | ~4s |

## 5 Capas del Sistema

```
🧠 INTELLIGENCE (Capa 5)
   └─ Qwen 2.5 Coder 32B
   
💚 CONSCIENCIA (Capa 4)
   └─ HealthMonitor, Quarantine
   
🔒 ROBUSTEZ (Capa 3)
   └─ Safe-Interrupt (SIGUSR1)
   
🚀 SEGURIDAD (Capa 2)
   └─ AtomicUpdate, Validators
   
⚡ VELOCIDAD (Capa 1)
   └─ <1s latencia, FileWatcher
```

## Casos de Uso

### "¿Funciona todo bien?"
```bash
aipha brain health
```

### "¿Hay problemas?"
```bash
aipha brain diagnose
```

### "¿Cómo lo mejoro?"
```bash
aipha brain propose
```

### "¿Está conectado el LLM?"
```bash
aipha brain test-connection
```

## API Key - Dónde Obtener

1. Ir a: https://huggingface.co/settings/tokens
2. Crear token (read)
3. Copiar token
4. En terminal: `echo "AIPHA_BRAIN_KEY=hf_TOKEN" > .env`

## Verificación del Sistema

```bash
# Test final completo
python3 test_final.py

# Validación de estructura
python3 -c "
from aiphalab.cli import cli
brain = cli.commands['brain']
print('Subcommands:', list(brain.commands.keys()))
"

# Ver últimos eventos
tail -20 memory/health_events.jsonl
```

## CLI Help

```bash
# Ver todos los comandos brain
aipha brain --help

# Ver ayuda de un comando específico
aipha brain test-connection --help
aipha brain diagnose --help
aipha brain propose --help
aipha brain health --help
```

## Resetear Sistema

```bash
# Limpiar memoria (cuidado: borra historial)
rm -rf memory/*

# Recrear estructura
python3 test_final.py
```

## Status Actual

✅ Sistema: PRODUCTION READY
✅ Comandos: 4/4 operacionales
✅ Documentación: Completa
✅ Seguridad: Implementada
✅ Testing: Validado

---
**Versión**: v2.0  
**Última actualización**: 2024-12-29  
**Status**: 🟢 ACTIVO
