from PBD_config import app
from flask import request, render_template

from Routes.Users import user
from Routes.Pets import pet
from Routes.Behavior import video

app.register_blueprint(user,url_prefix="/user")

app.register_blueprint(pet,url_prefix="/pet")

app.register_blueprint(video,url_prefix="/video")
app.secret_key = 'doxjjarjeh3die'

#...

@app.route('/')
def home():
    # 获取闪现消息
    message = request.args.get('message')
    return render_template('login.html', message=message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)