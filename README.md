# Aipha v2.0 - Sistema Autónomo de 5 Capas

Aipha es un sistema inteligente y autónomo que evoluciona continuamente. Implementa 5 capas de arquitectura: **Velocidad**, **Seguridad**, **Robustez**, **Consciencia** e **Inteligencia**.

## 🧬 ¿Qué hace único a Aipha?

| Característica | Bots Tradicionales | Aipha v2.0 |
|----------------|-------------------|------------|
| Velocidad | ❌ Segundos | ✅ <1s (SIGUSR1) |
| Seguridad | ❌ Básica | ✅ ACID Atómica |
| Robustez | ❌ Manual | ✅ Auto-recuperación |
| Consciencia | ❌ N/A | ✅ Health Monitor |
| Inteligencia | ❌ N/A | ✅ Qwen 2.5 Coder 32B |

## 🏛️ Arquitectura de 5 Capas

```
┌─────────────────────────────────────────────────────┐
│  CAPA 5: INTELIGENCIA (Qwen 2.5 Coder 32B LLM)     │
├─────────────────────────────────────────────────────┤
│  CAPA 4: CONSCIENCIA (Health Monitor + Quarantine) │
├─────────────────────────────────────────────────────┤
│  CAPA 3: ROBUSTEZ (Interrupciones Seguras)         │
├─────────────────────────────────────────────────────┤
│  CAPA 2: SEGURIDAD (Actualizaciones ACID)          │
├─────────────────────────────────────────────────────┤
│  CAPA 1: VELOCIDAD (File Watcher + SIGUSR1 <1s)   │
└─────────────────────────────────────────────────────┘
```

**Documentación completa**: [ARCHITECTURE.md](ARCHITECTURE.md)

## 🚀 Inicio Rápido

### Configuración Inicial
```bash
# 1. Copiar template de configuración
cp .env.example .env

# 2. Editar .env con tu API key de HuggingFace
# Obtén un token en: https://huggingface.co/settings/tokens
export AIPHA_BRAIN_KEY="hf_YOUR_TOKEN_HERE"

# 3. Verificar que todo funciona
python3 test_final.py
```

### Usar el CLI
```bash
# Ver estado del sistema
python3 -m aiphalab.cli status

# Ejecutar ciclo de automejora
python3 -m aiphalab.cli cycle run

# Dashboard en tiempo real
python3 -m aiphalab.cli dashboard

# Análisis con LLM
python3 -m aiphalab.cli llm analyze orchestrator
```

### Ejecutar Tests
```bash
pytest tests/ -v
```

## 📂 Estructura del Proyecto

```
Aipha_0.0.2/
├── core/                    # 🧠 Inteligencia Autónoma
│   ├── orchestrator.py      # Orquestador central
│   ├── context_sentinel.py  # Memoria persistente
│   ├── change_proposer.py   # Generador de propuestas
│   ├── llm_proposer.py      # Integración LLM
│   └── atomic_update_system.py
├── trading_manager/         # 📈 Estrategias de trading
├── oracle/                  # 🔮 Machine Learning
├── data_processor/          # 📊 Adquisición de datos
├── simulation/              # 🎲 Mercado sintético
├── tests/                   # 🧪 Suite de pruebas
├── memory/                  # 💾 Almacenamiento
└── life_cycle.py            # 🔄 Simulación del ciclo
```

## � Estructura del Proyecto

```
Aipha_0.0.2/
├── aiphalab/                 # 🖥️  Interface CLI
│   ├── cli.py                # Comandos del sistema
│   ├── dashboard.py          # Dashboard interactivo
│   └── formatters.py         # Formateo de salida
├── core/                      # 🧠 Núcleo (5 capas)
│   ├── orchestrator_hardened.py   # Capa 1: Velocidad
│   ├── atomic_update_system.py    # Capa 2: Seguridad
│   ├── execution_queue.py         # Capa 3: Robustez
│   ├── health_monitor.py          # Capa 4: Consciencia
│   ├── quarantine_manager.py      # Capa 4: Consciencia
│   ├── llm_client.py              # Capa 5: Inteligencia
│   ├── llm_assistant.py           # Capa 5: Inteligencia
│   └── ...
├── tests/                    # 🧪 Test suite
├── memory/                   # 💾 Almacenamiento persistente
├── ARCHITECTURE.md           # Documentación de arquitectura
├── IMPLEMENTATION_COMPLETE.md # Estado actual del sistema
├── .env.example              # Template de configuración
├── test_final.py             # Verificación del sistema
└── pyproject.toml            # Configuración del proyecto
```
