import os
import subprocess


def durationtoseconds(period):
    """
    @author Jayapraveen
    """

    # Duration format in PTxDxHxMxS
    if (period[:2] == "PT"):
        period = period[2:]
        day = int(period.split("D")[0] if 'D' in period else 0)
        hour = int(period.split("H")[0].split("D")[-1] if 'H' in period else 0)
        minute = int(
            period.split("M")[0].split("H")[-1] if 'M' in period else 0)
        second = period.split("S")[0].split("M")[-1]
        print("Total time: " + str(day) + " days " + str(hour) + " hours " +
              str(minute) + " minutes and " + str(second) + " seconds")
        total_time = float(
            str((day * 24 * 60 * 60) + (hour * 60 * 60) + (minute * 60) +
                (int(second.split('.')[0]))) + '.' +
            str(int(second.split('.')[-1])))
        return total_time

    else:
        print("Duration Format Error")
        return None


def mux_process(video_title, video_filepath, audio_filepath, output_path):
    """
    @author Jayapraveen
    """
    if os.name == "nt":
        command = "ffmpeg -y -i \"{}\" -i \"{}\" -acodec copy -vcodec copy -fflags +bitexact -map_metadata -1 -metadata title=\"{}\" \"{}\"".format(
            video_filepath, audio_filepath, video_title, output_path)
    else:
        command = "nice -n 7 ffmpeg -y -i \"{}\" -i \"{}\" -acodec copy -vcodec copy -fflags +bitexact -map_metadata -1 -metadata title=\"{}\" \"{}\"".format(
            video_filepath, audio_filepath, video_title, output_path)
    os.system(command)


def check_for_aria():
    try:
        subprocess.Popen(["aria2c", "-v"],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL).wait()
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(
            "> Unexpected exception while checking for Aria2c, please tell the program author about this! ",
            e)
        return True


def check_for_ffmpeg():
    try:
        subprocess.Popen(["ffmpeg"],
                         stderr=subprocess.DEVNULL,
                         stdout=subprocess.DEVNULL).wait()
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(
            "> Unexpected exception while checking for FFMPEG, please tell the program author about this! ",
            e)
        return True

