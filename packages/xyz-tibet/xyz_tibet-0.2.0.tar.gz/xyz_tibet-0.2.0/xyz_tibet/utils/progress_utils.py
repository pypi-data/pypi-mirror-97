# -*- encoding:utf-8 -*-

import sys
import time

from xyz_tibet.utils.control_utils import auto_blank_filled


class ShowProcess():
    """
    显示处理进度的类
    调用该类相关函数即可实现处理进度的显示
    """
    i = 0  # 当前的处理进度
    max_steps = 0  # 总共需要处理的次数
    max_arrow = 50  # 进度条的长度
    infoDone = 'done'

    # 初始化函数，需要知道总共的处理次数
    def __init__(self, max_steps, infoDone='Done'):
        self.max_steps = max_steps
        self.i = 0
        self.infoDone = infoDone

    # 显示函数，根据当前的处理进度i显示进度
    # 效果为[>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]100.00%
    def show_process(self, i=None):
        if i is not None:
            self.i = i
        else:
            self.i += 1
        num_arrow = int(self.i * self.max_arrow / self.max_steps)  # 计算显示多少个'>'
        num_line = self.max_arrow - num_arrow  # 计算显示多少个'-'
        percent = self.i * 100.0 / self.max_steps  # 计算完成进度，格式为xx.xx%
        process_bar = '[' + '>' * num_arrow + '-' * num_line + ']' \
                      + '%.2f' % percent + '%' + '\r'  # 带输出的字符串，'\r'表示不换行回到最左边
        sys.stdout.write(process_bar)  # 这两句打印字符到终端
        sys.stdout.flush()
        if self.i >= self.max_steps:
            self.close()

    def close(self):
        print('')
        print(self.infoDone)
        self.i = 0


def count_down(second, is_center=True):
    try:
        msg = "倒计时 {} 秒！\r"
        blank_number = auto_blank_filled(msg, just_get_prefix_blank_number=True)

        for i in range(second, 0, -1):
            if is_center:
                final_msg = ' ' * blank_number + msg.format(i)
                sys.stdout.write(final_msg)  # 这两句打印字符到终端
            else:
                sys.stdout.write(msg.format(i))  # 这两句打印字符到终端
            sys.stdout.flush()
            time.sleep(1)
    except Exception as e:
        print str(e)
