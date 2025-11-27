<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Tutor for Vocational Streams</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1 id="app-title">AI Tutor for Vocational Streams</h1>

        <div id="login-section" class="form-section">
            <h2>Login</h2>
            <label for="username">Username:</label>
            <input type="text" id="username" placeholder="Enter your username" required>
            
            <label for="password">Password:</label>
            <input type="password" id="password" placeholder="Enter your password" required>

            <button id="login-btn">Login</button>

            <p id="login-error" class="error"></p>
        </div>

        <div id="content-section" class="form-section" style="display: none;">
            <h2>Welcome, <span id="user-name"></span>!</h2>

            <label for="language-select">Select Language:</label>
            <select id="language-select">
                <option value="en">English</option>
                <option value="es">Spanish</option>
            </select>

            <label for="stream-select">Select Vocational Stream:</label>
            <select id="stream-select">
                <option value="IT">IT</option>
                <option value="Engineering">Engineering</option>
                <option value="Healthcare">Healthcare</option>
            </select>

            <div id="stream-description" class="stream-description"></div>

            <button id="logout-btn">Logout</button>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>



