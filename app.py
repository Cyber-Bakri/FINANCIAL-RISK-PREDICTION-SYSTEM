"""
Enhanced Financial Risk Prediction System - Flask Application
Professional-grade financial risk analysis and portfolio optimization system

Key Features:
- Global financial market support (US, NGX, UK, CA, AU, JP, DE, etc.)
- Intelligent portfolio optimization with market scanning
- Real-time risk analysis and predictions
- Advanced technical analysis and ML predictions
- Comprehensive symbol management and data collection

Author: Abubakri Olayide Abdul-Lateef
Project: B.Sc. Computer Science Final Year Project
Supervisor: Dr. (Mrs) A.O AMOO
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS

# Import our modules
from src.data_collector import SimpleDataCollector
from src.ml_predictor import SimpleMLPredictor
from src.risk_calculator import SimpleRiskCalculator
from src.portfolio_manager import SimplePortfolioManager
from src.monte_carlo import SimpleMonteCarlo

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')
CORS(app)

# Initialize core components
try:
    data_collector = SimpleDataCollector()
    ml_predictor = SimpleMLPredictor()
    risk_calculator = SimpleRiskCalculator()
    portfolio_manager = SimplePortfolioManager()
    monte_carlo = SimpleMonteCarlo()
    
    logger.info("All system components initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize components: {e}")
    # Continue anyway for demo purposes
    logger.warning("Some components may not be fully functional")

# =============================================================================
# GLOBAL MARKET AND SYMBOL MANAGEMENT ROUTES
# =============================================================================

@app.route('/api/markets')
def get_available_markets():
    """Get all available financial markets"""
    try:
        markets = {
            'US': {
                'name': 'United States',
                'currency': 'USD',
                'timezone': 'America/New_York',
                'description': 'NYSE, NASDAQ and major US exchanges'
            },
            'NGN': {
                'name': 'Nigeria',
                'currency': 'NGN', 
                'timezone': 'Africa/Lagos',
                'description': 'Nigerian Exchange (NGX)'
            },
            'UK': {
                'name': 'United Kingdom',
                'currency': 'GBP',
                'timezone': 'Europe/London',
                'description': 'London Stock Exchange'
            },
            'CA': {
                'name': 'Canada',
                'currency': 'CAD',
                'timezone': 'America/Toronto',
                'description': 'Toronto Stock Exchange'
            },
            'AU': {
                'name': 'Australia',
                'currency': 'AUD',
                'timezone': 'Australia/Sydney',
                'description': 'Australian Securities Exchange'
            },
            'JP': {
                'name': 'Japan',
                'currency': 'JPY',
                'timezone': 'Asia/Tokyo',
                'description': 'Tokyo Stock Exchange'
            },
            'DE': {
                'name': 'Germany',
                'currency': 'EUR',
                'timezone': 'Europe/Berlin',
                'description': 'Frankfurt Stock Exchange'
            },
            'CRYPTO': {
                'name': 'Cryptocurrency',
                'currency': 'USD',
                'timezone': 'UTC',
                'description': 'Major cryptocurrency pairs'
            }
        }
        
        return jsonify({
            'status': 'success',
            'markets': markets,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting markets: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/symbols')
def get_available_symbols():
    """Get all available symbols for specified market(s)"""
    try:
        market = request.args.get('market')  # Optional market filter
        refresh = request.args.get('refresh', 'false').lower() == 'true'
        
        logger.info(f"Fetching symbols for market: {market or 'all'}")
        
        # Get symbols from data collector
        symbols = data_collector.get_all_available_symbols(market=market, refresh=refresh)
        
        # Count total symbols
        total_symbols = sum(len(category_symbols) for category_symbols in symbols.values())
        
        return jsonify({
            'status': 'success',
            'symbols': symbols,
            'total_symbols': total_symbols,
            'market': market or 'global',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting symbols: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/market-analysis')
def analyze_market():
    """Comprehensive market analysis with investment recommendations"""
    try:
        market = request.args.get('market', 'US')
        portfolio_symbols = request.args.getlist('portfolio_symbols')
        investment_amount = float(request.args.get('investment_amount', 10000))
        
        logger.info(f"Analyzing {market} market with investment amount: ${investment_amount}")
        
        # Perform comprehensive market analysis
        analysis = data_collector.analyze_market_and_recommend(
            market=market,
            portfolio_symbols=portfolio_symbols,
            investment_amount=investment_amount
        )
        
        return jsonify({
            'status': 'success',
            'analysis': analysis
        })
        
    except Exception as e:
        logger.error(f"Error in market analysis: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# =============================================================================
# ENHANCED DATA AND PREDICTION ROUTES
# =============================================================================

@app.route('/api/historical-data')
def get_historical_data():
    """Get historical data for any global symbol"""
    try:
        symbol = request.args.get('symbol')
        days = int(request.args.get('days', 365))
        timeframe = request.args.get('timeframe', '1day')
        market = request.args.get('market')
        
        if not symbol:
            return jsonify({
                'status': 'error',
                'message': 'Symbol parameter is required'
            }), 400
        
        logger.info(f"Fetching historical data for {symbol} ({days} days, {timeframe})")
        
        # Get data using the enhanced data collector
        data = data_collector.get_historical_data(
            symbol=symbol,
            days=days,
            timeframe=timeframe,
            market=market
        )
        
        return jsonify({
            'status': 'success',
            'data': data
        })
        
    except Exception as e:
        logger.error(f"Error getting historical data: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/predict')
def predict_price():
    """Enhanced price prediction with multiple models"""
    try:
        symbol = request.args.get('symbol')
        days = int(request.args.get('days', 30))
        market = request.args.get('market')
        
        if not symbol:
            return jsonify({
                'status': 'error',
                'message': 'Symbol parameter is required'
            }), 400
        
        logger.info(f"Generating predictions for {symbol} ({days} days)")
        
        # Get historical data
        historical_data = data_collector.get_historical_data(
            symbol=symbol,
            days=365,
            market=market
        )
        
        if not historical_data.get('data'):
            return jsonify({
                'status': 'error',
                'message': f'No data available for {symbol}'
            }), 404
        
        # Generate predictions
        predictions = ml_predictor.predict_enhanced(
            symbol=symbol,
            historical_data=historical_data,
            days_ahead=days
        )
        
        return jsonify({
            'status': 'success',
            'predictions': predictions
        })
        
    except Exception as e:
        logger.error(f"Error generating predictions: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/portfolio-optimize')
def optimize_portfolio():
    """Enhanced portfolio optimization with global market scanning"""
    try:
        symbols = request.args.getlist('symbols')
        market = request.args.get('market', 'US')
        investment_amount = float(request.args.get('investment_amount', 10000))
        risk_level = request.args.get('risk_level', 'moderate')
        scan_market = request.args.get('scan_market', 'true').lower() == 'true'
        
        logger.info(f"Optimizing portfolio: {symbols} in {market} market")
        
        # If market scanning is enabled, get market recommendations
        if scan_market:
            market_analysis = data_collector.analyze_market_and_recommend(
                market=market,
                portfolio_symbols=symbols,
                investment_amount=investment_amount
            )
            
            # Add top recommendations to portfolio if not already included
            if 'portfolio_recommendations' in market_analysis:
                recommended_symbols = [
                    rec['symbol'] for rec in market_analysis['portfolio_recommendations']
                ]
                # Add top 5 recommendations that aren't already in portfolio
                for symbol in recommended_symbols[:5]:
                    if symbol not in symbols:
                        symbols.append(symbol)
        
        # Perform portfolio optimization
        optimization_result = portfolio_manager.optimize_portfolio_enhanced(
            symbols=symbols,
            market=market,
            investment_amount=investment_amount,
            risk_level=risk_level
        )
        
        return jsonify({
            'status': 'success',
            'optimization': optimization_result,
            'market_scan_enabled': scan_market
        })
        
    except Exception as e:
        logger.error(f"Error optimizing portfolio: {e}")
        return jsonify({
            'status': 'error', 
            'message': str(e)
        }), 500

# =============================================================================
# MAIN ROUTES
# =============================================================================

@app.route('/')
def index():
    """Enhanced main dashboard with global market support"""
    try:
        # Get available markets for the UI
        markets = {
            'US': 'United States (NYSE, NASDAQ)',
            'NGN': 'Nigeria (NGX)',
            'UK': 'United Kingdom (LSE)',
            'CA': 'Canada (TSX)',
            'AU': 'Australia (ASX)',
            'JP': 'Japan (TSE)',
            'DE': 'Germany (FSE)',
            'CRYPTO': 'Cryptocurrency'
        }
        
        return render_template('index.html', markets=markets)
        
    except Exception as e:
        logger.error(f"Error loading index page: {e}")
        return render_template('index.html', error=str(e))

@app.route('/api/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/market-status')
def get_market_status():
    """Get current market status and trading information"""
    try:
        status = data_collector.get_market_status()
        return jsonify(status)
    except Exception as e:
        logger.error(f"Market status error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/live-quote/<symbol>')
def get_live_quote(symbol):
    """Get live quote for a specific symbol"""
    try:
        quote = data_collector.get_live_quote(symbol.upper())
        return jsonify(quote)
    except Exception as e:
        logger.error(f"Live quote error for {symbol}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/live-quotes', methods=['POST'])
def get_multiple_live_quotes():
    """Get live quotes for multiple symbols"""
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        
        if not symbols:
            return jsonify({'error': 'No symbols provided'}), 400
        
        quotes = {}
        for symbol in symbols:
            quotes[symbol] = data_collector.get_live_quote(symbol.upper())
        
        return jsonify({
            'quotes': quotes,
            'timestamp': datetime.now().isoformat(),
            'market_status': data_collector.get_market_status()
        })
    except Exception as e:
        logger.error(f"Multiple live quotes error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/risk-analysis', methods=['POST'])
def risk_analysis():
    """Comprehensive risk analysis endpoint"""
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        weights = data.get('weights', [])
        confidence_level = data.get('confidence_level', 0.95)
        time_horizon = data.get('time_horizon', 1)
        
        # Validate inputs
        if not symbols or not weights or len(symbols) != len(weights):
            return jsonify({
                'success': False,
                'error': 'Invalid symbols or weights'
            }), 400
        
        # Run risk analysis
        risk_metrics = risk_calculator.calculate_portfolio_risk(
            symbols, weights, confidence_level, time_horizon
        )
        
        # Run Monte Carlo simulation
        monte_carlo_results = monte_carlo.run_simulation(
            symbols, weights, num_simulations=10000, time_horizon=time_horizon
        )
        
        # Run ML predictions
        ml_predictions = ml_predictor.predict_risk(symbols, time_horizon)
        
        return jsonify({
            'success': True,
            'risk_metrics': risk_metrics,
            'monte_carlo': monte_carlo_results,
            'ml_predictions': ml_predictions,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Risk analysis error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/portfolio-optimization', methods=['POST'])
def portfolio_optimization():
    """Portfolio optimization endpoint"""
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        method = data.get('method', 'max_sharpe')
        
        if not symbols:
            return jsonify({
                'success': False,
                'error': 'No symbols provided'
            }), 400
        
        # Run portfolio optimization
        optimization_result = portfolio_manager.optimize_portfolio(symbols, method)
        
        return jsonify({
            'success': True,
            **optimization_result,
            'method': method,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Portfolio optimization error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stress-test', methods=['POST'])
def stress_test():
    """Stress testing endpoint"""
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        weights = data.get('weights', [])
        scenarios = data.get('scenarios', ['market_crash', 'high_volatility', 'recession'])
        
        if not symbols or not weights:
            return jsonify({
                'success': False,
                'error': 'Symbols and weights required'
            }), 400
        
        # Run stress tests for each scenario
        stress_results = {}
        for scenario in scenarios:
            # Simulate stress scenario by modifying risk parameters
            if scenario == 'market_crash':
                # -20% market shock with doubled volatility
                stressed_risk = risk_calculator.calculate_portfolio_risk(
                    symbols, weights, confidence_level=0.95, time_horizon=1
                )
                # Apply stress multipliers
                stressed_risk['var_metrics']['historical_var'] *= 2.0
                stressed_risk['var_metrics']['parametric_var'] *= 2.0
                stressed_risk['portfolio_metrics']['volatility'] *= 2.0
                stressed_risk['portfolio_metrics']['max_drawdown'] *= 1.5
                
            elif scenario == 'high_volatility':
                # 3x volatility increase
                stressed_risk = risk_calculator.calculate_portfolio_risk(
                    symbols, weights, confidence_level=0.95, time_horizon=1
                )
                stressed_risk['var_metrics']['historical_var'] *= 1.5
                stressed_risk['var_metrics']['parametric_var'] *= 1.5
                stressed_risk['portfolio_metrics']['volatility'] *= 3.0
                
            elif scenario == 'recession':
                # -15% market shock with moderate volatility increase
                stressed_risk = risk_calculator.calculate_portfolio_risk(
                    symbols, weights, confidence_level=0.95, time_horizon=1
                )
                stressed_risk['var_metrics']['historical_var'] *= 1.7
                stressed_risk['var_metrics']['parametric_var'] *= 1.7
                stressed_risk['portfolio_metrics']['volatility'] *= 1.8
                stressed_risk['portfolio_metrics']['max_drawdown'] *= 1.3
            
            stress_results[scenario] = {
                'var_95': stressed_risk['var_metrics']['historical_var'],
                'var_99': stressed_risk['var_metrics']['historical_var'] * 1.3,
                'volatility': stressed_risk['portfolio_metrics']['volatility'],
                'max_drawdown': stressed_risk['portfolio_metrics']['max_drawdown']
            }
        
        return jsonify({
            'success': True,
            'stress_results': stress_results,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Stress test error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/symbols/available')
def get_symbols_available():
    """Get available symbols organized by category"""
    try:
        # Popular symbols by category
        symbols = {
            'Technology': {
                'AAPL': 'Apple Inc.',
                'MSFT': 'Microsoft Corporation',
                'GOOGL': 'Alphabet Inc.',
                'AMZN': 'Amazon.com Inc.',
                'TSLA': 'Tesla Inc.',
                'NVDA': 'NVIDIA Corporation',
                'META': 'Meta Platforms Inc.',
                'NFLX': 'Netflix Inc.'
            },
            'Finance': {
                'JPM': 'JPMorgan Chase & Co.',
                'BAC': 'Bank of America Corp.',
                'WFC': 'Wells Fargo & Company',
                'GS': 'The Goldman Sachs Group Inc.',
                'MS': 'Morgan Stanley',
                'C': 'Citigroup Inc.'
            },
            'Healthcare': {
                'JNJ': 'Johnson & Johnson',
                'PFE': 'Pfizer Inc.',
                'UNH': 'UnitedHealth Group Inc.',
                'ABBV': 'AbbVie Inc.',
                'MRK': 'Merck & Co. Inc.'
            },
            'Energy': {
                'XOM': 'Exxon Mobil Corporation',
                'CVX': 'Chevron Corporation',
                'COP': 'ConocoPhillips',
                'SLB': 'Schlumberger Limited'
            },
            'Consumer': {
                'WMT': 'Walmart Inc.',
                'HD': 'The Home Depot Inc.',
                'MCD': 'McDonald\'s Corporation',
                'NKE': 'NIKE Inc.',
                'SBUX': 'Starbucks Corporation'
            },
            'Cryptocurrency': {
                'BTC/USD': 'Bitcoin',
                'ETH/USD': 'Ethereum',
                'BNB/USD': 'Binance Coin',
                'ADA/USD': 'Cardano',
                'SOL/USD': 'Solana'
            },
            'ETFs': {
                'SPY': 'SPDR S&P 500 ETF',
                'QQQ': 'Invesco QQQ Trust',
                'IWM': 'iShares Russell 2000 ETF',
                'VTI': 'Vanguard Total Stock Market ETF'
            }
        }
        
        return jsonify({
            'success': True,
            'symbols': symbols,
            'total_count': sum(len(cat) for cat in symbols.values())
        })
        
    except Exception as e:
        logger.error(f"Error getting available symbols: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/symbols/popular')
def get_popular_symbols():
    """Get popular symbols for quick selection"""
    try:
        popular = [
            {'symbol': 'AAPL', 'name': 'Apple Inc.', 'category': 'Technology'},
            {'symbol': 'MSFT', 'name': 'Microsoft Corporation', 'category': 'Technology'},
            {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'category': 'Technology'},
            {'symbol': 'AMZN', 'name': 'Amazon.com Inc.', 'category': 'Technology'},
            {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'category': 'Technology'},
            {'symbol': 'NVDA', 'name': 'NVIDIA Corporation', 'category': 'Technology'},
            {'symbol': 'JPM', 'name': 'JPMorgan Chase & Co.', 'category': 'Finance'},
            {'symbol': 'JNJ', 'name': 'Johnson & Johnson', 'category': 'Healthcare'},
            {'symbol': 'SPY', 'name': 'SPDR S&P 500 ETF', 'category': 'ETFs'},
            {'symbol': 'BTC/USD', 'name': 'Bitcoin', 'category': 'Cryptocurrency'}
        ]
        
        limit = int(request.args.get('limit', 10))
        
        return jsonify({
            'success': True,
            'symbols': popular[:limit]
        })
        
    except Exception as e:
        logger.error(f"Error getting popular symbols: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/symbols/search')
def search_symbols():
    """Search for symbols by name or symbol"""
    try:
        query = request.args.get('q', '').upper().strip()
        
        if len(query) < 2:
            return jsonify({
                'success': True,
                'results': {}
            })
        
        # Simple search implementation
        all_symbols = {
            'AAPL': 'Apple Inc. (Technology)',
            'MSFT': 'Microsoft Corporation (Technology)',
            'GOOGL': 'Alphabet Inc. (Technology)',
            'AMZN': 'Amazon.com Inc. (Technology)',
            'TSLA': 'Tesla Inc. (Technology)',
            'NVDA': 'NVIDIA Corporation (Technology)',
            'META': 'Meta Platforms Inc. (Technology)',
            'NFLX': 'Netflix Inc. (Technology)',
            'JPM': 'JPMorgan Chase & Co. (Finance)',
            'BAC': 'Bank of America Corp. (Finance)',
            'JNJ': 'Johnson & Johnson (Healthcare)',
            'PFE': 'Pfizer Inc. (Healthcare)',
            'XOM': 'Exxon Mobil Corporation (Energy)',
            'WMT': 'Walmart Inc. (Consumer)',
            'SPY': 'SPDR S&P 500 ETF (ETFs)',
            'QQQ': 'Invesco QQQ Trust (ETFs)',
            'BTC/USD': 'Bitcoin (Cryptocurrency)',
            'ETH/USD': 'Ethereum (Cryptocurrency)'
        }
        
        results = {}
        for symbol, name in all_symbols.items():
            if query in symbol or query in name.upper():
                results[symbol] = name
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Error searching symbols: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/system-status')
def system_status():
    """Get system status and health check"""
    try:
        status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'components': {
                'data_collector': 'operational',
                'ml_predictor': 'operational',
                'risk_calculator': 'operational',
                'portfolio_manager': 'operational',
                'monte_carlo': 'operational'
            },
            'api_status': {
                'alpaca': 'checking...',
                'yfinance': 'operational',
                'cache': 'operational'
            }
        }
        
        # Check API connections
        try:
            account_info = data_collector.get_account_info()
            status['api_status']['alpaca'] = 'operational' if not account_info.get('error') else 'degraded'
        except:
            status['api_status']['alpaca'] = 'degraded'
        
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Resource not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'status': 'error', 
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs('logs', exist_ok=True)
    os.makedirs('data/cache', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    logger.info("Starting Enhanced Financial Risk Prediction System")
    logger.info("Global Markets Supported: US, NGN, UK, CA, AU, JP, DE, CRYPTO")
    
    # Run the application
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True
    ) 