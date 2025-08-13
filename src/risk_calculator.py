"""
Simple Risk Calculator for Financial Risk Prediction System
Focused on working VaR calculations for academic presentation
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Optional
import logging
from datetime import datetime
from .data_collector import SimpleDataCollector

logger = logging.getLogger(__name__)

class SimpleRiskCalculator:
    """Simple risk calculator with working VaR implementations"""
    
    def __init__(self):
        """Initialize the risk calculator"""
        self.data_collector = SimpleDataCollector()
        logger.info("Simple Risk Calculator initialized")
        
    def calculate_portfolio_risk(self, symbols: List[str], weights: List[float], 
                               confidence_level: float = 0.95, 
                               time_horizon: int = 1) -> Dict:
        """
        Calculate comprehensive portfolio risk metrics
        
        Args:
            symbols: List of asset symbols
            weights: Portfolio weights (must sum to 1)
            confidence_level: VaR confidence level (0.90, 0.95, 0.99)
            time_horizon: Time horizon in days
            
        Returns:
            Dictionary containing various risk metrics
        """
        try:
            logger.info(f"Calculating risk for portfolio: {symbols} with weights: {weights}")
            
            # Validate inputs
            if len(symbols) != len(weights):
                raise ValueError("Symbols and weights must have same length")
            
            if abs(sum(weights) - 1.0) > 1e-6:
                logger.warning("Weights don't sum to 1, normalizing...")
                weights = [w / sum(weights) for w in weights]
            
            # Get portfolio returns
            portfolio_returns = self._get_portfolio_returns(symbols, weights)
            
            if portfolio_returns is None or len(portfolio_returns) == 0:
                logger.error("Could not calculate portfolio returns")
                # Return default values
                return self._get_default_risk_metrics(symbols, weights, confidence_level, time_horizon)
            
            # VaR calculations
            var_historical = self._calculate_historical_var(portfolio_returns, confidence_level, time_horizon)
            var_parametric = self._calculate_parametric_var(portfolio_returns, confidence_level, time_horizon)
            expected_shortfall = self._calculate_expected_shortfall(portfolio_returns, confidence_level, time_horizon)
            
            # Other metrics
            volatility = self._calculate_volatility(portfolio_returns)
            max_drawdown = self._calculate_max_drawdown(portfolio_returns)
            sharpe_ratio = self._calculate_sharpe_ratio(portfolio_returns)
            
            risk_metrics = {
                'var_95': var_historical,  # Main VaR for frontend compatibility
                'var_99': self._calculate_historical_var(portfolio_returns, 0.99, time_horizon),
                'expected_shortfall': expected_shortfall,
                'volatility': volatility,
                'max_drawdown': max_drawdown,
                'sharpe_ratio': sharpe_ratio,
                'var_metrics': {
                    'historical_var': var_historical,
                    'parametric_var': var_parametric,
                    'expected_shortfall': expected_shortfall
                },
                'portfolio_metrics': {
                    'volatility': volatility,
                    'max_drawdown': max_drawdown,
                    'sharpe_ratio': sharpe_ratio
                },
                'metadata': {
                    'confidence_level': confidence_level,
                    'time_horizon': time_horizon,
                    'calculation_date': datetime.now().isoformat(),
                    'symbols': symbols,
                    'weights': weights,
                    'data_points': len(portfolio_returns)
                }
            }
            
            logger.info(f"Risk calculation completed successfully. Historical VaR: {var_historical:.4f}")
            return risk_metrics
            
        except Exception as e:
            logger.error(f"Error calculating portfolio risk: {str(e)}")
            return self._get_default_risk_metrics(symbols, weights, confidence_level, time_horizon)
    
    def _get_portfolio_returns(self, symbols: List[str], weights: List[float]) -> Optional[pd.Series]:
        """Calculate weighted portfolio returns"""
        try:
            returns_list = []
            
            for i, symbol in enumerate(symbols):
                logger.info(f"Fetching data for {symbol}")
                data = self.data_collector.get_historical_data(symbol, 252)
                
                if not data['data']:
                    logger.warning(f"No data available for {symbol}")
                    continue
                
                # Convert to DataFrame and calculate returns
                df = pd.DataFrame(data['data'])
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date')
                
                # Calculate daily returns
                prices = df['close'].values
                returns = np.diff(prices) / prices[:-1]
                
                # Weight the returns
                weighted_returns = returns * weights[i]
                returns_list.append(weighted_returns)
            
            if not returns_list:
                logger.error("No valid data found for any symbols")
                return None
            
            # Find minimum length to align all return series
            min_length = min(len(r) for r in returns_list)
            
            # Align and sum weighted returns
            portfolio_returns = np.zeros(min_length)
            for returns in returns_list:
                portfolio_returns += returns[-min_length:]
            
            return pd.Series(portfolio_returns)
            
        except Exception as e:
            logger.error(f"Error calculating portfolio returns: {str(e)}")
            return None
    
    def _calculate_historical_var(self, returns: pd.Series, confidence_level: float, time_horizon: int) -> float:
        """Calculate Historical VaR"""
        try:
            scaled_returns = returns * np.sqrt(time_horizon)
            alpha = 1 - confidence_level
            var = np.percentile(scaled_returns, alpha * 100)
            return float(-var)  # VaR is positive (loss)
        except Exception as e:
            logger.error(f"Error calculating historical VaR: {str(e)}")
            return 0.05  # Default 5% VaR
    
    def _calculate_parametric_var(self, returns: pd.Series, confidence_level: float, time_horizon: int) -> float:
        """Calculate Parametric VaR"""
        try:
            mean_return = returns.mean()
            std_return = returns.std()
            
            scaled_mean = mean_return * time_horizon
            scaled_std = std_return * np.sqrt(time_horizon)
            
            alpha = 1 - confidence_level
            z_score = stats.norm.ppf(alpha)
            
            var = -(scaled_mean + z_score * scaled_std)
            return float(var)
        except Exception as e:
            logger.error(f"Error calculating parametric VaR: {str(e)}")
            return 0.05  # Default 5% VaR
    
    def _calculate_expected_shortfall(self, returns: pd.Series, confidence_level: float, time_horizon: int) -> float:
        """Calculate Expected Shortfall (Conditional VaR)"""
        try:
            scaled_returns = returns * np.sqrt(time_horizon)
            alpha = 1 - confidence_level
            var_threshold = np.percentile(scaled_returns, alpha * 100)
            
            # Expected Shortfall is the mean of returns below VaR
            tail_losses = scaled_returns[scaled_returns <= var_threshold]
            if len(tail_losses) > 0:
                es = -tail_losses.mean()
            else:
                es = -var_threshold
            
            return float(es)
        except Exception as e:
            logger.error(f"Error calculating expected shortfall: {str(e)}")
            return 0.07  # Default 7% ES
    
    def _calculate_volatility(self, returns: pd.Series) -> float:
        """Calculate annualized volatility"""
        try:
            return float(returns.std() * np.sqrt(252))
        except Exception as e:
            logger.error(f"Error calculating volatility: {str(e)}")
            return 0.20  # Default 20% volatility
    
    def _calculate_max_drawdown(self, returns: pd.Series) -> float:
        """Calculate maximum drawdown"""
        try:
            cumulative = (1 + returns).cumprod()
            peak = cumulative.expanding().max()
            drawdown = (cumulative - peak) / peak
            return float(drawdown.min())
        except Exception as e:
            logger.error(f"Error calculating max drawdown: {str(e)}")
            return -0.15  # Default -15% max drawdown
    
    def _calculate_sharpe_ratio(self, returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio"""
        try:
            annual_return = returns.mean() * 252
            annual_vol = returns.std() * np.sqrt(252)
            
            if annual_vol == 0:
                return 0.0
            
            sharpe = (annual_return - risk_free_rate) / annual_vol
            return float(sharpe)
        except Exception as e:
            logger.error(f"Error calculating Sharpe ratio: {str(e)}")
            return 0.5  # Default Sharpe ratio
    
    def _get_default_risk_metrics(self, symbols: List[str], weights: List[float], 
                                 confidence_level: float, time_horizon: int) -> Dict:
        """Return default risk metrics when calculation fails"""
        logger.warning("Using default risk metrics due to calculation errors")
        
        return {
            'var_95': 0.05,  # 5% default VaR
            'var_99': 0.08,  # 8% default VaR 99%
            'expected_shortfall': 0.07,  # 7% default ES
            'volatility': 0.20,  # 20% default volatility
            'max_drawdown': -0.15,  # -15% default max drawdown
            'sharpe_ratio': 0.5,  # Default Sharpe ratio
            'var_metrics': {
                'historical_var': 0.05,  # 5% default VaR
                'parametric_var': 0.05,
                'expected_shortfall': 0.07  # 7% default ES
            },
            'portfolio_metrics': {
                'volatility': 0.20,  # 20% default volatility
                'max_drawdown': -0.15,  # -15% default max drawdown
                'sharpe_ratio': 0.5  # Default Sharpe ratio
            },
            'metadata': {
                'confidence_level': confidence_level,
                'time_horizon': time_horizon,
                'calculation_date': datetime.now().isoformat(),
                'symbols': symbols,
                'weights': weights,
                'note': 'Default values used due to data issues'
            }
        }
