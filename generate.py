# import idm
import random

# def set_seed(seed):
#     random.seed(seed)


def generate_random(per):  # 引数は1を生成する確率[%]
    x = random.randint(1, 100)
    if x > per:
        return 0
    else:
        return 1


def ganerate_car_timetable(q_lane1, q_lane2, q_lane3, frequency1, frequency2, frequency3, generatetime_lane1, generatetime_lane2, generatetime_lane3):
    for i in range(q_lane1 - 1):
        generatetime_lane1[i + 1] = generatetime_lane1[i] + frequency1
    for i in range(q_lane2 - 1):
        generatetime_lane2[i + 1] = generatetime_lane2[i] + frequency2 + \
            int(frequency2 * round(random.uniform(-0.5, 0.5), 2))
    for i in range(q_lane3 - 1):
        generatetime_lane3[i + 1] = generatetime_lane3[i] + frequency3 + \
            int(frequency3 * round(random.uniform(-0.5, 0.5), 2))
    return generatetime_lane1, generatetime_lane2, generatetime_lane3


def ganerate_car_timetable2(q_lane1, q_lane2, frequency1, frequency2, generatetime_lane1, generatetime_lane2):
    for i in range(q_lane1 - 1):
        generatetime_lane1[i + 1] = generatetime_lane1[i] + frequency1
    for i in range(q_lane2 - 1):
        generatetime_lane2[i + 1] = generatetime_lane2[i] + frequency2 + \
            int(frequency2 * round(random.uniform(-0.5, 0.5), 2))
    return generatetime_lane1, generatetime_lane2


def car_info_add(car, time, next_generate_car_id, car_info, car_lane, front_car_id, ratio):
    max_accl = round(random.uniform(0.55, 0.75), 2)  # 最大加速度
    desired_Deceleration = round(random.uniform(0.5, 1), 1)  # 希望減速度
    driver_reaction_time = round(random.uniform(0.54, 0.74), 2)  # 反応時間
    if front_car_id == -1:  # 前に車がいない場合
        if car_lane == 1:  # 合流部に車両が1台止まっているので実はここには入らないが、一応
            # vd=round(random.uniform(70/3.6,80/3.6),0)#希望速度
            vd = round(random.uniform(65 / 3.6, 75 / 3.6), 0)  # 希望速度
            v_measure = vd  # 初期速度
        elif car_lane == 2:
            # vd=round(random.uniform(85/3.6,95/3.6),0)#希望速度
            vd = round(random.uniform(65 / 3.6, 75 / 3.6), 0)  # 希望速度
            v_measure = vd  # 初期速度
        elif car_lane == 3:
            # vd=round(random.uniform(95/3.6,105/3.6),0)#希望速度
            vd = round(random.uniform(65 / 3.6, 75 / 3.6), 0)  # 希望速度
            v_measure = vd  # 初期速度
    else:  # 前に車がいる場合
        if car_lane == 1:
            #     v_measure=round(car[time][front_car_id][4],0)#初期速度
            #     # vd=round(random.uniform(70/3.6,80/3.6),0)#希望速度
            #     vd=round(random.uniform(55/3.6,55/3.6),0)#希望速度 20200817
            vd = round(random.uniform(65 / 3.6, 75 / 3.6), 0)  # 希望速度
            v_measure = vd  # 初期速度
        elif car_lane == 2:
            # v_measure=round(car[time][front_car_id][4],0)#初期速度
            # # vd=round(random.uniform(85/3.6,95/3.6),0)#希望速度
            # vd=round(random.uniform(65/3.6,75/3.6),0)#希望速度
            vd = round(random.uniform(65 / 3.6, 75 / 3.6), 0)  # 希望速度
            v_measure = vd  # 初期速度
        elif car_lane == 3:
            v_measure = round(car[time][front_car_id].vel, 0)  # 初期速度
            # vd=round(random.uniform(95/3.6,105/3.6),0)#希望速度
            vd = round(random.uniform(65 / 3.6, 75 / 3.6), 0)  # 希望速度
    # 0ID,1最大加速度,2希望減速度,3安全車頭時間,4反応時間,5停止時最低車間距離,6初期速度,7希望速度,8やさしいかどうか,9発生した時間,10合流時加速するか否か
    # 割合変更
    return [next_generate_car_id, max_accl, desired_Deceleration, 1.0, driver_reaction_time, 1.65, v_measure, vd, generate_random(ratio), time, 0]


def generate_car(time, run_car_list, car, car_info, car_max, next_generate_car_id, lane1_list, lane2_list, lane3_list, ratio, a, b, c, generatetime_lane1, generatetime_lane2, generatetime_lane3, q_lane1, q_lane2, q_lane3):
    if time == generatetime_lane1[a] and next_generate_car_id < car_max:
        if len(lane1_list) == 0:
            front_car_id = -1
            m = 9999
        else:
            front_car_id = int(lane1_list[-1])
            m = car[time][front_car_id].back
        # ----------------------------------------------------------------------------------------------------------------
        # car_info[next_generate_car_id]=car_info_add(car,time,next_generate_car_id,car_info,1,front_car_id,ratio)
        car_info[next_generate_car_id].ls_to_vars(car_info_add(
            car, time, next_generate_car_id, car_info, 1, front_car_id, ratio))
        # ------------------------------------------------------------------------------------------------------------------
        # 0ID、1前方位置、2後方位置、3車線、4速度、5加速度、6車間距離,7相対速度,8前方車両ID
        # 9車線変更している途中か,10車線変更先の車線,11車線変更開始時間,12車線変更先車間距離,13車線変更先前方車両ID,14目標車両ID
        car[time + 1][next_generate_car_id].ls_to_vars(
            [next_generate_car_id, 5, 0, 1, car_info[next_generate_car_id].v_init, 0, m, 0, front_car_id, 0, 0, 0, 0, -1, -1])
        run_car_list += [next_generate_car_id]
        next_generate_car_id += 1
        if a < q_lane1 - 1:
            a += 1
        # a=a+frequency1+int(frequency1*round(random.uniform(-0.5,0.5),2))
    if time == generatetime_lane2[b] and next_generate_car_id < car_max:
        if len(lane2_list) == 0:
            front_car_id = -1
            m = 9999
        else:
            front_car_id = int(lane2_list[-1])
            m = car[time][front_car_id].back
        car_info[next_generate_car_id].ls_to_vars(car_info_add(
            car, time, next_generate_car_id, car_info, 2, front_car_id, ratio))
        car[time + 1][next_generate_car_id].ls_to_vars(
            [next_generate_car_id, 5, 0, 2, car_info[next_generate_car_id].v_init, 0, m, 0, front_car_id, 0, 0, 0, 0, -1, -1])
        run_car_list += [next_generate_car_id]
        next_generate_car_id += 1
        # b=b+frequency2+int(frequency2*round(random.uniform(-0.5,0.5),2))
        if b < q_lane2 - 1:
            b += 1
    if time == generatetime_lane3[c] and next_generate_car_id < car_max:
        if len(lane3_list) == 0:
            front_car_id = -1
            m = 9999
        else:
            front_car_id = int(lane3_list[-1])
            m = car[time][front_car_id].back
        car_info[next_generate_car_id].ls_to_vars(car_info_add(
            car, time, next_generate_car_id, car_info, 3, front_car_id, ratio))
        car[time + 1][next_generate_car_id].ls_to_vars(
            [next_generate_car_id, 5, 0, 3, car_info[next_generate_car_id].v_init, 0, m, 0, front_car_id, 0, 0, 0, 0, -1, -1])
        run_car_list += [next_generate_car_id]
        next_generate_car_id += 1
        # c=c+frequency3+int(frequency3*round(random.uniform(-0.5,0.5),2))
        if c < q_lane3 - 1:
            c += 1
    return car, car_info, run_car_list, next_generate_car_id, a, b, c


def generate_car2(time, run_car_list, car, car_info, car_max, next_generate_car_id, lane1_list, lane2_list, ratio, a, b, generatetime_lane1, generatetime_lane2, q_lane1, q_lane2):
    if time == generatetime_lane1[a] and next_generate_car_id < car_max:
        if len(lane1_list) == 0:
            front_car_id = -1
            m = 9999
        else:
            front_car_id = int(lane1_list[-1])
            m = car[time][front_car_id].back
        car_info[next_generate_car_id].ls_to_vars(car_info_add(
            car, time, next_generate_car_id, car_info, 1, front_car_id, ratio))
        # 0ID、1前方位置、2後方位置、3車線、4速度、5加速度、6車間距離,7相対速度,8前方車両ID
        # 9車線変更している途中か,10車線変更先の車線,11車線変更開始時間,12車線変更先車間距離,13車線変更先前方車両ID,14目標車両ID
        car[time + 1][next_generate_car_id].ls_to_vars(
            [next_generate_car_id, 5, 0, 1, car_info[next_generate_car_id].v_init, 0, m, 0, front_car_id, 0, 0, 0, 0, -1, -1])
        run_car_list += [next_generate_car_id]
        next_generate_car_id += 1
        if a < q_lane1 - 1:
            a += 1
        # a=a+frequency1+int(frequency1*round(random.uniform(-0.5,0.5),2))
    if time == generatetime_lane2[b] and next_generate_car_id < car_max:
        if len(lane2_list) == 0:
            front_car_id = -1
            m = 9999
        else:
            front_car_id = int(lane2_list[-1])
            m = car[time][front_car_id].back
        car_info[next_generate_car_id].ls_to_vars(car_info_add(car, time, next_generate_car_id, car_info, 2, front_car_id, ratio))
        car[time + 1][next_generate_car_id].ls_to_vars([next_generate_car_id, 5, 0, 2, car_info[next_generate_car_id].v_init, 0, m, 0, front_car_id, 0, 0, 0, 0, -1, -1])

        run_car_list += [next_generate_car_id]
        next_generate_car_id += 1

        # b=b+frequency2+int(frequency2*round(random.uniform(-0.5,0.5),2))
        if b < q_lane2 - 1:
            b += 1
    return car, car_info, run_car_list, next_generate_car_id, a, b


def remove_car(car, time, run_car_list, road_length):
    """
    道路を走り終えた車両の削除
    """
    a = -1
    for car_id in run_car_list:
        if car[time][car_id].front > road_length:  # 前方位置
            run_car_list.remove(car_id)
        if car[time][car_id].shift_begin + 40 == time and car[time][car_id].lane == 1 and car[time - 1][car_id].shift_lane == 1:
            if car[time][car_id].vel < 40 / 3.6 or car[time - 40][car_id].vel - car[time][car_id].vel > 10 / 3.6:
                run_car_list.remove(car_id)
                a = 1
        if car[time][car_id].shift_lane == 0 and car[time][car_id].front > 950 and car[time][car_id].lane == 1 and a == -1:
            run_car_list.remove(car_id)
    return run_car_list
