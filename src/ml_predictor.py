"""
Simple ML Predictor for Financial Risk Prediction System
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
from datetime import datetime
from .data_collector import SimpleDataCollector

logger = logging.getLogger(__name__)

class SimpleMLPredictor:
    """Simple ML-based risk predictor with default predictions"""
    
    def __init__(self):
        self.data_collector = SimpleDataCollector()
        logger.info("Simple ML Predictor initialized")
        
    def predict_risk(self, symbols: List[str], time_horizon: int = 1) -> Dict:
        """Predict risk using simple heuristics (for demo purposes)"""
        try:
            logger.info(f"Generating ML predictions for symbols: {symbols}")
            
            predictions = {}
            
            for symbol in symbols:
                # Get basic volatility estimate
                volatility = self._estimate_volatility(symbol)
                
                # Generate reasonable predictions based on symbol characteristics
                if symbol.startswith('BTC') or symbol.startswith('ETH'):
                    # Crypto - higher volatility
                    pred_vol = volatility * 1.5
                    pred_return = 0.002  # Slightly positive expected return
                elif symbol in ['SPY', 'QQQ', 'VTI']:
                    # ETFs - lower volatility
                    pred_vol = volatility * 0.8
                    pred_return = 0.0008
                else:
                    # Individual stocks
                    pred_vol = volatility
                    pred_return = 0.001
                
                # Calculate VaR estimates from predictions
                var_95 = -(pred_return - 1.645 * pred_vol)  # 95% VaR
                var_99 = -(pred_return - 2.326 * pred_vol)  # 99% VaR
                
                predictions[symbol] = {
                    'predicted_volatility': float(pred_vol),
                    'predicted_return': float(pred_return),
                    'var_95': float(max(0, var_95)),
                    'var_99': float(max(0, var_99)),
                    'model_score': 0.75  # Fixed confidence score for demo
                }
            
            logger.info(f"ML predictions generated for {len(predictions)} symbols")
            
            return {
                'predictions': predictions,
                'metadata': {
                    'prediction_date': datetime.now().isoformat(),
                    'time_horizon': time_horizon,
                    'symbols': symbols,
                    'model_type': 'simple_heuristic',
                    'note': 'Simplified predictions for academic demonstration'
                }
            }
            
        except Exception as e:
            logger.error(f"Error in ML prediction: {str(e)}")
            return self._get_default_predictions(symbols, time_horizon)
    
    def _estimate_volatility(self, symbol: str) -> float:
        """Estimate volatility from historical data or use defaults"""
        try:
            data = self.data_collector.get_historical_data(symbol, 60)  # 60 days
            
            if not data['data'] or len(data['data']) < 10:
                # Use default volatility based on asset type
                if symbol.startswith('BTC') or symbol.startswith('ETH'):
                    return 0.04  # 4% daily volatility for crypto
                elif symbol in ['SPY', 'QQQ', 'VTI']:
                    return 0.012  # 1.2% daily volatility for ETFs
                else:
                    return 0.02  # 2% daily volatility for stocks
            
            # Calculate historical volatility
            df = pd.DataFrame(data['data'])
            df = df.sort_values('date')
            prices = df['close'].values
            returns = np.diff(prices) / prices[:-1]
            volatility = np.std(returns)
            
            return float(volatility)
            
        except Exception as e:
            logger.error(f"Error estimating volatility for {symbol}: {str(e)}")
            return 0.02  # Default 2% daily volatility
    
    def _get_default_predictions(self, symbols: List[str], time_horizon: int) -> Dict:
        """Return default predictions when calculation fails"""
        logger.warning("Using default ML predictions")
        
        predictions = {}
        for symbol in symbols:
            predictions[symbol] = {
                'predicted_volatility': 0.02,
                'predicted_return': 0.001,
                'var_95': 0.05,
                'var_99': 0.08,
                'model_score': 0.70
            }
        
        return {
            'predictions': predictions,
            'metadata': {
                'prediction_date': datetime.now().isoformat(),
                'time_horizon': time_horizon,
                'symbols': symbols,
                'note': 'Default predictions used due to calculation errors'
            }
        }
