from flask import Flask, render_template, request
import os

app = Flask(__name__)

FILES_PATH = 'static/users_files'


if not os.path.exists(FILES_PATH):
    os.makedirs(FILES_PATH)

@app.route('/', methods=['GET', 'POST'])
def f_page_1():
    if request.method == 'GET':
        return render_template('index.html')

    user_file = request.files.get('user_file')
    file_desc = request.form.get('file_desc')

    if user_file and user_file.filename.endswith('.txt'):
        file_path = os.path.join(FILES_PATH, user_file.filename)
        user_file.save(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            return render_template('index.html', message='Файл успішно завантажено!', content=file_content)
        except Exception as e:
            return render_template('index.html', message=f'Помилка читання файлу: {str(e)}')
    else:
        return render_template('index.html', message='Будь ласка, завантажте текстовий файл (.txt)')

if __name__ == '__main__':
    app.run(debug=True)