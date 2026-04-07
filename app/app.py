from flask import Flask, request, jsonify, render_template_string
import mysql.connector
import os
import time

app = Flask(__name__)

# IMPROVED: Database connection with retry logic for DevOps environments
def get_db():
    retries = 10
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host=os.environ.get('DB_HOST', 'db'),
                user=os.environ.get('DB_USER', 'root'),
                password=os.environ.get('DB_PASSWORD', 'rootpassword'),
                database=os.environ.get('DB_NAME', 'student_db')
            )
            return conn
        except Exception as e:
            print(f"Database not ready. Retrying in 5 seconds... ({retries} attempts left)")
            retries -= 1
            time.sleep(5)
    raise Exception("Could not connect to the database after several attempts.")

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Information Portal</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 22px;
        }
        .container {
            width: 100%;
            max-width: 750px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #e94560;
            font-size: 2rem;
            letter-spacing: 1px;
        }
        .header p {
            color: #a8b2d8;
            margin-top: 8px;
            font-size: 0.95rem;
        }
        .university-badge {
            display: inline-block;
            background: rgba(233,69,96,0.15);
            color: #e94560;
            border: 1px solid #e94560;
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            margin-top: 10px;
            letter-spacing: 1px;
        }
        .search-card {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 24px;
        }
        .search-card label {
            display: block;
            color: #a8b2d8;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        .search-row {
            display: flex;
            gap: 12px;
        }
        .search-row input {
            flex: 1;
            padding: 14px 18px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 10px;
            color: #ffffff;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.3s;
        }
        .search-row input:focus {
            border-color: #e94560;
        }
        .search-row input::placeholder { color: #4a5568; }
        .search-row button {
            padding: 14px 28px;
            background: #e94560;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s, transform 0.1s;
        }
        .search-row button:hover { background: #c73652; }
        .search-row button:active { transform: scale(0.97); }

        .result-card {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 30px;
            display: none;
        }
        .student-header {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 24px;
            padding-bottom: 20px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .avatar {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            background: linear-gradient(135deg, #e94560, #0f3460);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            font-weight: bold;
            color: white;
            flex-shrink: 0;
        }
        .student-name { color: #ffffff; font-size: 1.5rem; font-weight: 700; }
        .reg-badge {
            display: inline-block;
            background: rgba(233,69,96,0.2);
            color: #e94560;
            border: 1px solid rgba(233,69,96,0.4);
            padding: 3px 12px;
            border-radius: 20px;
            font-size: 0.82rem;
            margin-top: 5px;
        }
        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-bottom: 20px;
        }
        .info-box {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 10px;
            padding: 16px;
        }
        .info-box .label {
            color: #a8b2d8;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 6px;
        }
        .info-box .value {
            color: #ffffff;
            font-size: 1.05rem;
            font-weight: 600;
        }
        .cgpa-value { color: #4ade80 !important; font-size: 1.4rem !important; }
        .section-title {
            color: #a8b2d8;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 12px;
        }
        .subjects-list { list-style: none; }
        .subjects-list li {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 14px;
            background: rgba(255,255,255,0.04);
            border-radius: 8px;
            margin-bottom: 8px;
            color: #cdd6f4;
            font-size: 0.92rem;
        }
        .grade-badge {
            background: rgba(74,222,128,0.15);
            color: #4ade80;
            border: 1px solid rgba(74,222,128,0.3);
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 0.82rem;
            font-weight: 600;
        }
        .error-msg {
            color: #e94560;
            text-align: center;
            padding: 20px;
            display: none;
        }
        .loading { color: #a8b2d8; text-align: center; padding: 10px; display: none; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🎓 Student Portal</h1>
        <p>Search student information by registration number</p>
        <span class="university-badge">COMSATS University Islamabad</span>
    </div>

    <div class="search-card">
        <label>Registration Number</label>
        <div class="search-row">
            <input type="text" id="regInput" placeholder="e.g. FA23-BCS-058" />
            <button onclick="searchStudent()">Search</button>
        </div>
    </div>

    <div class="loading" id="loading">Searching...</div>
    <div class="error-msg" id="error"></div>

    <div class="result-card" id="result">
        <div class="student-header">
            <div class="avatar" id="avatar"></div>
            <div>
                <div class="student-name" id="sname"></div>
                <div class="reg-badge" id="sreg"></div>
            </div>
        </div>
        <div class="info-grid">
            <div class="info-box">
                <div class="label">Semester</div>
                <div class="value" id="ssem"></div>
            </div>
            <div class="info-box">
                <div class="label">CGPA</div>
                <div class="value cgpa-value" id="scgpa"></div>
            </div>
        </div>
        <div class="section-title">Enrolled Subjects</div>
        <ul class="subjects-list" id="ssubjects"></ul>
    </div>
</div>

<script>
async function searchStudent() {
    const reg = document.getElementById('regInput').value.trim();
    if (!reg) return;

    document.getElementById('result').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    document.getElementById('loading').style.display = 'block';

    try {
        const res = await fetch(`/search?reg=${encodeURIComponent(reg)}`);
        const data = await res.json();
        document.getElementById('loading').style.display = 'none';

        if (data.error) {
            document.getElementById('error').textContent = data.error;
            document.getElementById('error').style.display = 'block';
        } else {
            const initials = data.first_name[0] + data.last_name[0];
            document.getElementById('avatar').textContent = initials;
            document.getElementById('sname').textContent = data.first_name + ' ' + data.last_name;
            document.getElementById('sreg').textContent = data.registration_number;
            document.getElementById('ssem').textContent = data.semester || 'N/A';
            document.getElementById('scgpa').textContent = data.cgpa || 'N/A';

            const ul = document.getElementById('ssubjects');
            ul.innerHTML = '';
            data.subjects.forEach(s => {
                ul.innerHTML += `<li><span>${s.subject_name}</span><span class="grade-badge">${s.grade || 'N/A'}</span></li>`;
            });
            document.getElementById('result').style.display = 'block';
        }
    } catch (e) {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('error').textContent = 'Server error. Please try again.';
        document.getElementById('error').style.display = 'block';
    }
}

document.getElementById('regInput').addEventListener('keydown', e => {
    if (e.key === 'Enter') searchStudent();
});
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/search')
def search():
    reg = request.args.get('reg', '').strip()
    if not reg:
        return jsonify({'error': 'Please enter a registration number.'})
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE registration_number = %s", (reg,))
        student = cursor.fetchone()
        if not student:
            return jsonify({'error': f'No student found with registration number: {reg}'})

        cursor.execute("SELECT subject_name, grade FROM subjects WHERE student_id = %s", (student['id'],))
        subjects = cursor.fetchall()

        cursor.execute("SELECT cgpa, semester FROM transcripts WHERE student_id = %s", (student['id'],))
        transcript = cursor.fetchone()

        conn.close()
        return jsonify({
            'first_name': student['first_name'],
            'last_name': student['last_name'],
            'registration_number': student['registration_number'],
            'cgpa': str(transcript['cgpa']) if transcript else 'N/A',
            'semester': transcript['semester'] if transcript else 'N/A',
            'subjects': subjects
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
