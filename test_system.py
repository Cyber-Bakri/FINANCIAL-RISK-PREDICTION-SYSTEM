#!/usr/bin/env python3
"""
System Validation Script for Enhanced Financial Risk Prediction System
Comprehensive testing suite to validate all system components

Author: Abubakri Olayide Abdul-Lateef
Project: B.Sc. Computer Science Final Year Project
Supervisor: Dr. (Mrs) A.O AMOO
"""

import sys
import os
import time
import json
import requests
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported successfully"""
    print("🔍 Testing module imports...")
    
    try:
        from src.data_collector import SimpleDataCollector
        from src.risk_calculator import SimpleRiskCalculator
        from src.monte_carlo import SimpleMonteCarlo
        from src.ml_predictor import SimpleMLPredictor
        from src.portfolio_manager import SimplePortfolioManager
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_collector():
    """Test data collection functionality"""
    print("\n📊 Testing data collection...")
    
    try:
        from src.simple_data_collector import SimpleDataCollector
        collector = SimpleDataCollector()
        
        # Test with a simple stock symbol
        data = collector.get_historical_data('AAPL', 30)
        
        if data and 'data' in data and len(data['data']) > 0:
            print(f"✅ Successfully retrieved {len(data['data'])} data points for AAPL")
            print(f"   Data source: {data['metadata']['source']}")
            return True
        else:
            print("❌ No data received")
            return False
            
    except Exception as e:
        print(f"❌ Data collection error: {e}")
        return False

def test_risk_calculator():
    """Test risk calculation functionality"""
    print("\n⚠️ Testing risk calculations...")
    
    try:
        from src.simple_risk_calculator import SimpleRiskCalculator
        risk_calc = SimpleRiskCalculator()
        
        # Test with simple portfolio
        symbols = ['AAPL', 'MSFT']
        weights = [0.5, 0.5]
        
        risk_metrics = risk_calc.calculate_portfolio_risk(symbols, weights)
        
        if risk_metrics and 'var_metrics' in risk_metrics:
            var = risk_metrics['var_metrics']['historical_var']
            print(f"✅ Risk calculation successful. Historical VaR: {var:.4f}")
            return True
        else:
            print("❌ Risk calculation failed")
            return False
            
    except Exception as e:
        print(f"❌ Risk calculation error: {e}")
        return False

def test_monte_carlo():
    """Test Monte Carlo simulation"""
    print("\n🎲 Testing Monte Carlo simulation...")
    
    try:
        from src.simple_monte_carlo import SimpleMonteCarlo
        mc_sim = SimpleMonteCarlo()
        
        symbols = ['AAPL', 'MSFT']
        weights = [0.5, 0.5]
        
        results = mc_sim.run_simulation(symbols, weights, num_simulations=1000)
        
        if results and 'simulation_results' in results:
            num_sims = len(results['simulation_results']['portfolio_returns'])
            var_95 = results['risk_metrics']['var_95']
            print(f"✅ Monte Carlo simulation successful. Simulations: {num_sims}, VaR 95%: {var_95:.4f}")
            return True
        else:
            print("❌ Monte Carlo simulation failed")
            return False
            
    except Exception as e:
        print(f"❌ Monte Carlo simulation error: {e}")
        return False

def test_ml_predictor():
    """Test ML prediction functionality"""
    print("\n🤖 Testing ML predictions...")
    
    try:
        from src.simple_ml_predictor import SimpleMLPredictor
        ml_pred = SimpleMLPredictor()
        
        symbols = ['AAPL']
        predictions = ml_pred.predict_risk(symbols)
        
        if predictions and 'predictions' in predictions:
            pred = predictions['predictions']['AAPL']
            print(f"✅ ML prediction successful. Predicted volatility: {pred['predicted_volatility']:.4f}")
            return True
        else:
            print("❌ ML prediction failed")
            return False
            
    except Exception as e:
        print(f"❌ ML prediction error: {e}")
        return False

def test_portfolio_manager():
    """Test portfolio optimization"""
    print("\n📈 Testing portfolio optimization...")
    
    try:
        from src.simple_portfolio_manager import SimplePortfolioManager
        port_mgr = SimplePortfolioManager()
        
        symbols = ['AAPL', 'MSFT', 'GOOGL']
        result = port_mgr.optimize_portfolio(symbols, method='equal_weight')
        
        if result and 'optimized_weights' in result:
            weights = result['optimized_weights']
            total_weight = sum(weights.values())
            print(f"✅ Portfolio optimization successful. Total weight: {total_weight:.3f}")
            return True
        else:
            print("❌ Portfolio optimization failed")
            return False
            
    except Exception as e:
        print(f"❌ Portfolio optimization error: {e}")
        return False

def test_api_endpoints():
    """Test Flask API endpoints"""
    print("\n🌐 Testing API endpoints...")
    
    base_url = "http://localhost:5000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API test failed - server may not be running: {e}")
        return False
    
    # Test risk analysis endpoint
    try:
        payload = {
            'symbols': ['AAPL', 'MSFT'],
            'weights': [0.5, 0.5],
            'confidence_level': 0.95,
            'time_horizon': 1
        }
        
        response = requests.post(f"{base_url}/api/risk-analysis", json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Risk analysis API working")
                return True
            else:
                print(f"❌ Risk analysis API error: {data.get('error')}")
                return False
        else:
            print(f"❌ Risk analysis API failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Risk analysis API test failed: {e}")
        return False

def run_comprehensive_test():
    """Run all tests and provide summary"""
    print("🚀 Starting Enhanced Financial Risk Prediction System Tests")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Data Collection", test_data_collector),
        ("Risk Calculation", test_risk_calculator),
        ("Monte Carlo Simulation", test_monte_carlo),
        ("ML Prediction", test_ml_predictor),
        ("Portfolio Management", test_portfolio_manager),
        ("API Endpoints", test_api_endpoints)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! The system is ready for use.")
    else:
        print(f"\n⚠️ {total-passed} test(s) failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1) 