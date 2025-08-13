"""
Simple Data Collector for Financial Risk Prediction System
Focused on core functionality for academic presentation
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional
import time

logger = logging.getLogger(__name__)

class SimpleDataCollector:
    """Simple data collector using yfinance for reliable data access"""
    
    def __init__(self):
        """Initialize the simple data collector"""
        logger.info("Initializing Simple Data Collector")
        
    def get_historical_data(self, symbol: str, days: int = 252, 
                          timeframe: str = '1d', market: str = None) -> Dict:
        """
        Get historical data for a symbol using yfinance
        
        Args:
            symbol: Asset symbol (e.g., 'AAPL', 'BTC-USD')
            days: Number of days of historical data
            timeframe: Data timeframe (default '1d')
            market: Market identifier (optional)
            
        Returns:
            Dictionary containing historical data and metadata
        """
        try:
            # Convert crypto symbols to yfinance format
            if '/' in symbol:
                symbol = symbol.replace('/', '-')
            
            # Calculate start date - get extra days to ensure we have enough data
            start_date = datetime.now() - timedelta(days=days + 30)
            
            # Fetch data using yfinance with real-time updates
            ticker = yf.Ticker(symbol)
            hist_data = ticker.history(start=start_date, end=datetime.now(), 
                                     interval=timeframe, prepost=True, auto_adjust=True)
            
            if hist_data.empty:
                logger.warning(f"No data found for symbol {symbol}")
                return {
                    'data': [],
                    'metadata': {
                        'symbol': symbol,
                        'source': 'yfinance',
                        'error': f'No data found for {symbol}'
                    }
                }
            
            # Convert to list of dictionaries
            data_list = []
            for date, row in hist_data.iterrows():
                data_list.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': float(row['Open']),
                    'high': float(row['High']),
                    'low': float(row['Low']),
                    'close': float(row['Close']),
                    'volume': int(row['Volume']) if pd.notna(row['Volume']) else 0
                })
            
            logger.info(f"Successfully fetched {len(data_list)} data points for {symbol}")
            
            return {
                'data': data_list,
                'metadata': {
                    'symbol': symbol,
                    'source': 'yfinance',
                    'days_requested': days,
                    'days_received': len(data_list),
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'end_date': datetime.now().strftime('%Y-%m-%d')
                }
            }
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return {
                'data': [],
                'metadata': {
                    'symbol': symbol,
                    'source': 'yfinance',
                    'error': str(e)
                }
            }
    
    def get_multiple_symbols(self, symbols: List[str], days: int = 252) -> Dict:
        """
        Get historical data for multiple symbols
        
        Args:
            symbols: List of asset symbols
            days: Number of days of historical data
            
        Returns:
            Dictionary with symbol data
        """
        try:
            results = {}
            
            for symbol in symbols:
                data = self.get_historical_data(symbol, days)
                results[symbol] = data
                
                # Small delay to avoid rate limiting
                time.sleep(0.1)
            
            return results
                    
        except Exception as e:
            logger.error(f"Error fetching multiple symbols: {str(e)}")
            return {}
    
    def get_account_info(self) -> Dict:
        """
        Get account information (simplified for demo)
        """
        return {
            'status': 'demo_mode',
            'message': 'Using yfinance for data - no API key required'
        }
    
    def get_current_price(self, symbol: str) -> Optional[float]:
        """
        Get current price for a symbol
        
        Args:
            symbol: Asset symbol
            
        Returns:
            Current price or None if failed
        """
        try:
            # Convert crypto symbols to yfinance format
            if '/' in symbol:
                symbol = symbol.replace('/', '-')
                
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Try different price fields
            price = (info.get('currentPrice') or 
                    info.get('regularMarketPrice') or 
                    info.get('previousClose'))
            
            return float(price) if price else None
            
        except Exception as e:
            logger.error(f"Error getting current price for {symbol}: {str(e)}")
            return None
    
    def get_market_status(self) -> Dict:
        """
        Get current market status and trading hours
        """
        try:
            import yfinance as yf
            from datetime import datetime, timezone
            
            # Use SPY as a proxy for US market status
            spy = yf.Ticker("SPY")
            info = spy.info
            
            current_time = datetime.now()
            
            # Simple market hours check (9:30 AM - 4:00 PM ET on weekdays)
            is_weekday = current_time.weekday() < 5  # Monday = 0, Sunday = 6
            current_hour = current_time.hour
            
            # Approximate market hours check
            market_open = is_weekday and 9 <= current_hour < 16
                
            return {
                'is_market_open': market_open,
                'current_time': current_time.isoformat(),
                'market_session': 'regular' if market_open else 'closed',
                'data_freshness': 'real-time' if market_open else 'last_close',
                'supported_symbols': ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA', 'SPY', 'BTC-USD', 'ETH-USD']
            }
                
        except Exception as e:
            logger.error(f"Error getting market status: {str(e)}")
            return {
                'is_market_open': False,
                'error': str(e),
                'current_time': datetime.now().isoformat(),
                'data_freshness': 'cached'
            }
    
    def get_live_quote(self, symbol: str) -> Dict:
        """
        Get live quote with bid/ask and real-time price
        """
        try:
            if '/' in symbol:
                symbol = symbol.replace('/', '-')
                
            ticker = yf.Ticker(symbol)
            
            # Get real-time quote
            info = ticker.info
            hist = ticker.history(period="1d", interval="1m")
            
            if not hist.empty:
                latest = hist.iloc[-1]
                previous_close = info.get('previousClose', latest['Close'])
                current_price = latest['Close']
                
                return {
                    'symbol': symbol,
                    'current_price': float(current_price),
                    'previous_close': float(previous_close),
                    'change': float(current_price - previous_close),
                    'change_percent': float((current_price - previous_close) / previous_close * 100),
                    'volume': int(latest['Volume']) if pd.notna(latest['Volume']) else 0,
                    'timestamp': latest.name.isoformat(),
                    'bid': info.get('bid', current_price),
                    'ask': info.get('ask', current_price),
                    'market_cap': info.get('marketCap', 'N/A'),
                    'data_source': 'yfinance_realtime'
                }
            else:
                return {
                    'symbol': symbol,
                    'error': 'No recent data available',
                    'data_source': 'yfinance_realtime'
                }
            
        except Exception as e:
            logger.error(f"Error getting live quote for {symbol}: {str(e)}")
            return {
                'symbol': symbol,
                'error': str(e),
                'data_source': 'yfinance_realtime'
            }
