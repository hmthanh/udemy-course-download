import subprocess


def check_for_mp4decrypt():
    try:
        subprocess.Popen(["mp4decrypt"],
                         stderr=subprocess.DEVNULL,
                         stdout=subprocess.DEVNULL).wait()
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(
            "> Unexpected exception while checking for MP4Decrypt, please tell the program author about this! ",
            e)
        return True

