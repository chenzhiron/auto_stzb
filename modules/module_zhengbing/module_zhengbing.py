import time

from config.const import TIMESLEEP
from config.paths import path
from device.main_device import return_device
from modules.general.module_error_txt import click_zhengbing_error, swipe_zhengbing_error, require_zhengbing_error
from modules.general.module_options_name import zhengbing, require_zhengbing, queding, zhengbing_verify
from modules.module_address.module_address_area import address_affirm_button
from modules.module_zhengbing.module_zhengbing_area import (zhengbing_page_area,
                                                            zhengbing_page_swipe,
                                                            zhengbing_page_queren_area,
                                                            zhengbing_time_area,
                                                            zhengbing_time_queren_area,
                                                            )
from ocr.main import ocr_txt_verify, ocr_default
from tools.reg_click_direction import reg_direction
from tools.reg_screenshot import general_screenshot_tools
from tools.reg_time import split_string, reg_time


# 进入点击征兵页面
def module_zhengbing_click(auto_txt=zhengbing):
    time_number = 50
    while time_number > 0:
        time.sleep(TIMESLEEP)
        if ocr_txt_verify(path, auto_txt, zhengbing_page_area):
            device = return_device()
            x, y = reg_direction(zhengbing_page_area)
            device.click(x, y)
            return True
        else:
            time_number -= 1
    if time_number <= 0:
        raise Exception(click_zhengbing_error)


# 滑动征兵模块
def module_swipe_zhengbing_click(auto_txt=require_zhengbing):
    time_number = 50
    while time_number > 0:
        time.sleep(TIMESLEEP)
        if ocr_txt_verify(path, auto_txt, zhengbing_page_queren_area):
            for v in zhengbing_page_swipe:
                device = return_device()
                device.swipe(sx=v[0], sy=v[1], ex=v[2], ey=v[3], duration=v[4])
            break
        else:
            time_number -= 1
    if time_number <= 0:
        raise Exception(swipe_zhengbing_error)


# 计算征兵时间
def module_zhengbing_computed_time():
    time.sleep(TIMESLEEP)
    general_screenshot_tools(zhengbing_time_area)
    result = ocr_default(path).replace('\n', '').replace('\r', '')
    result = split_string(result, 8)
    max_time = []
    for v in result:
        max_time.append(reg_time(v))
    max_time.sort(reverse=True)
    return max_time[0]
    # 后续逻辑


# 验证征兵已满
def module_verify_zhengbing():
    time_number = 5
    while time_number > 0:
        time.sleep(TIMESLEEP)
        if ocr_txt_verify(path, zhengbing_verify, zhengbing_page_queren_area):
            return True
        time_number -= 1
    return False


# 点击确认征兵按钮
def module_zhengbing_affirm_btn():
    device = return_device()
    x, y = address_affirm_button
    device.click(x, y)
    time.sleep(TIMESLEEP)


# 确定征兵
def module_zhuangbing_require(auto_txt=queding):
    time_number = 50
    while time_number > 0:
        time.sleep(TIMESLEEP)
        # 确认 区域重新点击
        if ocr_txt_verify(path, auto_txt, zhengbing_time_queren_area):
            device = return_device()
            x, y = reg_direction(zhengbing_time_queren_area)
            device.click(x, y)
            break
        else:
            time_number -= 1
    if time_number <= 0:
        raise Exception(require_zhengbing_error)

# if __name__ == '__main__':
#     connect_device()
#     result = module_verify_zhengbing()
#     print(result)
#     module_zhengbing_click(path)
#     module_swipe_zhengbing_click(path)
#     maxtime = module_zhengbing_computed_time(path)
#     print(maxtime)
#     module_zhengbing_affirm_btn()
#     module_zhuangbing_require(path)
