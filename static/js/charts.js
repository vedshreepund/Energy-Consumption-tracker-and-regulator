
// Common chart configuration
const chartConfig = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top',
        },
        tooltip: {
            mode: 'index',
            intersect: false,
        }
    },
    scales: {
        y: {
            beginAtZero: true,
            title: {
                display: true,
                text: 'Power Consumption (kWh)'
            }
        }
    }
};

// Color palette
const colors = {
    primary: '#2c8c99',
    secondary: '#42b883',
    accent: '#35495e',
    light: 'rgba(44, 140, 153, 0.2)'
};

// Create hourly consumption chart
function createHourlyChart(data) {
    const ctx = document.getElementById('hourlyChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(item => item.hour),
            datasets: [{
                label: 'Hourly Consumption',
                data: data.map(item => item.consumption),
                borderColor: colors.primary,
                backgroundColor: colors.light,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: colors.primary
            }]
        },
        options: {
            ...chartConfig,
            scales: {
                ...chartConfig.scales,
                x: {
                    title: {
                        display: true,
                        text: 'Time of Day'
                    }
                }
            }
        }
    });
}

// Create weekly consumption chart
function createWeeklyChart(data) {
    const ctx = document.getElementById('weeklyChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => {
                const date = new Date(item.date);
                return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
            }),
            datasets: [{
                label: 'Daily Consumption',
                data: data.map(item => item.consumption),
                backgroundColor: colors.secondary,
                borderColor: colors.accent,
                borderWidth: 1,
                borderRadius: 5
            }]
        },
        options: {
            ...chartConfig,
            scales: {
                ...chartConfig.scales,
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            }
        }
    });
}

// Create daily consumption chart
function createDailyChart(data) {
    const ctx = document.getElementById('dailyChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => {
                const date = new Date(item.date);
                return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
            }),
            datasets: [{
                label: 'Daily Consumption',
                data: data.map(item => item.consumption),
                backgroundColor: colors.secondary,
                borderColor: colors.accent,
                borderWidth: 1,
                borderRadius: 5
            }]
        },
        options: {
            ...chartConfig,
            scales: {
                ...chartConfig.scales,
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            }
        }
    });
}

// Create monthly consumption chart
function createMonthlyChart(data) {
    const ctx = document.getElementById('monthlyChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => item.month),
            datasets: [{
                label: 'Monthly Consumption',
                data: data.map(item => item.consumption),
                backgroundColor: colors.primary,
                borderColor: colors.accent,
                borderWidth: 1,
                borderRadius: 5
            }]
        },
        options: {
            ...chartConfig,
            scales: {
                ...chartConfig.scales,
                x: {
                    title: {
                        display: true,
                        text: 'Month'
                    }
                }
            }
        }
    });
}
