import logging
import os
import time

from flask import Flask, render_template, jsonify, Response, send_file
from moviepy.editor import VideoFileClip

from camera_control import start_recording, stop_recording, get_status

app = Flask(__name__)

recording = False  # 録画状態を表す変数

# 保存先フォルダの作成
folder_path = os.path.dirname(__file__) + '/videos'
if not os.path.exists(folder_path):
    os.mkdir(folder_path)
    logging.info(f"フォルダ '{folder_path}' を作成しました。")
else:
    logging.info(f"フォルダ '{folder_path}' は既に存在します。")

# ログの設定
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_format)
logger = logging.getLogger(__name__)

# 環境変数 'FLASK_ENV' の値によってデバッグモードを切り替える
if os.environ.get('FLASK_ENV') == 'production':
    app.debug = False
elif os.environ.get('FLASK_ENV') is None:
    app.debug = True
else:
    app.debug = True


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/', methods=['GET'])
def index():
    logger.info('Rendering index.html...')
    return render_template('index.html', recording=recording)


@app.route('/video/get_status', methods=['GET'])
def get_status_route():
    logger.debug('Getting status...')
    return jsonify({"status": get_status(recording)})


@app.route('/video/start_recording', methods=['POST'])
def start_recording_route():
    global recording
    result, success = start_recording(folder_path, recording)
    if success:
        recording = True
        logger.info('Recording started.')
    return jsonify({"message": result}), 200 if success else 400


@app.route('/video/stop_recording', methods=['POST'])
def stop_recording_route():
    global recording
    result, success = stop_recording(recording)
    if success:
        recording = False
        logger.info('Recording stopped.')
    return jsonify({"message": result}), 200 if success else 400


@app.route('/video/list', methods=['GET'])
def video_list():
    videos = []
    # サンプルとして/videos配下の動画のリストをリストとして定義
    video_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    for filename in video_files:
        file_path = os.path.join(folder_path, filename)
        if file_path.lower().endswith('.mp4'):
            try:
                clip = VideoFileClip(file_path)
                videos.append(
                    {"filename": filename, "length": clip.duration,
                     "size": round(os.path.getsize(file_path) / 1024 / 1024, 2)})  # MBに変換
                clip.close()
            except Exception as e:
                logger.error(f"エラー: {filename}を処理中に問題が発生しました。")
    logger.info(videos)
    return render_template('video_list.html', videos=videos)


@app.route('/video/<filename>', methods=['GET'])
def download_video(filename: str):
    target = f"{folder_path}/{filename}"
    if not os.path.exists(target):
        return jsonify({"file is not found": "recording now!!"}), 400
    return send_file(target, mimetype='video/mpeg')


@app.route('/video/<filename>/delete', methods=['DELETE'])
def delete_video(filename: str):
    global recording
    if recording is True:
        return jsonify({"message": "recording now!!"}), 400
    try:
        # ファイルを削除
        os.remove(os.path.join(folder_path, filename))
        logger.info(f"ファイル '{filename}' を削除しました。")
        return jsonify({"message": ""}), 200
    except FileNotFoundError:
        logger.warn(f"エラー: ファイル '{filename}' が見つかりません。")
        return jsonify({"message": "file not found!!"}), 400
    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        return jsonify({"message": "{e}"}), 500


def generate_status():
    while True:
        time.sleep(3)  # 3秒ごとに更新
        status = get_status(recording)
        logger.debug('Sending status: %s', status)
        yield f"data: {status}\n\n"


@app.route('/video/stream_status')
def stream_status():
    logger.debug('Streaming status...')
    return Response(generate_status(), content_type='text/event-stream')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
