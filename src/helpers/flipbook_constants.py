from src.media.resolution import Resolution


class FlipbookConstants:
    class Video:
        SUPPORTED_FORMATS = frozenset({'mov', 'mp4'})

    class Font:
        DEFAULT = 'fonts/arial.ttf'
        SIZE = 50
        # resolution for which SIZE is appropriate
        REF_RES = Resolution(1500, 900)

