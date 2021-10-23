import mp4parse
import os
import glob
import codecs
import widevine_pssh_pb2
import base64
import re
from sanitize import sanitize, slugify, SLUG_OK


def extract_kid(mp4_file):
    """
    Parameters
    ----------
    mp4_file : str
        MP4 file with a PSSH header


    Returns
    -------
    String

    """

    boxes = mp4parse.F4VParser.parse(filename=mp4_file)
    for box in boxes:
        if box.header.box_type == 'moov':
            pssh_box = next(x for x in box.pssh if x.system_id == "edef8ba979d64acea3c827dcd51d21ed")
            hex = codecs.decode(pssh_box.payload, "hex")

            pssh = widevine_pssh_pb2.WidevinePsshData()
            pssh.ParseFromString(hex)
            content_id = base64.b16encode(pssh.content_id)
            return content_id.decode("utf-8")

    # No Moof or PSSH header found
    return None


def _clean(text):
    ok = re.compile(r'[^\\/:*?!"<>|]')
    text = "".join(x if ok.match(x) else "_" for x in text)
    text = re.sub(r"\.+$", "", text.strip())
    return text


def _sanitize(self, unsafetext):
    text = _clean(sanitize(
        slugify(unsafetext, lower=False, spaces=True, ok=SLUG_OK + "().[]")))
    return text


def cleanup(path):
    """
    @author Jayapraveen
    """
    leftover_files = glob.glob(path + '/*.mp4', recursive=True)
    for file_list in leftover_files:
        try:
            os.remove(file_list)
        except OSError:
            print(f"Error deleting file: {file_list}")
    os.removedirs(path)
