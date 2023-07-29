import datetime
import platform
import subprocess


def get_status(recording):
    return "録画中" if recording else "録画していません"


def start_recording(folder_path, is_recording):
    if not is_recording:
        try:
            recording_command = ["raspivid", "-o",
                                 f"{folder_path}/video_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.h264", "-t",
                                 "0"]

            if platform.system() == 'Darwin':
                recording_command = ["ffmpeg", "-f", "avfoundation", "-framerate", "30", "-i", "0",
                                     f"{folder_path}/video_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"]

            subprocess.Popen(recording_command)  # 無限に録画
            return "Recording started", True
        except Exception as e:
            return str(e), False
    return "Already recording", False


def stop_recording(is_recording):
    if is_recording:
        try:
            stop_recording_command = ["pkill", "raspivid"]  # raspividプロセスを終了するコマンド
            if platform.system() == 'Darwin':
                stop_recording_command = ["killall", "ffmpeg"]  # ffmpegプロセスを終了するコマンド
            subprocess.run(stop_recording_command)
            return "Recording stopped", True
        except Exception as e:
            return str(e), False
    return "Not recording", False
