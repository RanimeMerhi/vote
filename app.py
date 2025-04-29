import gspread
from flask import Flask, render_template_string, request
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\ADMIN\Downloads\testvote-458317-e3c36e2b4ecd.json', scope)
client = gspread.authorize(creds)

# Your sheet name here
sheet = client.open("test-vote").sheet1

# Simple HTML form template
HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Vote</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f4f4f4;
            padding: 30px;
        }
        h2 {
            text-align: center;
            color: #333;
        }
        .form-container {
            max-width: 500px;
            margin: auto;
            background: #fff;
            padding: 25px 30px;
            border-radius: 14px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }

        .input-group {
            position: relative;
            margin-bottom: 25px;
        }

        .input-group input {
    width: 100%;
    padding: 14px 16px 14px 46px;
    border-radius: 12px;
    border: 1.5px solid #ccc;
    font-size: 15px;
    transition: 0.3s ease;
    box-sizing: border-box;
}

        .input-group input:focus {
            outline: none;
            border-color: #007BFF;
        }

        .input-group .icon {
            position: absolute;
            top: 50%;
            left: 12px;
            transform: translateY(-50%);
            color: #888;
        }

        .options {
            display: flex;
            justify-content: space-around;
            gap: 10px;
            margin-bottom: 25px;
        }

        .option-card {
            flex: 1;
            border: 2px solid #ccc;
            padding: 12px;
            border-radius: 12px;
            text-align: left;
            cursor: pointer;
            display: flex;
            align-items: center;
            transition: all 0.3s ease;
            background-color: #f9f9f9;
        }

        .option-card:hover {
            border-color: #007BFF;
            background: #e6f0ff;
        }

        .option-card input[type="radio"] {
            display: none;
        }

        .option-label {
            flex-grow: 1;
            font-size: 18px;
            padding-left: 10px;
        }

        .option-logo {
            width: 60px;
            height: 60px;
            object-fit: contain;
        }

        button {
            width: 100%;
            padding: 14px;
            font-size: 16px;
            background-color: #007BFF;
            border: none;
            color: white;
            border-radius: 10px;
            cursor: pointer;
            transition: background 0.3s ease;
        }

        button:hover {
            background-color: #0056b3;
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="form-container">
        <h2>Vote for an Option</h2>
        <form action="/submit" method="POST">
            
            <div class="input-group">
                <i class="fas fa-user icon"></i>
                <input type="text" name="name" placeholder="Your Name" required>
            </div>

            <div class="options">
                <label class="option-card">
                    <input type="radio" name="vote" value="Option A" required>
                    <div class="option-label">Option A</div>
                    <img src="https://play-lh.googleusercontent.com/vcmnPx61Y6vAWnnrzj6x6KoX27xrHTTVeC1RvxapxouWzJGY8kisn_MEzSHuHWfsNE8" alt="Option A Logo" class="option-logo">
                </label>
                <label class="option-card">
                    <input type="radio" name="vote" value="Option B" required>
                    <div class="option-label">Option B</div>
                    <img src="https://i0.wp.com/mid-east.info/wp-content/uploads/2016/11/olx-logo.jpg" alt="Option B Logo" class="option-logo">
                </label>
            </div>

            <button type="submit">Submit Vote</button>
        </form>
    </div>
</body>
</html>
"""



@app.route('/')
def index():
    return render_template_string(HTML_FORM)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    vote = request.form['vote']
    sheet.append_row([name, vote])
    return f"<h3>Thanks for voting, {name}!</h3>"

if __name__ == '__main__':
    app.run(debug=True)
