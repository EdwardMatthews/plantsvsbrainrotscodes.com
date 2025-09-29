// Filter codes functionality
function filterCodes(filter) {
    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');

    // Filter code rows
    const allCodes = document.querySelectorAll('.code-row');

    allCodes.forEach(code => {
        switch(filter) {
            case 'all':
                code.style.display = 'grid';
                break;
            case 'active':
                if (code.classList.contains('active-code')) {
                    code.style.display = 'grid';
                } else {
                    code.style.display = 'none';
                }
                break;
            case 'expired':
                if (code.classList.contains('expired-code')) {
                    code.style.display = 'grid';
                } else {
                    code.style.display = 'none';
                }
                break;
            case 'new':
                const statusElement = code.querySelector('.code-status');
                if (statusElement && statusElement.classList.contains('new')) {
                    code.style.display = 'grid';
                } else {
                    code.style.display = 'none';
                }
                break;
        }
    });

    // Show/hide sections based on filter
    const sectionsToToggle = document.querySelectorAll('.codes-section');
    if (filter === 'expired') {
        sectionsToToggle.forEach(section => {
            if (section.querySelector('h2').textContent.includes('Expired')) {
                section.style.display = 'block';
            } else {
                section.style.display = 'none';
            }
        });
    } else if (filter === 'active' || filter === 'new') {
        sectionsToToggle.forEach(section => {
            if (section.querySelector('h2').textContent.includes('Active')) {
                section.style.display = 'block';
            } else {
                section.style.display = 'none';
            }
        });
    } else {
        sectionsToToggle.forEach(section => {
            section.style.display = 'block';
        });
    }
}

// Enhanced copy functionality for codes page
document.addEventListener('DOMContentLoaded', function() {
    // Add click tracking for codes
    document.querySelectorAll('.copy-code-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const codeRow = this.closest('.code-row');
            const codeText = codeRow.querySelector('.code-text').textContent;

            // Visual feedback
            this.textContent = 'Copied!';
            this.classList.add('copied');

            // Track usage
            trackCodeInteraction(codeText, 'copy');

            // Reset button after delay
            setTimeout(() => {
                this.textContent = 'Copy';
                this.classList.remove('copied');
            }, 2000);
        });
    });

    // Add hover effects to code rows
    document.querySelectorAll('.code-row').forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 5px 15px rgba(124, 58, 237, 0.2)';
        });

        row.addEventListener('mouseleave', function() {
            this.style.boxShadow = 'none';
        });
    });

    // Auto-check for new codes (mock)
    checkForNewCodes();
});

// Track code interactions
function trackCodeInteraction(code, action) {
    // Analytics tracking would go here
    console.log(`Code ${action}: ${code}`);

    // Store in local storage for user history
    const history = JSON.parse(localStorage.getItem('codeHistory') || '[]');
    history.push({
        code: code,
        action: action,
        timestamp: new Date().toISOString()
    });
    localStorage.setItem('codeHistory', JSON.stringify(history.slice(-50))); // Keep last 50 interactions
}

// Check for new codes (mock implementation)
function checkForNewCodes() {
    // In production, this would check an API
    const lastCheck = localStorage.getItem('lastCodeCheck');
    const now = new Date().getTime();

    if (!lastCheck || now - parseInt(lastCheck) > 3600000) { // Check every hour
        console.log('Checking for new codes...');
        localStorage.setItem('lastCodeCheck', now.toString());

        // Mock: Show notification if "new" codes found
        if (Math.random() > 0.8) { // 20% chance to show notification
            showNewCodesNotification();
        }
    }
}

// Show notification for new codes
function showNewCodesNotification() {
    const notification = document.createElement('div');
    notification.className = 'new-codes-notification';
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-icon">🎉</span>
            <span class="notification-text">New codes available! Refresh to see the latest codes.</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        z-index: 10000;
        animation: slideInRight 0.5s ease;
        max-width: 350px;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.5s ease';
        setTimeout(() => {
            notification.remove();
        }, 500);
    }, 5000);
}

// Search functionality for codes
function searchCodes(query) {
    const lowerQuery = query.toLowerCase();
    document.querySelectorAll('.code-row').forEach(row => {
        const codeText = row.querySelector('.code-text').textContent.toLowerCase();
        const rewardText = row.querySelector('.code-reward').textContent.toLowerCase();

        if (codeText.includes(lowerQuery) || rewardText.includes(lowerQuery)) {
            row.style.display = 'grid';
        } else {
            row.style.display = 'none';
        }
    });
}

// Sort codes by date
function sortCodesByDate(order = 'newest') {
    const codesContainer = document.querySelector('.codes-table');
    const codeRows = Array.from(document.querySelectorAll('.code-row'));

    codeRows.sort((a, b) => {
        const dateA = new Date(a.querySelector('.code-date').textContent.replace('Added: ', ''));
        const dateB = new Date(b.querySelector('.code-date').textContent.replace('Added: ', ''));

        return order === 'newest' ? dateB - dateA : dateA - dateB;
    });

    // Re-append sorted elements
    codeRows.forEach(row => {
        codesContainer.appendChild(row);
    });
}