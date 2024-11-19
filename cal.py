import numpy as np
import random
from tqdm import tqdm
import idm
import accl
import generate
import save
from operator import itemgetter
from Car_class import Car, Car_info, make_car, make_car_info


# calculate_accl
def simulation(time_max,  # シミュレーション時間
               q_lane1,  # 加速車線交通量
               q_lane2,  # 走行車線交通量
               q_lane3,  # 追越車線交通量
               acceleration_lane_start,  # 合流開始地点
               acceleration_lane_end,  # 合流終了地点
               use_base_station,  # 基地局有無
               ratio,  # 自動運転車比率
               seed  # シード値
               ):

    # ####ここから初期化部#####
    run_car_list = []
    # number_of_cars=1#これは現在の車の台数が入る変数、合流部に車両を設置するので、最初から1台になっている
    time_max = time_max * 10  # 0.1秒間隔で計算する。例えば600秒分計算するなら6000回計算することになる。
    # シミュレーションで動かす最大の車の台数=加速車線の最大台数+走行車線の最大台数+追越車線の最大台数
    CAR_MAX = q_lane1 + q_lane2 + q_lane3
    # 加速車線での車両発生間隔=最大時間/加速車線の最大台数(例:600秒/100台=6秒に1回に発生)
    frequency1 = int(time_max / q_lane1)
    frequency2 = int(time_max / q_lane2)  # 走行車線での車両発生間隔
    frequency3 = int(time_max / q_lane3)  # 追越車線での車両発生間隔
    a, b, c = 0, 0, 0

    next_generate_car_id = 1  # 次に発生する車両ID
    road_length = 800  # 道路の長さ
    communication_area = 30  # 通信範囲
    communication_start_point = 100  # 合流可能地点から何メートル前から通信を開始するか
    vel_sencer, uploaded_vel = 0, 0  # 最後に記録した速度
    SH_RATIO = 3.6  # 秒速と時速の比

    # ★固定値の車情報
    # 0ID,1最大加速度,2希望減速度,3安全車頭時間,4反応時間,5停止時最低車間距離,6初期速度,7希望速度,8優しいかどうか,9車両発生時刻,10合流部での加速するか否か
    # ------------------------------------------------------------------------------------
    # car_info=np.zeros((CAR_MAX,11))
    car_info = make_car_info(CAR_MAX)
    # car_info_add
    # --------------------------------------------------------------------------------------
    # car_info[0]=[0,0,0,1.0,1,1.65,0,0,0]#合流部に設置する車両の情報 delete by kino 2020-01-28    car_info[10][8]=0or1

    # ★固定値ではない車情報
    # -------------------------------------------------------------------
    # car = np.zeros((time_max+1201,CAR_MAX,15))
    # car = [[Car(id) for id in range(CAR_MAX)]for time in range(time_max+1201)]
    car = make_car(time_max + 1201, CAR_MAX)
    # -------------------------------------------------------------------
    # 0ID、1前方位置、2後方位置、3車線、4速度、5加速度、6車間距離,7相対速度,8前方車両ID
    # 9車線変更している途中か,10車線変更先の車線,11車線変更開始時間,12車線変更先車間距離,13車線変更先前方車両ID,14目標車両ID
    # for time in range(time_max):delete by kino 2020-01-28
    #    car[time][0]=[0,acceleration_lane_end+1,acceleration_lane_end,1,0,0,0,0,-1,0,0,0,0,-1,-1]#合流部の車設置delete by kino car[time-10][ID][5]

    # ★基地局情報
    # 例:加速車線の車両ID=123は位置700mから位置750mの間を走っている走行車線の車両に要求を出す。ID=456が承認した場合
    # base_station[123]=[750,700,456] base_station[10][2] = 14
    # 0位置A,1位置B,2承認車両ID calculate_accl
    base_station = np.zeros((CAR_MAX, 3))
    for i in range(CAR_MAX):
        base_station[i][2] = -1  # 譲る車両が存在しないときは-1

    random.seed(seed)  # cal.pyシード値固定
    # 車両の発生時刻の初期化と生成
    generatetime_lane1 = np.zeros(q_lane1)
    generatetime_lane2 = np.zeros(q_lane2)
    generatetime_lane3 = np.zeros(q_lane3)
    generatetime_lane1, generatetime_lane2, generatetime_lane3 = generate.ganerate_car_timetable(q_lane1,
                                                                                                 q_lane2,
                                                                                                 q_lane3,
                                                                                                 frequency1,
                                                                                                 frequency2,
                                                                                                 frequency3,
                                                                                                 generatetime_lane1,
                                                                                                 generatetime_lane2,
                                                                                                 generatetime_lane3
                                                                                                 )
    time_max += 1200  # すべての車が走りきるための時間
    # ####ここまで初期化部#####
    # ######シミュレーション開始#######
    for time in tqdm(range(time_max), desc='simu'):  # シミュレーションする時間だけループ
        # 車線ごとに前方位置順にIDを並べたリストが返ってくる(降順)このリストは時間が進むごとに更新される。
        lane1_list, lane2_list, lane3_list = idm.return_lane_list(
            car, run_car_list, time)

        if use_base_station == 1:  # センサのときのみ
            vel_sencer, tmp_id, tmp_position = 0, 0, 9999  # 初期化
            flag = 0  # 初期化

            for k in lane2_list:  # 走行車線の車両
                if lane2_list is not None:
                    k = int(k)
                    if acceleration_lane_start - 35 < car[time][k].back < acceleration_lane_start - 25:
                        if 0 < car[time][k].back - acceleration_lane_start + 30 < tmp_position:
                            tmp_position = car[time][k].back - \
                                acceleration_lane_start + 30
                            tmp_id = k
                            flag = 1

            if flag == 1:
                vel_sencer = car[time][tmp_id].vel
                uploaded_vel = vel_sencer
            else:
                vel_sencer = uploaded_vel  # 最後に記録した速度を代入

        for j in run_car_list:  # 車両の数だけループ
            # 現在の情報を変数にコピーするだけ
            car_id = int(car[time][j].id)  # ID
            car_front = car[time][j].front  # 前方位置
            car_back = car[time][j].back  # 後方位置
            car_lane = car[time][j].lane  # 車線
            car_vel = car[time][j].vel  # 速度m/s
            shift_lane = car[time][j].shift_lane  # 車線変更してる途中かどうか
            shift_lane_to = car[time][j].shift_lane_to  # どこの車線に変更しようとしてるか
            shift_begin = car[time][j].shift_begin  # 車線変更開始時間
            # 車間と前にいる車のIDを調べる処理
            front_car_id, car_distance = idm.calculate_car_distance(car, time, int(
                car_id), car_lane, lane1_list, lane2_list, lane3_list, acceleration_lane_end)
            # delta_vを調べる処理,delta_vは前の車両との速度差
            if front_car_id == -1:  # -1のときは車が前にいない状態
                if (car_lane == 1 and ((car_vel * car_vel / 3.8) / 2 + 5 > (acceleration_lane_end - car_front))):
                    # その地点から最大減速度で減速し続けて加速車線の終了地点の直前で止まる条件なら、終了地点に停止車両がいる扱いにする。+5は終点の5メートル前という意味
                    delta_v = car_vel
                else:
                    delta_v = 0
            else:
                delta_v = car_vel - \
                    car[time][int(front_car_id)].vel  # 自分の速度－相手の速度

            car_accl, shift_distance_go, shift_id_go, target_id, shift_lane, shift_lane_to, shift_begin = accl.calculate_accl(car, car_info, base_station, time, j, run_car_list, car_id, car_front, car_back, car_lane, car_vel, delta_v, front_car_id,
                                                                                                                              car_distance, use_base_station, shift_lane, shift_lane_to, shift_begin, acceleration_lane_start, acceleration_lane_end, communication_area, communication_start_point, vel_sencer)

            # 車線変更・合流(ここでは車線変更開始するだけ)
            # 加速車線にいるか,位置が合流できる範囲か
            if shift_lane == 0:  # 車線変更を開始していないとき
                if car_lane == 1:
                    # 加速車線に入ったら希望速度の変更 走行車線と同じ速度にする
                    if acceleration_lane_start < car_front and (0 / SH_RATIO) < car_info[int(car_id)].vd < (65 / SH_RATIO) and car_info[j].acc_on_cross == 0:
                        car_info[int(car_id)].vd = round(random.uniform(
                            65 / SH_RATIO, 75 / SH_RATIO), 0)  # 希望速度変更 加速車線に入ったら希望速度の変更
                        car_info[j].acc_on_cross = 1
                    # 合流可能ならば本線に合流する
                    if idm.merging_lane2(car, time, run_car_list, j, 2) and car_back > acceleration_lane_start:
                        shift_lane = 1  # 車線変更してる途中かどうか
                        shift_lane_to = 2  # どこの車線に変更しようとしてるか
                        shift_begin = time  # 車線変更開始時間
                        car_info[int(car_id)].vd = round(random.uniform(
                            65 / SH_RATIO, 75 / SH_RATIO), 0)  # 希望速度変更 加速車線に入ったら希望速度の変更
                        car_info[car_id].acc_on_cross = 0  # 合流時のポリシーを解除する
                    elif use_base_station >= 1:  # 合流可能でなくて基地局ありのとき譲るよう要求を行う
                        if car_back > acceleration_lane_start - communication_start_point:  # 合流可能でないとき  加速車線手前－50ｍ合流車両の後ろより車線変更を始める位置
                            car_id = int(car_id)
                            # まだIDが更新されていないときは中に入る(譲ってくれる車両がいないとき)
                            if base_station[car_id][2] == -1:
                                base_station[car_id][0] = car_front
                                base_station[car_id][1] = car_back - \
                                    communication_area
                                list = [[]]
                                # 近くを走っている車両を調べる
                                for i in run_car_list:
                                    # 走行している車線が走行車線のとき,走行位置が検索範囲内か,優しいかどうか
                                    if car[time][i].lane == 2 and base_station[car_id][1] < car[time][i].front < base_station[car_id][0] and car_info[i].kindness == 1:
                                        list += [[car[time][i].id, round(car_front - car[time][i].front, 0)]]
                                del list[0]  # リストの先頭は0が入って不要なので削除
                                if len(list) >= 1:  # 譲ってくれる車両があった場合
                                    list.sort(key=itemgetter(1, 0))
                                    base_station[car_id][2] = list[0][0]
                                else:  # 譲る車がいなかった場合
                                    base_station[car_id][2] = -1
                # elif car_lane==2:#車線変更制御。走行→追い越し
                #     if idm.change_lane(car,time,run_car_list,j,3):
                #         shift_lane   =1#車線変更してる途中かどうか
                #         shift_lane_to=3#どこの車線に変更しようとしてるか
                #         shift_begin  =time#車線変更開始時間
                #         car_info[int(car_id)][7]=round(random.uniform(65/SH_RATIO,75/SH_RATIO),0)#希望速度変更
                # elif car_lane==3:#車線変更制御。走行→追い越し
                #     if idm.change_lane(car,time,run_car_list,j,2):
                #         shift_lane   =1#車線変更してる途中かどうか
                #         shift_lane_to=2#どこの車線に変更しようとしてるか
                #         shift_begin  =time#車線変更開始時間
                #         car_info[int(car_id)][7]=round(random.uniform(65/SH_RATIO,75/SH_RATIO),0)#希望速度変更
            # 車線変更・合流(終了)
            if shift_lane == 1 and time == shift_begin + 40:
                car_lane = shift_lane_to
                shift_lane_to, shift_lane, shift_begin = 0, 0, 0

            # 現在速度計算
            car_vel += car_accl / 10  # 速度計算
            if car_vel < 0:
                car_vel = 0

            # 位置計算
            car_front = round(car_front + car_vel / 10, 2)  # 前方位置代入
            car_back = round(car_back + car_vel / 10, 2)  # 後方位置代入

            car[time + 1][j].id = car_id  # ID代入
            car[time + 1][j].front = car_front  # 前方位置代入
            car[time + 1][j].back = car_back  # 後方位置代入
            car[time + 1][j].lane = car_lane  # 車線代入
            car[time + 1][j].vel = round(car_vel, 2)  # 速度代入
            car[time + 1][j].accl = round(car_accl, 2)  # 加速度代入
            car[time][j].distance = round(car_distance, 2)  # 車間距離代入
            car[time][j].delta_v = round(delta_v, 2)  # 相対速度
            car[time][j].front_car_id = front_car_id  # 前方車両ID
            car[time + 1][j].shift_lane = shift_lane  # 車線変更してる途中かどうか
            car[time + 1][j].shift_lane_to = shift_lane_to  # どこの車線に変更しようとしてるか
            car[time + 1][j].shift_begin = shift_begin  # 車線変更開始時間
            car[time + 1][j].shift_distance_go = shift_distance_go  # 車線変更先車間距離
            car[time + 1][j].shift_id_go = shift_id_go  # 車線変更先前方車両ID
            car[time + 1][j].target_id = target_id  # 目標車両ID

        # 車両発生
        # car,car_info,run_car_list,next_generate_car_id,a,b=generate.generate_car2(time,run_car_list,car,car_info,CAR_MAX,next_generate_car_id,lane1_list,lane2_list,ratio,a,b,generatetime_lane1,generatetime_lane2,q_lane1,q_lane2)
        car, car_info, run_car_list, next_generate_car_id, a, b, c = generate.generate_car(
            time, run_car_list, car, car_info, CAR_MAX, next_generate_car_id, lane1_list, lane2_list, lane3_list, ratio, a, b, c, generatetime_lane1, generatetime_lane2, generatetime_lane3, q_lane1, q_lane2, q_lane3)
        # 車両削除
        run_car_list = generate.remove_car(
            car, time, run_car_list, road_length)
    # ######シミュレーション終了#######

    # #######記録開始########
    save.save4(car, base_station, use_base_station, CAR_MAX, time_max, 10, q_lane1, q_lane2,
               q_lane3, acceleration_lane_start, acceleration_lane_end, seed, car_info, ratio, road_length)
    # #######記録終了########
