# Instagram Auto Post

""" Automation of posting images to Instagram """

import time
import os
import json
import pickle
from warnings import warn
from random import randint
from random import randrange
from InstagramAPI import InstagramAPI
from PIL import Image
from photo import Photo


class AutoPost:

    def __init__(self, usrname, pssword, post_dir):
        """
        initialise auto post class
        :param usrname: username for instagram user
        :param pssword: password for instagram user
        :param post_dir: direcory containing the data to post

        post_dir needs to contain:
            1. an /images/ directory. This directory will hold the images that will be uploaded to instagram
            2. data.json. This file contains the caption info corresponding to each image
            3. tags.txt. The hashtags that will be used for each upload
            4. borders.txt. Stylistic borders used to separate the caption and the tag
        """
        self.api = self.api_login(usrname, pssword)
        if self.api is None:
            return
        self.post_dir = post_dir
        self.validate_post_dir()
        self.image_dir = self.post_dir + 'images/'
        self.images = self.get_post_images()
        self.borders = self.get_post_borders(post_dir + 'borders.txt')
        self.tags = self.get_post_tags(post_dir + 'tags.txt')
        self.data_path = self.post_dir + '/data.json'
        self.data = self.get_post_data()
        self.posts = []
        self.create_posts()
        self.auto_post()

    def validate_post_dir(self):
        """ validate post directory. Appending a / if required """
        if self.post_dir[-1] == '/':
            return
        self.post_dir = self.post_dir + '/'

    @staticmethod
    def api_login(usrname, pssword):
        """
        login to unofficial instagram api and return api object
        :return: instagram api
        """
        api = InstagramAPI(usrname, pssword)
        api.login()
        if api.isLoggedIn:
            return api
        last_response = api.LastResponse
        response = json.loads(last_response.text)
        print(json.dumps(response, indent=2, sort_keys=True))
        return None

    def pickle_api(self, filename):
        """
        picke api for use later
        :param filename: filename to save pickled api
        """
        pickle_file = filename + '.pk'
        with open(pickle_file, 'wb') as file:
            pickle.dump(self.api, file)

    def open_api_pickle(self, pickle_file):
        """
        open open picked api and store in self if exists
        :param pickle_file: file name
        """
        with open(pickle_file, 'rb') as file:
            self.api = pickle.load(file)

    def get_post_images(self):
        """
        get list of image files to post
        :return: list of image files
        """
        image_files = sorted([f for f in os.listdir(self.image_dir) if f.endswith('jpg')])
        return image_files

    @staticmethod
    def remove_image_exif_data(image_filepath, image):
        """
        remove EXIF data which may contains info about camera, and potentially GPS coords
        :param image_filepath: filepath to image to alter
        :param image: open image PIL object
        """
        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)
        image_without_exif.save(image_filepath)

    @staticmethod
    def get_post_borders(border_file_path):
        """
        get list of image files to post
        :param border_file_path: filepath to post borders
        :return: list of all borders
        """
        with open(border_file_path, 'r') as f:
            border_list = f.readlines()
        return border_list

    @staticmethod
    def get_post_tags(tags_file_path):
        """
        get all hashtags to be used for the posts
        :param tags_file_path:
        :return: list of hashtags
        """
        with open(tags_file_path, 'r') as f:
            post_tags = f.read()
        return post_tags

    def get_post_data(self):
        """
        get the json data which will be used for the post
        :return: instagram post content in json structure
        """
        with open(self.data_path) as data:
            post_data = json.load(data)
        return post_data

    @staticmethod
    def dump_json(data, output_file):
        """
        dump json data to file
        :param data: json data to dump
        :param output_file: output file to write
        """
        with open(output_file, 'w') as outfile:
            json.dump(data, outfile, indent=2)

    def single_post(self, image_filepath, caption):
        """
        post a single photo
        :param image_filepath: filepath to image
        :param caption: post caption
        """
        self.api.uploadPhoto(image_filepath, caption, upload_id=None)

    def remove_caption_from_filedata(self, content_index):
        """
        remove post from data file
        :param content_index: content index to pop
        """
        self.data['post'].pop(content_index)
        self.dump_json(self.data, self.data_path)

    def create_posts(self):
        """
        create list of post objects
        """
        print('creating posts..')
        for i, post in enumerate(self.data['post']):
            os.chdir(self.image_dir)
            image_filepath = self.image_dir + self.images[i]
            image = Image.open(image_filepath)
            self.remove_image_exif_data(image_filepath, image)
            caption = '\"' + post['content'] + '\"' + ' - ' + post['author'] + '\n•\n' + self.borders[i] + '\n•\n' + self.tags
            photo = Photo(caption, image_filepath)
            self.posts.append(photo)
        print('{} posts to upload'.format(len(self.posts)))

    def auto_post(self, update_filesystem=False):
        """
        auto post images to instagram with a delay
        :param update_filesystem: remove files locally and update post data
        """
        print('begin auto post...')
        for i, post in enumerate(self.posts):
            time.sleep(randrange(1, 5))
            try:
                print('uploading image: {}'.format(post.filepath))
                self.api.uploadPhoto(post.filepath, post.caption, upload_id=None)
                result = self.api.LastJson['status']
                print('upload status : ' + result)
            except Exception as e:
                print(e)
                continue
            if result == 'ok':
                print('upload successful!')
            else:
                warn('upload failed!')
            if result == 'ok' and update_filesystem:
                print('removing file from filesystem')
                os.remove(post.filepath)
                self.remove_caption_from_filedata(i)
            time_between_posts = randint(30, 60) * 60
            print('waiting {} minutes before next post'.format(str(time_between_posts / 60)))
            time.sleep(time_between_posts)


# Program driver
if __name__ == '__main__':
    u, p = 'username@me.com', 'password123'
    post_directory = '/fullpath/to/post/directory/'
    auto_post = AutoPost(usrname=u, pssword=p, post_dir=post_directory)
