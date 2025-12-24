# Aipha v0.0.2 - Guía de Estudio: FASE 1 (ContextSentinel)

Esta guía explica el funcionamiento de la **Capa 1: Core**, específicamente el componente `ContextSentinel`, que es la base de la memoria persistente de Aipha.

## 🧠 ¿Qué es ContextSentinel?

`ContextSentinel` es el sistema de memoria de Aipha. Su función es permitir que el sistema "recuerde" lo que ha hecho en ejecuciones pasadas. Sin esto, cada vez que inicias Aipha, sería como si fuera la primera vez que opera.

### 📁 Estructura de Archivos
La memoria se almacena en la carpeta raíz `/memory/`:
- **`current_state.json`**: Almacena el estado actual (ej. última configuración, variables de entorno, aprendizaje acumulado). Es **mutable**.
- **`action_history.jsonl`**: Un registro de cada acción tomada por el sistema. Es **append-only** (solo se añade, nunca se borra), lo que garantiza un rastro de auditoría.

---

## 🛠️ Cómo funciona el Código

El componente reside en `core/context_sentinel.py`.

### 1. Guardar Memoria (Estado)
Se usa para guardar datos clave que el sistema necesitará después.
```python
from core.context_sentinel import ContextSentinel
sentinel = ContextSentinel()

# Guardar un valor
sentinel.add_memory("oracle_threshold", {"value": 0.75})
```

### 2. Consultar Memoria
```python
# Recuperar el valor
data = sentinel.query_memory("oracle_threshold")
print(data["value"]) # 0.75
```

### 3. Registrar Acciones
Cada vez que Aipha toma una decisión importante, la registra aquí.
```python
sentinel.add_action(
    agent="ChangeProposer",
    action_type="PROPOSAL_GENERATED",
    details={"reason": "Low win rate detected"}
)
```

---

## 🧪 Verificación de la Fase 1

Para asegurar que todo funciona correctamente, hemos implementado una suite de pruebas en `tests/test_context_sentinel.py`.

### Ejecutar Pruebas:
```bash
pytest tests/test_context_sentinel.py -v
```

### Qué estamos probando:
- **Persistencia**: Si guardas algo en una ejecución y cierras el programa, ¿sigue ahí al volver a abrirlo? (Test: `test_memory_persists_between_instances`).
- **Integridad**: ¿Qué pasa si el archivo JSON se corrompe? El sistema debe ser capaz de recuperarse.
- **Historial**: ¿Se están registrando todas las acciones correctamente?

---

## 🚀 Siguiente Paso: FASE 2 (ChangeProposer)

Ahora que Aipha tiene memoria, el siguiente paso es usar esa memoria para **proponer mejoras**. El `ChangeProposer` analizará el historial y el estado para sugerir cambios en la configuración de las otras capas.

---
*Documento generado como parte del Plan de Estudio Aipha v0.0.2.*
