import mp4parse
import codecs
import widevine_pssh_pb2
import base64


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


def _print_course_info(course_data):
    print("\n\n\n\n")
    course_title = course_data.get("title")
    chapter_count = course_data.get("total_chapters")
    lecture_count = course_data.get("total_lectures")

    print("> Course: {}".format(course_title))
    print("> Total Chapters: {}".format(chapter_count))
    print("> Total Lectures: {}".format(lecture_count))
    print("\n")

    chapters = course_data.get("chapters")
    for chapter in chapters:
        chapter_title = chapter.get("chapter_title")
        chapter_index = chapter.get("chapter_index")
        chapter_lecture_count = chapter.get("lecture_count")
        chapter_lectures = chapter.get("lectures")

        print("> Chapter: {} ({} of {})".format(chapter_title, chapter_index,
                                                chapter_count))

        for lecture in chapter_lectures:
            lecture_title = lecture.get("lecture_title")
            lecture_index = lecture.get("index")
            lecture_asset_count = lecture.get("assets_count")
            lecture_is_encrypted = lecture.get("is_encrypted")
            lecture_subtitles = lecture.get("subtitles")
            lecture_extension = lecture.get("extension")
            lecture_sources = lecture.get("sources")
            lecture_video_sources = lecture.get("video_sources")

            if lecture_sources:
                lecture_sources = sorted(lecture.get("sources"),
                                         key=lambda x: int(x.get("height")),
                                         reverse=True)
            if lecture_video_sources:
                lecture_video_sources = sorted(
                    lecture.get("video_sources"),
                    key=lambda x: int(x.get("height")),
                    reverse=True)

            if lecture_is_encrypted:
                lecture_qualities = [
                    "{}@{}x{}".format(x.get("type"), x.get("width"),
                                      x.get("height"))
                    for x in lecture_video_sources
                ]
            elif not lecture_is_encrypted and lecture_sources:
                lecture_qualities = [
                    "{}@{}x{}".format(x.get("type"), x.get("height"),
                                      x.get("width")) for x in lecture_sources
                ]

            if lecture_extension:
                continue

            print("  > Lecture: {} ({} of {})".format(lecture_title,
                                                      lecture_index,
                                                      chapter_lecture_count))
            print("    > DRM: {}".format(lecture_is_encrypted))
            print("    > Asset Count: {}".format(lecture_asset_count))
            print("    > Captions: {}".format(
                [x.get("language") for x in lecture_subtitles]))
            print("    > Qualities: {}".format(lecture_qualities))

        if chapter_index != chapter_count:
            print("\n\n")
