from flask import Flask, request, jsonify, render_template_string
import re

app = Flask(__name__)

# HTML-шаблон с формой для ввода данных
html_form = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Submission</title>
</head>
<body>
    <h1>Submit Your Data</h1>
    <form action="/submit" method="POST">
        <label for="name">Name (3-50 characters):</label><br>
        <input type="text" id="name" name="name" required><br><br>

        <label for="email">Email:</label><br>
        <input type="email" id="email" name="email" required><br><br>

        <label for="age">Age (18-100):</label><br>
        <input type="number" id="age" name="age" required><br><br>

        <label for="password">Password (min 8 characters, at least 1 letter and 1 number):</label><br>
        <input type="password" id="password" name="password" required><br><br>

        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""


# Главная страница с формой
@app.route('/', methods=['GET'])
def home():
    return render_template_string(html_form)


# Обработка данных с формы
@app.route('/submit', methods=['POST'])
def submit_data():
    # Получение данных из формы
    name = request.form.get('name')
    email = request.form.get('email')
    age = request.form.get('age')
    password = request.form.get('password')

    # Проверка поля 'name' (длина от 3 до 50 символов)
    if not isinstance(name, str) or not (3 <= len(name) <= 50):
        return jsonify({"error": "Invalid 'name'. It must be a string with 3 to 50 characters."}), 400

    # Проверка поля 'email' (валидный формат email)
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_pattern, email):
        return jsonify({"error": "Invalid 'email'. It must be a valid email address."}), 400

    # Проверка поля 'age' (должно быть числом от 18 до 100)
    if not age.isdigit() or not (18 <= int(age) <= 100):
        return jsonify({"error": "Invalid 'age'. It must be an integer between 18 and 100."}), 400

    # Проверка поля 'password' (минимум 8 символов, хотя бы одна буква и одна цифра)
    if len(password) < 8 or not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
        return jsonify({
                           "error": "Invalid 'password'. It must be at least 8 characters long and contain both letters and numbers."}), 400

    # Если все проверки пройдены
    return jsonify({"message": "All data is valid!"}), 200


if __name__ == '__main__':
    app.run(port=5000)