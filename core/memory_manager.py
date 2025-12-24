"""
Memory Manager - Persistencia de estado y decisiones.
Responsable de registrar todas las acciones y métricas.
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import hashlib

logger = logging.getLogger(__name__)

@dataclass
class ActionEntry:
    """Entrada de acción registrada en el historial."""
    timestamp: str
    agent: str
    component: str
    action: str
    status: str  # "success", "failure", "pending"
    details: Dict[str, Any]
    entry_hash: str = ""

    def compute_hash(self) -> str:
        """Calcula hash SHA256 para integridad."""
        entry_dict = asdict(self)
        entry_dict.pop("entry_hash", None)
        content = json.dumps(entry_dict, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()

class MemoryManager:
    """Gestiona la memoria persistente del sistema."""
    def __init__(self, storage_root: Path = Path("memory")):
        self.storage_root = Path(storage_root)
        self.storage_root.mkdir(parents=True, exist_ok=True)
        
        self.action_history_file = self.storage_root / "action_history.jsonl"
        self.system_state_file = self.storage_root / "system_state.json"
        self.metrics_file = self.storage_root / "performance_metrics.json"
        
        logger.info(f"MemoryManager inicializado en {self.storage_root}")

    def record_action(self, 
                     agent: str,
                     component: str,
                     action: str,
                     details: Dict[str, Any],
                     status: str = "success") -> str:
        """
        Registra una acción en el historial (append-only).
        
        Args:
            agent: Agente que realiza la acción (ej: "ChangeProposer")
            component: Componente afectado (ej: "Oracle")
            action: Descripción de la acción
            details: Datos adicionales (métricas, parámetros, etc.)
            status: Estado de la acción
            
        Returns:
            Hash de la entrada para verificación
        """
        entry = ActionEntry(
            timestamp=datetime.utcnow().isoformat() + "Z",
            agent=agent,
            component=component,
            action=action,
            status=status,
            details=details
        )
        entry.entry_hash = entry.compute_hash()
        
        # Append-only a archivo JSONL
        with open(self.action_history_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry)) + "\n")
        
        logger.info(f"[{agent}] {action} → {status}")
        return entry.entry_hash

    def get_action_history(self, agent: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Lee el historial de acciones.
        
        Args:
            agent: Filtrar por agente (ej: "ChangeProposer")
            limit: Número máximo de entradas
            
        Returns:
            Lista de acciones (más recientes primero)
        """
        if not self.action_history_file.exists():
            return []
        
        entries = []
        with open(self.action_history_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    if agent is None or entry["agent"] == agent:
                        entries.append(entry)
        
        return entries[-limit:]

    def update_system_state(self, updates: Dict[str, Any]) -> None:
        """
        Actualiza el estado global del sistema.
        
        Args:
            updates: Diccionario de cambios
        """
        state = self._load_state()
        state.update(updates)
        state["last_update"] = datetime.utcnow().isoformat() + "Z"
        
        with open(self.system_state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        
        logger.info(f"Sistema state actualizado: {list(updates.keys())}")

    def get_system_state(self) -> Dict[str, Any]:
        """Obtiene el estado actual del sistema."""
        return self._load_state()

    def record_metric(self, component: str, metric_name: str, value: float, 
                     metadata: Optional[Dict] = None) -> None:
        """
        Registra una métrica de rendimiento.
        
        Args:
            component: Componente (ej: "Oracle")
            metric_name: Nombre de la métrica (ej: "win_rate")
            value: Valor numérico
            metadata: Datos adicionales (período, dataset, etc.)
        """
        metrics = self._load_metrics()
        
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "component": component,
            "metric": metric_name,
            "value": value,
            "metadata": metadata or {}
        }
        
        # Mantener solo últimas 1000 métricas por componente
        metrics.append(entry)
        if len(metrics) > 1000:
            metrics = metrics[-1000:]
        
        with open(self.metrics_file, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)
        
        logger.debug(f"{component}.{metric_name} = {value}")

    def get_metrics(self, component: Optional[str] = None, 
                   metric_name: Optional[str] = None,
                   limit: int = 100) -> List[Dict[str, Any]]:
        """
        Recupera métricas registradas.
        
        Args:
            component: Filtrar por componente
            metric_name: Filtrar por métrica específica
            limit: Número máximo de registros
            
        Returns:
            Lista de métricas
        """
        metrics = self._load_metrics()
        
        # Filtrar
        filtered = [m for m in metrics 
                   if (component is None or m["component"] == component)
                   and (metric_name is None or m["metric"] == metric_name)]
        
        return filtered[-limit:]

    def _load_state(self) -> Dict[str, Any]:
        """Carga estado del archivo."""
        if self.system_state_file.exists():
            with open(self.system_state_file, "r") as f:
                return json.load(f)
        return {"initialized": True}

    def _load_metrics(self) -> List[Dict[str, Any]]:
        """Carga métricas del archivo."""
        if self.metrics_file.exists():
            with open(self.metrics_file, "r") as f:
                return json.load(f)
        return []
