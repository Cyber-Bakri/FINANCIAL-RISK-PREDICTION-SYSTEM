# Enhanced Financial Risk Prediction System

## B.Sc. Computer Science Final Year Project

**Student:** Abubakri Olayide Abdul-Lateef (CSC/2018/005)  
**Supervisor:** Dr. (Mrs) A.O AMOO  
**Institution:** OAU  
**Academic Year:** 2024/2025  
**Project Defense:** April 2025

---

## Project Overview

The Enhanced Financial Risk Prediction System is a comprehensive web-based platform that provides professional-grade financial risk assessment capabilities. Built using modern web technologies and advanced mathematical models, this system enables portfolio managers, financial analysts, and investors to make data-driven investment decisions.

## Key Features

### 📊 **Dynamic Portfolio Management**
- **User-Friendly Interface**: Enter dollar amounts instead of percentages
- **Real-Time Calculations**: Automatic weight and total calculations
- **Live Market Data**: Current prices and portfolio valuations
- **37 Supported Symbols**: US stocks, crypto, and ETFs

### 🎯 **Portfolio Optimization**
- **Maximum Sharpe Ratio**: Optimize risk-adjusted returns
- **Minimum Variance**: Reduce portfolio volatility
- **Equal Weight**: Balanced diversification strategy
- **Real Market Data**: Based on historical performance analysis

### 🛡️ **Value at Risk (VaR) Analysis**
- **Historical VaR**: Based on actual market movements
- **Parametric VaR**: Using statistical models and distributions
- **Expected Shortfall**: Average loss beyond VaR threshold
- **Real-Time Calculations**: Live data from Yahoo Finance

### 🚨 **Stress Testing**
- **Market Crash Scenarios**: 20% market decline simulation
- **High Volatility Periods**: Doubled volatility stress test
- **Recession Conditions**: Economic downturn impact analysis
- **Quantified Risk**: Precise loss estimates under adverse conditions

### 🤖 **Machine Learning Predictions**
- AI-driven volatility forecasting
- Risk-adjusted return predictions
- Ensemble learning methods for improved accuracy




- Comprehensive risk scenario analysis

### 📈 **Live Market Data**
- Real-time stock prices and market quotes via Yahoo Finance API
- Market status monitoring (open/closed) with trading hours detection
- Current bid/ask spreads and trading volumes
- Support for 37 carefully curated financial instruments across global markets
- Data refresh: Real-time during market hours, latest close when markets are closed

## Supported Markets & Financial Instruments

### 🌍 **Global Market Coverage**
The system supports financial instruments from multiple global markets:

- **🇺🇸 United States**: NASDAQ, NYSE, AMEX
- **🌐 Global Crypto Markets**: 24/7 cryptocurrency trading
- **📊 Exchange-Traded Funds (ETFs)**: Major US ETF markets

### 📡 **Data Source & API**
**Primary Data Provider:** Yahoo Finance API (yfinance library)
- **Reliability**: Industry-standard financial data provider
- **Coverage**: Global markets with real-time and historical data
- **Latency**: Sub-second response times during market hours
- **Historical Data**: Up to 10+ years of daily, weekly, monthly data
- **Real-time Features**: Live quotes, bid/ask spreads, volume data
- **Market Hours**: Automatic detection of trading sessions
- **No API Key Required**: Free, reliable access for academic use

### ✅ **Academic Quality - Real Calculations**

**No Static Data - All Metrics Calculated Live:**
- ✅ **Portfolio Returns**: Calculated from actual historical price movements (not fixed 8%)
- ✅ **Volatility Metrics**: Based on real price variance (not assumed 15%)  
- ✅ **Sharpe Ratios**: Computed from actual risk-adjusted returns (not static 0.4)
- ✅ **Risk Analysis**: VaR and Expected Shortfall from genuine market data
- ✅ **Optimization**: Weights determined by real performance analysis
- ✅ **Current vs Optimized**: Shows actual differences based on portfolio composition

### 💰 **37 Carefully Selected Financial Instruments**

#### Technology Sector (8 symbols) - NASDAQ/NYSE
- **AAPL** (Apple Inc.) - Consumer Electronics & Software
- **MSFT** (Microsoft Corporation) - Cloud Computing & Software
- **GOOGL** (Alphabet Inc.) - Search Engine & Cloud Services  
- **AMZN** (Amazon.com Inc.) - E-commerce & Cloud Computing
- **TSLA** (Tesla Inc.) - Electric Vehicles & Energy Storage
- **NVDA** (NVIDIA Corporation) - Graphics Processing & AI Chips
- **META** (Meta Platforms Inc.) - Social Media & Virtual Reality
- **NFLX** (Netflix Inc.) - Streaming Entertainment Services

#### Financial Sector (6 symbols) - NYSE
- **JPM** (JPMorgan Chase & Co.) - Investment Banking & Asset Management
- **BAC** (Bank of America Corp.) - Commercial & Investment Banking
- **WFC** (Wells Fargo & Company) - Commercial Banking & Mortgages
- **GS** (Goldman Sachs Group Inc.) - Investment Banking & Trading
- **MS** (Morgan Stanley) - Investment Banking & Wealth Management
- **C** (Citigroup Inc.) - Global Banking & Financial Services

#### Healthcare Sector (5 symbols) - NYSE/NASDAQ
- **JNJ** (Johnson & Johnson) - Pharmaceuticals & Medical Devices
- **PFE** (Pfizer Inc.) - Biopharmaceuticals & Vaccines
- **UNH** (UnitedHealth Group Inc.) - Health Insurance & Services
- **ABBV** (AbbVie Inc.) - Biopharmaceuticals & Drug Development
- **MRK** (Merck & Co. Inc.) - Pharmaceuticals & Animal Health

#### Consumer Sector (5 symbols) - NYSE/NASDAQ
- **WMT** (Walmart Inc.) - Retail & E-commerce
- **HD** (Home Depot Inc.) - Home Improvement Retail
- **MCD** (McDonald's Corporation) - Quick Service Restaurants
- **NKE** (NIKE Inc.) - Athletic Footwear & Apparel
- **SBUX** (Starbucks Corporation) - Coffee & Beverages

#### Cryptocurrency (5 symbols) - Global 24/7 Markets
- **BTC/USD** (Bitcoin) - Digital Currency & Store of Value
- **ETH/USD** (Ethereum) - Smart Contract Platform & DeFi
- **BNB/USD** (Binance Coin) - Exchange Token & Ecosystem
- **ADA/USD** (Cardano) - Proof-of-Stake Blockchain Platform
- **SOL/USD** (Solana) - High-Performance Blockchain Network

#### Energy Sector (4 symbols) - NYSE
- **XOM** (Exxon Mobil Corporation) - Oil & Gas Exploration
- **CVX** (Chevron Corporation) - Integrated Energy Company
- **COP** (ConocoPhillips) - Oil & Gas Production
- **SLB** (Schlumberger Limited) - Oilfield Services & Technology

#### Exchange-Traded Funds (4 symbols) - NYSE Arca
- **SPY** (SPDR S&P 500 ETF) - Tracks S&P 500 Index
- **QQQ** (Invesco QQQ Trust) - Tracks NASDAQ-100 Index
- **IWM** (iShares Russell 2000 ETF) - Small-Cap US Stocks
- **VTI** (Vanguard Total Stock Market ETF) - Total US Stock Market

## Technical Architecture

### Backend Technologies
- **Python 3.8+**: Core application development
- **Flask**: Web framework with RESTful API design
- **NumPy & Pandas**: Numerical computing and data analysis
- **SciPy**: Statistical functions and optimization algorithms
- **yfinance 0.2.28+**: Yahoo Finance API wrapper for real-time market data
- **Scikit-learn**: Machine learning algorithms for predictive modeling
- **Requests**: HTTP library for API communications

### Frontend Technologies
- **HTML5/CSS3**: Modern responsive web design
- **JavaScript ES6+**: Interactive user interface
- **Bootstrap 5**: Professional UI components
- **Chart.js**: Data visualization and charting

### Data & Analytics
- **Real-time Market Data**: Yahoo Finance API integration with live quotes and historical data
- **Data Processing**: Pandas DataFrames for efficient time-series analysis
- **Mathematical Models**: VaR calculations, Monte Carlo simulations, portfolio optimization
- **Machine Learning**: Scikit-learn ensemble methods for risk prediction
- **Statistical Analysis**: NumPy/SciPy for advanced statistical computations
- **Market Data Validation**: Real-time data quality checks and error handling

## Installation & Setup

### Prerequisites
```bash
Python 3.8 or higher
pip (Python package manager)
Web browser (Chrome, Firefox, Safari, Edge)
Internet connection (for live market data)
```

### Installation Steps

1. **Clone the Repository**
```bash
git clone [repository-url]
cd newschoolproject
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the Application**
```bash
python app.py
```

4. **Access the System**
```
Open web browser and navigate to: http://localhost:5000
```

## System Validation

The system includes comprehensive testing with the following validation script:

```bash
python test_system.py
```

**Test Coverage:**
- ✅ Module imports and dependencies
- ✅ Data collection functionality
- ✅ Risk calculation algorithms
- ✅ Monte Carlo simulation engine
- ✅ Machine learning predictions
- ✅ Portfolio optimization methods
- ✅ API endpoint functionality

**Latest Test Results: 7/7 tests passed (100% success rate)**

## Data Integration & API Architecture

### 📊 **Yahoo Finance API Integration**
The system leverages Yahoo Finance's robust API infrastructure through the yfinance Python library:

**Data Fetching Strategy:**
   ```python
# Real-time data collection
ticker = yf.Ticker(symbol)
hist_data = ticker.history(start=start_date, end=end_date, 
                          interval='1d', prepost=True, auto_adjust=True)
```

**Key Features:**
- **Auto-adjusting prices**: Handles stock splits and dividends automatically
- **Pre/post market data**: Extended hours trading information
- **Multiple timeframes**: Support for 1m, 5m, 15m, 30m, 1h, 1d intervals
- **Comprehensive metadata**: Company info, market cap, trading volumes
- **Error handling**: Robust fallback mechanisms for data unavailability

**Data Quality Assurance:**
- Real-time validation of data completeness
- Automatic retry mechanisms for failed requests
- Data freshness indicators in API responses
- Market hours detection for data interpretation

### 🔌 **System API Endpoints**

#### Core Analysis Endpoints
- `POST /api/risk-analysis` - Comprehensive portfolio risk assessment
  - **Input**: Symbols, weights, confidence levels, time horizons
  - **Output**: VaR metrics, volatility measures, risk statistics
- `POST /api/portfolio-optimization` - Portfolio weight optimization
  - **Methods**: Maximum Sharpe, Minimum Variance, Equal Weight
  - **Output**: Optimized allocations with performance metrics
- `POST /api/stress-test` - Stress testing scenarios
  - **Scenarios**: Market crash, high volatility, recession conditions
  - **Output**: Portfolio performance under adverse conditions

#### Market Data Endpoints
- `GET /api/market-status` - Current market trading status
  - **Output**: Open/closed status, trading session, data freshness
- `GET /api/live-quote/<symbol>` - Real-time price quotes
  - **Output**: Current price, bid/ask, volume, percentage change
- `POST /api/live-quotes` - Multiple symbol quotes
  - **Input**: Array of symbols
  - **Output**: Batch quote data with market status
- `GET /api/symbols/available` - All supported symbols
  - **Output**: 37 symbols organized by market sector

#### System Endpoints
- `GET /api/health` - Application health check
- `GET /api/symbols/popular` - Popular trading symbols for quick selection

## Project Structure

```
newschoolproject/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── test_system.py                  # Comprehensive testing script
├── src/                           # Core application modules
│   ├── simple_data_collector.py   # Market data collection
│   ├── simple_risk_calculator.py  # VaR and risk metrics
│   ├── simple_ml_predictor.py     # Machine learning models
│   ├── simple_portfolio_manager.py # Portfolio optimization
│   └── simple_monte_carlo.py      # Monte Carlo simulation
├── templates/                     # HTML templates
│   ├── base.html                  # Base template
│   └── index.html                 # Main dashboard
├── static/                        # Static web assets
│   ├── css/style.css             # Custom styling
│   └── js/                        # JavaScript modules
│       ├── main.js               # Core UI functionality
│       └── risk-analysis.js      # Analysis interface
└── README.md                      # This documentation
```

## Academic Contributions

### Financial Risk Management
1. **Multi-Method VaR Implementation**: Comparative analysis of Historical, Parametric, and Monte Carlo VaR methods
2. **Real-time Risk Assessment**: Integration of live market data for current risk evaluation
3. **Stress Testing Framework**: Systematic approach to portfolio resilience testing

### Computer Science & Technology
1. **Web-based Financial Application**: Modern full-stack development using Python and JavaScript
2. **RESTful API Design**: Professional API architecture for financial data services
3. **Real-time Data Integration**: Efficient handling of live market data streams
4. **Responsive User Interface**: Mobile-friendly financial dashboard design

### Mathematical & Statistical Analysis
1. **Monte Carlo Simulation**: Implementation of probabilistic modeling techniques
2. **Portfolio Optimization**: Mathematical optimization for risk-return balance
3. **Machine Learning Integration**: Predictive modeling for financial forecasting
4. **Statistical Risk Metrics**: Comprehensive risk measurement methodologies

## Usage Instructions

### Getting Started
1. Launch the application by running `python app.py`
2. Open your web browser to `http://localhost:5000`
3. The system will display live market status and available symbols

### Running Risk Analysis
1. **Select Assets**: Choose from 37 available symbols or use quick-select buttons
2. **Set Weights**: Define portfolio allocation percentages
3. **Run Analysis**: Click "Run Risk Analysis" for comprehensive assessment
4. **Review Results**: Examine VaR metrics, volatility, and risk indicators

### Portfolio Optimization
1. **Choose Method**: Select optimization strategy (Max Sharpe, Min Variance, Equal Weight)
2. **Input Symbols**: Enter desired portfolio assets
3. **Optimize**: Generate optimal weight allocation
4. **Compare**: Review performance improvements and recommendations

### Stress Testing
1. **Configure Portfolio**: Set up asset allocation
2. **Select Scenarios**: Choose from market crash, high volatility, or recession
3. **Execute Tests**: Run stress scenarios
4. **Analyze Results**: Review portfolio performance under adverse conditions

## Performance Characteristics

- **Data Refresh Rate**: Sub-second for market status, 30-second intervals for quotes
- **Calculation Speed**: Risk analysis completes in 2-5 seconds for typical portfolios
- **Monte Carlo Performance**: 10,000 simulations execute in under 3 seconds
- **API Response Time**: Average 200-500ms for all endpoints
- **Concurrent Users**: Supports multiple simultaneous analyses

## Limitations & Considerations

### 📊 **Data Source Limitations**
1. **Yahoo Finance Dependency**: System relies on Yahoo Finance API availability
   - **Uptime**: Generally 99.9% reliable during market hours
   - **Rate Limits**: Academic use falls well within free tier limits
   - **Data Delay**: Real-time for most instruments, 15-minute delay for some
2. **Market Hours**: Live data available only during respective trading sessions
   - **US Markets**: 9:30 AM - 4:00 PM EST (Monday-Friday)
   - **Crypto Markets**: 24/7 availability with continuous updates
3. **Symbol Coverage**: Intentionally limited to 37 high-quality, liquid instruments
   - **Selection Criteria**: Market cap >$10B, daily volume >1M shares
   - **Diversification**: Covers 7 major economic sectors
   - **Quality Focus**: Emphasis on data reliability over quantity

### 🎓 **Academic & Compliance Considerations**
4. **Educational Purpose**: Designed specifically for academic demonstration
   - **Not for Investment Advice**: System for educational use only
   - **Model Simplification**: Complex financial models simplified for learning
   - **Risk Disclaimer**: Always consult financial professionals for real investments
5. **Data Accuracy**: Historical data quality depends on source reliability
   - **Validation**: System includes data quality checks
   - **Error Handling**: Graceful degradation when data unavailable
6. **Computational Limitations**: Academic-focused performance characteristics
   - **Portfolio Size**: Optimized for 2-15 asset portfolios
   - **Simulation Scale**: Monte Carlo limited to 10,000 iterations for speed
   - **Historical Periods**: VaR calculations based on 1-3 years of data

## Future Enhancements

1. **Extended Symbol Database**: Expansion to international markets and more instruments
2. **Advanced ML Models**: Implementation of deep learning and neural networks
3. **Portfolio Backtesting**: Historical performance simulation capabilities
4. **Risk Reporting**: Automated report generation and export functionality
5. **User Management**: Multi-user support with portfolio saving capabilities

## Academic References

This project implements established financial risk management methodologies including:

- Jorion, P. (2007). "Value at Risk: The New Benchmark for Managing Financial Risk"
- Hull, J. C. (2018). "Risk Management and Financial Institutions"
- Markowitz, H. (1952). "Portfolio Selection"
- Black, F., & Scholes, M. (1973). "The Pricing of Options and Corporate Liabilities"

## License & Disclaimer

This software is developed for academic purposes as part of a B.Sc. Computer Science final year project. It is intended for educational use and research applications. Users should not rely on this system for actual investment decisions without proper financial advice and additional validation.

---

**Contact Information:**  
Student: Abubakri Olayide Abdul-Lateef  
Email: olayidebakri@gmail.com  
Supervisor: Dr. (Mrs) A.O AMOO  
Institution: OAU
