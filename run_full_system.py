"""
Full System Runner - Ejecuta el pipeline completo de Aipha.
Flujo: Data Processor -> Trading Manager -> Oracle -> Autonomous Intelligence
"""
import subprocess
import sys
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def run_step(name, command):
    logger.info(f"\n>>> INICIANDO: {name}")
    logger.info(f"Comando: {command}")
    try:
        # Capturar tanto stdout como stderr
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        output = result.stdout + "\n" + result.stderr
        logger.info(f"✅ {name} completado con éxito.")
        return output.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ ERROR en {name}:")
        output = e.stdout + "\n" + e.stderr
        logger.error(output)
        return f"ERROR:\n{output}"

def main():
    report_lines = []
    report_lines.append("# Reporte de Ejecución Completa del Sistema Aipha\n")
    report_lines.append(f"**Fecha de ejecución**: {subprocess.check_output('date', shell=True, text=True).strip()}\n")
    report_lines.append("Este reporte documenta el flujo completo desde la adquisición de datos hasta la automejora autónoma.\n")
    
    steps = [
        ("Capa 2: Data Processor", "python3 data_processor/acquire_data.py"),
        ("Capa 3: Trading Manager", "python3 trading_manager/strategies/proof_strategy.py"),
        ("Capa 4: Oracle", "python3 oracle/strategies/proof_strategy_v2.py"),
        ("Capa 1: Autonomous Intelligence", "python3 -m core.orchestrator")
    ]
    
    for name, cmd in steps:
        output = run_step(name, cmd)
        report_lines.append(f"## {name}\n")
        report_lines.append(f"**Comando**: `{cmd}`\n")
        if output:
            report_lines.append("```text\n" + output + "\n```\n")
        else:
            report_lines.append("*Sin salida detectada.*\n")
        
    # Guardar reporte
    report_path = "full_system_test_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.writelines(report_lines)
    
    logger.info(f"\n✨ PRUEBA COMPLETA FINALIZADA. Reporte generado en: {report_path}")

if __name__ == "__main__":
    main()
