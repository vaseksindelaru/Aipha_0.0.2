"""
LLM Proposer - Genera propuestas de cambio usando un LLM.
FASE 8: Integración con Qwen 2.5 Coder via HuggingFace.
"""
import logging
import json
import os
from typing import Dict, Any, Optional, List
from dataclasses import asdict
import uuid

from core.change_proposer import ChangeProposal, ChangeProposer

logger = logging.getLogger(__name__)

# Configuración LLM (Qwen 2.5 Coder via HuggingFace)
LLM_CONFIG = {
    "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
    "api_base": "https://router.huggingface.co/v1",
    "api_key": os.environ.get("HF_API_KEY")  # Requiere HF_API_KEY en variables de entorno
}

SYSTEM_PROMPT = """Eres un experto en optimización de estrategias de trading algorítmico.
Tu tarea es analizar las métricas de rendimiento y el código actual para proponer mejoras específicas.

REGLAS:
1. Solo propón UN cambio a la vez
2. El cambio debe ser pequeño y verificable
3. Responde SOLO en JSON válido

PARÁMETROS MODIFICABLES:
- atr_period: int (8-20) - Periodo ATR para calcular volatilidad
- sl_factor: float (0.5-1.5) - Multiplicador Stop Loss
- tp_factor: float (1.5-3.0) - Multiplicador Take Profit

FORMATO DE RESPUESTA (JSON):
{
    "should_change": true/false,
    "parameter": "atr_period|sl_factor|tp_factor",
    "current_value": <número>,
    "new_value": <número>,
    "justification": "Razón del cambio"
}"""


class LLMProposer:
    """
    Genera propuestas de cambio usando un LLM.
    Incluye fallback a heurísticas si el LLM falla.
    """
    
    def __init__(self, sentinel, config: Dict[str, str] = None):
        self.sentinel = sentinel
        self.config = config or LLM_CONFIG
        self.heuristic_fallback = ChangeProposer(sentinel)
        self._client = None
        logger.info("LLMProposer (Fase 8 - Qwen 2.5) inicializado")

    def _get_client(self):
        """Lazy initialization del cliente OpenAI."""
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(
                    base_url=self.config["api_base"],
                    api_key=self.config["api_key"]
                )
            except ImportError:
                logger.error("openai package not installed. Run: pip install openai")
                raise
        return self._client

    def _get_current_code(self) -> str:
        """Lee el código actual del componente objetivo."""
        try:
            from pathlib import Path
            code_path = Path("trading_manager/building_blocks/labelers/potential_capture_engine.py")
            return code_path.read_text()[:2000]  # Limitar a 2000 chars
        except Exception as e:
            logger.warning(f"Error leyendo código: {e}")
            return ""

    def _build_user_prompt(self) -> str:
        """Construye el prompt para el LLM."""
        metrics = self.sentinel.query_memory("trading_metrics") or {}
        code_snippet = self._get_current_code()
        
        return f"""## MÉTRICAS ACTUALES
- Win Rate: {metrics.get('win_rate', 'N/A')}
- Total Trades: {metrics.get('total_trades', 'N/A')}
- Drawdown: {metrics.get('current_drawdown', 'N/A')}

## CÓDIGO ACTUAL (fragmento)
```python
{code_snippet[:1000]}
```

Analiza estas métricas y propón un cambio si es necesario. Responde SOLO en JSON."""

    def propose_changes(self, lookback_days: int = 7) -> List[ChangeProposal]:
        """Genera propuestas usando el LLM, con fallback a heurísticas."""
        try:
            return self._llm_propose()
        except Exception as e:
            logger.warning(f"LLM falló ({e}), usando heurísticas de fallback")
            return self.heuristic_fallback.propose_changes(lookback_days)

    def _llm_propose(self) -> List[ChangeProposal]:
        """Genera propuesta usando el LLM."""
        client = self._get_client()
        
        logger.info("Consultando LLM para propuesta de cambio...")
        
        response = client.chat.completions.create(
            model=self.config["model"],
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": self._build_user_prompt()}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        # Parsear respuesta
        content = response.choices[0].message.content
        logger.info(f"Respuesta LLM: {content[:200]}...")
        
        # Extraer JSON de la respuesta
        proposal_data = self._parse_llm_response(content)
        
        if not proposal_data or not proposal_data.get("should_change"):
            logger.info("LLM decidió no proponer cambios")
            return []
        
        # Construir ChangeProposal
        param = proposal_data["parameter"]
        current = proposal_data["current_value"]
        new_val = proposal_data["new_value"]
        
        # Determinar tipo de dato para el diff
        type_str = "int" if param == "atr_period" else "float"
        
        proposal = ChangeProposal(
            proposal_id=f"AIPHA-LLM-{uuid.uuid4().hex[:6].upper()}",
            title=f"Optimización LLM: {param}",
            target_component="trading_manager.building_blocks.labelers.potential_capture_engine",
            impact_justification=proposal_data.get("justification", "Optimización sugerida por LLM"),
            estimated_difficulty="Baja",
            diff_content=f"-     {param}: {type_str} = {current},\n+     {param}: {type_str} = {new_val},",
            test_plan="tests/test_potential_capture_engine.py",
            metrics={"source": "LLM", "model": self.config["model"]},
            priority="high"
        )
        
        return [proposal]

    def _parse_llm_response(self, content: str) -> Optional[Dict[str, Any]]:
        """Extrae JSON de la respuesta del LLM."""
        try:
            # Intentar parsear directamente
            return json.loads(content)
        except json.JSONDecodeError:
            # Buscar JSON en la respuesta
            import re
            match = re.search(r'\{[^{}]+\}', content, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    pass
        
        logger.warning("No se pudo parsear respuesta del LLM como JSON")
        return None
