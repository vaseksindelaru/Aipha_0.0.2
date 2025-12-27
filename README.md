# Aipha v0.0.2 - Sistema de Trading Autónomo

Aipha es un sistema de trading algorítmico que **evoluciona solo**. A diferencia de los bots tradicionales, Aipha implementa un bucle cerrado de automejora que ajusta sus propios parámetros sin intervención humana.

## 🧬 ¿Qué hace único a Aipha?

| Característica | Bots Tradicionales | Aipha v0.0.2 |
|----------------|-------------------|--------------|
| Memoria | ❌ Ninguna | ✅ Persistente |
| Aprendizaje | ❌ Manual | ✅ Automático |
| Adaptación | ❌ Requiere dev | ✅ Autónoma |
| LLM | ❌ N/A | ✅ Qwen 2.5 Coder |

## 🏛️ Arquitectura

```
                    ┌─────────────────────────┐
                    │    CAPA 1: CORE         │
                    │  (Autonomous Intel)     │
                    └───────────┬─────────────┘
                                │ ← Retroalimentación
    ┌───────────────┬───────────┴───────────┬───────────────┐
    │               │                       │               │
    ▼               ▼                       ▼               ▼
┌───────┐     ┌───────────┐          ┌──────────┐    ┌───────────┐
│ Data  │ → → │ Trading   │ → → → → →│  Oracle  │ → →│   Post    │
│Processor│   │ Manager   │          │   (ML)   │    │ Processor │
└───────┘     └───────────┘          └──────────┘    └───────────┘
```

**Documentación completa**: [ARCHITECTURE.md](ARCHITECTURE.md)

## 🚀 Inicio Rápido

### Ejecutar Simulación
```bash
export HF_API_KEY="your_huggingface_key"  # Para LLM
export PYTHONPATH=$PYTHONPATH:.
python3 life_cycle.py
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

## 🔧 Componentes Principales

| Componente | Archivo | Función |
|------------|---------|---------|
| Orquestador | `core/orchestrator.py` | Dirige ciclo de automejora |
| Memoria | `core/context_sentinel.py` | Persistencia JSON/JSONL |
| Proposer | `core/change_proposer.py` | Genera cambios dinámicos |
| LLM | `core/llm_proposer.py` | Razonamiento avanzado |
| Atómico | `core/atomic_update_system.py` | Protocolo de 5 pasos |

## 📈 Estado Actual

- ✅ Fase 1-3: Core funcional (Memoria, Propuestas, Ejecución)
- ✅ Fase 4-5: Simulación multi-régimen
- ✅ Fase 6: Múltiples regímenes de mercado
- ✅ Fase 7: Hysteresis y límites de parámetros
- ✅ Fase 8: Integración LLM (Qwen 2.5)

## 🗺️ Próximos Pasos

- [ ] Fase 9: Multi-Asset
- [ ] Fase 10: Backtesting antes de aplicar
- [ ] Fase 11: Ejecución en exchanges reales
- [ ] Fase 12: Dashboard web

---

*Aipha v0.0.2 - Un sistema que no solo opera, sino que evoluciona.*
