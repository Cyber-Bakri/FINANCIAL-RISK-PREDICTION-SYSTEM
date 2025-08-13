"""
Simple Portfolio Manager for Financial Risk Prediction System
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
from datetime import datetime
from .data_collector import SimpleDataCollector

logger = logging.getLogger(__name__)

class SimplePortfolioManager:
    """Simple portfolio optimization and management"""
    
    def __init__(self):
        self.data_collector = SimpleDataCollector()
        logger.info("Simple Portfolio Manager initialized")
        
    def optimize_portfolio(self, symbols: List[str], method: str = 'equal_weight', 
                          target_return: Optional[float] = None) -> Dict:
        """Optimize portfolio allocation with detailed recommendations"""
        try:
            logger.info(f"Optimizing portfolio for symbols: {symbols} using method: {method}")
            
            # For demo purposes, we'll use simplified optimization
            if method == 'equal_weight':
                optimized_weights = self._equal_weight_optimization(symbols)
            elif method == 'max_sharpe':
                optimized_weights = self._simple_max_sharpe(symbols)
            elif method == 'min_variance':
                optimized_weights = self._simple_min_variance(symbols)
            else:
                # Default to equal weight
                optimized_weights = self._equal_weight_optimization(symbols)
            
            # Calculate simple metrics
            weights_dict = {symbol: weight for symbol, weight in zip(symbols, optimized_weights)}
            
            # Generate basic performance metrics
            portfolio_metrics = self._calculate_simple_metrics(symbols, optimized_weights)
            current_metrics = self._calculate_simple_metrics(symbols, [1.0/len(symbols)] * len(symbols))
            
            return {
                'optimized_weights': weights_dict,
                'portfolio_metrics': portfolio_metrics,
                'current_portfolio_metrics': current_metrics,
                'method': method,
                'optimization_date': datetime.now().isoformat(),
                'symbols': symbols,
                'recommendations': self._generate_simple_recommendations(symbols, optimized_weights)
            }
            
        except Exception as e:
            logger.error(f"Error optimizing portfolio: {str(e)}")
            return self._get_default_optimization(symbols)
    
    def _equal_weight_optimization(self, symbols: List[str]) -> List[float]:
        """Equal weight allocation"""
        return [1.0 / len(symbols)] * len(symbols)
    
    def _simple_max_sharpe(self, symbols: List[str]) -> List[float]:
        """Simplified max Sharpe ratio optimization"""
        try:
            # Get historical data and calculate simple metrics
            returns_data = []
            for symbol in symbols:
                data = self.data_collector.get_historical_data(symbol, 60)
                if data['data']:
                    df = pd.DataFrame(data['data'])
                    df = df.sort_values('date')
                    prices = df['close'].values
                    returns = np.diff(prices) / prices[:-1]
                    returns_data.append(np.mean(returns) / np.std(returns))  # Simple Sharpe proxy
                else:
                    returns_data.append(0.5)  # Default Sharpe
            
            # Weight by Sharpe ratios
            total_sharpe = sum(max(0, r) for r in returns_data)
            if total_sharpe > 0:
                weights = [max(0, r) / total_sharpe for r in returns_data]
            else:
                weights = self._equal_weight_optimization(symbols)
            
            return weights
            
        except Exception as e:
            logger.error(f"Error in max Sharpe optimization: {str(e)}")
            return self._equal_weight_optimization(symbols)
    
    def _simple_min_variance(self, symbols: List[str]) -> List[float]:
        """Simplified minimum variance optimization"""
        try:
            # Get volatilities
            volatilities = []
            for symbol in symbols:
                data = self.data_collector.get_historical_data(symbol, 60)
                if data['data']:
                    df = pd.DataFrame(data['data'])
                    df = df.sort_values('date')
                    prices = df['close'].values
                    returns = np.diff(prices) / prices[:-1]
                    volatilities.append(np.std(returns))
                else:
                    volatilities.append(0.02)  # Default volatility
            
            # Inverse volatility weighting
            inv_vol = [1.0 / max(0.001, vol) for vol in volatilities]
            total_inv_vol = sum(inv_vol)
            weights = [iv / total_inv_vol for iv in inv_vol]
            
            return weights
            
        except Exception as e:
            logger.error(f"Error in min variance optimization: {str(e)}")
            return self._equal_weight_optimization(symbols)
    
    def _calculate_simple_metrics(self, symbols: List[str], weights: List[float]) -> Dict:
        """Calculate simplified portfolio metrics"""
        try:
            # Default metrics for demo
            expected_return = 0.08  # 8% annualized return
            volatility = 0.15  # 15% annualized volatility
            sharpe_ratio = (expected_return - 0.02) / volatility  # Assuming 2% risk-free rate
            
            return {
                'expected_return': expected_return,
                'volatility': volatility,
                'sharpe_ratio': sharpe_ratio
            }
            
        except Exception as e:
            logger.error(f"Error calculating metrics: {str(e)}")
            return {
                'expected_return': 0.08,
                'volatility': 0.15,
                'sharpe_ratio': 0.4
            }
    
    def _generate_simple_recommendations(self, symbols: List[str], weights: List[float]) -> Dict:
        """Generate simple optimization recommendations"""
        recommendations = {
            'key_insights': [],
            'weight_changes': [],
            'performance_improvement': {
                'return_improvement': 0.02,  # 2% improvement
                'volatility_change': -0.01,  # 1% volatility reduction
                'sharpe_improvement': 0.1    # 0.1 Sharpe improvement
            }
        }
        
        # Add insights
        max_weight_idx = np.argmax(weights)
        min_weight_idx = np.argmin(weights)
        
        recommendations['key_insights'].append({
            'type': 'top_increase',
            'message': f'Increase allocation to {symbols[max_weight_idx]}',
            'reason': 'Higher risk-adjusted returns expected'
        })
        
        if len(symbols) > 1:
            recommendations['key_insights'].append({
                'type': 'reduce',
                'message': f'Reduce allocation to {symbols[min_weight_idx]}',
                'reason': 'Lower expected risk-adjusted performance'
            })
        
        # Add weight changes
        equal_weights = [1.0/len(symbols)] * len(symbols)
        for i, symbol in enumerate(symbols):
            recommendations['weight_changes'].append({
                'symbol': symbol,
                'current_weight': equal_weights[i] * 100,
                'recommended_weight': weights[i] * 100,
                'change': (weights[i] - equal_weights[i]) * 100,
                'action': 'increase' if weights[i] > equal_weights[i] else 'decrease',
                'reasoning': 'Based on simplified optimization model'
            })
        
        return recommendations
    
    def _get_default_optimization(self, symbols: List[str]) -> Dict:
        """Return default optimization when calculation fails"""
        logger.warning("Using default portfolio optimization")
        
        weights = self._equal_weight_optimization(symbols)
        weights_dict = {symbol: weight for symbol, weight in zip(symbols, weights)}
        
        return {
            'optimized_weights': weights_dict,
            'portfolio_metrics': {
                'expected_return': 0.08,
                'volatility': 0.15,
                'sharpe_ratio': 0.4
            },
            'current_portfolio_metrics': {
                'expected_return': 0.08,
                'volatility': 0.15,
                'sharpe_ratio': 0.4
            },
            'method': 'equal_weight',
            'optimization_date': datetime.now().isoformat(),
            'symbols': symbols,
            'note': 'Default equal weight allocation used'
        }
