# Photo Object


class Photo:

    def __init__(self, filepath, caption):
        """
        Post object for api upload
        :param filepath: filepath to image
        :param caption: caption for instagram post
        """
        self.filepath = filepath
        self.caption = caption
