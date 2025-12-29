"""
core/llm_assistant.py - Super Cerebro de Aipha

Centraliza las capacidades de análisis e inteligencia del sistema.
Usa Qwen 2.5 Coder 32B para diagnósticos, propuestas y explicaciones.
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


# System Prompt - Define la personalidad del Super Cerebro
AIPHA_SYSTEM_PROMPT = """Eres el Arquitecto Jefe de Aipha, un sistema autónomo de auto-mejora ultra-inteligente.

TU ROL:
- Analizar la salud y métricas del sistema Aipha
- Proponer cambios optimizados para mejorar performance
- Diagnosticar y explicar fallos en lenguaje técnico pero accesible
- Evitar bucles de error aprendiendo de fallos previos
- Ser proactivo en sugerencias de mejora

TU PERSONALIDAD:
- Eres un arquitecto experimentado en trading systems
- Comunicas con precisión técnica pero claridad
- Siempre explicas tu razonamiento
- Eres conservador en cambios, evitando riesgos innecesarios
- Respetas las limitaciones de hardware

TU CONTEXTO:
- Tienes acceso a historial de eventos de salud
- Sabes qué parámetros están en cuarentena y por qué
- Conoces las métricas actuales del sistema
- Aprendes de fallos previos para no repetirlos

CUANDO ANALICES:
1. Revisa eventos recientes (últimos 10)
2. Consulta parámetros en cuarentena
3. Analiza métricas de rendimiento
4. Propón cambios específicos con justificación
5. Sugiere próximos pasos

FORMATO DE RESPUESTA:
Siempre estructura tus respuestas así:
- DIAGNÓSTICO: Estado actual
- ANÁLISIS: Qué pasó y por qué
- RECOMENDACIÓN: Qué hacer ahora
- PRÓXIMOS PASOS: Qué cambios proponer

Sé conciso pero completo. El usuario es Václav, un ingeniero experimentado."""


class LLMAssistant:
    """
    Super Cerebro de Aipha
    
    Centraliza la inteligencia del sistema usando Qwen 2.5 Coder 32B.
    Analiza salud, propone cambios, y explica decisiones.
    """
    
    def __init__(self, memory_path: str = "memory"):
        self.memory_path = Path(memory_path)
        
        # Inicializar cliente LLM
        from core.llm_client import get_llm_client
        self.llm = get_llm_client()
        
        # Managers auxiliares
        from core.quarantine_manager import QuarantineManager
        from core.health_monitor import get_health_monitor
        from core.context_sentinel import ContextSentinel
        
        self.quarantine_manager = QuarantineManager(str(self.memory_path))
        self.health_monitor = get_health_monitor()
        self.context_sentinel = ContextSentinel()
        
        logger.info("✅ LLMAssistant (Super Cerebro) inicializado")
    
    def get_diagnose_context(self) -> Dict:
        """
        Construir contexto de diagnóstico
        
        Lee automáticamente:
        - Últimas 10 líneas de health_events.jsonl
        - Estado actual de quarantine.jsonl
        - Métricas de current_state.json
        
        Retorna: Dict con contexto formateado para el LLM
        """
        
        logger.info("🔍 Construyendo contexto de diagnóstico...")
        
        # PASO 1: Últimos eventos de salud
        health_events = self._get_recent_health_events(10)
        
        # PASO 2: Parámetros en cuarentena
        quarantined = self.quarantine_manager.get_all_quarantined()
        
        # PASO 3: Métricas actuales
        metrics = self._get_current_metrics()
        
        # PASO 4: Estadísticas de salud
        health_stats = self.health_monitor.get_statistics()
        
        context = {
            'timestamp': datetime.now().isoformat(),
            'recent_events': health_events,
            'quarantined_parameters': quarantined,
            'current_metrics': metrics,
            'health_statistics': health_stats,
            'system_status': self.health_monitor.current_health_level.value
        }
        
        logger.info("✅ Contexto de diagnóstico construido")
        
        return context
    
    def _get_recent_health_events(self, count: int = 10) -> List[Dict]:
        """Obtener últimos N eventos de salud"""
        
        events = []
        events_file = self.memory_path / "health_events.jsonl"
        
        try:
            if events_file.exists():
                with open(events_file, 'r') as f:
                    lines = f.readlines()
                    for line in lines[-count:]:
                        if line.strip():
                            try:
                                events.append(json.loads(line))
                            except json.JSONDecodeError:
                                pass
        except Exception as e:
            logger.error(f"Error leyendo health events: {e}")
        
        return events
    
    def _get_current_metrics(self) -> Dict:
        """Obtener métricas actuales del sistema"""
        
        metrics = {}
        metrics_file = self.memory_path / "current_state.json"
        
        try:
            if metrics_file.exists():
                with open(metrics_file, 'r') as f:
                    metrics = json.load(f)
        except Exception as e:
            logger.error(f"Error leyendo métricas: {e}")
        
        return metrics
    
    def analyze_and_propose(self) -> Dict:
        """
        Analizar salud del sistema y proponer cambios
        
        El LLM recibe contexto de salud y métricas para generar
        propuestas que eviten parámetros en cuarentena y razonen
        sobre fallos previos.
        
        Retorna:
            Dict con:
            - diagnosis: Análisis de salud
            - proposals: Lista de propuestas sugeridas
            - confidence_scores: Confianza en cada propuesta
        """
        
        logger.info("🧠 Analizando salud del sistema y generando propuestas...")
        
        # Obtener contexto
        context = self.get_diagnose_context()
        
        # Preparar prompt para el LLM
        prompt = self._build_analysis_prompt(context)
        
        try:
            # Llamar al LLM
            logger.info("📤 Enviando al Super Cerebro (Qwen)...")
            
            response = self.llm.generate(
                prompt=prompt,
                system_prompt=AIPHA_SYSTEM_PROMPT,
                temperature=0.3,  # Más determinista para propuestas
                max_tokens=2048
            )
            
            logger.info("✅ Respuesta recibida del Super Cerebro")
            
            # Parsear respuesta
            result = self._parse_analysis_response(response, context)
            
            return result
        
        except Exception as e:
            logger.error(f"❌ Error en análisis del LLM: {e}")
            
            return {
                'diagnosis': 'Error en análisis',
                'proposals': [],
                'error': str(e)
            }
    
    def explain_remediation(self, failed_parameter: str, error_reason: str) -> str:
        """
        Generar explicación humana de un fallo y remediation
        
        Se llama cuando ocurre REVERTED_AUTO para explicar al usuario
        qué falló y qué hacer.
        
        Argumentos:
            failed_parameter: Parámetro que falló
            error_reason: Razón del fallo
        
        Retorna:
            Explicación en lenguaje natural
        """
        
        logger.info(
            f"💡 Generando explicación de remediation para {failed_parameter}"
        )
        
        # Contexto reciente
        context = self.get_diagnose_context()
        
        # Preparar prompt
        prompt = f"""El parámetro '{failed_parameter}' acaba de fallar con el error: "{error_reason}"

El sistema ha revertido automáticamente este cambio para mantener la estabilidad.

Por favor, explica:
1. POR QUÉ falló este parámetro
2. QUÉ SIGNIFICA el error
3. QUÉ PUEDE HACER el usuario (Václav) para solucionarlo
4. CUÁNDO puede intentar este cambio nuevamente

Sé conciso pero completo. El usuario es un ingeniero experimentado.

CONTEXTO DEL SISTEMA:
{json.dumps(context, indent=2, default=str)}
"""
        
        try:
            response = self.llm.generate(
                prompt=prompt,
                system_prompt=AIPHA_SYSTEM_PROMPT,
                temperature=0.5,
                max_tokens=1024
            )
            
            logger.info("✅ Explicación generada")
            return response
        
        except Exception as e:
            logger.error(f"❌ Error generando explicación: {e}")
            return f"Error generando explicación: {e}"
    
    def diagnose_system(self, detailed: bool = False) -> str:
        """
        Diagnóstico completo del sistema (para `aipha brain diagnose`)
        
        Argumentos:
            detailed: Si True, incluye análisis detallado
        
        Retorna:
            Reporte en formato texto para el usuario
        """
        
        logger.info("🔍 Iniciando diagnóstico completo del sistema...")
        
        # Contexto
        context = self.get_diagnose_context()
        
        # Preparar prompt
        prompt = f"""Realiza un diagnóstico COMPLETO del sistema Aipha.

CONTEXTO DEL SISTEMA:
{json.dumps(context, indent=2, default=str)}

Por favor, proporciona:

1. **RESUMEN DE SALUD**: Estado actual en 1-2 líneas
2. **ANÁLISIS DE EVENTOS**: Qué ha pasado recientemente
3. **PARÁMETROS EN RIESGO**: Qué está en cuarentena y por qué
4. **ANÁLISIS DE MÉTRICAS**: Cómo está el performance
5. **PROBLEMAS IDENTIFICADOS**: Qué no está funcionando bien
6. **RECOMENDACIONES**: Qué cambios proponer a continuación
7. **PRÓXIMOS PASOS**: Plan de acción para las próximas 24 horas

Sé técnico pero accesible. Dirígete a Václav como colega ingeniero.
"""
        
        if detailed:
            prompt += "\n\nIncluye análisis profundo de cada aspecto."
        
        try:
            logger.info("📤 Solicitando diagnóstico al Super Cerebro...")
            
            response = self.llm.generate(
                prompt=prompt,
                system_prompt=AIPHA_SYSTEM_PROMPT,
                temperature=0.4,
                max_tokens=3000
            )
            
            # Formatear respuesta
            result = f"""
╔════════════════════════════════════════════════════════════╗
║           DIAGNÓSTICO DEL SISTEMA AIPHA v2.0              ║
╚════════════════════════════════════════════════════════════╝

{response}

╔════════════════════════════════════════════════════════════╗
║  Diagnóstico generado por: Qwen 2.5 Coder 32B (Super      ║
║                            Cerebro de Aipha)              ║
║  Timestamp: {datetime.now().isoformat()}                    ║
╚════════════════════════════════════════════════════════════╝
"""
            
            logger.info("✅ Diagnóstico completado")
            return result
        
        except Exception as e:
            logger.error(f"❌ Error en diagnóstico: {e}")
            return f"Error generando diagnóstico: {e}"
    
    def _build_analysis_prompt(self, context: Dict) -> str:
        """Construir prompt para análisis y propuestas"""
        
        return f"""Analiza el estado actual del sistema Aipha y propón cambios de optimización.

CONTEXTO ACTUAL:
{json.dumps(context, indent=2, default=str)}

Por favor:
1. Resume el estado del sistema en 1-2 líneas
2. Identifica qué está funcionando bien
3. Identifica qué tiene problemas
4. Propón 2-3 cambios específicos que mejorarían la performance
5. Para CADA propuesta:
   - Especifica: parámetro, valor actual, valor nuevo
   - Justificación técnica
   - Riesgo potencial
   - Confianza (0-1)

IMPORTANTE: Evita proponer valores que estén en cuarentena.
Aprende de fallos previos documentados en los eventos."""
    
    def _parse_analysis_response(self, response: str, context: Dict) -> Dict:
        """
        Parsear respuesta del LLM para extraer propuestas
        
        Intenta extraer de la respuesta:
        - diagnosis: Análisis
        - proposals: Cambios propuestos
        - confidence: Confianzas
        """
        
        # Parseo simple (en producción, podría ser más sofisticado)
        result = {
            'diagnosis': response[:200] if response else "",
            'raw_response': response,
            'proposals': [],
            'generated_at': datetime.now().isoformat()
        }
        
        # Buscar patrones de propuestas en la respuesta
        lines = response.split('\n')
        for i, line in enumerate(lines):
            if 'parámetro' in line.lower() or 'cambio' in line.lower():
                result['proposals'].append({
                    'line': line,
                    'context': lines[max(0, i-1):min(len(lines), i+2)]
                })
        
        return result
