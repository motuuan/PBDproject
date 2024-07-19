# routes/video_feed.py
from flask import Blueprint, Response, session, jsonify, render_template, redirect, url_for
from Service.Behavior import gen_frames, gain_records
from Model.Behavior import Behavior
from PBD_config import db_init as db
from sqlalchemy import func
from datetime import datetime,timedelta

video = Blueprint('video', __name__)


@video.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    owner = session['Uid']
    return Response(gen_frames(owner), mimetype='multipart/x-mixed-replace; boundary=frame')


@video.route('/behave_piechart', methods=['GET', 'POST'])
def behave_piechart():
    behavior_counts = db.session.query(Behavior.Bclass, db.func.count(Behavior.Bclass).label('count')).group_by(
        Behavior.Bclass).all()
    data = {bclass: count for bclass, count in behavior_counts}
    return jsonify(data)


@video.route('/behavior_linechart', methods=['GET', 'POST'])
def behavior_linechart():
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    behavior_entries = db.session.query(
        Behavior.Btime,
        Behavior.Bclass,
        func.count('*').label('count')
    ).filter(
        Behavior.Btime >= today,
        Behavior.Btime < tomorrow
    ).group_by(
        Behavior.Btime, Behavior.Bclass
    ).all()

    time_periods = {
        "早晨": (0, 6),
        "上午": (7, 10),
        "中午": (11, 15),
        "下午": (16, 19),
        "晚上": (20, 24)
    }

    grouped_data = {period: {} for period in time_periods}

    for entry in behavior_entries:
        bclass = entry.Bclass
        btime = entry.Btime
        count = entry.count

        for period, (start, end) in time_periods.items():
            if start <= btime.hour < end:
                if bclass not in grouped_data[period]:
                    grouped_data[period][bclass] = 0
                grouped_data[period][bclass] += count
                break

    # 将数据转换为前端所需的格式
    response_data = {}
    for period, classes in grouped_data.items():
        for bclass, count in classes.items():
            if bclass not in response_data:
                response_data[bclass] = []
            response_data[bclass].append({'Btime': period, 'count': count})

    return jsonify(response_data)

@video.route('/behave_category')
def behave_category():
    behavior_counts = db.session.query(Behavior.Bclass, db.func.count(Behavior.Bclass).label('count')).group_by(
        Behavior.Bclass).all()
    data = {bclass: count for bclass, count in behavior_counts}
    return jsonify(data)


@video.route('/get_records', methods=['GET'])
def get_records():
    user = session.get('Uid')
    if not user:
        return redirect(url_for('user.login', message='请先登录'))

    result = gain_records(user)
    return render_template('detect_records.html', records=result.json['data'])



@video.route('/watchchart')
def watchchart():
    # Uid = session.get('Uid')
    # u = User_operation()
    # user_info = u.get_user_info(Uid)

    return render_template('chart.html')

