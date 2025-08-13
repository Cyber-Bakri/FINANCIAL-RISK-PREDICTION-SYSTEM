/**
 * Risk Analysis JavaScript Module
 * Handles portfolio risk analysis, Monte Carlo simulation, and ML predictions
 */

// Global variables for caching results
let currentAnalysisData = null;
let currentPortfolioConfig = null;

// Helper function to get total portfolio value from dynamic system
function getTotalPortfolioValue() {
    const totalValueElement = document.getElementById('totalValue');
    if (totalValueElement) {
        // Extract numeric value from formatted string like "$100,000"
        const totalText = totalValueElement.textContent || totalValueElement.innerText || '$0';
        const numericValue = parseFloat(totalText.replace(/[$,]/g, ''));
        return isNaN(numericValue) ? 100000 : numericValue; // Default to 100k if parsing fails
    }
    return 100000; // Default fallback
}

// Helper function to get portfolio data from dynamic system
function getPortfolioData() {
    // Make sure portfolio data is up to date
    if (typeof updatePortfolioData === 'function') {
        updatePortfolioData();
    }
    
    // Get symbols and weights from hidden fields (updated by dynamic system)
    const symbolsInput = document.getElementById('symbols');
    const weightsInput = document.getElementById('weights');
    
    if (!symbolsInput || !weightsInput) {
        throw new Error('Portfolio input fields not found');
    }
    
    const symbols = symbolsInput.value.split(',').map(s => s.trim()).filter(s => s);
    const weights = weightsInput.value.split(',').map(w => parseFloat(w.trim())).filter(w => !isNaN(w));
    
    if (!symbols || symbols.length === 0) {
        throw new Error('Please add at least one asset to your portfolio');
    }
    
    if (symbols.length !== weights.length) {
        throw new Error('Number of symbols and weights must match');
    }
    
    return { symbols, weights };
}

/**
 * Main function to run comprehensive risk analysis
 */
async function runRiskAnalysis() {
    try {
        console.log('Starting risk analysis...');
        
        // Get portfolio data from dynamic system
        const { symbols, weights } = getPortfolioData();
        
        console.log('Portfolio data:', { symbols, weights });
        
        // Validate portfolio data
        if (!symbols || symbols.length === 0) {
            throw new Error('Please enter at least one asset symbol');
        }
        
        if (symbols.length !== weights.length) {
            throw new Error('Number of symbols must match number of weights');
        }
        
        const totalWeight = weights.reduce((sum, w) => sum + w, 0);
        if (Math.abs(totalWeight - 100) > 0.01) {
            throw new Error('Portfolio weights must sum to 100%');
        }
        
        // Prepare configuration for API
        currentPortfolioConfig = {
            symbols: symbols,
            weights: weights.map(w => w / 100), // Convert to decimals
            confidence_level: parseFloat(document.getElementById('confidenceLevel').value),
            time_horizon: parseInt(document.getElementById('timeHorizon').value),
            portfolio_value: getTotalPortfolioValue()
        };
        
        // Show loading indicator
        Utils.showLoading();
        
        // Run risk analysis
        const analysisData = await Utils.makeRequest('/risk-analysis', {
            method: 'POST',
            body: JSON.stringify(currentPortfolioConfig)
        });
        
        // Store results
        currentAnalysisData = analysisData;
        
        // Update UI with results
        updateRiskMetrics(analysisData);
        updatePortfolioMetrics(analysisData);
        updateCharts(analysisData);
        
        // Hide loading and show results
        Utils.hideLoading();
        Utils.showResults();
        
        Utils.showSuccess('Risk analysis completed successfully!');
        
    } catch (error) {
        Utils.hideLoading();
        Utils.showError('Risk analysis failed: ' + error.message);
        console.error('Risk analysis error:', error);
    }
}

/**
 * Update risk metrics display cards
 */
function updateRiskMetrics(data) {
    const riskMetrics = data.risk_metrics.var_metrics;
    const monteCarloMetrics = data.monte_carlo.risk_metrics;
    
    // Get first symbol for ML predictions (could be enhanced to show portfolio-level ML predictions)
    const firstSymbol = Object.keys(data.ml_predictions.predictions)[0];
    const mlPredictions = data.ml_predictions.predictions[firstSymbol] || {};
    
    // Update VaR displays
    document.getElementById('historicalVar').textContent = 
        Utils.formatPercentage(riskMetrics.historical_var);
    
    document.getElementById('parametricVar').textContent = 
        Utils.formatPercentage(riskMetrics.parametric_var);
    
    document.getElementById('monteCarloVar').textContent = 
        Utils.formatPercentage(monteCarloMetrics.var_95);
    
    document.getElementById('mlVar').textContent = 
        Utils.formatPercentage(mlPredictions.var_95 || 0);
}

/**
 * Update portfolio metrics display
 */
function updatePortfolioMetrics(data) {
    const portfolioMetrics = data.risk_metrics.portfolio_metrics;
    const monteCarloStats = data.monte_carlo.simulation_results.statistics;
    
    // Update metrics
    document.getElementById('portfolioVolatility').textContent = 
        Utils.formatPercentage(portfolioMetrics.volatility);
    
    document.getElementById('sharpeRatio').textContent = 
        portfolioMetrics.sharpe_ratio.toFixed(3);
    
    document.getElementById('maxDrawdown').textContent = 
        Utils.formatPercentage(Math.abs(portfolioMetrics.max_drawdown));
    
    document.getElementById('expectedShortfall').textContent = 
        Utils.formatPercentage(data.risk_metrics.var_metrics.expected_shortfall);
    
    document.getElementById('lossProbability').textContent = 
        Utils.formatPercentage(monteCarloStats.probability_of_loss);
    
    // Calculate average ML score across all symbols
    const mlPredictions = data.ml_predictions.predictions;
    const avgMlScore = Object.values(mlPredictions).reduce((sum, pred) => 
        sum + (pred.model_score || 0), 0) / Object.keys(mlPredictions).length;
    
    document.getElementById('mlScore').textContent = 
        (avgMlScore * 100).toFixed(1) + '%';
}

/**
 * Update all charts with new data
 */
function updateCharts(data) {
    ChartManager.updateMonteCarloChart(data.monte_carlo);
    ChartManager.updateRiskComparisonChart(data);
}

/**
 * Optimize portfolio using various methods
 */
async function optimizePortfolio() {
    try {
        console.log('Starting portfolio optimization...');
        
        // Get portfolio data from dynamic system
        const { symbols, weights } = getPortfolioData();
        
        if (!symbols || symbols.length === 0) {
            throw new Error('Please enter at least one asset for portfolio optimization');
        }
        
        Utils.showLoading();
        
        // Get selected optimization method
        const optimizationMethod = document.getElementById('optimizationMethod').value || 'max_sharpe';
        console.log('Using optimization method:', optimizationMethod);
        
        // Run portfolio optimization
        const optimizationData = await Utils.makeRequest('/portfolio-optimization', {
            method: 'POST',
            body: JSON.stringify({
                symbols: symbols,
                current_weights: weights.map(w => w / 100), // Convert percentages to decimals
                method: optimizationMethod
            })
        });
        
        Utils.hideLoading();
        
        // Update portfolio with optimized weights
        console.log('Optimization data received:', optimizationData);
        
        if (optimizationData.optimized_weights) {
            console.log('Optimized weights:', optimizationData.optimized_weights);
            
            if (typeof updatePortfolioWithOptimizedWeights === 'function') {
                console.log('Updating portfolio dynamically...');
                updatePortfolioWithOptimizedWeights(optimizationData.optimized_weights);
                Utils.showSuccess('Portfolio optimized! Investment amounts updated in the form.');
            } else {
                console.log('Dynamic update function not available, using fallback...');
                // Fallback: just update hidden weights field
                const weightsInput = document.getElementById('weights');
                if (weightsInput) {
                    const newWeights = symbols.map(symbol => {
                        const weight = optimizationData.optimized_weights[symbol];
                        return weight ? (weight * 100).toFixed(1) : '0';
                    });
                    weightsInput.value = newWeights.join(',');
                    Utils.showSuccess('Portfolio optimized! Weights updated.');
                }
            }
        } else {
            console.warn('No optimized weights received from API');
        }
        
        // Show optimization results with visual feedback
        showOptimizationResults(optimizationData);
        
        // Scroll to optimization results and add visual highlight
        const optimizationSection = document.getElementById('optimizationResults');
        if (optimizationSection) {
            optimizationSection.style.display = 'block';
            optimizationSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            
            // Add visual highlight
            optimizationSection.style.border = '2px solid #28a745';
            setTimeout(() => {
                optimizationSection.style.border = '';
            }, 3000);
        }
        
    } catch (error) {
        Utils.hideLoading();
        Utils.showError('Portfolio optimization failed: ' + error.message);
        console.error('Portfolio optimization error:', error);
    }
}

/**
 * Show portfolio optimization results with detailed recommendations
 */
function showOptimizationResults(data) {
    // Create optimization results modal or section
    let resultsHTML = `
        <div class="optimization-results mt-4">
            <div class="card border-success">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0"><i class="fas fa-chart-pie me-2"></i>Portfolio Optimization Results (${data.method.replace('_', ' ').toUpperCase()})</h5>
                </div>
                <div class="card-body">
                    <!-- Performance Comparison -->
                    <div class="row mb-4">
                        <div class="col-md-6">
                            <h6 class="text-muted">Current Portfolio</h6>
                            <div class="row">
                                <div class="col-4 text-center">
                                    <div class="metric-box">
                                        <div class="metric-value">${Utils.formatPercentage(data.current_portfolio_metrics.expected_return)}</div>
                                        <div class="metric-label">Expected Return</div>
                                    </div>
                                </div>
                                <div class="col-4 text-center">
                                    <div class="metric-box">
                                        <div class="metric-value">${Utils.formatPercentage(data.current_portfolio_metrics.volatility)}</div>
                                        <div class="metric-label">Volatility</div>
                                    </div>
                                </div>
                                <div class="col-4 text-center">
                                    <div class="metric-box">
                                        <div class="metric-value">${data.current_portfolio_metrics.sharpe_ratio.toFixed(3)}</div>
                                        <div class="metric-label">Sharpe Ratio</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <h6 class="text-success">Optimized Portfolio</h6>
                            <div class="row">
                                <div class="col-4 text-center">
                                    <div class="metric-box border-success">
                                        <div class="metric-value text-success">${Utils.formatPercentage(data.portfolio_metrics.expected_return)}</div>
                                        <div class="metric-label">Expected Return</div>
                                    </div>
                                </div>
                                <div class="col-4 text-center">
                                    <div class="metric-box border-success">
                                        <div class="metric-value text-success">${Utils.formatPercentage(data.portfolio_metrics.volatility)}</div>
                                        <div class="metric-label">Volatility</div>
                                    </div>
                                </div>
                                <div class="col-4 text-center">
                                    <div class="metric-box border-success">
                                        <div class="metric-value text-success">${data.portfolio_metrics.sharpe_ratio.toFixed(3)}</div>
                                        <div class="metric-label">Sharpe Ratio</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
    `;

    // Add recommendations if available
    if (data.recommendations) {
        resultsHTML += `
                    <!-- Key Recommendations -->
                    <div class="mb-4">
                        <h6><i class="fas fa-lightbulb me-2"></i>Key Recommendations</h6>
        `;
        
        if (data.recommendations.key_insights && data.recommendations.key_insights.length > 0) {
            data.recommendations.key_insights.forEach(insight => {
                const badgeClass = insight.type === 'top_increase' ? 'bg-success' : 'bg-warning';
                const icon = insight.type === 'top_increase' ? 'fa-arrow-up' : 'fa-arrow-down';
                
                resultsHTML += `
                        <div class="alert alert-light border-start border-3 border-${insight.type === 'top_increase' ? 'success' : 'warning'}">
                            <div class="d-flex align-items-center">
                                <i class="fas ${icon} me-2 text-${insight.type === 'top_increase' ? 'success' : 'warning'}"></i>
                                <div>
                                    <strong>${insight.message}</strong><br>
                                    <small class="text-muted">${insight.reason}</small>
                                </div>
                            </div>
                        </div>
                `;
            });
        }
        
        resultsHTML += `</div>`;
        
        // Add detailed weight changes
        if (data.recommendations.weight_changes) {
            resultsHTML += `
                    <!-- Weight Changes -->
                    <div class="mb-4">
                        <h6><i class="fas fa-balance-scale me-2"></i>Recommended Weight Changes</h6>
                        <div class="table-responsive">
                            <table class="table table-sm table-hover">
                                <thead class="table-light">
                                    <tr>
                                        <th>Symbol</th>
                                        <th>Current</th>
                                        <th>Recommended</th>
                                        <th>Change</th>
                                        <th>Action</th>
                                        <th>Reasoning</th>
                                    </tr>
                                </thead>
                                <tbody>
            `;
            
            data.recommendations.weight_changes.forEach(change => {
                const changeClass = change.change > 0 ? 'text-success' : change.change < 0 ? 'text-danger' : 'text-muted';
                const actionBadge = change.action === 'increase' ? 'bg-success' : change.action === 'decrease' ? 'bg-danger' : 'bg-secondary';
                
                resultsHTML += `
                                    <tr>
                                        <td><strong>${change.symbol}</strong></td>
                                        <td>${change.current_weight.toFixed(1)}%</td>
                                        <td>${change.recommended_weight.toFixed(1)}%</td>
                                        <td class="${changeClass}">
                                            ${change.change > 0 ? '+' : ''}${change.change.toFixed(1)}%
                                        </td>
                                        <td><span class="badge ${actionBadge}">${change.action.toUpperCase()}</span></td>
                                        <td><small>${change.reasoning}</small></td>
                                    </tr>
                `;
            });
            
            resultsHTML += `
                                </tbody>
                            </table>
                        </div>
                    </div>
            `;
        }
        
        // Add performance improvement summary
        if (data.recommendations.performance_improvement) {
            const perf = data.recommendations.performance_improvement;
            resultsHTML += `
                    <!-- Performance Improvement -->
                    <div class="row">
                        <div class="col-md-4">
                            <div class="text-center p-3 bg-light rounded">
                                <div class="h4 text-${perf.return_improvement >= 0 ? 'success' : 'danger'}">
                                    ${perf.return_improvement >= 0 ? '+' : ''}${perf.return_improvement.toFixed(2)}%
                                </div>
                                <div class="text-muted">Return Improvement</div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="text-center p-3 bg-light rounded">
                                <div class="h4 text-${perf.volatility_change <= 0 ? 'success' : 'warning'}">
                                    ${perf.volatility_change >= 0 ? '+' : ''}${perf.volatility_change.toFixed(2)}%
                                </div>
                                <div class="text-muted">Volatility Change</div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="text-center p-3 bg-light rounded">
                                <div class="h4 text-${perf.sharpe_improvement >= 0 ? 'success' : 'danger'}">
                                    ${perf.sharpe_improvement >= 0 ? '+' : ''}${perf.sharpe_improvement.toFixed(3)}
                                </div>
                                <div class="text-muted">Sharpe Improvement</div>
                            </div>
                        </div>
                    </div>
            `;
        }
    }
    
    resultsHTML += `
                </div>
            </div>
        </div>
    `;
    
    // Remove existing results and add new ones
    const existingResults = document.querySelector('.optimization-results');
    if (existingResults) {
        existingResults.remove();
    }
    
    // Insert after the portfolio form
    const portfolioForm = document.querySelector('#portfolioForm');
    const portfolioSection = portfolioForm ? portfolioForm.parentElement : document.querySelector('.config-panel .container-fluid');
    if (portfolioSection) {
        portfolioSection.insertAdjacentHTML('afterend', resultsHTML);
    }
    
    // Scroll to results
    document.querySelector('.optimization-results').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Run stress testing scenarios
 */
async function runStressTest() {
    try {
        console.log('Starting stress test...');
        
        // Get portfolio data from dynamic system
        const { symbols, weights } = getPortfolioData();
        
        if (!symbols || symbols.length === 0) {
            throw new Error('Please enter at least one asset for stress testing');
        }
        
        Utils.showLoading();
        
        // Run stress test
        const stressData = await Utils.makeRequest('/stress-test', {
            method: 'POST',
            body: JSON.stringify({
                symbols: symbols,
                weights: weights.map(w => w / 100), // Convert to decimals
                scenarios: ['market_crash', 'high_volatility', 'recession']
            })
        });
        
        Utils.hideLoading();
        
        // Update stress test results with visual feedback
        updateStressTestResults(stressData.stress_results);
        
        // Show stress test section with animation
        const stressSection = document.getElementById('stressTestResults');
        stressSection.style.display = 'block';
        stressSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Add visual highlight
        stressSection.style.border = '2px solid #ffc107';
        setTimeout(() => {
            stressSection.style.border = '';
        }, 3000);
        
        Utils.showSuccess('Stress test completed! Results updated below.');
        
    } catch (error) {
        Utils.hideLoading();
        Utils.showError('Stress test failed: ' + error.message);
        console.error('Stress test error:', error);
    }
}

/**
 * Update stress test results with enhanced display
 */
function updateStressTestResults(stressResults) {
    // Create enhanced stress test results
    let stressHTML = `
        <div class="stress-test-results mt-4">
            <div class="card border-warning">
                <div class="card-header bg-warning text-dark">
                    <h5 class="mb-0"><i class="fas fa-exclamation-triangle me-2"></i>Stress Test Results</h5>
                </div>
                <div class="card-body">
                    <p class="text-muted mb-4">Analysis of portfolio performance under adverse market conditions</p>
                    
                    <div class="row">
    `;
    
    const scenarioDescriptions = {
        'market_crash': {
            title: 'Market Crash',
            description: '20% market decline with doubled volatility',
            icon: 'fa-chart-line-down',
            severity: 'severe'
        },
        'high_volatility': {
            title: 'High Volatility',
            description: 'Triple volatility with normal returns',
            icon: 'fa-wave-square',
            severity: 'moderate'
        },
        'recession': {
            title: 'Recession',
            description: '15% market decline with increased volatility',
            icon: 'fa-trending-down',
            severity: 'moderate'
        }
    };
    
    Object.entries(stressResults).forEach(([scenario, results], index) => {
        const scenarioInfo = scenarioDescriptions[scenario] || {
            title: scenario.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
            description: 'Custom stress scenario',
            icon: 'fa-exclamation',
            severity: 'moderate'
        };
        
        const severityClass = scenarioInfo.severity === 'severe' ? 'severe' : '';
        
        stressHTML += `
                        <div class="col-md-4 mb-4">
                            <div class="card stress-scenario-card ${severityClass} h-100">
                                <div class="card-body">
                                    <div class="d-flex align-items-center mb-3">
                                        <i class="fas ${scenarioInfo.icon} fa-2x me-3 text-${scenarioInfo.severity === 'severe' ? 'danger' : 'warning'}"></i>
                                        <div>
                                            <h6 class="card-title mb-0">${scenarioInfo.title}</h6>
                                            <small class="text-muted">${scenarioInfo.description}</small>
                                        </div>
                                    </div>
                                    
                                    <div class="row g-2">
                                        <div class="col-6">
                                            <div class="text-center p-2 bg-light rounded">
                                                <div class="fw-bold text-danger">${Utils.formatPercentage(results.var_95)}</div>
                                                <small class="text-muted">VaR 95%</small>
                                            </div>
                                        </div>
                                        <div class="col-6">
                                            <div class="text-center p-2 bg-light rounded">
                                                <div class="fw-bold text-dark">${Utils.formatPercentage(results.var_99)}</div>
                                                <small class="text-muted">VaR 99%</small>
                                            </div>
                                        </div>
                                        <div class="col-6">
                                            <div class="text-center p-2 bg-light rounded">
                                                <div class="fw-bold text-warning">${Utils.formatPercentage(results.volatility)}</div>
                                                <small class="text-muted">Volatility</small>
                                            </div>
                                        </div>
                                        <div class="col-6">
                                            <div class="text-center p-2 bg-light rounded">
                                                <div class="fw-bold text-info">${Utils.formatPercentage(Math.abs(results.max_drawdown))}</div>
                                                <small class="text-muted">Max Drawdown</small>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <!-- Risk Assessment -->
                                    <div class="mt-3">
                                        ${generateRiskAssessment(results, scenarioInfo.severity)}
                                    </div>
                                </div>
                            </div>
                        </div>
        `;
    });
    
    stressHTML += `
                    </div>
                    
                    <!-- Summary and Recommendations -->
                    <div class="mt-4 p-3 bg-light rounded">
                        <h6><i class="fas fa-lightbulb me-2"></i>Stress Test Insights</h6>
                        ${generateStressTestInsights(stressResults)}
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing results and add new ones
    const existingResults = document.querySelector('.stress-test-results');
    if (existingResults) {
        existingResults.remove();
    }
    
    // Insert after optimization results or portfolio form
    const optimizationResults = document.querySelector('.optimization-results');
    const portfolioForm = document.querySelector('#portfolioForm');
    const insertAfter = optimizationResults || (portfolioForm ? portfolioForm.parentElement : document.querySelector('.config-panel .container-fluid'));
    
    if (insertAfter) {
        insertAfter.insertAdjacentHTML('afterend', stressHTML);
    }
    
    // Scroll to results
    document.querySelector('.stress-test-results').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Generate risk assessment for a stress scenario
 */
function generateRiskAssessment(results, severity) {
    const var95 = Math.abs(results.var_95);
    let riskLevel, riskColor, riskMessage;
    
    if (var95 > 0.15) {
        riskLevel = 'High Risk';
        riskColor = 'danger';
        riskMessage = 'Significant potential losses';
    } else if (var95 > 0.08) {
        riskLevel = 'Moderate Risk';
        riskColor = 'warning';
        riskMessage = 'Manageable risk level';
    } else {
        riskLevel = 'Low Risk';
        riskColor = 'success';
        riskMessage = 'Well-protected portfolio';
    }
    
    return `
        <div class="d-flex align-items-center">
            <span class="badge bg-${riskColor} me-2">${riskLevel}</span>
            <small class="text-muted">${riskMessage}</small>
        </div>
    `;
}

/**
 * Generate stress test insights and recommendations
 */
function generateStressTestInsights(stressResults) {
    const scenarios = Object.keys(stressResults);
    const worstScenario = scenarios.reduce((worst, current) => 
        Math.abs(stressResults[current].var_95) > Math.abs(stressResults[worst].var_95) ? current : worst
    );
    
    const bestScenario = scenarios.reduce((best, current) => 
        Math.abs(stressResults[current].var_95) < Math.abs(stressResults[best].var_95) ? current : best
    );
    
    const insights = [];
    
    // Worst case analysis
    const worstVaR = Math.abs(stressResults[worstScenario].var_95);
    insights.push(`
        <div class="mb-2">
            <strong>Worst Case:</strong> In a ${worstScenario.replace(/_/g, ' ')} scenario, 
            your portfolio could lose up to ${Utils.formatPercentage(worstVaR)} with 95% confidence.
        </div>
    `);
    
    // Resilience analysis
    const avgVaR = scenarios.reduce((sum, scenario) => sum + Math.abs(stressResults[scenario].var_95), 0) / scenarios.length;
    if (avgVaR < 0.10) {
        insights.push(`
            <div class="mb-2 text-success">
                <i class="fas fa-shield-alt me-1"></i>
                <strong>Portfolio Resilience:</strong> Your portfolio shows good resilience across stress scenarios 
                with average VaR of ${Utils.formatPercentage(avgVaR)}.
            </div>
        `);
    } else {
        insights.push(`
            <div class="mb-2 text-warning">
                <i class="fas fa-exclamation-triangle me-1"></i>
                <strong>Portfolio Vulnerability:</strong> Consider diversification to reduce average stress VaR 
                of ${Utils.formatPercentage(avgVaR)}.
            </div>
        `);
    }
    
    return insights.join('');
}

/**
 * Download analysis results as JSON
 */
function downloadResults() {
    if (!currentAnalysisData) {
        Utils.showError('No analysis data available to download');
        return;
    }
    
    const dataStr = JSON.stringify(currentAnalysisData, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = `risk-analysis-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    Utils.showSuccess('Analysis results downloaded successfully!');
}

/**
 * Export analysis results as PDF report
 */
async function exportToPDF() {
    if (!currentAnalysisData) {
        Utils.showError('No analysis data available to export');
        return;
    }
    
    try {
        // This would typically integrate with a PDF generation library
        // For now, we'll create a simple HTML report that can be printed
        const reportWindow = window.open('', '_blank');
        const reportHTML = generateReportHTML(currentAnalysisData, currentPortfolioConfig);
        
        reportWindow.document.write(reportHTML);
        reportWindow.document.close();
        reportWindow.print();
        
        Utils.showSuccess('Report opened in new window. Use browser print function to save as PDF.');
        
    } catch (error) {
        Utils.showError('Failed to generate PDF report: ' + error.message);
        console.error('PDF export error:', error);
    }
}

/**
 * Generate HTML report for printing/PDF export
 */
function generateReportHTML(data, config) {
    const date = new Date().toLocaleDateString();
    const time = new Date().toLocaleTimeString();
    
    return `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Financial Risk Analysis Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .header { text-align: center; margin-bottom: 40px; }
                .section { margin: 30px 0; }
                .metrics-table { width: 100%; border-collapse: collapse; }
                .metrics-table th, .metrics-table td { 
                    border: 1px solid #ddd; padding: 8px; text-align: left; 
                }
                .metrics-table th { background-color: #f2f2f2; }
                .risk-card { 
                    display: inline-block; margin: 10px; padding: 20px; 
                    border: 1px solid #ddd; border-radius: 5px; text-align: center; width: 200px;
                }
                @media print { body { margin: 20px; } }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Enhanced Financial Risk Prediction System</h1>
                <h2>Portfolio Risk Analysis Report</h2>
                <p>Generated on ${date} at ${time}</p>
                <p>Portfolio: ${config.symbols.join(', ')}</p>
                <p>Weights: ${config.weights.map(w => Utils.formatPercentage(w)).join(', ')}</p>
            </div>
            
            <div class="section">
                <h3>Risk Metrics Summary</h3>
                <div class="risk-card">
                    <h4>Historical VaR (95%)</h4>
                    <p>${Utils.formatPercentage(data.risk_metrics.var_metrics.historical_var)}</p>
                </div>
                <div class="risk-card">
                    <h4>Parametric VaR (95%)</h4>
                    <p>${Utils.formatPercentage(data.risk_metrics.var_metrics.parametric_var)}</p>
                </div>
                <div class="risk-card">
                    <h4>Monte Carlo VaR (95%)</h4>
                    <p>${Utils.formatPercentage(data.monte_carlo.risk_metrics.var_95)}</p>
                </div>
                <div class="risk-card">
                    <h4>Expected Shortfall</h4>
                    <p>${Utils.formatPercentage(data.risk_metrics.var_metrics.expected_shortfall)}</p>
                </div>
            </div>
            
            <div class="section">
                <h3>Portfolio Metrics</h3>
                <table class="metrics-table">
                    <tr><th>Metric</th><th>Value</th></tr>
                    <tr><td>Volatility</td><td>${Utils.formatPercentage(data.risk_metrics.portfolio_metrics.volatility)}</td></tr>
                    <tr><td>Sharpe Ratio</td><td>${data.risk_metrics.portfolio_metrics.sharpe_ratio.toFixed(3)}</td></tr>
                    <tr><td>Maximum Drawdown</td><td>${Utils.formatPercentage(Math.abs(data.risk_metrics.portfolio_metrics.max_drawdown))}</td></tr>
                    <tr><td>Probability of Loss</td><td>${Utils.formatPercentage(data.monte_carlo.simulation_results.statistics.probability_of_loss)}</td></tr>
                </table>
            </div>
            
            <div class="section">
                <h3>Analysis Parameters</h3>
                <table class="metrics-table">
                    <tr><th>Parameter</th><th>Value</th></tr>
                    <tr><td>Confidence Level</td><td>${Utils.formatPercentage(config.confidence_level)}</td></tr>
                    <tr><td>Time Horizon</td><td>${config.time_horizon} day(s)</td></tr>
                    <tr><td>Portfolio Value</td><td>${Utils.formatCurrency(config.portfolio_value)}</td></tr>
                    <tr><td>Monte Carlo Simulations</td><td>${data.monte_carlo.metadata.num_simulations.toLocaleString()}</td></tr>
                </table>
            </div>
            
            <footer style="margin-top: 50px; text-align: center; font-size: 12px; color: #666;">
                <p>Enhanced Financial Risk Prediction System - Final Year Project</p>
                <p>By: Abubakri Olayide Abdul-Lateef (CSC/2018/005)</p>
                <p>Supervisor: Dr. (Mrs) A.O AMOO</p>
            </footer>
        </body>
        </html>
    `;
}

// Add keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl+Enter to run risk analysis
    if (event.ctrlKey && event.key === 'Enter') {
        event.preventDefault();
        runRiskAnalysis();
    }
    
    // Ctrl+O to optimize portfolio
    if (event.ctrlKey && event.key === 'o') {
        event.preventDefault();
        optimizePortfolio();
    }
    
    // Ctrl+S to download results
    if (event.ctrlKey && event.key === 's') {
        event.preventDefault();
        downloadResults();
    }
});

// Make functions globally available
window.runRiskAnalysis = runRiskAnalysis;
window.optimizePortfolio = optimizePortfolio;
window.runStressTest = runStressTest;
window.downloadResults = downloadResults;
window.exportToPDF = exportToPDF; 