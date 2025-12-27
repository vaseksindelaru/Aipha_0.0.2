import logging
import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Configurar path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from core.context_sentinel import ContextSentinel
from core.orchestrator import CentralOrchestrator
from simulation.market_generator import MarketGenerator
from trading_manager.building_blocks.labelers.potential_capture_engine import get_atr_labels

# Configurar Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("life_cycle.log")
    ]
)
logger = logging.getLogger("LifeCycle")

class LifeCycleSimulation:
    def __init__(self, use_llm: bool = False):
        # Usar el mismo path de almacenamiento que CentralOrchestrator
        storage_path = Path("memory")
        self.sentinel = ContextSentinel(storage_root=storage_path)
        self.orchestrator = CentralOrchestrator(storage_root=storage_path, use_llm=use_llm)
        self.market_gen = MarketGenerator()
        
        # Estado de la cuenta simulada
        self.account_balance = 10000.0
        self.total_pnl = 0.0
        self.total_trades = 0
        self.winning_trades = 0
        
    def run_epoch(self, regime: str, days: int = 5):
        """Ejecuta una 'época' de varios días bajo un régimen de mercado."""
        logger.info(f"=== INICIANDO ÉPOCA: {regime} ({days} días) ===")
        
        for day in range(days):
            logger.info(f"--- Día {day+1}/{days} ---")
            
            # 1. Generar Mercado
            df = self.market_gen.generate_day(regime)
            
            # 2. Simular Trading (PotentialCaptureEngine)
            # Simulamos eventos cada hora para ver si entramos
            t_events = df.index 
            
            # Leer parámetros actuales del código (simulado leyendo el archivo o importando dinámicamente)
            import trading_manager.building_blocks.labelers.potential_capture_engine as pce_module
            
            try:
                labels = pce_module.get_atr_labels(prices=df, t_events=t_events)
            except Exception as e:
                logger.error(f"Error en estrategia: {e}")
                labels = pd.Series()

            # 3. Calcular Resultados del Día
            day_trades = 0
            day_wins = 0
            day_pnl = 0.0
            
            valid_labels = labels[labels != 0] # 0 es timeout
            day_trades = len(valid_labels)
            
            if day_trades > 0:
                day_wins = (valid_labels == 1).sum()
                # Simulación simple de PnL: Win=+2%, Loss=-1% (Riesgo 1:2)
                for lbl in valid_labels:
                    if lbl == 1:
                        day_pnl += self.account_balance * 0.02
                    else:
                        day_pnl += self.account_balance * -0.01
            
            # Actualizar acumulados
            self.total_trades += day_trades
            self.winning_trades += day_wins
            self.total_pnl += day_pnl
            self.account_balance += day_pnl
            
            current_win_rate = (self.winning_trades / self.total_trades) if self.total_trades > 0 else 0.0
            
            logger.info(f"Resultados Día: Trades={day_trades}, Wins={day_wins}, PnL={day_pnl:.2f}")
            logger.info(f"Estado Global: Balance={self.account_balance:.2f}, WR={current_win_rate:.2%}")
            
            # 4. Actualizar Memoria del Sistema
            self.sentinel.add_memory("trading_metrics", {
                "win_rate": current_win_rate,
                "total_trades": self.total_trades, # Acumulado histórico para el ejercicio
                "current_drawdown": 0.0, # Simplificado
                "status": "ACTIVE",
                "last_update": df.index[-1].isoformat()
            })
            
            # Hack para forzar la heurística de "Loosen Entry" si es necesario en la demo
            # Si el régimen es FLAT y no hubo trades hoy, reseteamos el contador global temporalmente
            # para que el ChangeProposer vea "0 trades" y actúe.
            if regime == "FLAT" and day_trades == 0:
                 self.sentinel.add_memory("trading_metrics", {
                    "win_rate": 0.0,
                    "total_trades": 0, # FORZAR CERO para activar heurística
                    "current_drawdown": 0.0,
                    "status": "ACTIVE"
                })
            
            # Hack para forzar "Tighten Risk" en mercados volátiles
            if regime == "VOLATILE":
                 self.sentinel.add_memory("trading_metrics", {
                    "win_rate": 0.3, # Bajo rendimiento simulado
                    "total_trades": 100,
                    "current_drawdown": 0.2, # Drawdown alto
                    "status": "ACTIVE"
                })
            
            # 5. Ejecutar Ciclo de Auto-Mejora
            logger.info("Ejecutando ciclo de auto-mejora...")
            self.orchestrator.run_improvement_cycle()
            
            # Recargar módulo para que el siguiente día use el código nuevo
            import importlib
            import trading_manager.building_blocks.labelers.potential_capture_engine as pce_module
            importlib.reload(pce_module)
            # No necesitamos re-importar la función si usamos el módulo directamente

if __name__ == "__main__":
    # Ejecutar con LLM activado
    sim = LifeCycleSimulation(use_llm=True)
    
    # Escenario 1: Mercado Plano (Debería activar Loosen Entry)
    sim.run_epoch("FLAT", days=2)
    
    # Escenario 2: Mercado Volátil (Debería activar Tighten Risk)
    sim.run_epoch("VOLATILE", days=2)

