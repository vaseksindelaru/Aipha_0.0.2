"""
Dashboard CLI - Visualización rápida del estado de Aipha.
Muestra métricas recientes, estado del sistema y últimas acciones.
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import json

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.memory_manager import MemoryManager
from core.config_manager import ConfigManager

class Dashboard:
    def __init__(self, storage_root: Path = Path("memory")):
        self.memory = MemoryManager(storage_root=storage_root)
        self.config = ConfigManager(config_path=storage_root / "aipha_config.json")

    def show(self):
        """Muestra el dashboard en la consola."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 60)
        print(f" 🤖 AIPHA AUTONOMOUS DASHBOARD | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # 1. Estado del Sistema
        state = self.memory.get_system_state()
        print("\n[ESTADO DEL SISTEMA]")
        print(f"  Último Ciclo: {state.get('last_improvement_cycle', 'N/A')}")
        print(f"  Propuestas (Último): {state.get('last_cycle_proposals', 0)}")
        print(f"  Aprobadas (Último): {state.get('last_cycle_approved', 0)}")
        print(f"  Aplicadas (Último): {state.get('last_cycle_applied', 0)}")
        
        # 2. Métricas Clave
        print("\n[MÉTRICAS RECIENTES]")
        for component in ["Trading", "Oracle"]:
            metrics = self.memory.get_metrics(component=component, limit=1)
            if metrics:
                m = metrics[0]
                print(f"  {component}: {m['metric']} = {m['value']:.4f} ({m['timestamp']})")
            else:
                print(f"  {component}: Sin datos")
                
        # 3. Configuración Actual
        print("\n[CONFIGURACIÓN ACTIVA]")
        conf = self.config.get_all()
        print(f"  Trading TP/SL: {conf.get('Trading', {}).get('tp_factor', 'N/A')} / {conf.get('Trading', {}).get('sl_factor', 'N/A')}")
        print(f"  Oracle Threshold: {conf.get('Oracle', {}).get('confidence_threshold', 'N/A')}")
        
        # 4. Últimas Acciones
        print("\n[ÚLTIMAS ACCIONES]")
        actions = self.memory.get_action_history(limit=5)
        for a in actions:
            time_str = a['timestamp'].split('T')[1][:8]
            print(f"  [{time_str}] {a['agent']} -> {a['action']} ({a['status']})")
            
        print("\n" + "=" * 60)
        print(" Presione Ctrl+C para salir.")

if __name__ == "__main__":
    dashboard = Dashboard()
    try:
        dashboard.show()
    except KeyboardInterrupt:
        print("\nSaliendo del dashboard...")
