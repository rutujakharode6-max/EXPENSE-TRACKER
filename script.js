// State
let expenses = JSON.parse(localStorage.getItem('expenses')) || [];
let monthlyBudget = parseFloat(localStorage.getItem('monthlyBudget')) || 1000.00;

// Pastel Colors defined in requirements
const colors = {
    pink: '#FFB3BA',
    green: '#BAFFC9',
    blue: '#BAE1FF',
    yellow: '#FFFFBA',
    purple: '#E6B3FF',
    orange: '#FFDFBA'
};

const categoryColors = {
    'Food': colors.pink,
    'Transport': colors.blue,
    'Shopping': colors.purple,
    'Utilities': colors.yellow,
    'Entertainment': colors.green,
    'Other': colors.orange
};

const categoryIcons = {
    'Food': 'ph-hamburger',
    'Transport': 'ph-car',
    'Shopping': 'ph-shopping-bag',
    'Utilities': 'ph-lightning',
    'Entertainment': 'ph-game-controller',
    'Other': 'ph-dots-three-circle'
};

// DOM Elements
const expenseForm = document.getElementById('expense-form');
const expenseList = document.getElementById('expense-list');
const totalSpentEl = document.getElementById('total-spent');
const budgetAmountEl = document.getElementById('budget-amount');
const budgetProgressEl = document.getElementById('budget-progress');

// Modal Elements
const setBudgetBtn = document.getElementById('set-budget-btn');
const budgetModal = document.getElementById('budget-modal');
const saveBudgetBtn = document.getElementById('save-budget');
const cancelBudgetBtn = document.getElementById('cancel-budget');
const newBudgetInput = document.getElementById('new-budget');

// Chart instances
let lineChartInstance = null;
let barChartInstance = null;

// Initialize
function init() {
    // Set default date to today
    document.getElementById('date').valueAsDate = new Date();
    
    updateUI();
    initCharts();
    setupEventListeners();
}

// Event Listeners
function setupEventListeners() {
    expenseForm.addEventListener('submit', addExpense);
    
    setBudgetBtn.addEventListener('click', () => {
        newBudgetInput.value = monthlyBudget;
        budgetModal.classList.remove('hidden');
    });
    
    cancelBudgetBtn.addEventListener('click', () => {
        budgetModal.classList.add('hidden');
    });
    
    saveBudgetBtn.addEventListener('click', () => {
        const newBudget = parseFloat(newBudgetInput.value);
        if (!isNaN(newBudget) && newBudget > 0) {
            monthlyBudget = newBudget;
            localStorage.setItem('monthlyBudget', monthlyBudget);
            updateUI();
            budgetModal.classList.add('hidden');
        }
    });
}

// Add Expense
function addExpense(e) {
    e.preventDefault();
    
    const desc = document.getElementById('desc').value;
    const amount = parseFloat(document.getElementById('amount').value);
    const category = document.getElementById('category').value;
    const date = document.getElementById('date').value;
    
    if (!desc || isNaN(amount) || !category || !date) return;
    
    const expense = {
        id: Date.now().toString(),
        desc,
        amount,
        category,
        date
    };
    
    expenses.push(expense);
    saveData();
    updateUI();
    updateCharts();
    
    // Reset form except date
    document.getElementById('desc').value = '';
    document.getElementById('amount').value = '';
    document.getElementById('category').selectedIndex = 0;
}

// Delete Expense
function deleteExpense(id) {
    expenses = expenses.filter(exp => exp.id !== id);
    saveData();
    updateUI();
    updateCharts();
}

// Save to LocalStorage
function saveData() {
    localStorage.setItem('expenses', JSON.stringify(expenses));
}

// Update UI (List & Budget)
function updateUI() {
    // Clear list
    expenseList.innerHTML = '';
    
    // Sort expenses by date descending
    const sortedExpenses = [...expenses].sort((a, b) => new Date(b.date) - new Date(a.date));
    
    let total = 0;
    
    sortedExpenses.forEach(exp => {
        total += exp.amount;
        
        const li = document.createElement('li');
        li.className = 'expense-item';
        
        const iconClass = categoryIcons[exp.category] || categoryIcons['Other'];
        const bgColor = categoryColors[exp.category] || colors.pink;
        
        li.innerHTML = `
            <div class="item-icon" style="background-color: ${bgColor}80; color: #555;">
                <i class="ph ${iconClass}"></i>
            </div>
            <div class="item-details">
                <div class="item-title">${exp.desc}</div>
                <div class="item-date">${exp.date} &bull; ${exp.category}</div>
            </div>
            <div class="item-amount" style="color: ${bgColor}">$${exp.amount.toFixed(2)}</div>
            <button class="delete-btn" onclick="deleteExpense('${exp.id}')">
                <i class="ph ph-trash"></i>
            </button>
        `;
        
        expenseList.appendChild(li);
    });
    
    // Update totals
    totalSpentEl.textContent = `Total: $${total.toFixed(2)}`;
    budgetAmountEl.textContent = `$${monthlyBudget.toFixed(2)}`;
    
    // Update progress bar
    const progressPercent = Math.min((total / monthlyBudget) * 100, 100);
    budgetProgressEl.style.width = `${progressPercent}%`;
    
    if (progressPercent > 90) {
        budgetProgressEl.style.background = 'linear-gradient(90deg, #FFB3BA, #FF9A9E)'; // Red-ish if close to budget
    } else {
        budgetProgressEl.style.background = 'linear-gradient(90deg, var(--pastel-green), var(--pastel-blue))';
    }
}

// Charts Initialization
function initCharts() {
    Chart.defaults.font.family = "'Outfit', sans-serif";
    Chart.defaults.color = '#7A7A7A';
    updateCharts();
}

function updateCharts() {
    // Process Data for Bar Chart (Category Breakdown)
    const categoryTotals = {};
    expenses.forEach(exp => {
        categoryTotals[exp.category] = (categoryTotals[exp.category] || 0) + exp.amount;
    });
    
    const barLabels = Object.keys(categoryTotals);
    const barData = Object.values(categoryTotals);
    const barColors = barLabels.map(label => categoryColors[label] || colors.pink);
    
    // Process Data for Line Chart (Trends)
    // Group by date, last 7 days with data
    const dateTotals = {};
    expenses.forEach(exp => {
        dateTotals[exp.date] = (dateTotals[exp.date] || 0) + exp.amount;
    });
    
    const sortedDates = Object.keys(dateTotals).sort();
    const lineLabels = sortedDates;
    const lineData = sortedDates.map(date => dateTotals[date]);
    
    // Render Bar Chart
    const ctxBar = document.getElementById('barChart').getContext('2d');
    if (barChartInstance) barChartInstance.destroy();
    
    barChartInstance = new Chart(ctxBar, {
        type: 'doughnut',
        data: {
            labels: barLabels,
            datasets: [{
                data: barData,
                backgroundColor: barColors,
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: { boxWidth: 12, usePointStyle: true }
                }
            },
            cutout: '70%'
        }
    });
    
    // Render Line Chart
    const ctxLine = document.getElementById('lineChart').getContext('2d');
    
    // Create gradient
    let gradient = ctxLine.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(186, 225, 255, 0.5)'); // pastel blue
    gradient.addColorStop(1, 'rgba(186, 225, 255, 0.0)');
    
    if (lineChartInstance) lineChartInstance.destroy();
    
    lineChartInstance = new Chart(ctxLine, {
        type: 'line',
        data: {
            labels: lineLabels.length ? lineLabels : ['No Data'],
            datasets: [{
                label: 'Daily Expenses',
                data: lineData.length ? lineData : [0],
                borderColor: colors.blue,
                backgroundColor: gradient,
                borderWidth: 3,
                pointBackgroundColor: colors.pink,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5,
                fill: true,
                tension: 0.4 // Smooth curves
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { borderDash: [5, 5], color: 'rgba(0,0,0,0.05)' },
                    border: { display: false }
                },
                x: {
                    grid: { display: false },
                    border: { display: false }
                }
            }
        }
    });
}

// Start App
init();
