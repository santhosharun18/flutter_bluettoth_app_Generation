document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('generateForm');
    const submitBtn = form?.querySelector('button[type="submit"]');
    
    if (form && submitBtn) {
        form.addEventListener('submit', function(e) {
            const prompt = document.getElementById('prompt').value.trim();
            
            if (!prompt) {
                e.preventDefault();
                alert('Please enter a description for your app');
                return;
            }
            
            if (prompt.length < 10) {
                e.preventDefault();
                alert('Please provide a more detailed description (at least 10 characters)');
                return;
            }
            
            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="btn-icon">⏳</span> Generating...';
        });
    }
    
    // Add some interactive features
    const promptTextarea = document.getElementById('prompt');
    if (promptTextarea) {
        // Example prompts
        const examples = [
            "Create a todo list app with add, delete, and mark complete features. Use a clean blue design.",
            "Build a simple calculator app with basic arithmetic operations and a modern purple theme.",
            "Make a weather app that shows current conditions with a beautiful green color scheme.",
            "Design a note-taking app with the ability to save and edit notes, using an orange theme."
        ];
        
        // Add placeholder cycling
        let exampleIndex = 0;
        setInterval(() => {
            if (promptTextarea.value === '') {
                promptTextarea.placeholder = examples[exampleIndex];
                exampleIndex = (exampleIndex + 1) % examples.length;
            }
        }, 3000);
    }
});

// Utility functions for progress tracking
function formatAgentName(agentKey) {
    const names = {
        'prompt_analyzer': 'Prompt Analysis',
        'architecture_designer': 'Architecture Design',
        'code_generator': 'Code Generation', 
        'build_automator': 'APK Building',
        'completed': 'Completed'
    };
    return names[agentKey] || agentKey;
}

function showNotification(message, type = 'info') {
    // Simple notification system
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: ${type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : '#4f46e5'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);
