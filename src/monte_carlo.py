"""
Simple Monte Carlo Simulator for Financial Risk Prediction System
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional
import logging
from datetime import datetime
from .data_collector import SimpleDataCollector

logger = logging.getLogger(__name__)

class SimpleMonteCarlo:
    """Simple Monte Carlo simulator for portfolio risk analysis"""
    
    def __init__(self):
        self.data_collector = SimpleDataCollector()
        logger.info("Simple Monte Carlo Simulator initialized")
        
    def run_simulation(self, symbols: List[str], weights: List[float], 
                      num_simulations: int = 10000, time_horizon: int = 1, 
                      initial_portfolio_value: float = 100000) -> Dict:
        """Run Monte Carlo simulation for portfolio risk analysis"""
        try:
            logger.info(f"Running Monte Carlo simulation with {num_simulations} iterations")
            
            # Get historical returns for simulation parameters
            portfolio_params = self._calculate_portfolio_parameters(symbols, weights)
            
            if portfolio_params is None:
                logger.warning("Using default parameters for Monte Carlo simulation")
                portfolio_params = {'mean': 0.0008, 'std': 0.02}  # Default daily parameters
            
            # Run simulations
            simulated_returns = self._simulate_portfolio_returns(
                portfolio_params, num_simulations, time_horizon
            )
            
            # Calculate final values
            final_values = initial_portfolio_value * (1 + simulated_returns)
            
            # Calculate risk metrics
            var_95 = self._calculate_mc_var(simulated_returns, 0.95)
            var_99 = self._calculate_mc_var(simulated_returns, 0.99)
            expected_shortfall_95 = self._calculate_mc_expected_shortfall(simulated_returns, 0.95)
            expected_shortfall_99 = self._calculate_mc_expected_shortfall(simulated_returns, 0.99)
            
            # Statistics
            mean_return = np.mean(simulated_returns)
            std_return = np.std(simulated_returns)
            prob_loss = np.sum(simulated_returns < 0) / num_simulations
            
            # Percentiles
            percentiles = np.percentile(simulated_returns, [1, 5, 25, 50, 75, 95, 99])
            
            logger.info(f"Monte Carlo simulation completed. VaR 95%: {var_95:.4f}")
            
            return {
                'simulation_results': {
                    'portfolio_returns': simulated_returns.tolist()[:1000],  # Limit for JSON size
                    'final_values': final_values.tolist()[:1000],
                    'statistics': {
                        'mean_return': float(mean_return),
                        'std_return': float(std_return),
                        'probability_of_loss': float(prob_loss)
                    }
                },
                'risk_metrics': {
                    'var_95': float(var_95),
                    'var_99': float(var_99),
                    'expected_shortfall_95': float(expected_shortfall_95),
                    'expected_shortfall_99': float(expected_shortfall_99)
                },
                'percentiles': {
                    '1st': float(percentiles[0]),
                    '5th': float(percentiles[1]),
                    '25th': float(percentiles[2]),
                    '50th': float(percentiles[3]),
                    '75th': float(percentiles[4]),
                    '95th': float(percentiles[5]),
                    '99th': float(percentiles[6])
                },
                'metadata': {
                    'num_simulations': num_simulations,
                    'time_horizon': time_horizon,
                    'initial_value': initial_portfolio_value,
                    'simulation_date': datetime.now().isoformat(),
                    'symbols': symbols,
                    'weights': weights
                }
            }
            
        except Exception as e:
            logger.error(f"Error in Monte Carlo simulation: {str(e)}")
            return self._get_default_simulation_results(num_simulations, time_horizon, initial_portfolio_value)
    
    def _calculate_portfolio_parameters(self, symbols: List[str], weights: List[float]) -> Optional[Dict]:
        """Calculate portfolio mean and standard deviation from historical data"""
        try:
            returns_list = []
            
            for i, symbol in enumerate(symbols):
                data = self.data_collector.get_historical_data(symbol, 252)
                
                if not data['data']:
                    logger.warning(f"No data available for {symbol}")
                    continue
                
                # Calculate returns
                df = pd.DataFrame(data['data'])
                df = df.sort_values('date')
                prices = df['close'].values
                returns = np.diff(prices) / prices[:-1]
                
                # Weight the returns
                weighted_returns = returns * weights[i]
                returns_list.append(weighted_returns)
            
            if not returns_list:
                return None
            
            # Combine weighted returns
            min_length = min(len(r) for r in returns_list)
            portfolio_returns = np.zeros(min_length)
            for returns in returns_list:
                portfolio_returns += returns[-min_length:]
            
            return {
                'mean': np.mean(portfolio_returns),
                'std': np.std(portfolio_returns)
            }
            
        except Exception as e:
            logger.error(f"Error calculating portfolio parameters: {str(e)}")
            return None
    
    def _simulate_portfolio_returns(self, params: Dict, num_simulations: int, time_horizon: int) -> np.ndarray:
        """Generate simulated portfolio returns"""
        mean = params['mean']
        std = params['std']
        
        # Adjust for time horizon
        scaled_mean = mean * time_horizon
        scaled_std = std * np.sqrt(time_horizon)
        
        # Generate random returns
        simulated_returns = np.random.normal(scaled_mean, scaled_std, num_simulations)
        
        return simulated_returns
    
    def _calculate_mc_var(self, returns: np.ndarray, confidence_level: float) -> float:
        """Calculate Monte Carlo VaR"""
        alpha = 1 - confidence_level
        var = np.percentile(returns, alpha * 100)
        return float(-var)  # VaR is positive (loss)
    
    def _calculate_mc_expected_shortfall(self, returns: np.ndarray, confidence_level: float) -> float:
        """Calculate Monte Carlo Expected Shortfall"""
        alpha = 1 - confidence_level
        var_threshold = np.percentile(returns, alpha * 100)
        
        # Expected Shortfall is the mean of returns below VaR
        tail_losses = returns[returns <= var_threshold]
        if len(tail_losses) > 0:
            es = -np.mean(tail_losses)
        else:
            es = -var_threshold
        
        return float(es)
    
    def _get_default_simulation_results(self, num_simulations: int, time_horizon: int, 
                                      initial_portfolio_value: float) -> Dict:
        """Return default simulation results when calculation fails"""
        logger.warning("Using default Monte Carlo simulation results")
        
        # Generate default simulation
        default_returns = np.random.normal(0.0008, 0.02, num_simulations)
        final_values = initial_portfolio_value * (1 + default_returns)
        
        return {
            'simulation_results': {
                'portfolio_returns': default_returns.tolist()[:1000],
                'final_values': final_values.tolist()[:1000],
                'statistics': {
                    'mean_return': 0.0008,
                    'std_return': 0.02,
                    'probability_of_loss': 0.45
                }
            },
            'risk_metrics': {
                'var_95': 0.05,
                'var_99': 0.08,
                'expected_shortfall_95': 0.07,
                'expected_shortfall_99': 0.10
            },
            'percentiles': {
                '1st': -0.08,
                '5th': -0.05,
                '25th': -0.01,
                '50th': 0.001,
                '75th': 0.02,
                '95th': 0.04,
                '99th': 0.07
            },
            'metadata': {
                'num_simulations': num_simulations,
                'time_horizon': time_horizon,
                'initial_value': initial_portfolio_value,
                'simulation_date': datetime.now().isoformat(),
                'note': 'Default simulation used due to data issues'
            }
        }
