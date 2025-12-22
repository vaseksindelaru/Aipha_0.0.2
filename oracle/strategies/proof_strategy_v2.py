import pandas as pd
import duckdb
import logging
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from trading_manager.building_blocks.detectors.key_candle_detector import SignalDetector
from trading_manager.building_blocks.labelers.potential_capture_engine import get_atr_labels
from oracle.building_blocks.features.feature_engineer import FeatureEngineer
from oracle.building_blocks.oracles.oracle_engine import OracleEngine

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def run_proof_strategy_v2():
    db_path = "data_processor/data/aipha_data.duckdb"
    table_name = "btc_1h_data"
    model_path = "oracle/models/proof_oracle.joblib"
    
    logger.info("--- INICIANDO PROOF STRATEGY V2 (CON ORÁCULO) ---")
    
    # 1. Carga de Datos y Modelo
    if not os.path.exists(db_path) or not os.path.exists(model_path):
        logger.error("Faltan archivos necesarios (DB o Modelo).")
        return

    conn = duckdb.connect(db_path)
    df = conn.execute(f"SELECT * FROM {table_name}").df()
    conn.close()
    
    df['Open_Time'] = pd.to_datetime(df['Open_Time'])
    df = df.sort_values('Open_Time').set_index('Open_Time')
    
    oracle = OracleEngine.load(model_path)

    # 2. Detección de Señales (Layer 3)
    df = SignalDetector.detect_key_candles(df, volume_percentile_threshold=80)
    t_events = df[df['is_key_candle']].index
    
    if len(t_events) == 0:
        logger.warning("No se detectaron señales.")
        return

    # 3. Extracción de Features y Predicción (Layer 4)
    features = FeatureEngineer.extract_features(df, t_events)
    predictions = oracle.predict(features)
    
    # Filtrar solo señales donde el Oráculo predice 1 (Éxito)
    oracle_signals = t_events[predictions == 1]
    
    logger.info(f"Señales originales: {len(t_events)}")
    logger.info(f"Señales filtradas por el Oráculo: {len(oracle_signals)}")

    if len(oracle_signals) == 0:
        logger.warning("El Oráculo no validó ninguna señal.")
        return

    # 4. Etiquetado Real para Verificación (Layer 3)
    labels = get_atr_labels(df, oracle_signals, tp_factor=2.0, sl_factor=1.0, time_limit=24)

    # 5. Resultados
    logger.info("--- RESULTADOS FINALES (ESTRATEGIA FILTRADA) ---")
    counts = labels.value_counts().sort_index()
    
    summary = {
        "Total Señales Filtradas": len(labels),
        "Take Profit (1)": counts.get(1, 0),
        "Stop Loss (-1)": counts.get(-1, 0),
        "Neutral (0)": counts.get(0, 0)
    }
    
    for key, val in summary.items():
        print(f"{key}: {val}")
        
    if len(labels) > 0:
        win_rate = (summary["Take Profit (1)"] / len(labels)) * 100
        print(f"Win Rate Filtrado: {win_rate:.2f}%")

if __name__ == "__main__":
    run_proof_strategy_v2()
