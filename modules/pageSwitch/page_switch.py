import time

import numpy as np

from device.automation import get_screenshots
from device.operate import operate_adb_tap, operate_adb_swipe
from modules.utils.main import calculate_max_timestamp, executeClickArea
from modules.general.module_options_name import shili, zhengbing, require_zhengbing, zhengbing_satisfy, queding, \
    going_list_txt, person_battle, battle_details, saodang, biaoji
from modules.general.option_verify_area import address_area_start, address_sign_verify, address_sign_land_area, \
    address_execute_order_area, address_execute_list, computed_going_time_area, computed_going_list_area, \
    address_going_require, click_draw_area, click_draw_detail_area, person_battle_area, person_detail_battle_area, \
    person_status_number_area, enemy_status_number_area, status_area, shili_area, zhengbing_page_verify_area, \
    click_list_x_y, zhengbing_page_area, zhengbing_page_swipe_verify, zhengbing_page_swipe, zhengbing_time_area, \
    queding_area
from ocr.main import ocr_default


def handle_in_map_conscription(l, *args):
    times = 0
    while 1:
        try:
            time.sleep(0.3)
            image = get_screenshots()
            # 点击势力
            if appear_then_click(image.crop(shili_area), shili_area, [shili]):
                continue
            if appear_then_click(image.crop(zhengbing_page_verify_area),
                                 zhengbing_page_verify_area,
                                 [shili], False):
                x, y = click_list_x_y
                operate_adb_tap(x * l, y)
                continue
            if appear_then_click(image.crop(zhengbing_page_area), zhengbing_page_area, zhengbing):
                continue
            if appear_then_click(image.crop(zhengbing_page_swipe_verify), zhengbing_page_swipe_verify,
                                 [require_zhengbing, zhengbing_satisfy],
                                 False):
                for v in zhengbing_page_swipe:
                    operate_adb_swipe(v[0], v[1], v[2], v[3])
                time_res = ocr_reg(ocr_default(np.array(image.crop(zhengbing_time_area))))
                times = calculate_max_timestamp(time_res)
                x, y = executeClickArea(zhengbing_page_swipe_verify)
                operate_adb_tap(x, y)
                continue
            if appear_then_click(image.crop(queding_area), queding_area, queding):
                return {
                    'type': 1,
                    'result': times,
                    'lists': l,
                    'args': args
                }
        except Exception as e:
            print('发生了错误', e)
            return None


def handle_out_map():
    pass


def appear_then_click(img_source, click_area, check_txt, clicked=True):
    res = ocr_default(np.array(img_source))
    if bool(res[0]):
        result = ''
        for sublist in res:
            for item in sublist:
                result += item[1][0]
        if result in check_txt:
            if clicked:
                x, y = executeClickArea(click_area)
                operate_adb_tap(x, y)
            return True
        else:
            return False
    else:
        return False


def handle_in_lists_action(l, txt=saodang, *args):
    while 1:
        try:
            time.sleep(0.3)
            image = get_screenshots()
            if not appear_then_click(image.crop(address_sign_verify), address_sign_verify, [biaoji], False):
                operate_adb_tap(address_area_start[0], address_area_start[1])
                continue
            if appear_then_click(image.crop(address_sign_verify), address_sign_verify, [biaoji]):
                continue
            if ocr_default(np.array(image.crop(address_sign_land_area)))[0]:
                operate_adb_tap(address_sign_land_area[0], address_sign_land_area[1])
                continue
            result = ocr_default(np.array(image.crop(address_execute_order_area)))
            if bool(result[0]):
                for idx in range(len(result)):
                    res = result[idx]
                    for line in res:
                        if line[1][0] == txt:
                            first_list = line[0]
                            center_point = [sum(coord) / len(coord) for coord in zip(*first_list)]
                            operate_adb_tap(820 + center_point[0], 200 + center_point[1])
                            continue
            if appear_then_click(image.crop(computed_going_list_area), computed_going_list_area, [going_list_txt],
                                 False):
                # 此处位置需要补充队伍排序问题
                x, y = address_execute_list
                operate_adb_tap(x, y)
                continue
            if appear_then_click(image.crop(address_going_require), address_going_require, [txt], False):
                time_res = ocr_reg(ocr_default(np.array(image.crop(computed_going_time_area))))
                times = calculate_max_timestamp(time_res)
                x, y = executeClickArea(address_going_require)
                operate_adb_tap(x, y)
                return {
                    'type': 2,
                    'result': times,
                    'lists': l,
                    'args': args
                }
        except Exception as e:
            print('发生了错误', e)
            return None


def handle_out_lists_action():
    pass


def handle_in_battle_result(l, times, *args):
    battle_result = {}
    while 1:
        try:
            time.sleep(0.3)
            image = get_screenshots()

            if appear_then_click(image.crop(shili_area), shili_area, [shili], False):
                operate_adb_tap(click_draw_area[0], click_draw_area[1])
                continue
            if appear_then_click(image.crop(person_battle_area), person_battle_area, [person_battle], False):
                operate_adb_tap(click_draw_detail_area[0], click_draw_detail_area[1])
                continue
            if appear_then_click(image.crop(person_detail_battle_area), person_detail_battle_area, [battle_details],
                                 False):
                status = ''
                person_number = ''
                enemy_number = ''
                while not bool(status) and not bool(person_number) and not bool(enemy_number):
                    status = ocr_reg(ocr_default(np.array(image.crop(status_area))))
                    person_number = ocr_reg(ocr_default(np.array(image.crop(person_status_number_area))))
                    enemy_number = ocr_reg(ocr_default(np.array(image.crop(enemy_status_number_area))))

                battle_result['status'] = status
                battle_result['person'] = person_number
                battle_result['enemy'] = enemy_number
                return {
                    'type': 3,
                    'result': battle_result,
                    'lists': l,
                    'times': times,
                    'args': args
                }
        except Exception as e:
            print('执行战报发生了错误', e)
            return None


def ocr_reg(res):
    if bool(res[0]):
        return [item[1][0] for sublist in res for item in sublist]
    else:
        return []
