<!doctype html>
<html lang="en">
 <head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NeuronNova - AI Learning Companion</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      width: 100%;
      height: 100%;
      background-color: #f8f9fa;
      overflow-x: hidden;
    }
    
    html {
      height: 100%;
      width: 100%;
    }
    
    .gradient-bg {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .card-hover {
      transition: all 0.3s ease;
    }
    
    .card-hover:hover {
      transform: translateY(-4px);
      box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    }
    
    .subject-card {
      cursor: pointer;
      border: 2px solid transparent;
      transition: all 0.3s ease;
    }
    
    .subject-card:hover {
      border-color: #667eea;
      transform: scale(1.02);
    }
    
    .progress-bar {
      transition: width 0.3s ease;
    }
    
    .fade-in {
      animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    .loading-spinner {
      border: 3px solid #f3f4f6;
      border-top: 3px solid #667eea;
      border-radius: 50%;
      width: 24px;
      height: 24px;
      animation: spin 1s linear infinite;
      margin: 0 auto;
    }
    
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    
    .btn-primary {
      transition: all 0.2s ease;
    }
    
    .btn-primary:hover:not(:disabled) {
      transform: scale(1.02);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .btn-primary:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
    
    #app {
      width: 100%;
      min-height: 100vh;
    }
  </style>
  <style>@view-transition { navigation: auto; }</style>
  <script src="/_sdk/data_sdk.js" type="text/javascript"></script>
  <script src="/_sdk/element_sdk.js" type="text/javascript"></script>
 </head>
 <body>
  <div id="app"></div>
  <script>
    // Configuration
    const config = {
      platformName: "NeuronNova",
      tagline: "Your AI Learning Companion",
      welcomeMessage: "Welcome back! Ready to learn?",
      assignmentLabel: "Assignments",
      worksheetLabel: "Practice Worksheets",
      backgroundColor: "#f8f9fa",
      primaryColor: "#667eea",
      secondaryColor: "#ffffff",
      textColor: "#1f2937",
      accentColor: "#764ba2"
    };
    
    // State management
    let currentView = 'login';
    let currentUser = '';
    let selectedSubject = '';
    let selectedClass = '';
    let userActivities = [];

    // Subject data
    const subjects = {
      mathematics: {
        name: 'Mathematics',
        icon: '🔢',
        color: '#3b82f6',
        topics: ['Algebra', 'Geometry', 'Trigonometry', 'Calculus', 'Statistics', 'Number Theory']
      },
      science: {
        name: 'Science',
        icon: '🔬',
        color: '#10b981',
        topics: ['Physics', 'Chemistry', 'Biology', 'Environmental Science', 'Astronomy']
      },
      english: {
        name: 'English',
        icon: '📚',
        color: '#f59e0b',
        topics: ['Grammar', 'Literature', 'Writing', 'Comprehension', 'Vocabulary', 'Poetry']
      }
    };

    // Initialize app
    function initApp() {
      // Load activities from localStorage
      const stored = localStorage.getItem('neuronNovaActivities');
      if (stored) {
        try {
          userActivities = JSON.parse(stored);
        } catch (e) {
          userActivities = [];
        }
      }
      renderCurrentView();
    }

    function saveActivities() {
      localStorage.setItem('neuronNovaActivities', JSON.stringify(userActivities));
    }

    function renderCurrentView() {
      if (currentView === 'login') {
        renderLogin();
      } else if (currentView === 'dashboard') {
        renderDashboard();
      } else if (currentView === 'subject') {
        renderSubjectView();
      }
    }

    function renderLogin() {
      const app = document.getElementById('app');
      app.innerHTML = `
        <div class="w-full min-h-screen flex items-center justify-center p-6" style="background-color: ${config.backgroundColor};">
          <div class="w-full max-w-md">
            <div class="fade-in rounded-2xl shadow-2xl p-8" style="background-color: ${config.secondaryColor};">
              <div class="text-center mb-8">
                <div class="text-6xl mb-4">🧠</div>
                <h1 class="text-4xl font-bold mb-2" style="color: ${config.textColor};">${config.platformName}</h1>
                <p class="text-lg" style="color: ${config.textColor}; opacity: 0.7;">${config.tagline}</p>
              </div>
              
              <form id="loginForm" onsubmit="event.preventDefault(); handleLogin();">
                <div class="mb-4">
                  <label for="username" class="block mb-2 font-medium" style="color: ${config.textColor};">Username</label>
                  <input 
                    type="text" 
                    id="username" 
                    required 
                    class="w-full px-4 py-3 rounded-lg border-2 focus:outline-none transition-colors"
                    style="border-color: #e5e7eb; background-color: ${config.backgroundColor}; color: ${config.textColor};"
                    placeholder="Enter your username"
                  >
                </div>
                
                <div class="mb-6">
                  <label for="password" class="block mb-2 font-medium" style="color: ${config.textColor};">Password</label>
                  <input 
                    type="password" 
                    id="password" 
                    required 
                    class="w-full px-4 py-3 rounded-lg border-2 focus:outline-none transition-colors"
                    style="border-color: #e5e7eb; background-color: ${config.backgroundColor}; color: ${config.textColor};"
                    placeholder="Enter your password"
                  >
                </div>
                
                <div id="loginMessage" class="mb-4 p-3 rounded-lg text-center" style="display: none;"></div>
                
                <button 
                  type="submit" 
                  id="loginButton" 
                  class="btn-primary w-full py-3 rounded-lg font-semibold text-white"
                  style="background-color: ${config.primaryColor};"
                >
                  Sign In
                </button>
              </form>
              
              <p class="text-center mt-6 text-sm" style="color: ${config.textColor}; opacity: 0.5;">Demo: Use any username/password to continue</p>
            </div>
          </div>
        </div>
      `;
    }

    function handleLogin() {
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;
      const messageEl = document.getElementById('loginMessage');
      const buttonEl = document.getElementById('loginButton');
      
      if (username && password) {
        buttonEl.innerHTML = '<div class="loading-spinner"></div>';
        buttonEl.disabled = true;
        
        setTimeout(() => {
          currentUser = username;
          currentView = 'dashboard';
          renderCurrentView();
        }, 1000);
      } else {
        messageEl.style.display = 'block';
        messageEl.style.backgroundColor = '#fee2e2';
        messageEl.style.color = '#991b1b';
        messageEl.textContent = 'Please enter both username and password';
      }
    }

    function renderDashboard() {
      const app = document.getElementById('app');
      const recentActivities = userActivities.slice(-5).reverse();
      const completedCount = userActivities.filter(a => a.completed).length;
      
      app.innerHTML = `
        <div class="w-full" style="min-height: 100vh; background-color: ${config.backgroundColor};">
          <div class="gradient-bg text-white p-6 shadow-lg" style="background: linear-gradient(135deg, ${config.primaryColor} 0%, ${config.accentColor} 100%);">
            <div class="max-w-7xl mx-auto">
              <div class="flex justify-between items-center flex-wrap gap-4">
                <div>
                  <h1 class="text-3xl font-bold mb-2">${config.welcomeMessage}</h1>
                  <p class="text-lg opacity-90">Hello, ${currentUser}! 👋</p>
                </div>
                <button 
                  onclick="logout()" 
                  class="px-6 py-2 rounded-lg bg-white bg-opacity-20 hover:bg-opacity-30 transition-all font-medium"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
          
          <div class="max-w-7xl mx-auto p-6 md:p-8">
            <div class="mb-12">
              <h2 class="text-2xl font-bold mb-6" style="color: ${config.textColor};">Choose Your Subject</h2>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                ${Object.entries(subjects).map(([key, subject]) => `
                  <div 
                    onclick="selectSubject('${key}')" 
                    class="subject-card rounded-xl p-6 shadow-lg card-hover"
                    style="background-color: ${config.secondaryColor};"
                  >
                    <div class="text-5xl mb-4">${subject.icon}</div>
                    <h3 class="text-xl font-bold mb-2" style="color: ${config.textColor};">${subject.name}</h3>
                    <p style="color: ${config.textColor}; opacity: 0.7;">${subject.topics.length} topics available</p>
                  </div>
                `).join('')}
              </div>
            </div>
            
            ${recentActivities.length > 0 ? `
              <div class="mb-12">
                <h2 class="text-2xl font-bold mb-6" style="color: ${config.textColor};">Recent Activity</h2>
                <div class="rounded-xl shadow-lg p-6" style="background-color: ${config.secondaryColor};">
                  ${recentActivities.map(activity => `
                    <div class="flex items-center justify-between py-4 border-b last:border-0" style="border-color: ${config.backgroundColor};">
                      <div class="flex items-center gap-4">
                        <div class="text-3xl">${subjects[activity.subject]?.icon || '📝'}</div>
                        <div>
                          <p class="font-semibold" style="color: ${config.textColor};">${activity.title}</p>
                          <p class="text-sm" style="color: ${config.textColor}; opacity: 0.6;">${subjects[activity.subject]?.name || activity.subject}</p>
                        </div>
                      </div>
                      <div class="text-right">
                        ${activity.completed 
                          ? `<span class="px-3 py-1 rounded-full text-white bg-green-500 text-sm font-medium">✓ Completed</span>` 
                          : `<span class="px-3 py-1 rounded-full text-sm font-medium" style="background-color: ${config.backgroundColor}; color: ${config.textColor};">In Progress</span>`
                        }
                        ${activity.score ? `<p class="text-sm mt-1" style="color: ${config.textColor}; opacity: 0.7;">Score: ${activity.score}%</p>` : ''}
                      </div>
                    </div>
                  `).join('')}
                </div>
              </div>
            ` : ''}
            
            <div>
              <h2 class="text-2xl font-bold mb-6" style="color: ${config.textColor};">Your Progress</h2>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="rounded-xl shadow-lg p-6" style="background-color: ${config.secondaryColor};">
                  <div class="flex items-center justify-between mb-3">
                    <p class="font-semibold" style="color: ${config.textColor};">Activities Completed</p>
                    <p class="text-3xl font-bold" style="color: ${config.primaryColor};">${completedCount}</p>
                  </div>
                  <div class="w-full rounded-full h-3" style="background-color: ${config.backgroundColor};">
                    <div 
                      class="progress-bar h-3 rounded-full" 
                      style="width: ${userActivities.length > 0 ? (completedCount / userActivities.length * 100) : 0}%; background-color: ${config.primaryColor};"
                    ></div>
                  </div>
                </div>
                
                <div class="rounded-xl shadow-lg p-6" style="background-color: ${config.secondaryColor};">
                  <div class="flex items-center justify-between mb-3">
                    <p class="font-semibold" style="color: ${config.textColor};">Total Activities</p>
                    <p class="text-3xl font-bold" style="color: ${config.primaryColor};">${userActivities.length}</p>
                  </div>
                  <p style="color: ${config.textColor}; opacity: 0.7;">Keep up the great work!</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    function selectSubject(subject) {
      selectedSubject = subject;
      currentView = 'subject';
      renderCurrentView();
    }

    function renderSubjectView() {
      const app = document.getElementById('app');
      const subject = subjects[selectedSubject];
      
      app.innerHTML = `
        <div class="w-full" style="min-height: 100vh; background-color: ${config.backgroundColor};">
          <div class="gradient-bg text-white p-6 shadow-lg" style="background: linear-gradient(135deg, ${config.primaryColor} 0%, ${config.accentColor} 100%);">
            <div class="max-w-7xl mx-auto">
              <button 
                onclick="backToDashboard()" 
                class="mb-4 px-4 py-2 rounded-lg bg-white bg-opacity-20 hover:bg-opacity-30 transition-all font-medium"
              >
                ← Back to Dashboard
              </button>
              <div class="flex items-center gap-4">
                <div class="text-6xl">${subject.icon}</div>
                <div>
                  <h1 class="text-3xl font-bold mb-2">${subject.name}</h1>
                  <p class="text-lg opacity-90">Master the fundamentals and beyond</p>
                </div>
              </div>
            </div>
          </div>
          
          <div class="max-w-7xl mx-auto p-6 md:p-8">
            <div class="mb-8">
              <label for="classSelect" class="block text-xl font-semibold mb-3" style="color: ${config.textColor};">Select Your Class</label>
              <select 
                id="classSelect" 
                onchange="selectClass(this.value)" 
                class="px-4 py-3 rounded-lg border-2 focus:outline-none min-w-64"
                style="border-color: #e5e7eb; background-color: ${config.secondaryColor}; color: ${config.textColor};"
              >
                <option value="">Choose class...</option>
                ${[6, 7, 8, 9, 10, 11, 12].map(cls => `<option value="${cls}">Class ${cls}</option>`).join('')}
              </select>
            </div>
            
            <div id="topicsSection" style="display: none;">
              <div class="mb-12">
                <h2 class="text-2xl font-bold mb-6" style="color: ${config.textColor};">Core Topics</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  ${subject.topics.map((topic, idx) => `
                    <div 
                      class="rounded-xl p-5 shadow-lg card-hover cursor-pointer" 
                      style="background-color: ${config.secondaryColor};"
                      onclick="startLesson('${topic}', 'lesson')"
                    >
                      <div class="flex items-center justify-between">
                        <div class="flex items-center gap-4">
                          <div 
                            class="w-12 h-12 rounded-full flex items-center justify-center font-bold text-white text-lg" 
                            style="background-color: ${config.primaryColor};"
                          >
                            ${idx + 1}
                          </div>
                          <div>
                            <h3 class="font-semibold text-lg" style="color: ${config.textColor};">${topic}</h3>
                            <p class="text-sm" style="color: ${config.textColor}; opacity: 0.6;">Interactive lesson</p>
                          </div>
                        </div>
                        <div class="text-2xl">▶</div>
                      </div>
                    </div>
                  `).join('')}
                </div>
              </div>
              
              <div class="mb-12">
                <h2 class="text-2xl font-bold mb-6" style="color: ${config.textColor};">${config.worksheetLabel}</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  ${subject.topics.slice(0, 3).map(topic => `
                    <div 
                      class="rounded-xl p-5 shadow-lg card-hover cursor-pointer" 
                      style="background-color: ${config.secondaryColor};"
                      onclick="startLesson('${topic}', 'worksheet')"
                    >
                      <div class="flex items-center justify-between">
                        <div class="flex items-center gap-4">
                          <div class="text-4xl">📝</div>
                          <div>
                            <h3 class="font-semibold text-lg" style="color: ${config.textColor};">${topic} Practice</h3>
                            <p class="text-sm" style="color: ${config.textColor}; opacity: 0.6;">10 practice problems</p>
                          </div>
                        </div>
                        <div class="text-2xl">→</div>
                      </div>
                    </div>
                  `).join('')}
                </div>
              </div>
              
              <div>
                <h2 class="text-2xl font-bold mb-6" style="color: ${config.textColor};">${config.assignmentLabel}</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  ${subject.topics.slice(0, 2).map((topic, idx) => `
                    <div 
                      class="rounded-xl p-5 shadow-lg card-hover cursor-pointer" 
                      style="background-color: ${config.secondaryColor};"
                      onclick="startLesson('${topic}', 'assignment')"
                    >
                      <div class="flex items-center justify-between">
                        <div class="flex items-center gap-4">
                          <div class="text-4xl">✍️</div>
                          <div>
                            <h3 class="font-semibold text-lg" style="color: ${config.textColor};">Assignment ${idx + 1}: ${topic}</h3>
                            <p class="text-sm" style="color: ${config.textColor}; opacity: 0.6;">Due in 7 days</p>
                          </div>
                        </div>
                        <div class="text-2xl">→</div>
                      </div>
                    </div>
                  `).join('')}
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    function selectClass(classNum) {
      selectedClass = classNum;
      const topicsSection = document.getElementById('topicsSection');
      if (classNum) {
        topicsSection.style.display = 'block';
        topicsSection.classList.add('fade-in');
      } else {
        topicsSection.style.display = 'none';
      }
    }

    function startLesson(topic, type) {
      const activity = {
        id: Date.now().toString(),
        type: type,
        subject: selectedSubject,
        title: `${type === 'lesson' ? 'Lesson' : type === 'worksheet' ? 'Worksheet' : 'Assignment'}: ${topic}`,
        completed: false,
        score: null,
        timestamp: new Date().toISOString()
      };
      
      userActivities.push(activity);
      saveActivities();
      showMessage(`Started ${activity.title}! This is tracked in your progress.`, 'success');
    }

    function showMessage(text, type) {
      const messageDiv = document.createElement('div');
      messageDiv.className = 'fixed top-6 right-6 px-6 py-4 rounded-lg shadow-xl fade-in text-white font-medium';
      messageDiv.style.backgroundColor = type === 'success' ? '#10b981' : '#ef4444';
      messageDiv.style.zIndex = '1000';
      messageDiv.textContent = text;
      
      document.body.appendChild(messageDiv);
      
      setTimeout(() => {
        messageDiv.style.opacity = '0';
        messageDiv.style.transition = 'opacity 0.3s ease';
        setTimeout(() => messageDiv.remove(), 300);
      }, 3000);
    }

    function backToDashboard() {
      currentView = 'dashboard';
      selectedSubject = '';
      selectedClass = '';
      renderCurrentView();
    }

    function logout() {
      currentView = 'login';
      currentUser = '';
      selectedSubject = '';
      selectedClass = '';
      renderCurrentView();
    }

    // Initialize on page load
    window.addEventListener('DOMContentLoaded', initApp);
  </script>
 <script>(function(){function c(){var b=a.contentDocument||a.contentWindow.document;if(b){var d=b.createElement('script');d.innerHTML="window.__CF$cv$params={r:'9a4e5c737550a734',t:'MTc2NDIxMjI3OS4wMDAwMDA='};var a=document.createElement('script');a.nonce='';a.src='/cdn-cgi/challenge-platform/scripts/jsd/main.js';document.getElementsByTagName('head')[0].appendChild(a);";b.getElementsByTagName('head')[0].appendChild(d)}}if(document.body){var a=document.createElement('iframe');a.height=1;a.width=1;a.style.position='absolute';a.style.top=0;a.style.left=0;a.style.border='none';a.style.visibility='hidden';document.body.appendChild(a);if('loading'!==document.readyState)c();else if(window.addEventListener)document.addEventListener('DOMContentLoaded',c);else{var e=document.onreadystatechange||function(){};document.onreadystatechange=function(b){e(b);'loading'!==document.readyState&&(document.onreadystatechange=e,c())}}}})();</script></body>
</html>
