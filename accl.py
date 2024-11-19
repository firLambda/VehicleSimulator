import idm
# import random

# def set_seed(seed):
#     random.seed(seed)


def calculate_accl(car, car_info, base_station, time, j, run_car_list, car_id, car_front, car_back, car_lane, car_vel, delta_v, front_car_id,
                   car_distance, use_base_station, shift_lane, shift_lane_to, shift_begin, acceleration_lane_start, acceleration_lane_end, communication_area, communication_start_point, vel_sencer):
  """
  加速度を計算して加速度を返す
  """
  # ★以下は通常の車両追従の加速度算出
  desired_vehicle_distance = idm.desired_vehicle_distance(
      car_info[j].dis_stop, car_vel, car_info[j].passing_time, car_info[j].driver_reaction_time, delta_v, car_info[j].max_accl, car_info[j].desired_Deceleration)  # 希望車間距離を調べる処理

  car_accl = idm.calculate_accl(
      car_info[j].max_accl, car_vel, desired_vehicle_distance, car_distance, car_info[j].vd)  # 希望車間距離から加速度算出

  target_id = int(front_car_id)  # target_idはどの車両を目指して走行するかを示す。

  if use_base_station == 0:  # 基地なし
    if car_lane == 1 and acceleration_lane_start < car_front < acceleration_lane_end and car_accl >= 0:  # 合流可能な範囲に入って前方車両がいなければ最大加速度で加速する
      if (car_vel * car_vel / 3.8) / 2 + 5 < (acceleration_lane_end - car_front):
        if idm.search_car(car, car_info, time, run_car_list, j, acceleration_lane_start, acceleration_lane_end, 2):
          car_accl = float(car_info[j].max_accl)
        else:
          car_accl = 0
  # ★以下は基地局を使った譲るなどを考慮したになにか入れる)car,time,j
    if car_lane == 1:  # 加速車線加速度算出
      if use_base_station == 1:  # 基地局あり(ここ
        # 加速車線を走る車が譲ってくれる車両の前方車両の後方を目指して走る
        give_way_id = base_station[car_id][2]  # 譲ってくれる車両ID
        if give_way_id != -1:  # 譲ってくれる車両がいたとき
          if (car[time][j].lane == 2):  # 譲ってくれる車両が走行車線を走っている時
            driving_lane_front_car_id = (car[time][give_way_id].shift_id_go)  # 譲る車両の前方車両ID
            accl_car_distance = (car[time][driving_lane_front_car_id].distance - car_front)  # 譲る車の前方車両との車間距離
            accl_car_delta_v = car_vel - car[time][int(driving_lane_front_car_id)].vel  # 速度差
            accl_desired_vehicle_distance = idm.desired_vehicle_distance(car_info[j].dis_stop, car_vel, car_info[j].passing_time, car_info[j].driver_reaction_time, accl_car_delta_v, car_info[j].max_accl, car_info[j].desired_Deceleration)
            if accl_car_distance < 0:  # 譲る車両の前方車両が自車の後方にいるとき
              accl_car_accl = -1.0
            else:
              accl_car_accl = idm.calculate_accl(
                  car_info[j].max_accl, car_vel, accl_desired_vehicle_distance, accl_car_distance, car_info[j].vd)
            if accl_car_accl < car_accl:  # 加速度で比較
              car_accl = accl_car_accl
              target_id = driving_lane_front_car_id  # target_idはどの車両を目指して走っているかを示す
          else:  # 譲ってくれる車両が追い越し車線にいるとき
            base_station[int(car_id)][2] = -1  # -1に更新
    elif car_lane == 2:  # 走行車線
      # 自分が譲るかどうかを調べる
      for i in run_car_list:  # iが加速車線の車両ID
        # 基地局に自分の車が登録されていて、譲る相手の車が加速車線を走っているときその車に譲る
        if base_station[i][2] == car_id and (car[time][i].lane) == 1:
          accl_car_distance = (
              car[time][i].back - car_front)  # 加速車線の車両との車間
          accl_car_delta_v = car_vel - \
              car[time][i].vel  # 加速車線との車両との速度差
          accl_desired_vehicle_distance = idm.desired_vehicle_distance(
              car_info[j].dis_stop, car_vel, car_info[j].passing_time, car_info[j].driver_reaction_time, accl_car_delta_v, car_info[j].max_accl, car_info[j].desired_Deceleration)
          if accl_car_distance < 0:
            accl_car_accl = -1.0
          else:
            accl_car_accl = idm.calculate_accl(
                car_info[j].max_accl, car_vel, accl_desired_vehicle_distance, accl_car_distance, car_info[j].vd)
          if accl_car_accl < car_accl:  # 加速度で比較
            car_accl = accl_car_accl
            target_id = i

  # ★以下は車線変更の途中を考慮した加速度算出
  # 前方で車線変更している車がいたらそれに合わせる
  shift_distance_come = 9999  # shift_distance_comeは車線変更しようとしてくる車両との車間距離
  shift_id_come = -1  # shift_id_comeは前方で車線変更する車両ID,いない場合は-1
  desired_vehicle_distance_come = 0
  for i in run_car_list:
    # 車線変更しようとしてる,自分のいる車線に変更しようとしてる
    if car[time][i].shift_lane == 1 and car[time][i].shift_lane_to == car_lane and car[time][i].front < acceleration_lane_start - 50 and car[time][i].vel > 40 / 3.6:
      shift_distance_come_tmp = car[time][i].front - car_front
      if 0 < shift_distance_come_tmp < shift_distance_come:  # 0以上の最小値を調べている
        shift_distance_come = shift_distance_come_tmp  # 車間距離更新
        shift_id_come = car[time][i].id
  if shift_id_come != -1:
    shift_distance_come = car[time][int(
        shift_id_come)].back - car_front  # 車線変更しようとしている車両との車間距離
    shift_delta_v_come = car_vel - \
        car[time][int(shift_id_come)].vel  # 車線変更しようとしている車両との相対速度
    desired_vehicle_distance_come = idm.desired_vehicle_distance(
        car_info[j].dis_stop, car_vel, car_info[j].passing_time, car_info[j].driver_reaction_time, shift_delta_v_come, car_info[j].max_accl, car_info[j].desired_Deceleration)
    if shift_distance_come < 0:
      accl_car_accl = -0.5
    else:
      accl_car_accl = idm.calculate_accl(
          car_info[j].max_accl, car_vel, desired_vehicle_distance_come, shift_distance_come, car_info[j].vd)
    if accl_car_accl < car_accl and desired_vehicle_distance_come > shift_distance_come:
      car_accl = accl_car_accl
      target_id = shift_id_come
  # 自分が車線変更しようとしてるならば、車線変更先の前方車両に速度をあわせる// shira
  shift_distance_go = 9999  # 車線変更先の前方車両との車間距離
  shift_id_go = -1  # 車間距離先の前方車両ID
  desired_vehicle_distance_go = 0  # 車線変更先の前方車両との希望車間距離
  if shift_lane == 1:  # 自分が車線変更しているとき
    for i in run_car_list:  # 車線変更先の前方車両を探す
      if car[time][i].lane == shift_lane_to:  # 探している車が車線変更先と同じ車線のとき
        shift_distance_go_tmp = car[time][i].front - car_front
        if shift_distance_go_tmp > 0 and shift_distance_go_tmp < shift_distance_go:  # 0以上の最小値を調べている
          shift_distance_go = shift_distance_go_tmp  # 車間距離更新
          shift_id_go = car[time][i].id
    if shift_id_go != -1:  # 車線変更先の前方車両がいたら
      # 車線変更先の前方車両の後方位置-自分の前方位置
      shift_distance_go = car[time][int(shift_id_go)].back - car_front
      shift_delta_v_go = car_vel - car[time][int(shift_id_go)].vel  # 相対速度
      desired_vehicle_distance_go = idm.desired_vehicle_distance(
          car_info[j].dis_stop, car_vel, car_info[j].passing_time, car_info[j].driver_reaction_time, shift_delta_v_go, car_info[j].max_accl, car_info[j].desired_Deceleration)
      if shift_distance_go < 0:
        accl_car_accl = -0.5
      else:
        accl_car_accl = idm.calculate_accl(
            car_info[j].max_accl, car_vel, desired_vehicle_distance_go, shift_distance_go, car_info[j].vd)
      if accl_car_accl < car_accl and desired_vehicle_distance_go > shift_distance_go:
        car_accl = accl_car_accl
        target_id = shift_id_go

  # 以下はログデータに9999や0が続いていると見にくいから消す処理
  if shift_distance_go == 9999 or shift_distance_go == 0:
    shift_distance_go = None
  # ここまで加速度処理
  return car_accl, shift_distance_go, shift_id_go, target_id, shift_lane, shift_lane_to, shift_begin

# def vel_control(car,car_info,time,car_id,acceleration_lane_start,acceleration_lane_end,target_vel):

#     return car_accl
