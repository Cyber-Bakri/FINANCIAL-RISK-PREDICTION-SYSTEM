/**
 * Enhanced Financial Risk Prediction System
 * Main JavaScript file for UI interactions and utilities
 */

// Global configuration
const CONFIG = {
    API_BASE_URL: '/api',
    CHART_COLORS: {
        primary: '#007bff',
        success: '#28a745',
        danger: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8'
    },
    ANIMATION_DURATION: 1000
};

// Global variables
let selectedPortfolio = [];
let availableSymbols = {};
let popularSymbols = [];

// Utility functions
const Utils = {
    // Format currency values
    formatCurrency: function(value) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(value);
    },

    // Format percentage values
    formatPercentage: function(value, decimals = 2) {
        return (value * 100).toFixed(decimals) + '%';
    },

    // Format large numbers
    formatNumber: function(value, decimals = 2) {
        if (Math.abs(value) >= 1e9) {
            return (value / 1e9).toFixed(decimals) + 'B';
        } else if (Math.abs(value) >= 1e6) {
            return (value / 1e6).toFixed(decimals) + 'M';
        } else if (Math.abs(value) >= 1e3) {
            return (value / 1e3).toFixed(decimals) + 'K';
        } else {
            return value.toFixed(decimals);
        }
    },

    // Show loading indicator
    showLoading: function() {
        document.getElementById('loadingIndicator').style.display = 'block';
        document.getElementById('resultsSection').style.display = 'none';
    },

    // Hide loading indicator
    hideLoading: function() {
        document.getElementById('loadingIndicator').style.display = 'none';
    },

    // Show results section
    showResults: function() {
        document.getElementById('resultsSection').style.display = 'block';
        document.getElementById('resultsSection').classList.add('fade-in-up');
    },

    // Show error message
    showError: function(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    },

    // Show success message
    showSuccess: function(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-success alert-dismissible fade show';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 3 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 3000);
    },

    // Make API request
    makeRequest: async function(endpoint, options = {}) {
        try {
            const response = await fetch(CONFIG.API_BASE_URL + endpoint, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (!data.success) {
                throw new Error(data.error || 'API request failed');
            }

            return data;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    },

    // Validate portfolio inputs
    validatePortfolioInputs: function() {
        // Make sure portfolio data is up to date
        if (typeof updatePortfolioData === 'function') {
            updatePortfolioData();
        }
        
        const symbols = document.getElementById('symbols').value.trim();
        const weights = document.getElementById('weights').value.trim();
        
        if (!symbols) {
            throw new Error('Please add at least one asset to your portfolio');
        }

        if (!weights) {
            throw new Error('Please enter investment amounts for your assets');
        }

        const symbolArray = symbols.split(',').map(s => s.trim()).filter(s => s);
        const weightArray = weights.split(',').map(w => parseFloat(w.trim())).filter(w => !isNaN(w));

        if (symbolArray.length !== weightArray.length) {
            throw new Error('Number of symbols must match number of weights');
        }

        const totalWeight = weightArray.reduce((sum, w) => sum + w, 0);
        if (Math.abs(totalWeight - 100) > 0.01) {
            throw new Error('Weights must sum to 100%');
        }

        return {
            symbols: symbolArray,
            weights: weightArray.map(w => w / 100) // Convert to decimals
        };
    },

    // Get portfolio configuration
    getPortfolioConfig: function() {
        const validation = this.validatePortfolioInputs();
        
        return {
            symbols: validation.symbols,
            weights: validation.weights,
            confidence_level: parseFloat(document.getElementById('confidenceLevel').value),
            time_horizon: parseInt(document.getElementById('timeHorizon').value),
            portfolio_value: getTotalPortfolioValue()
        };
    }
};

// Chart management
const ChartManager = {
    charts: {},

    // Create or update Monte Carlo chart
    updateMonteCarloChart: function(data) {
        const ctx = document.getElementById('monteCarloChart').getContext('2d');
        
        if (this.charts.monteCarlo) {
            this.charts.monteCarlo.destroy();
        }

        // Create histogram data
        const returns = data.simulation_results.portfolio_returns;
        const bins = 50;
        const min = Math.min(...returns);
        const max = Math.max(...returns);
        const binWidth = (max - min) / bins;
        
        const histogram = new Array(bins).fill(0);
        const labels = [];
        
        for (let i = 0; i < bins; i++) {
            labels.push((min + i * binWidth).toFixed(4));
        }
        
        returns.forEach(value => {
            const binIndex = Math.min(Math.floor((value - min) / binWidth), bins - 1);
            histogram[binIndex]++;
        });

        this.charts.monteCarlo = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Frequency',
                    data: histogram,
                    backgroundColor: 'rgba(0, 123, 255, 0.6)',
                    borderColor: 'rgba(0, 123, 255, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Frequency'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Portfolio Returns'
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Distribution of Portfolio Returns'
                    },
                    legend: {
                        display: false
                    }
                }
            }
        });
    },

    // Create or update risk comparison chart
    updateRiskComparisonChart: function(data) {
        const ctx = document.getElementById('riskComparisonChart').getContext('2d');
        
        if (this.charts.riskComparison) {
            this.charts.riskComparison.destroy();
        }

        this.charts.riskComparison = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Historical VaR', 'Parametric VaR', 'Monte Carlo VaR', 'ML Predicted VaR'],
                datasets: [{
                    label: 'VaR (95%)',
                    data: [
                        data.risk_metrics.var_metrics.historical_var,
                        data.risk_metrics.var_metrics.parametric_var,
                        data.monte_carlo.risk_metrics.var_95,
                        data.ml_predictions.predictions[Object.keys(data.ml_predictions.predictions)[0]]?.var_95 || 0
                    ],
                    backgroundColor: [
                        'rgba(220, 53, 69, 0.6)',
                        'rgba(255, 193, 7, 0.6)',
                        'rgba(23, 162, 184, 0.6)',
                        'rgba(52, 58, 64, 0.6)'
                    ],
                    borderColor: [
                        'rgba(220, 53, 69, 1)',
                        'rgba(255, 193, 7, 1)',
                        'rgba(23, 162, 184, 1)',
                        'rgba(52, 58, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'VaR Value'
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Risk Metrics Comparison'
                    },
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
};

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Financial Risk Prediction System - Initializing...');
    
    // Initialize basic functionality
    setupBasicEventListeners();
    
    // Initialize portfolio with default assets
    loadSamplePortfolio();
    
    console.log('System initialized successfully');
});

// Setup basic event listeners
function setupBasicEventListeners() {
    // Portfolio input validation
    const symbolsInput = document.getElementById('symbols');
    const weightsInput = document.getElementById('weights');
    
    if (symbolsInput) {
        symbolsInput.addEventListener('input', validatePortfolioInputs);
    }
    
    const amountsInput = document.getElementById('amounts');
    if (amountsInput) {
        amountsInput.addEventListener('input', validatePortfolioInputs);
    }
}

// Portfolio management with dynamic asset rows
let portfolioAssets = [];

// Add a new asset row
function addAssetRow(symbol = '', amount = 25000) {
    const portfolioContainer = document.getElementById('portfolioAssets');
    const index = portfolioAssets.length;
    
    const assetRow = document.createElement('div');
    assetRow.className = 'row mb-2 asset-row';
    assetRow.id = `asset-${index}`;
    
    assetRow.innerHTML = `
        <div class="col-md-4">
            <input type="text" class="form-control symbol-input" 
                   placeholder="e.g., AAPL" 
                   value="${symbol}"
                   onchange="updatePortfolioData()"
                   style="text-transform: uppercase;">
        </div>
        <div class="col-md-4">
            <div class="input-group">
                <span class="input-group-text">$</span>
                <input type="number" class="form-control amount-input" 
                       placeholder="25000" 
                       value="${amount}"
                       min="100" 
                       step="100"
                       onchange="updatePortfolioData()">
            </div>
        </div>
        <div class="col-md-3">
            <span class="weight-display text-muted">0%</span>
        </div>
        <div class="col-md-1">
            <button type="button" class="btn btn-outline-danger btn-sm" onclick="removeAssetRow(${index})">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `;
    
    portfolioContainer.appendChild(assetRow);
    portfolioAssets.push({symbol, amount});
    updatePortfolioData();
}

// Remove an asset row
function removeAssetRow(index) {
    const assetRow = document.getElementById(`asset-${index}`);
    if (assetRow) {
        assetRow.remove();
        portfolioAssets.splice(index, 1);
        
        // Re-index remaining rows
        const remainingRows = document.querySelectorAll('.asset-row');
        remainingRows.forEach((row, newIndex) => {
            row.id = `asset-${newIndex}`;
            const removeBtn = row.querySelector('button');
            removeBtn.setAttribute('onclick', `removeAssetRow(${newIndex})`);
        });
        
        updatePortfolioData();
    }
}

// Update portfolio with optimized weights
function updatePortfolioWithOptimizedWeights(optimizedWeights) {
    console.log('updatePortfolioWithOptimizedWeights called with:', optimizedWeights);
    
    const totalValue = getTotalPortfolioValue();
    const assetRows = document.querySelectorAll('.asset-row');
    
    console.log('Total portfolio value:', totalValue);
    console.log('Number of asset rows found:', assetRows.length);
    
    let updated = false;
    
    assetRows.forEach((row, index) => {
        const symbolInput = row.querySelector('.symbol-input');
        const amountInput = row.querySelector('.amount-input');
        
        if (!symbolInput || !amountInput) {
            console.warn(`Row ${index}: Missing input elements`);
            return;
        }
        
        const symbol = symbolInput.value.trim().toUpperCase();
        const weight = optimizedWeights[symbol];
        
        console.log(`Row ${index}: Symbol=${symbol}, Weight=${weight}`);
        
        if (weight && totalValue > 0) {
            const newAmount = Math.round(totalValue * weight);
            console.log(`Updating ${symbol}: $${amountInput.value} -> $${newAmount}`);
            amountInput.value = newAmount;
            updated = true;
        }
    });
    
    if (updated) {
        console.log('Portfolio amounts updated, recalculating...');
        // Update the portfolio data
        updatePortfolioData();
    } else {
        console.warn('No portfolio amounts were updated');
    }
}

// Get total portfolio value (for optimization updates)
function getTotalPortfolioValue() {
    const totalValueElement = document.getElementById('totalValue');
    if (totalValueElement) {
        const totalText = totalValueElement.textContent || totalValueElement.innerText || '$0';
        const numericValue = parseFloat(totalText.replace(/[$,]/g, ''));
        return isNaN(numericValue) ? 100000 : numericValue;
    }
    return 100000;
}

// Update portfolio data and hidden fields
function updatePortfolioData() {
    const assetRows = document.querySelectorAll('.asset-row');
    const symbols = [];
    const amounts = [];
    let total = 0;
    
    assetRows.forEach((row, index) => {
        const symbolInput = row.querySelector('.symbol-input');
        const amountInput = row.querySelector('.amount-input');
        const weightDisplay = row.querySelector('.weight-display');
        
        const symbol = symbolInput.value.trim().toUpperCase();
        const amount = parseFloat(amountInput.value) || 0;
        
        if (symbol && amount > 0) {
            symbols.push(symbol);
            amounts.push(amount);
            total += amount;
        }
        
        // Update the symbol input to uppercase
        symbolInput.value = symbol;
    });
    
    // Calculate and display weights
    assetRows.forEach((row, index) => {
        const amountInput = row.querySelector('.amount-input');
        const weightDisplay = row.querySelector('.weight-display');
        const amount = parseFloat(amountInput.value) || 0;
        
        if (total > 0 && amount > 0) {
            const weight = ((amount / total) * 100).toFixed(1);
            weightDisplay.textContent = `${weight}%`;
        } else {
            weightDisplay.textContent = '0%';
        }
    });
    
    // Update summary
    document.getElementById('totalValue').textContent = `$${total.toLocaleString()}`;
    document.getElementById('assetCount').textContent = symbols.length;
    
    // Update hidden fields for backend compatibility
    document.getElementById('symbols').value = symbols.join(',');
    const weights = amounts.map(amount => total > 0 ? ((amount / total) * 100).toFixed(2) : 0);
    document.getElementById('weights').value = weights.join(',');
    
    // Update portfolioAssets array
    portfolioAssets = symbols.map((symbol, index) => ({
        symbol,
        amount: amounts[index] || 0
    }));
}

// Validate portfolio inputs
function validatePortfolioInputs() {
    updatePortfolioData();
    const symbols = document.getElementById('symbols').value.split(',').filter(s => s.trim());
    const hasValidAssets = symbols.length > 0 && portfolioAssets.every(asset => asset.amount >= 100);
    
    // Visual validation feedback could be added here if needed
    return hasValidAssets;
}

// System health check
async function checkSystemHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        if (data.status === 'healthy') {
            console.log('System is healthy');
            updateSystemStatus('online');
        }
    } catch (error) {
        console.error('System health check failed:', error);
        updateSystemStatus('offline');
    }
}

function updateSystemStatus(status) {
    const indicator = document.getElementById('systemStatus');
    if (indicator) {
        indicator.className = `status-indicator status-${status === 'online' ? 'good' : 'danger'}`;
        indicator.title = `System is ${status}`;
    }
}

// Initialize symbol selection functionality
async function initializeSymbolSelection() {
    try {
        // Load available symbols
        await loadAvailableSymbols();
        
        // Load popular symbols
        await loadPopularSymbols();
        
        // Setup category dropdown
        setupCategoryDropdown();
        
        console.log('Symbol selection initialized');
    } catch (error) {
        console.error('Failed to initialize symbol selection:', error);
        showNotification('Failed to load symbol data', 'error');
    }
}

// Load available symbols from API
async function loadAvailableSymbols() {
    try {
        const response = await fetch('/api/symbols/available');
        const data = await response.json();
        
        if (data.success) {
            availableSymbols = data.symbols;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Error loading available symbols:', error);
        throw error;
    }
}

// Load popular symbols from API
async function loadPopularSymbols() {
    try {
        const response = await fetch('/api/symbols/popular?limit=15');
        const data = await response.json();
        
        if (data.success) {
            popularSymbols = data.symbols;
            displayPopularSymbols();
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Error loading popular symbols:', error);
        throw error;
    }
}

// Display popular symbols
function displayPopularSymbols() {
    const container = document.getElementById('popularSymbols');
    if (!container) return;
    
    container.innerHTML = '';
    
    popularSymbols.forEach(symbolData => {
        const button = document.createElement('button');
        button.className = 'popular-symbol';
        button.innerHTML = `<strong>${symbolData.symbol}</strong><br><small>${symbolData.name}</small>`;
        button.title = `${symbolData.name} (${symbolData.category})`;
        button.onclick = () => addSymbolToPortfolio(symbolData.symbol, symbolData.name, symbolData.category);
        
        container.appendChild(button);
    });
}

// Setup category dropdown
function setupCategoryDropdown() {
    const select = document.getElementById('categorySelect');
    if (!select) return;
    
    // Clear existing options
    select.innerHTML = '<option value="">Select a category...</option>';
    
    // Add categories
    Object.keys(availableSymbols).forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        select.appendChild(option);
    });
}

// Setup event listeners
function setupEventListeners() {
    // Search functionality
    const searchInput = document.getElementById('symbolSearch');
    const searchBtn = document.getElementById('searchBtn');
    
    if (searchInput && searchBtn) {
        searchInput.addEventListener('input', debounce(performSearch, 300));
        searchBtn.addEventListener('click', performSearch);
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                performSearch();
            }
        });
    }
    
    // Category selection
    const categorySelect = document.getElementById('categorySelect');
    if (categorySelect) {
        categorySelect.addEventListener('change', displayCategorySymbols);
    }
    
    // Manual input toggle
    const manualInputCheckbox = document.getElementById('manualInput');
    if (manualInputCheckbox) {
        manualInputCheckbox.addEventListener('change', toggleManualInput);
    }
}

// Perform symbol search
async function performSearch() {
    const searchInput = document.getElementById('symbolSearch');
    const resultsContainer = document.getElementById('searchResults');
    
    if (!searchInput || !resultsContainer) return;
    
    const query = searchInput.value.trim();
    
    if (query.length < 2) {
        resultsContainer.style.display = 'none';
        return;
    }
    
    try {
        const response = await fetch(`/api/symbols/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data.success) {
            displaySearchResults(data.results);
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Search error:', error);
        showNotification('Search failed', 'error');
    }
}

// Display search results
function displaySearchResults(results) {
    const container = document.getElementById('searchResults');
    if (!container) return;
    
    if (Object.keys(results).length === 0) {
        container.innerHTML = '<div class="text-muted p-2">No symbols found</div>';
        container.style.display = 'block';
        return;
    }
    
    container.innerHTML = '';
    
    Object.entries(results).forEach(([symbol, description]) => {
        const item = document.createElement('div');
        item.className = 'search-result-item';
        item.innerHTML = `<strong>${symbol}</strong><br><small>${description}</small>`;
        item.onclick = () => {
            const [name, category] = description.includes('(') ? 
                [description.split(' (')[0], description.split(' (')[1].replace(')', '')] :
                [description, 'Unknown'];
            addSymbolToPortfolio(symbol, name, category);
            container.style.display = 'none';
            document.getElementById('symbolSearch').value = '';
        };
        
        container.appendChild(item);
    });
    
    container.style.display = 'block';
}

// Display category symbols
function displayCategorySymbols() {
    const select = document.getElementById('categorySelect');
    const container = document.getElementById('categorySymbols');
    
    if (!select || !container) return;
    
    const category = select.value;
    
    if (!category) {
        container.style.display = 'none';
        return;
    }
    
    const symbols = availableSymbols[category];
    if (!symbols) return;
    
    container.innerHTML = '';
    
    Object.entries(symbols).forEach(([symbol, name]) => {
        const span = document.createElement('span');
        span.className = 'category-symbol';
        span.textContent = symbol;
        span.title = name;
        span.onclick = () => addSymbolToPortfolio(symbol, name, category);
        
        container.appendChild(span);
    });
    
    container.style.display = 'block';
}

// Add symbol to portfolio
function addSymbolToPortfolio(symbol, name, category) {
    // Check if symbol already exists
    if (selectedPortfolio.find(item => item.symbol === symbol)) {
        showNotification(`${symbol} is already in your portfolio`, 'warning');
        return;
    }
    
    // Add to portfolio
    const portfolioItem = {
        symbol: symbol,
        name: name,
        category: category,
        weight: selectedPortfolio.length === 0 ? 100 : Math.round(100 / (selectedPortfolio.length + 1))
    };
    
    selectedPortfolio.push(portfolioItem);
    
    // Rebalance weights equally
    rebalanceWeights();
    
    // Update display
    updateSelectedSymbolsDisplay();
    updateManualInputs();
    
    showNotification(`Added ${symbol} to portfolio`, 'success');
}

// Remove symbol from portfolio
function removeSymbolFromPortfolio(symbol) {
    selectedPortfolio = selectedPortfolio.filter(item => item.symbol !== symbol);
    
    // Rebalance weights
    rebalanceWeights();
    
    // Update display
    updateSelectedSymbolsDisplay();
    updateManualInputs();
    
    showNotification(`Removed ${symbol} from portfolio`, 'info');
}

// Rebalance portfolio weights equally
function rebalanceWeights() {
    if (selectedPortfolio.length === 0) return;
    
    const equalWeight = Math.round(100 / selectedPortfolio.length);
    let remainder = 100 - (equalWeight * selectedPortfolio.length);
    
    selectedPortfolio.forEach((item, index) => {
        item.weight = equalWeight + (index < remainder ? 1 : 0);
    });
}

// Update weight for specific symbol
function updateSymbolWeight(symbol, weight) {
    const item = selectedPortfolio.find(item => item.symbol === symbol);
    if (item) {
        item.weight = parseFloat(weight) || 0;
        updateSelectedSymbolsDisplay();
        updateManualInputs();
    }
}

// Update selected symbols display
function updateSelectedSymbolsDisplay() {
    const container = document.getElementById('selectedSymbols');
    if (!container) return;
    
    if (selectedPortfolio.length === 0) {
        container.innerHTML = '<div class="selected-portfolio-empty">No assets selected. Add assets using the search or category selection above.</div>';
        container.classList.remove('has-symbols');
        return;
    }
    
    container.classList.add('has-symbols');
    
    let html = '';
    
    selectedPortfolio.forEach(item => {
        html += `
            <div class="symbol-badge">
                <div>
                    <strong>${item.symbol}</strong>
                    <small class="d-block">${item.name}</small>
                </div>
                <input type="number" class="weight-input" value="${item.weight}" 
                       min="0" max="100" step="0.1"
                       onchange="updateSymbolWeight('${item.symbol}', this.value)"
                       title="Weight (%)">
                <span>%</span>
                <button class="remove-symbol" onclick="removeSymbolFromPortfolio('${item.symbol}')" 
                        title="Remove from portfolio">×</button>
            </div>
        `;
    });
    
    // Add portfolio summary
    const totalWeight = selectedPortfolio.reduce((sum, item) => sum + item.weight, 0);
    html += `
        <div class="portfolio-summary">
            <h6><i class="fas fa-chart-pie me-2"></i>Portfolio Summary</h6>
            <div class="portfolio-item">
                <span>Total Assets:</span>
                <strong>${selectedPortfolio.length}</strong>
            </div>
            <div class="portfolio-item">
                <span>Total Weight:</span>
                <strong class="${totalWeight === 100 ? 'text-success' : 'text-warning'}">${totalWeight.toFixed(1)}%</strong>
            </div>
            ${totalWeight !== 100 ? '<div class="text-warning small">⚠️ Weights should sum to 100%</div>' : ''}
        </div>
    `;
    
    container.innerHTML = html;
}

// Update manual input fields
function updateManualInputs() {
    const symbolsInput = document.getElementById('symbols');
    const weightsInput = document.getElementById('weights');
    
    if (symbolsInput && weightsInput) {
        symbolsInput.value = selectedPortfolio.map(item => item.symbol).join(',');
        weightsInput.value = selectedPortfolio.map(item => item.weight).join(',');
    }
}

// Toggle manual input section
function toggleManualInput() {
    const checkbox = document.getElementById('manualInput');
    const section = document.getElementById('manualInputSection');
    
    if (checkbox && section) {
        section.style.display = checkbox.checked ? 'block' : 'none';
    }
}

// Load default portfolio
function loadDefaultPortfolio() {
    // Add some default symbols
    const defaultSymbols = [
        { symbol: 'AAPL', name: 'Apple Inc.', category: 'Technology' },
        { symbol: 'MSFT', name: 'Microsoft Corporation', category: 'Technology' },
        { symbol: 'GOOGL', name: 'Alphabet Inc.', category: 'Technology' },
        { symbol: 'TSLA', name: 'Tesla Inc.', category: 'Technology' }
    ];
    
    defaultSymbols.forEach(item => {
        selectedPortfolio.push({
            ...item,
            weight: 25
        });
    });
    
    updateSelectedSymbolsDisplay();
    updateManualInputs();
}

// Get portfolio data for API calls
function getPortfolioData() {
    // Check if manual input is being used
    const manualInput = document.getElementById('manualInput');
    
    if (manualInput && manualInput.checked) {
        // Use manual input
        const symbolsInput = document.getElementById('symbols').value;
        const weightsInput = document.getElementById('weights').value;
        
        const symbols = symbolsInput.split(',').map(s => s.trim()).filter(s => s);
        const weights = weightsInput.split(',').map(w => parseFloat(w.trim())).filter(w => !isNaN(w));
        
        return { symbols, weights };
    } else {
        // Use selected portfolio
        const symbols = selectedPortfolio.map(item => item.symbol);
        const weights = selectedPortfolio.map(item => item.weight);
        
        return { symbols, weights };
    }
}

// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 100px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Quick symbol addition function
function addQuickSymbol(symbol, name) {
    // Check if symbol already exists
    const existingSymbols = portfolioAssets.map(asset => asset.symbol);
    if (existingSymbols.includes(symbol)) {
        showNotification(`${symbol} is already in your portfolio`, 'warning');
        return;
    }
    
    // Calculate amount for new symbol (default $25,000 or maintain average)
    let newAmount = 25000;
    if (portfolioAssets.length > 0) {
        const avgAmount = portfolioAssets.reduce((sum, asset) => sum + asset.amount, 0) / portfolioAssets.length;
        newAmount = Math.round(avgAmount);
    }
    
    // Add new asset row
    addAssetRow(symbol, newAmount);
    
    showNotification(`Added ${symbol} (${name}) - $${newAmount.toLocaleString()}`, 'success');
    
    // Trigger live quotes update
    setTimeout(loadLiveQuotes, 500);
}

// Clear portfolio function
function clearPortfolio() {
    const portfolioContainer = document.getElementById('portfolioAssets');
    portfolioContainer.innerHTML = '';
    portfolioAssets = [];
    document.getElementById('symbols').value = '';
    document.getElementById('weights').value = '';
    document.getElementById('totalValue').textContent = '$0';
    document.getElementById('assetCount').textContent = '0';
    showNotification('Portfolio cleared', 'info');
}

// Load sample portfolio function
function loadSamplePortfolio() {
    clearPortfolio();
    
    const sampleAssets = [
        {symbol: 'AAPL', amount: 20000},
        {symbol: 'MSFT', amount: 20000},
        {symbol: 'GOOGL', amount: 20000},
        {symbol: 'TSLA', amount: 20000},
        {symbol: 'SPY', amount: 20000}
    ];
    
    sampleAssets.forEach(asset => {
        addAssetRow(asset.symbol, asset.amount);
    });
    
    showNotification('Sample portfolio loaded successfully', 'success');
}

// Live Market Data Functions
async function loadMarketStatus() {
    try {
        const response = await fetch('/api/market-status');
        const status = await response.json();
        updateMarketStatusDisplay(status);
    } catch (error) {
        console.error('Error loading market status:', error);
    }
}

function updateMarketStatusDisplay(status) {
    const statusElement = document.getElementById('market-status');
    if (!statusElement) return;
    
    const isOpen = status.is_market_open;
    const statusText = isOpen ? 'OPEN' : 'CLOSED';
    const dataFreshness = status.data_freshness || 'unknown';
    
    statusElement.innerHTML = `
        <div class="d-flex align-items-center">
            <span class="badge ${isOpen ? 'bg-success' : 'bg-danger'} me-2">
                <i class="fas ${isOpen ? 'fa-circle' : 'fa-pause-circle'}"></i>
                Market ${statusText}
            </span>
            <small class="text-muted">
                Data: ${dataFreshness === 'real-time' ? 'Live' : 'Last Close'}
            </small>
        </div>
        <small class="text-muted d-block">
            Updated: ${new Date().toLocaleTimeString()}
        </small>
    `;
}

async function loadLiveQuotes() {
    const symbolsInput = document.getElementById('symbols');
    if (!symbolsInput || !symbolsInput.value.trim()) return;
    
    try {
        const symbols = symbolsInput.value.split(',').map(s => s.trim()).filter(s => s);
        if (symbols.length === 0) return;
        
        const response = await fetch('/api/live-quotes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbols })
        });
        
        const data = await response.json();
        displayLiveQuotes(data.quotes);
    } catch (error) {
        console.error('Error loading live quotes:', error);
    }
}

function displayLiveQuotes(quotes) {
    const quotesContainer = document.getElementById('live-quotes');
    const quotesSection = document.getElementById('live-quotes-section');
    if (!quotesContainer) return;
    
    const hasValidQuotes = Object.values(quotes).some(quote => !quote.error);
    
    if (!hasValidQuotes) {
        if (quotesSection) quotesSection.style.display = 'none';
        return;
    }
    
    let html = '<div class="row">';
    
    for (const [symbol, quote] of Object.entries(quotes)) {
        if (quote.error) continue;
        
        const changeClass = quote.change >= 0 ? 'text-success' : 'text-danger';
        const changeIcon = quote.change >= 0 ? 'fa-arrow-up' : 'fa-arrow-down';
        
        html += `
            <div class="col-md-4 mb-2">
                <div class="card border-0 shadow-sm">
                    <div class="card-body py-2">
                        <h6 class="card-title fw-bold mb-1">${symbol}</h6>
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="h6 mb-0">$${quote.current_price?.toFixed(2) || 'N/A'}</span>
                            <span class="${changeClass} small">
                                <i class="fas ${changeIcon}"></i>
                                ${quote.change_percent?.toFixed(2) || '0.00'}%
                            </span>
                        </div>
                        <small class="text-muted">
                            <i class="fas fa-clock me-1"></i>
                            ${new Date(quote.timestamp).toLocaleTimeString() || 'Live'}
                        </small>
                    </div>
                </div>
            </div>
        `;
    }
    
    html += '</div>';
    quotesContainer.innerHTML = html;
    
    // Show the quotes section
    if (quotesSection) quotesSection.style.display = 'block';
}

// Initialize live data when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Load market status immediately and then every 30 seconds
    loadMarketStatus();
    setInterval(loadMarketStatus, 30000);
    
    // Load live quotes when symbols change
    const symbolsInput = document.getElementById('symbols');
    if (symbolsInput) {
        symbolsInput.addEventListener('input', function() {
            clearTimeout(this.liveQuoteTimeout);
            this.liveQuoteTimeout = setTimeout(loadLiveQuotes, 1000); // Debounce
        });
        
        // Initial load if symbols are present
        if (symbolsInput.value.trim()) {
            setTimeout(loadLiveQuotes, 1000);
        }
    }
});

// Show all symbols modal
async function showAllSymbols() {
    try {
        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('symbolsModal'));
        modal.show();
        
        // Load symbols
        const response = await fetch('/api/symbols/available');
        const data = await response.json();
        
        let html = '';
        let selectedSymbols = new Set();
        
        for (const [category, symbols] of Object.entries(data.symbols)) {
            html += `
                <div class="mb-4">
                    <h6 class="fw-bold text-primary mb-3">
                        <i class="fas fa-folder me-2"></i>${category.toUpperCase()} (${Object.keys(symbols).length} symbols)
                    </h6>
                    <div class="row">
            `;
            
            for (const [symbol, name] of Object.entries(symbols)) {
                html += `
                    <div class="col-md-6 mb-2">
                        <div class="form-check">
                            <input class="form-check-input symbol-checkbox" type="checkbox" value="${symbol}" id="symbol_${symbol}">
                            <label class="form-check-label" for="symbol_${symbol}">
                                <strong>${symbol}</strong> - ${name}
                            </label>
                        </div>
                    </div>
                `;
            }
            
            html += `
                    </div>
                </div>
            `;
        }
        
        html += `
            <div class="mt-3 p-3 bg-light rounded">
                <h6 class="mb-2">Quick Actions:</h6>
                <button class="btn btn-sm btn-outline-primary me-2" onclick="selectCategory('TECHNOLOGY')">Select Tech</button>
                <button class="btn btn-sm btn-outline-success me-2" onclick="selectCategory('FINANCE')">Select Finance</button>
                <button class="btn btn-sm btn-outline-warning me-2" onclick="selectCategory('CRYPTOCURRENCY')">Select Crypto</button>
                <button class="btn btn-sm btn-outline-secondary" onclick="clearSymbolSelection()">Clear All</button>
            </div>
        `;
        
        document.getElementById('allSymbolsContent').innerHTML = html;
        
    } catch (error) {
        console.error('Error loading symbols:', error);
        document.getElementById('allSymbolsContent').innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Error loading symbols. Please try again.
            </div>
        `;
    }
}

// Add selected symbols to portfolio
function addSelectedSymbols() {
    const checkboxes = document.querySelectorAll('.symbol-checkbox:checked');
    const selectedSymbols = Array.from(checkboxes).map(cb => cb.value);
    
    if (selectedSymbols.length === 0) {
        showNotification('Please select at least one symbol', 'warning');
        return;
    }
    
    // Add to symbols input
    const symbolsInput = document.getElementById('symbols');
    const currentSymbols = symbolsInput.value.split(',').map(s => s.trim()).filter(s => s);
    
    // Merge with existing, avoiding duplicates
    const allSymbols = [...new Set([...currentSymbols, ...selectedSymbols])];
    symbolsInput.value = allSymbols.join(',');
    
    // Auto-generate equal weights
    const weightsInput = document.getElementById('weights');
    const equalWeight = (100 / allSymbols.length).toFixed(1);
    weightsInput.value = Array(allSymbols.length).fill(equalWeight).join(',');
    
    // Close modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('symbolsModal'));
    modal.hide();
    
    showNotification(`Added ${selectedSymbols.length} symbols to portfolio`, 'success');
    
    // Trigger validation and live quotes
    validatePortfolioInputs();
    setTimeout(loadLiveQuotes, 500);
}

// Select all symbols in a category
function selectCategory(category) {
    const checkboxes = document.querySelectorAll('.symbol-checkbox');
    checkboxes.forEach(checkbox => {
        const label = document.querySelector(`label[for="${checkbox.id}"]`);
        const labelText = label.textContent.toUpperCase();
        
        // Determine if this symbol belongs to the category
        let belongsToCategory = false;
        if (category === 'TECHNOLOGY' && ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX'].includes(checkbox.value)) {
            belongsToCategory = true;
        } else if (category === 'FINANCE' && ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'C'].includes(checkbox.value)) {
            belongsToCategory = true;
        } else if (category === 'CRYPTOCURRENCY' && checkbox.value.includes('/USD')) {
            belongsToCategory = true;
        }
        
        checkbox.checked = belongsToCategory;
    });
}

// Clear symbol selection
function clearSymbolSelection() {
    const checkboxes = document.querySelectorAll('.symbol-checkbox');
    checkboxes.forEach(checkbox => checkbox.checked = false);
}

// Make functions globally available
window.Utils = Utils;
window.ChartManager = ChartManager;
window.CONFIG = CONFIG;
window.addQuickSymbol = addQuickSymbol;
window.clearPortfolio = clearPortfolio;
window.loadSamplePortfolio = loadSamplePortfolio;
window.loadMarketStatus = loadMarketStatus;
window.loadLiveQuotes = loadLiveQuotes;
window.showAllSymbols = showAllSymbols;
window.addSelectedSymbols = addSelectedSymbols;
window.selectCategory = selectCategory;
window.clearSymbolSelection = clearSymbolSelection;
window.addAssetRow = addAssetRow;
window.removeAssetRow = removeAssetRow;
window.updatePortfolioData = updatePortfolioData;
window.updatePortfolioWithOptimizedWeights = updatePortfolioWithOptimizedWeights; 