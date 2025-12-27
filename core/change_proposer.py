"""
Change Proposer - Sugiere mejoras automáticamente basadas en métricas.
Usa análisis de tendencias para proponer cambios cuantitativos.
"""
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import uuid

logger = logging.getLogger(__name__)

@dataclass
class ChangeProposal:
    """Propuesta inmutable de cambio (Study Plan V5)"""
    proposal_id: str
    title: str
    target_component: str
    impact_justification: str
    estimated_difficulty: str
    diff_content: str
    test_plan: str
    metrics: Dict[str, Any]
    priority: str = "normal"
    estimated_complexity: str = "moderate"

class ChangeProposer:
    """
    Genera propuestas de cambio dinámicas basadas en métricas del sistema.
    FASE 7: Motor Heurístico Refinado (Hysteresis + Limits).
    """
    
    # Límites de parámetros
    PARAM_LIMITS = {
        "atr_period": {"min": 8, "max": 20, "step": 2},
        "sl_factor": {"min": 0.5, "max": 1.5, "step": 0.1},
        "tp_factor": {"min": 1.5, "max": 3.0, "step": 0.25}
    }
    
    # Cooldown para hysteresis (ciclos antes de poder proponer tipo opuesto)
    HYSTERESIS_COOLDOWN = 3
    
    def __init__(self, sentinel):
        self.sentinel = sentinel
        logger.info("ChangeProposer (Fase 7 - Refinado) inicializado")

    def propose_changes(self, lookback_days: int = 7) -> List[ChangeProposal]:
        """Analiza el estado actual y propone cambios si es necesario."""
        current_state = self.sentinel.query_memory("trading_metrics")
        if not current_state:
            logger.warning("No hay métricas de trading disponibles.")
            return []

        proposals = []
        
        # Obtener historial de propuestas para hysteresis
        proposal_history = self.sentinel.query_memory("proposal_history") or {}
        last_type = proposal_history.get("last_type")
        cycles_since = proposal_history.get("cycles_since_last", 0)
        
        # Análisis Heurístico
        win_rate = current_state.get("win_rate", 0.0)
        total_trades = current_state.get("total_trades", 0)
        drawdown = current_state.get("current_drawdown", 0.0)

        # Regla 1: "Loosen Entry" (Si no hay actividad)
        if total_trades == 0:
            if self._can_propose("loosen", last_type, cycles_since):
                proposal = self._create_loosen_entry_proposal()
                if proposal:
                    logger.info("Detectada inactividad. Generando propuesta 'Loosen Entry'.")
                    proposals.append(proposal)
                    self._update_proposal_history("loosen")

        # Regla 2: "Tighten Risk" (Si el performance es pobre)
        elif win_rate < 0.4 or drawdown > 0.15:
            if self._can_propose("tighten", last_type, cycles_since):
                proposal = self._create_tighten_risk_proposal()
                if proposal:
                    logger.info(f"Detectado bajo rendimiento (WR: {win_rate}). Generando 'Tighten Risk'.")
                    proposals.append(proposal)
                    self._update_proposal_history("tighten")

        # Regla 3: "Stabilize" (Si hay buen rendimiento)
        elif win_rate > 0.6:
            if self._can_propose("stabilize", last_type, cycles_since):
                proposal = self._create_stabilize_proposal()
                if proposal:
                    logger.info(f"Detectado buen rendimiento (WR: {win_rate}). Generando 'Stabilize'.")
                    proposals.append(proposal)
                    self._update_proposal_history("stabilize")
        
        # Incrementar contador de ciclos si no hubo propuesta
        if not proposals:
            self._increment_cycle_counter()

        return proposals

    def _can_propose(self, proposal_type: str, last_type: str, cycles_since: int) -> bool:
        """Verifica hysteresis: evita cambios opuestos rápidos."""
        opposites = {"loosen": "tighten", "tighten": "loosen"}
        if last_type and opposites.get(proposal_type) == last_type:
            if cycles_since < self.HYSTERESIS_COOLDOWN:
                logger.info(f"Hysteresis: Bloqueando '{proposal_type}' (último fue '{last_type}', {cycles_since}/{self.HYSTERESIS_COOLDOWN} ciclos)")
                return False
        return True

    def _update_proposal_history(self, proposal_type: str):
        """Actualiza historial para hysteresis."""
        self.sentinel.add_memory("proposal_history", {
            "last_type": proposal_type,
            "cycles_since_last": 0
        })

    def _increment_cycle_counter(self):
        """Incrementa contador de ciclos sin propuesta."""
        history = self.sentinel.query_memory("proposal_history") or {}
        self.sentinel.add_memory("proposal_history", {
            "last_type": history.get("last_type"),
            "cycles_since_last": history.get("cycles_since_last", 0) + 1
        })

    def _get_current_param(self, param_name: str) -> float:
        """Lee el valor actual de un parámetro del código fuente."""
        try:
            import re
            from pathlib import Path
            code_path = Path("trading_manager/building_blocks/labelers/potential_capture_engine.py")
            content = code_path.read_text()
            match = re.search(rf"{param_name}:\s*\w+\s*=\s*([\d.]+)", content)
            if match:
                return float(match.group(1))
        except Exception as e:
            logger.warning(f"No se pudo leer {param_name}: {e}")
        return self.PARAM_LIMITS[param_name]["min"] + (self.PARAM_LIMITS[param_name]["max"] - self.PARAM_LIMITS[param_name]["min"]) / 2

    def _create_loosen_entry_proposal(self) -> Optional[ChangeProposal]:
        """Estrategia: Reducir periodo ATR (con límites)."""
        current = int(self._get_current_param("atr_period"))
        limits = self.PARAM_LIMITS["atr_period"]
        new_value = current - limits["step"]
        
        if new_value < limits["min"]:
            logger.info(f"Límite alcanzado: atr_period ya está en mínimo ({current})")
            return None
        
        return ChangeProposal(
            proposal_id=f"AIPHA-DYN-{uuid.uuid4().hex[:6].upper()}",
            title="Ajuste Dinámico: Aumentar Sensibilidad de Entrada",
            target_component="trading_manager.building_blocks.labelers.potential_capture_engine",
            impact_justification=f"ATR period {current} → {new_value} para capturar más señales.",
            estimated_difficulty="Baja",
            diff_content=f"-     atr_period: int = {current},\n+     atr_period: int = {new_value},",
            test_plan="tests/test_potential_capture_engine.py",
            metrics={"expected_trades_increase": "medium"},
            priority="high"
        )

    def _create_tighten_risk_proposal(self) -> Optional[ChangeProposal]:
        """Estrategia: Reducir Stop Loss (con límites)."""
        current = self._get_current_param("sl_factor")
        limits = self.PARAM_LIMITS["sl_factor"]
        new_value = round(current - limits["step"], 2)
        
        if new_value < limits["min"]:
            logger.info(f"Límite alcanzado: sl_factor ya está en mínimo ({current})")
            return None
        
        return ChangeProposal(
            proposal_id=f"AIPHA-DYN-{uuid.uuid4().hex[:6].upper()}",
            title="Ajuste Dinámico: Protección de Capital",
            target_component="trading_manager.building_blocks.labelers.potential_capture_engine",
            impact_justification=f"SL factor {current} → {new_value} para reducir drawdown.",
            estimated_difficulty="Media",
            diff_content=f"-     sl_factor: float = {current},\n+     sl_factor: float = {new_value},",
            test_plan="tests/test_potential_capture_engine.py",
            metrics={"expected_drawdown_reduction": "medium"},
            priority="critical"
        )

    def _create_stabilize_proposal(self) -> Optional[ChangeProposal]:
        """Estrategia: Aumentar Take Profit (con límites)."""
        current = self._get_current_param("tp_factor")
        limits = self.PARAM_LIMITS["tp_factor"]
        new_value = round(current + limits["step"], 2)
        
        if new_value > limits["max"]:
            logger.info(f"Límite alcanzado: tp_factor ya está en máximo ({current})")
            return None
        
        return ChangeProposal(
            proposal_id=f"AIPHA-DYN-{uuid.uuid4().hex[:6].upper()}",
            title="Ajuste Dinámico: Maximización de Beneficios",
            target_component="trading_manager.building_blocks.labelers.potential_capture_engine",
            impact_justification=f"TP factor {current} → {new_value} para capturar tendencias.",
            estimated_difficulty="Baja",
            diff_content=f"-     tp_factor: float = {current},\n+     tp_factor: float = {new_value},",
            test_plan="tests/test_potential_capture_engine.py",
            metrics={"expected_profit_increase": "medium"},
            priority="normal"
        )
