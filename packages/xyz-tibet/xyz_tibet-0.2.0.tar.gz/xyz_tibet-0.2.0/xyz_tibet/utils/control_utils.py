# -*- coding:utf-8 -*-
import warnings

from huepy import *

from xyz_tibet.utils.encoding_utils import ensure_utf8, ensure_unicode


class CustomColors:
    RED = "\033[1;31;40m"
    BLUE = "\033[1;34;40m"
    YELLOW = "\033[1;33;40m"
    GREEN = "\033[1;32;40m"
    NEW_BLUE = "\033[0;37;44m"
    CYAN = "\033[1;36;40m"
    PURPLE = "\033[1;35;40m"

    # 自定义颜色
    REAL_PURPLE = "\033[1;34;40m"
    CHECK_COLOR = '\33[95m'
    CYAN_MIX = '\033[1;32;44m'

    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


import subprocess


def get_color_code():
    """

    """
    for background_color in range(40, 48):
        for font_color in range(30, 37):
            print '\\033[1;{};{}m'.format(font_color, background_color),
            print_color_str('hello', "\033[1;{};{}m".format(font_color, background_color))


def print_color_str(some_str, color, is_center=False):
    """
    打印彩色字符串
    """
    some_str = str(some_str)
    if is_center:
        some_str = auto_blank_filled(some_str)
    if not color:
        print some_str
    else:
        print color + some_str + CustomColors.ENDC


try:
    TERMINAL_WIDTH = int(subprocess.check_output(['stty', 'size']).split()[1])
except Exception as e:
    # print_color_str('获取TERMINAL_WIDTH失败,采用默认值,错误信息:{}'.format(str(e)), color=CustomColors.RED)
    TERMINAL_WIDTH = 179


################################################################################################################
# 常用函数
################################################################################################################

class ColorfulPrint(object):
    """

    """

    @classmethod
    def print_text_str(cls, some_str):
        """
        """
        print bold(white(some_str))

    @classmethod
    def print_warning_str(cls, some_str, is_center=False):
        """
        """
        some_str = str(some_str)
        if is_center:
            some_str = auto_blank_filled(some_str)
        print bold(purple(some_str))

    @classmethod
    def print_warning_str_with_line(cls, some_str, is_center=False):
        """
        """
        some_str = str(some_str)
        if is_center:
            some_str = auto_blank_filled(some_str)

        line = bold(purple("─" * TERMINAL_WIDTH))
        print line
        print bold(purple(some_str.center(TERMINAL_WIDTH)))
        print line

    @classmethod
    def print_error_str(cls, some_str, is_center=False):
        """
        """
        some_str = str(some_str)
        print_color_str(some_str, CustomColors.RED, is_center=is_center)

    @classmethod
    def print_error_str_with_line(cls, some_str, is_center=False):
        """
        """
        some_str = str(some_str)
        print_color_str("─" * TERMINAL_WIDTH, CustomColors.RED)
        print_color_str(some_str, CustomColors.RED, is_center=is_center)
        print_color_str("─" * TERMINAL_WIDTH, CustomColors.RED)

    @classmethod
    def print_success_str(cls, some_str, is_center=False):
        """
        """
        some_str = str(some_str)
        print_color_str(some_str, CustomColors.GREEN, is_center=is_center)

    @classmethod
    def print_success_str_with_line(cls, some_str, is_center=False):
        """
        """
        some_str = str(some_str)
        print_color_str("─" * TERMINAL_WIDTH, CustomColors.GREEN)
        print_color_str(some_str, CustomColors.GREEN, is_center=is_center)
        print_color_str("─" * TERMINAL_WIDTH, CustomColors.GREEN)

    @classmethod
    def print_cool_paragraph(cls, some_paragraph, color=lightblue, title='', is_center=True, with_split_line=False,
                             absolute_center=False):
        """
        """
        if with_split_line:
            split_line = bold(bg(color(' ' * TERMINAL_WIDTH)))
            print(split_line)
        else:
            print

        # 打印标题
        if title:
            if is_center:
                title = auto_blank_filled(title)
            print bold(color(italic(title)))

        # 打印内容,居中

        if is_center:
            if absolute_center:
                line_list = some_paragraph.split('\n')
                for line in line_list:
                    blank_count = auto_blank_filled(line, just_get_prefix_blank_number=True)
                    print ' ' * blank_count, color(italic(line))
            else:
                line_list = some_paragraph.split('\n')
                blank_count_list = list()
                for line in line_list:
                    blank_count = auto_blank_filled(line, just_get_prefix_blank_number=True)
                    blank_count_list.append(blank_count)

                min_count = min(blank_count_list)
                for line in line_list:
                    print ' ' * min_count, color(italic(line))
        else:
            print color(italic(some_paragraph))

        if with_split_line:
            split_line = bold(bg(color(' ' * TERMINAL_WIDTH)))
            print(split_line)
        else:
            print


def print_warning_str(some_str, is_center=False):
    """
    """
    warnings.warn(
        "该函数废弃: 用新的ColorfulPrint类取代这个了!!",
        DeprecationWarning
    )
    some_str = str(some_str)
    if is_center:
        some_str = auto_blank_filled(some_str)
    print bold(purple(some_str))


def print_warning_str_with_line(some_str, is_center=False):
    """
    """
    warnings.warn(
        "该函数废弃: 用新的ColorfulPrint类取代这个了!!",
        DeprecationWarning
    )
    some_str = str(some_str)
    if is_center:
        some_str = auto_blank_filled(some_str)

    line = bold(purple("─" * TERMINAL_WIDTH))
    print line
    print bold(purple(some_str.center(TERMINAL_WIDTH)))
    print line


def print_error_str(some_str, is_center=False):
    """
    """
    warnings.warn(
        "该函数废弃: 用新的ColorfulPrint类取代这个了!!",
        DeprecationWarning
    )
    some_str = str(some_str)
    print_color_str(some_str, CustomColors.RED, is_center=is_center)


def print_error_str_with_line(some_str, is_center=False):
    """
    """
    warnings.warn(
        "该函数废弃: 用新的ColorfulPrint类取代这个了!!",
        DeprecationWarning
    )
    some_str = str(some_str)
    print_color_str("─" * TERMINAL_WIDTH, CustomColors.RED)
    print_color_str(some_str, CustomColors.RED, is_center=is_center)
    print_color_str("─" * TERMINAL_WIDTH, CustomColors.RED)


def print_success_str(some_str, is_center=False):
    """
    """
    warnings.warn(
        "该函数废弃: 用新的ColorfulPrint类取代这个了!!",
        DeprecationWarning
    )
    some_str = str(some_str)
    print_color_str(some_str, CustomColors.GREEN, is_center=is_center)


def print_success_str_with_line(some_str, is_center=False):
    """
    """
    warnings.warn(
        "该函数废弃: 用新的ColorfulPrint类取代这个了!!",
        DeprecationWarning
    )
    some_str = str(some_str)
    print_color_str("─" * TERMINAL_WIDTH, CustomColors.GREEN)
    print_color_str(some_str, CustomColors.GREEN, is_center=is_center)
    print_color_str("─" * TERMINAL_WIDTH, CustomColors.GREEN)


################################################################################################################
# 自定义函数
################################################################################################################
def print_color_notify_msg(custom_str, color=None, is_center=False):
    """

    """
    custom_str = str(custom_str)
    print_color_str("─" * TERMINAL_WIDTH, color=color)
    print_color_str(custom_str, color=color, is_center=is_center)
    print_color_str("─" * TERMINAL_WIDTH, color=color)


def print_small_notify_msg(custom_str, color=CustomColors.CYAN, is_center=False):
    """

    """
    print_color_str("─" * TERMINAL_WIDTH, color=color)
    print_color_str(custom_str, color=color, is_center=is_center)


def print_cyan_notify_msg(custom_str, is_center=False):
    """

    """
    print_color_notify_msg(custom_str, CustomColors.CYAN, is_center=is_center)


################################################################################################################
# 格式控制函数
################################################################################################################
def auto_blank_filled(some_str, just_get_prefix_blank_number=False):
    """
    """
    chinese_count, other = count_chinese_count(some_str)
    blank_count = (TERMINAL_WIDTH - (chinese_count * 2 + other)) / 2
    if blank_count <= 0:
        blank_count = 0
    if just_get_prefix_blank_number:
        return blank_count
    return ' ' * blank_count + some_str + ' ' * blank_count


def count_chinese_count(some_str):
    """
    """
    some_str = str(some_str)
    utf_l = len(ensure_utf8(some_str))
    uni_l = len(ensure_unicode(some_str))
    chinese_count = (utf_l - uni_l) / 2
    return chinese_count, uni_l - chinese_count


def is_some_str_contain_chinese_char(some_str):
    """
    """
    chinese_count, _ = count_chinese_count(some_str)
    if chinese_count > 0:
        return True
    return False


def is_number(some_str):
    try:
        float(some_str)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(some_str)
        return True
    except (TypeError, ValueError):
        pass

    return False


def best_judge_is_contain_chinese(some_str):
    """
    """
    chinese_count, _ = count_chinese_count(some_str=some_str)
    if chinese_count > 0:
        return True
    return False
