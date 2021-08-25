def split_course_key(key):
    """Split an OpenEdX course key by organization, course and course run codes.
    We first try splitting the key as a version 1 key (course-v1:org+course+run)
    and fallback the old version (org/course/run).

    See https://github.com/openfun/richie/blob/master/src/richie/apps/courses/lms/edx.py
    """
    if key.startswith("course-v1:"):
        organization, course, run = key[10:].split("+")
    else:
        organization, course, run = key.split("/")

    return organization, course, run
