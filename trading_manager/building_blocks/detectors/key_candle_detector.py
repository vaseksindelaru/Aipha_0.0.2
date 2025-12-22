import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class SignalDetector:
    """Detecta señales basadas en características específicas de las velas."""

    @staticmethod
    def detect_key_candles(
        df: pd.DataFrame,
        volume_lookback: int = 50,
        volume_percentile_threshold: int = 80,
        body_percentile_threshold: int = 30
    ) -> pd.DataFrame:
        """
        Detecta 'velas clave' basadas en volumen inusual y cuerpo pequeño.
        
        Args:
            df: DataFrame con columnas Open, High, Low, Close, Volume.
            volume_lookback: Periodo para calcular el percentil de volumen.
            volume_percentile_threshold: Percentil de volumen para considerar 'alto volumen'.
            body_percentile_threshold: Porcentaje máximo del cuerpo respecto al rango total.
            
        Returns:
            DataFrame con la columna 'is_key_candle'.
        """
        if df.empty:
            logger.warning("DataFrame vacío recibido en detect_key_candles.")
            return df

        # Asegurar que las columnas necesarias existen
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in required_cols:
            if col not in df.columns:
                logger.error(f"Columna faltante: {col}")
                return df

        # 1. Calcular el umbral de volumen (percentil móvil)
        # Nota: Usamos rolling para el percentil si queremos que sea dinámico, 
        # pero la guía sugiere un percentil de los últimos N periodos.
        df['volume_threshold'] = df['Volume'].rolling(window=volume_lookback).apply(
            lambda x: np.percentile(x, volume_percentile_threshold)
        )

        # 2. Cálculos de tamaño de vela
        df['body_size'] = abs(df['Close'] - df['Open'])
        df['candle_range'] = df['High'] - df['Low']
        
        # Evitar división por cero
        df['body_percentage'] = np.where(
            df['candle_range'] > 0,
            (df['body_size'] / df['candle_range']) * 100,
            100
        )

        # 3. Detección de la vela clave
        df['is_key_candle'] = (
            (df['Volume'] >= df['volume_threshold']) & 
            (df['body_percentage'] <= body_percentile_threshold)
        )

        # Limpiar columnas temporales si se desea, o mantenerlas para debug
        # df.drop(columns=['volume_threshold', 'body_size', 'candle_range', 'body_percentage'], inplace=True)

        logger.info(f"Detección completada. Velas clave encontradas: {df['is_key_candle'].sum()}")
        return df
