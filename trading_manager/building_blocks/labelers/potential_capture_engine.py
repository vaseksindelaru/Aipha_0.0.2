import pandas as pd
import numpy as np
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)

def get_atr_labels(
    prices: pd.DataFrame,
    t_events: pd.Index,
    sides: Optional[pd.Series] = None,
    atr_period: int = 14,
    tp_factor: float = 2.0,
    sl_factor: float = 1.2,
    time_limit: int = 24
) -> pd.Series:
    """
    Versión básica del Triple Barrier Method usando ATR para las barreras.
    Soporta posiciones Long (1) y Short (-1).
    
    Args:
        prices: DataFrame con columnas High, Low, Close.
        t_events: Índice de timestamps donde ocurrió una señal.
        sides: Serie con el lado de la señal (1 o -1) para cada timestamp en t_events.
        atr_period: Periodo para el cálculo del ATR.
        tp_factor: Multiplicador del ATR para el Take Profit.
        sl_factor: Multiplicador del ATR para el Stop Loss.
        time_limit: Número máximo de velas para mantener la posición.
        
    Returns:
        Serie de pandas con etiquetas (1, -1, 0) para cada evento.
        1: Éxito (TP tocado), -1: Fracaso (SL tocado), 0: Límite de tiempo.
    """
    if t_events.empty:
        return pd.Series(dtype='int64')

    # 1. Calcular ATR (Average True Range)
    high_low = prices['High'] - prices['Low']
    high_close = abs(prices['High'] - prices['Close'].shift())
    low_close = abs(prices['Low'] - prices['Close'].shift())
    
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=atr_period).mean()

    labels = []
    
    for start_time in t_events:
        if start_time not in prices.index:
            continue
            
        # Determinar el lado (por defecto Long si no se provee)
        side = sides.loc[start_time] if sides is not None else 1
        if isinstance(side, pd.Series):
            side = side.iloc[0]
            
        # Obtener datos desde el evento
        idx = prices.index.get_loc(start_time)
        if isinstance(idx, slice):
            idx = idx.start
        elif isinstance(idx, np.ndarray):
            idx = np.where(idx)[0][0]
            
        future_prices = prices.iloc[idx : idx + time_limit + 1]
        
        if len(future_prices) < 2:
            labels.append(0)
            continue
            
        entry_price = future_prices.iloc[0]['Close']
        current_atr = atr.loc[start_time]
        if isinstance(current_atr, pd.Series):
            current_atr = current_atr.iloc[0]
        
        if pd.isna(current_atr):
            labels.append(0)
            continue

        # Definir barreras según el lado
        if side == 1: # Long
            tp_barrier = entry_price + (current_atr * tp_factor)
            sl_barrier = entry_price - (current_atr * sl_factor)
        else: # Short
            tp_barrier = entry_price - (current_atr * tp_factor)
            sl_barrier = entry_price + (current_atr * sl_factor)
        
        label = 0 # Default: Time limit reached
        
        # Recorrer el futuro para ver qué barrera se toca primero
        for i in range(1, len(future_prices)):
            high = future_prices.iloc[i]['High']
            low = future_prices.iloc[i]['Low']
            
            if side == 1: # Lógica Long
                if high >= tp_barrier:
                    label = 1
                    break
                if low <= sl_barrier:
                    label = -1
                    break
            else: # Lógica Short
                if low <= tp_barrier: # En Short, TP está abajo
                    label = 1
                    break
                if high >= sl_barrier: # En Short, SL está arriba
                    label = -1
                    break
                
        labels.append(label)

    return pd.Series(labels, index=t_events)
    atr_period: int = 10,
    atr_period: int = 10,
    atr_period: int = 10,
    sl_factor: float = 0.8,
