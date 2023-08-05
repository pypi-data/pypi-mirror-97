from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common import keys
from selenium.common import exceptions
import time
import os
import glob
import numpy as np
from . import strings as cc_strings
from . import clock as cc_clock
from . import download as cc_download
# from . import strings, clock, download


class MixamoBot:

    def __init__(self, directory_driver, directory_downloads, timeout=300):

        self.timeout = timeout
        self.directory_downloads = directory_downloads

        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "prefs", {"download.default_directory": self.directory_downloads,
                      "download.prompt_for_download": False})

        self.driver = webdriver.Chrome(executable_path=directory_driver, options=options)
        self.driver.set_page_load_timeout(300)
        self.driver.set_window_size(1200, 1040)

        mixamo_website = 'https://www.mixamo.com/#/'
        self.driver.get(mixamo_website)

    def signup(self, email=None, password=None, first_name=None, last_name=None, birthday=None):

        if email is None:
            email = cc_strings.generate_a_random_email()

        if password is None:
            password = cc_strings.n_to_string_of_n_random_digits(n=10)

        if first_name is None:
            first_name = cc_strings.generate_a_random_name()

        if last_name is None:
            last_name = cc_strings.generate_a_random_name()

        if birthday is None:
            birthday = dict(day='1', month='1', year='1990')
            #
        elif isinstance(birthday, dict):
            if birthday.get('day') is None:
                birthday['day'] = '1'
            if birthday.get('month') is None:
                birthday['month'] = '1'  # birthday['month'] = 1 is January, birthday['month'] = 2 is February ...
            if birthday.get('year') is None:
                birthday['year'] = '1990'
        else:
            raise ValueError('birthday has to be None or a dictionary')

        website_create_account = (
            'https://auth.services.adobe.com/en_US/deeplink.html?deeplink=signup&callback=https%3A%2F%2Fims-na1.'
            'adobelogin.com%2Fims%2Fadobeid%2Fmixamo1%2FAdobeID%2Fcode%3Fredirect_uri%3Dhttps%253A%252F%252Fwww.'
            'mixamo.com%252F%2523%252Fimsauth&client_id=mixamo1&scope=openid%2CAdobeID%2Cfetch_sao%2Csao.creativ'
            'e_cloud&denied_callback=https%3A%2F%2Fims-na1.adobelogin.com%2Fims%2Fdenied%2Fmixamo1%3Fredirect_ur'
            'i%3Dhttps%253A%252F%252Fwww.mixamo.com%252F%2523%252Fimsauth%26response_type%3Dcode&relay=6b253098-'
            '29c9-48f1-9f17-a3f1a393fcff&locale=en_US&flow_type=code&ctx_id=mixamo_web&idp_flow_type=create_acco'
            'unt&el=true#/signup')

        self.driver.get(website_create_account)
        timer = cc_clock.Timer()
        job_done = False
        while not job_done:
            try:
                self.driver.find_element_by_name('email').send_keys(email)
                job_done = True
            except exceptions.NoSuchElementException:
                if timer.get_seconds() > self.timeout:
                    raise TimeoutError('I cannot find the "email" box')
                time.sleep(1)
        self.driver.find_element_by_name('firstname').send_keys(first_name)
        self.driver.find_element_by_name('lastname').send_keys(last_name)
        self.driver.find_element_by_css_selector(
            'button.spectrum-Tool.spectrum-Tool--quiet.PasswordField-VisibilityToggle').click()

        self.driver.find_element_by_name('password').send_keys(password)

        self.driver.find_element_by_id('Signup-DateOfBirthChooser-Month').click()
        # time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='react-spectrum-9-menu']/li[{}]".format(birthday['month'])).click()
        # self.driver.find_element_by_name('day').click()
        self.driver.find_element_by_name('day').send_keys(birthday['day'])
        # self.driver.find_element_by_name('year').click()
        self.driver.find_element_by_name('year').send_keys(birthday['year'])

        time.sleep(3)
        self.driver.find_element_by_name('submit').click()
        time.sleep(40)

    def login(self, username, password):
        # click LOG IN
        timer = cc_clock.Timer()
        job_done = False
        while not job_done:
            try:
                self.driver.find_element_by_xpath("//a[contains(., 'Log in')]").click()
                job_done = True
            except exceptions.NoSuchElementException:
                if timer.get_seconds() > self.timeout:
                    raise TimeoutError('I cannot find the "Log in" button')
                time.sleep(1)

        timer = cc_clock.Timer()
        job_done = False
        while not job_done:
            try:
                self.driver.find_element_by_name('username').send_keys(username)
                job_done = True

            except exceptions.NoSuchElementException:
                if timer.get_seconds() > self.timeout:
                    raise TimeoutError('I cannot find the "username" box')
                time.sleep(1)

        time.sleep(0.2)
        self.driver.find_element_by_xpath("//span[contains(., 'Continue')]").click()

        timer = cc_clock.Timer()
        job_done = False
        while not job_done:
            try:
                self.driver.find_element_by_name('password').send_keys(password)
                job_done = True
                time.sleep(0.2)
            except exceptions.NoSuchElementException:
                if timer.get_seconds() > self.timeout:
                    raise TimeoutError('I cannot find the "password" box')
                time.sleep(1)

        time.sleep(0.2)
        self.driver.find_element_by_xpath("//span[contains(., 'Continue')]").click()

        time.sleep(40)

    def activate_character(self, name_character, websites_search_actors):

        timer = cc_clock.Timer()
        job_done = False
        while not job_done:
            try:
                current_actor_element = self.driver.find_element_by_css_selector('h2.text-center.h5')
                job_done = True
            except exceptions.NoSuchElementException:
                if timer.get_seconds() > self.timeout:
                    raise TimeoutError('I cannot find the name of the active character')
                time.sleep(1)
        current_actor_name = current_actor_element.text

        if name_character.upper() != current_actor_name.upper():
            self.driver.get(websites_search_actors)

            timer = cc_clock.Timer()
            job_done = False
            while not job_done:
                try:
                    self.driver.find_element_by_xpath("//p[contains(., '{}')]".format(name_character)).click()
                    job_done = True
                except exceptions.NoSuchElementException:
                    if timer.get_seconds() > self.timeout:
                        raise TimeoutError('I cannot find the character box')
                    time.sleep(1)

            timer = cc_clock.Timer()
            job_done = False
            while not job_done:
                try:
                    self.driver.find_element_by_xpath("//button[contains(., 'Use this character')]").click()
                    job_done = True
                except exceptions.NoSuchElementException:
                    if timer.get_seconds() > self.timeout:
                        raise TimeoutError('I cannot find the "Use this character" button')
                    time.sleep(1)
            # search_box.clear()
            time.sleep(30)

    def activate_character_old(self, name_character, search_actor_as):

        timer = cc_clock.Timer()
        job_done = False
        while not job_done:
            try:
                current_actor_element = self.driver.find_element_by_css_selector('h2.text-center.h5')
                job_done = True
            except exceptions.NoSuchElementException:
                if timer.get_seconds() > self.timeout:
                    raise TimeoutError('I cannot find the name of the active character')
                time.sleep(1)
        current_actor_name = current_actor_element.text

        if name_character.upper() != current_actor_name.upper():
            self.driver.get('https://www.mixamo.com/#/?page=1&type=Character')
            timer = cc_clock.Timer()
            job_done = False
            while not job_done:
                try:
                    self.driver.find_element_by_name('search').send_keys(search_actor_as + keys.Keys.ENTER)
                    job_done = True
                except exceptions.NoSuchElementException:
                    if timer.get_seconds() > self.timeout:
                        raise TimeoutError('I cannot find the "search" box')
                    time.sleep(1)

            timer = cc_clock.Timer()
            job_done = False
            while not job_done:
                try:
                    self.driver.find_element_by_xpath("//p[contains(., '{}')]".format(name_character)).click()
                    job_done = True
                except exceptions.NoSuchElementException:
                    if timer.get_seconds() > self.timeout:
                        raise TimeoutError('I cannot find the character box')
                    time.sleep(1)

            timer = cc_clock.Timer()
            job_done = False
            while not job_done:
                try:
                    self.driver.find_element_by_xpath("//button[contains(., 'Use this character')]").click()
                    job_done = True
                except exceptions.NoSuchElementException:
                    if timer.get_seconds() > self.timeout:
                        raise TimeoutError('I cannot find the "Use this character" button')
                    time.sleep(1)
            # search_box.clear()
            time.sleep(30)

    def activate_animation(
            self, websites_animation, n_search_results_expected, i_search_result):

        self.driver.get(websites_animation)
        timer = cc_clock.Timer()
        elements_animations = self.driver.find_elements_by_css_selector('div.product-overlay')
        n_animation_elements_from_web = len(elements_animations)
        while n_animation_elements_from_web != n_search_results_expected:

            if timer.get_seconds() > self.timeout:
                raise ValueError(
                    'The following condition is not met:\n'
                    'n_animation_elements_from_web = n_search_results_expected\n'
                    'n_animation_elements_from_web = {}\n'
                    'n_search_results_expected = {}\n'.format(
                        n_animation_elements_from_web, n_search_results_expected))
            time.sleep(1)
            elements_animations = self.driver.find_elements_by_css_selector('div.product-overlay')
            n_animation_elements_from_web = len(elements_animations)

        elements_animations[i_search_result].click()

    def check_n_frames_default_from_web(self, n_frames_default_expected):

        n_frames_default_from_web = -1
        while n_frames_default_from_web == n_frames_default_expected:
            n_frames_default_from_web -= 1

        timer = cc_clock.Timer()

        while n_frames_default_from_web != n_frames_default_expected:

            if timer.get_seconds() > self.timeout:
                print(timer.get_seconds())
                raise ValueError(
                    'The following condition is not met:\n'
                    'n_frames_default_from_web = n_frames_default[i_animation]\n'
                    'n_frames_default_from_web = {}\n'
                    'n_frames_default_expected = {}'.format(n_frames_default_from_web, n_frames_default_expected))

            try:
                text_total_frames = self.driver.find_element_by_xpath("//small[contains(., 'total frames')]").text
            except exceptions.NoSuchElementException:
                time.sleep(1)
                if timer.get_seconds() > self.timeout:
                    raise TimeoutError('I cannot get the n_frames_default_from_web')
                else:
                    continue
            n_frames_default_from_web_str = ''
            for s in text_total_frames:
                try:
                    int(s)
                    n_frames_default_from_web_str += s
                except ValueError:
                    pass
            try:
                n_frames_default_from_web = int(n_frames_default_from_web_str)
            except ValueError:
                continue

    def get_n_frames_from_web(self, time_out=120):
        timer = cc_clock.Timer()
        n_frames_from_web_old = -2
        n_frames_from_web = -1
        while n_frames_from_web != n_frames_from_web_old:
            try:
                text_total_frames = self.driver.find_element_by_xpath("//small[contains(., 'total frames')]").text
                n_frames_from_web_old = n_frames_from_web
            except exceptions.NoSuchElementException:
                time.sleep(2)
                if timer.get_seconds() > time_out:
                    raise TimeoutError('I cannot get the n_frames_from_web')
                else:
                    continue
            n_frames_from_web_str = ''
            for s in text_total_frames:
                try:
                    int(s)
                    n_frames_from_web_str += s
                except ValueError:
                    pass
            try:
                n_frames_from_web = int(n_frames_from_web_str)
            except ValueError:
                continue

        return n_frames_from_web

    def set_animation_parameters(self, parameters, elements_variables_mixamo=None):
        if elements_variables_mixamo is None:
            elements_variables_mixamo = self.driver.find_elements_by_css_selector(
                'input.input-text-unstyled.animation-slider-value.input-text-editable')[::-1]

        n_variables_mixamo = len(elements_variables_mixamo)
        for i_variable_mixamo in range(n_variables_mixamo):
            elements_variables_mixamo[i_variable_mixamo].send_keys(
                str(webdriver.common.keys.Keys.BACKSPACE * 5) +
                str(parameters[i_variable_mixamo]) + keys.Keys.ENTER)

    def set_animation_trim(self, start=0, end=100, elements_trim=None):

        if elements_trim is None:
            elements_trim = self.driver.find_elements_by_name('trim')

        elements_trim[0].send_keys(
            str(webdriver.common.keys.Keys.BACKSPACE * 5) + str(start) + keys.Keys.ENTER)
        elements_trim[1].send_keys(
            str(webdriver.common.keys.Keys.BACKSPACE * 5) + str(end) + keys.Keys.ENTER)

    def adjust_trim_to_make_n_frames_equal_or_larger_than_threshold(
            self, trims, trim_range, adjust_trim=None, threshold=60, elements_trim=None):

        if adjust_trim is None:
            adjust_trim = np.asarray([True, True], dtype=bool)

        if elements_trim is None:
            elements_trim = self.driver.find_elements_by_name('trim')

        n_frames_from_web = self.get_n_frames_from_web()
        frames_are_less_than_threshold = n_frames_from_web < threshold

        trim_start = trims[0]  # ???????????????
        adjust_trim_start = adjust_trim[0] and (
                trim_start > int(trim_range[0]))

        trim_end = trims[1]  # ???????????????
        adjust_trim_end = adjust_trim[1] and (
                trim_end < int(trim_range[1]))
        i = True
        adjust_trim_of_this_fbx = frames_are_less_than_threshold and (adjust_trim_start or adjust_trim_end)
        while adjust_trim_of_this_fbx:

            if adjust_trim_start and adjust_trim_end:
                if i:
                    trim_start -= 1
                    elements_trim[0].send_keys(
                        str(webdriver.common.keys.Keys.BACKSPACE * 5) + str(trim_start) + keys.Keys.ENTER)
                    i = False
                else:
                    trim_end += 1
                    elements_trim[1].send_keys(
                        str(webdriver.common.keys.Keys.BACKSPACE * 5) + str(trim_end) + keys.Keys.ENTER)
                    i = True

            elif adjust_trim_start:
                trim_start -= 1
                elements_trim[0].send_keys(
                    str(webdriver.common.keys.Keys.BACKSPACE * 5) + str(trim_start) + keys.Keys.ENTER)

            elif adjust_trim_end:
                trim_end += 1
                elements_trim[1].send_keys(
                    str(webdriver.common.keys.Keys.BACKSPACE * 5) + str(trim_end) + keys.Keys.ENTER)

            n_frames_from_web = self.get_n_frames_from_web()
            frames_are_less_than_threshold = n_frames_from_web < threshold

            adjust_trim_start = adjust_trim[0] and (
                    trim_start > int(trim_range[0]))

            adjust_trim_end = adjust_trim[1] and (
                    trim_end < int(trim_range[1]))

            adjust_trim_of_this_fbx = frames_are_less_than_threshold and (
                    adjust_trim_start or adjust_trim_end)

    def download_animation(self, saved_fbx_as, rename_fbx_as):

        # self.driver.find_element_by_css_selector('button.btn-block.btn.btn-primary').click()
        self.driver.find_element_by_xpath("//button[contains(., 'Download')]").click()

        timer = cc_clock.Timer()
        job_done = False
        while not job_done:
            try:
                menus = self.driver.find_elements_by_id('formControlsSelect')
                job_done = True
            except exceptions.NoSuchElementException:
                if timer.get_seconds() > self.timeout:
                    raise TimeoutError('I cannot find the downloading menus')
                time.sleep(1)

        element_menu_format = menus[0]
        menu_format = ui.Select(element_menu_format)
        menu_format.select_by_visible_text('FBX(.fbx)')

        element_menu_skin = menus[1]
        menu_skin = ui.Select(element_menu_skin)
        menu_skin.select_by_visible_text('Without Skin')

        element_menu_frames_per_second = menus[2]
        menu_frames_per_second = ui.Select(element_menu_frames_per_second)
        menu_frames_per_second.select_by_visible_text('30')

        element_menu_keyframe_reduction = menus[3]
        menu_keyframe_reduction = ui.Select(element_menu_keyframe_reduction)
        menu_keyframe_reduction.select_by_visible_text('none')

        list_fbx_to_move = glob.glob(os.path.join(self.directory_downloads, '*.fbx'))
        n_fbx_to_move = len(list_fbx_to_move)
        if n_fbx_to_move != 0:
            raise Exception('n_fbx_to_move should be equal to 0 after the last download.\n'
                            'The value of n_fbx_to_move was {}.'.format(n_fbx_to_move))
        time.sleep(0.2)

        # download_elements = self.driver.find_elements_by_css_selector('button.btn.btn-primary')
        # download_elements[1].click()
        self.driver.find_elements_by_xpath("//button[contains(., 'Download')]")[1].click()

        cc_download.wait_downloading(saved_fbx_as, max_seconds_wait=180)

        list_fbx_to_move = glob.glob(os.path.join(self.directory_downloads, '*.fbx'))
        n_fbx_to_move = len(list_fbx_to_move)
        if n_fbx_to_move != 1:
            raise Exception('n_fbx_to_move should be equal to 1 after the last download.\n'
                            'The value of n_fbx_to_move was {}.'.format(n_fbx_to_move))
        os.rename(saved_fbx_as, rename_fbx_as)

    def download_t_pose(self, rename_fbx_as, timeout_dowloading=600):

        # self.driver.find_element_by_css_selector('button.btn-block.btn.btn-primary').click()
        self.driver.find_element_by_xpath("//button[contains(., 'Download')]").click()

        timer = cc_clock.Timer()
        job_done = False
        while not job_done:
            try:
                menus = self.driver.find_elements_by_id('formControlsSelect')
                job_done = True
            except exceptions.NoSuchElementException:
                if timer.get_seconds() > self.timeout:
                    raise TimeoutError('I cannot find the downloading menus')
                time.sleep(1)

        element_menu_format = menus[0]
        menu_format = ui.Select(element_menu_format)
        menu_format.select_by_visible_text('FBX(.fbx)')

        element_menu_pose = menus[1]
        menu_pose = ui.Select(element_menu_pose)
        menu_pose.select_by_visible_text('T-pose')

        list_fbx_to_rename = glob.glob(os.path.join(self.directory_downloads, '*.fbx'))
        n_fbx_to_rename = len(list_fbx_to_rename)
        if n_fbx_to_rename != 0:
            raise Exception('n_fbx_to_rename should be equal to 0 after the last download.\n'
                            'The value of n_fbx_to_rename was {}.'.format(n_fbx_to_rename))

        time.sleep(0.2)
        # download_elements = self.driver.find_elements_by_css_selector('button.btn.btn-primary')
        # download_elements[1].click()
        self.driver.find_elements_by_xpath("//button[contains(., 'Download')]")[1].click()

        timer = cc_clock.Timer()
        while n_fbx_to_rename != 1:
            if timer.get_seconds() > timeout_dowloading:
                raise TimeoutError('actor was not downloaded')
            list_fbx_to_rename = glob.glob(os.path.join(self.directory_downloads, '*.fbx'))
            n_fbx_to_rename = len(list_fbx_to_rename)
            time.sleep(1)

        os.rename(list_fbx_to_rename[0], rename_fbx_as)
