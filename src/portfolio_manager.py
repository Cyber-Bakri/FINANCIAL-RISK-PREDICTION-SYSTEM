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
                          current_weights: Optional[List[float]] = None, 
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
            
            # Use provided current weights or default to equal weights
            if not current_weights or len(current_weights) != len(symbols):
                current_weights = [1.0 / len(symbols)] * len(symbols)
            
            # Generate basic performance metrics
            portfolio_metrics = self._calculate_simple_metrics(symbols, optimized_weights)
            current_metrics = self._calculate_simple_metrics(symbols, current_weights)
            
            return {
                'optimized_weights': weights_dict,
                'portfolio_metrics': portfolio_metrics,
                'current_portfolio_metrics': current_metrics,
                'method': method,
                'optimization_date': datetime.now().isoformat(),
                'symbols': symbols,
                'recommendations': self._generate_simple_recommendations(symbols, optimized_weights, current_weights)
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
            logger.info(f"Starting max Sharpe optimization for {symbols}")
            
            # Get historical data and calculate metrics
            sharpe_ratios = []
            
            for symbol in symbols:
                try:
                    data = self.data_collector.get_historical_data(symbol, 252)  # 1 year of data
                    logger.info(f"Got data for {symbol}: {len(data.get('data', [])) if data else 0} records")
                    
                    if data and data.get('data') and len(data['data']) > 20:
                        df = pd.DataFrame(data['data'])
                        df = df.sort_values('date')
                        prices = df['close'].values
                        
                        # Calculate daily returns
                        returns = np.diff(prices) / prices[:-1]
                        
                        # Remove any infinite or NaN values
                        returns = returns[np.isfinite(returns)]
                        
                        if len(returns) > 10:
                            mean_return = np.mean(returns)
                            std_return = np.std(returns)
                            
                            if std_return > 0:
                                sharpe = mean_return / std_return
                            else:
                                sharpe = 0
                        else:
                            sharpe = 0
                    else:
                        sharpe = 0
                        
                    sharpe_ratios.append(sharpe)
                    logger.info(f"{symbol}: Sharpe ratio = {sharpe:.4f}")
                    
                except Exception as e:
                    logger.warning(f"Error calculating Sharpe for {symbol}: {str(e)}")
                    sharpe_ratios.append(0)
            
            # Convert negative Sharpe ratios to small positive values for weighting
            adjusted_sharpes = [max(0.01, s + abs(min(sharpe_ratios)) + 0.1) if s < 0 else max(0.01, s) for s in sharpe_ratios]
            
            # Weight by adjusted Sharpe ratios
            total_sharpe = sum(adjusted_sharpes)
            if total_sharpe > 0:
                weights = [s / total_sharpe for s in adjusted_sharpes]
                logger.info(f"Max Sharpe weights: {dict(zip(symbols, weights))}")
            else:
                logger.warning("All Sharpe ratios are zero, using equal weights")
                weights = self._equal_weight_optimization(symbols)
            
            return weights
            
        except Exception as e:
            logger.error(f"Error in max Sharpe optimization: {str(e)}")
            return self._equal_weight_optimization(symbols)
    
    def _simple_min_variance(self, symbols: List[str]) -> List[float]:
        """Simplified minimum variance optimization"""
        try:
            logger.info(f"Starting min variance optimization for {symbols}")
            
            # Get volatilities
            volatilities = []
            for symbol in symbols:
                try:
                    data = self.data_collector.get_historical_data(symbol, 252)  # 1 year of data
                    logger.info(f"Got data for {symbol}: {len(data.get('data', [])) if data else 0} records")
                    
                    if data and data.get('data') and len(data['data']) > 20:
                        df = pd.DataFrame(data['data'])
                        df = df.sort_values('date')
                        prices = df['close'].values
                        
                        # Calculate daily returns
                        returns = np.diff(prices) / prices[:-1]
                        
                        # Remove any infinite or NaN values
                        returns = returns[np.isfinite(returns)]
                        
                        if len(returns) > 10:
                            volatility = np.std(returns)
                        else:
                            volatility = 0.02  # Default volatility
                    else:
                        volatility = 0.02  # Default volatility
                        
                    volatilities.append(volatility)
                    logger.info(f"{symbol}: Volatility = {volatility:.4f}")
                    
                except Exception as e:
                    logger.warning(f"Error calculating volatility for {symbol}: {str(e)}")
                    volatilities.append(0.02)  # Default volatility
            
            # Inverse volatility weighting (lower volatility = higher weight)
            inv_vol = [1.0 / max(0.001, vol) for vol in volatilities]
            total_inv_vol = sum(inv_vol)
            weights = [iv / total_inv_vol for iv in inv_vol]
            
            logger.info(f"Min variance weights: {dict(zip(symbols, weights))}")
            
            return weights
            
        except Exception as e:
            logger.error(f"Error in min variance optimization: {str(e)}")
            return self._equal_weight_optimization(symbols)
    
    def _calculate_simple_metrics(self, symbols: List[str], weights: List[float]) -> Dict:
        """Calculate real portfolio metrics from historical data"""
        try:
            logger.info(f"Calculating real metrics for {symbols} with weights {weights}")
            
            # Get historical data and calculate portfolio metrics
            portfolio_returns = []
            individual_returns = []
            individual_volatilities = []
            
            for i, symbol in enumerate(symbols):
                try:
                    data = self.data_collector.get_historical_data(symbol, 252)  # 1 year
                    
                    if data and data.get('data') and len(data['data']) > 20:
                        df = pd.DataFrame(data['data'])
                        df = df.sort_values('date')
                        prices = df['close'].values
                        
                        # Calculate daily returns
                        returns = np.diff(prices) / prices[:-1]
                        returns = returns[np.isfinite(returns)]
                        
                        if len(returns) > 10:
                            # Individual asset metrics
                            annual_return = np.mean(returns) * 252
                            annual_vol = np.std(returns) * np.sqrt(252)
                            
                            individual_returns.append(annual_return)
                            individual_volatilities.append(annual_vol)
                            
                            # Weighted returns for portfolio calculation
                            weighted_returns = returns * weights[i]
                            portfolio_returns.append(weighted_returns)
                            
                            logger.info(f"{symbol}: Return={annual_return:.2%}, Vol={annual_vol:.2%}")
                        else:
                            logger.warning(f"Insufficient data for {symbol}")
                            individual_returns.append(0.08)  # Fallback
                            individual_volatilities.append(0.20)
                    else:
                        logger.warning(f"No data for {symbol}")
                        individual_returns.append(0.08)  # Fallback
                        individual_volatilities.append(0.20)
                        
                except Exception as e:
                    logger.error(f"Error processing {symbol}: {e}")
                    individual_returns.append(0.08)  # Fallback
                    individual_volatilities.append(0.20)
            
            # Calculate portfolio metrics
            if portfolio_returns and len(portfolio_returns) > 0:
                # Align return series lengths
                min_length = min(len(r) for r in portfolio_returns)
                aligned_returns = [r[-min_length:] for r in portfolio_returns]
                
                # Sum weighted returns
                portfolio_return_series = np.sum(aligned_returns, axis=0)
                
                # Portfolio metrics
                expected_return = np.mean(portfolio_return_series) * 252
                volatility = np.std(portfolio_return_series) * np.sqrt(252)
                
                # Sharpe ratio (assuming 2% risk-free rate)
                risk_free_rate = 0.02
                sharpe_ratio = (expected_return - risk_free_rate) / volatility if volatility > 0 else 0
                
                logger.info(f"Portfolio metrics: Return={expected_return:.2%}, Vol={volatility:.2%}, Sharpe={sharpe_ratio:.3f}")
                
            else:
                # Fallback to weighted average of individual metrics
                expected_return = np.average(individual_returns, weights=weights)
                volatility = np.sqrt(np.average(np.array(individual_volatilities)**2, weights=weights))
                sharpe_ratio = (expected_return - 0.02) / volatility if volatility > 0 else 0
                
                logger.info(f"Using weighted average metrics: Return={expected_return:.2%}, Vol={volatility:.2%}")
            
            return {
                'expected_return': float(expected_return),
                'volatility': float(volatility),
                'sharpe_ratio': float(sharpe_ratio)
            }
            
        except Exception as e:
            logger.error(f"Error calculating real metrics: {str(e)}")
            # Return reasonable fallback values
            return {
                'expected_return': 0.08,
                'volatility': 0.18,
                'sharpe_ratio': 0.33
            }
    
    def _generate_simple_recommendations(self, symbols: List[str], optimized_weights: List[float], current_weights: List[float] = None) -> Dict:
        """Generate simple optimization recommendations"""
        # Use equal weights as default if current weights not provided
        if current_weights is None:
            current_weights = [1.0 / len(symbols)] * len(symbols)
            
        recommendations = {
            'key_insights': [],
            'weight_changes': [],
            'performance_improvement': self._calculate_performance_improvement(
                symbols, current_weights, optimized_weights
            )
        }
        
        # Add insights
        max_weight_idx = np.argmax(optimized_weights)
        min_weight_idx = np.argmin(optimized_weights)
        
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
        
        # Add weight changes using actual current weights
        for i, symbol in enumerate(symbols):
            current_weight = current_weights[i]
            optimized_weight = optimized_weights[i]
            change = (optimized_weight - current_weight) * 100
            
            recommendations['weight_changes'].append({
                'symbol': symbol,
                'current_weight': current_weight * 100,
                'recommended_weight': optimized_weight * 100,
                'change': change,
                'action': 'increase' if change > 0.1 else ('decrease' if change < -0.1 else 'hold'),
                'reasoning': 'Based on risk-return optimization analysis'
            })
        
        return recommendations
    
    def _calculate_performance_improvement(self, symbols: List[str], current_weights: List[float], 
                                         optimized_weights: List[float]) -> Dict:
        """Calculate real performance improvement between current and optimized portfolios"""
        try:
            # Calculate metrics for both portfolios
            current_metrics = self._calculate_simple_metrics(symbols, current_weights)
            optimized_metrics = self._calculate_simple_metrics(symbols, optimized_weights)
            
            # Calculate improvements
            return_improvement = optimized_metrics['expected_return'] - current_metrics['expected_return']
            volatility_change = optimized_metrics['volatility'] - current_metrics['volatility']
            sharpe_improvement = optimized_metrics['sharpe_ratio'] - current_metrics['sharpe_ratio']
            
            return {
                'return_improvement': float(return_improvement),
                'volatility_change': float(volatility_change),
                'sharpe_improvement': float(sharpe_improvement)
            }
            
        except Exception as e:
            logger.error(f"Error calculating performance improvement: {e}")
            return {
                'return_improvement': 0.0,
                'volatility_change': 0.0,
                'sharpe_improvement': 0.0
            }
    
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
