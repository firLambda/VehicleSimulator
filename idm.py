def search_car(car, car_info, time, run_car_list, number, acceleration_lane_start, acceleration_lane_end, lane_destination):
  """
  合流可能課調べる関数
  """
  pa = -1
  pb = -1
  Dpap = 9999  # とりあえず1000入れてみる
  # Vpa=200#とりあえず200入れてみる
  car_vel = car[time][number].vel

  if car_vel == 0:
    car_vel = 0.01

  if car[time][number].front < acceleration_lane_start:
    # このままの速度で走ったときのacceleration_lane_startまでの時間
    limit = (acceleration_lane_start - car[time][number].front) / car_vel
  else:
    # このままの速度で走ったときの終点までの時間
    limit = (acceleration_lane_end - car[time][number].front) / car_vel

  can_accl = False  # 加速して良い時 True

  for k in run_car_list:

    if car[time][k].lane == lane_destination and lane_destination == 2:  # 変更先の車線かどうか
      car_distance_tmp = car[time][k].front - car[time][number].front  # 前方位置同士を引き算する

      if car_distance_tmp >= 0 and car_distance_tmp < Dpap:  # 0以上の最小値を調べている
        Dpap = car_distance_tmp  # 車間距離更新(前方位置同士から算出した)
        pa = car[time][k].id
        # Vpa=car[time][k][4]

    elif car[time][k].front == lane_destination and lane_destination == 1:  # 変更先の車線かどうか
      car_distance_tmp = car[time][k].back - car[time][number].front  # 前方位置同士を引き算する

      if car_distance_tmp >= -5 and car_distance_tmp < Dpap:  # 0以上の最小値を調べている
        Dpap = car_distance_tmp  # 車間距離更新(前方位置同士から算出した)
        pa = car[time][k].id
        # Vpa=car[time][k][4]

  # 今度は後方位置を考慮した車間距離を求める。
  if not pa == -1:
    Dpap = car[time][int(pa)].back - car[time][number].front  # 相手の後方から自分の前方を引き算
    delta_Vpa = car[time][number].vel - car[time][int(pa)].vel  # 前方車両との速度差

    if lane_destination == 1:
      if Dpap <= 1.6:
        if car[time][number].front < acceleration_lane_start:
          if 1.6 > Dpap - (delta_Vpa * limit):
            can_accl = True

        elif delta_Vpa > 0:
          if 11.6 > -Dpap + (delta_Vpa * (limit - 4)) and limit > 4:
            can_accl = True

        elif delta_Vpa <= 0:
          if 1.6 > Dpap - (delta_Vpa * (limit - 4)) and limit > 4:
            can_accl = True

      else:
        if 1.6 > Dpap - (delta_Vpa * (limit - 4)) and limit > 4:  # 前方車両のほうが遅い場合
          can_accl = True

      if car[time][number].front > acceleration_lane_end - 50 or delta_Vpa > 10:
        can_accl = False

    elif lane_destination == 2:
      if delta_Vpa > 0:  # 前方車両のほうが遅い場合
        if Dpap >= 0:
          if limit < Dpap / delta_Vpa and 1.6 < Dpap - (delta_Vpa * limit):
            can_accl = True
          else:
            can_accl = False

        else:
          if car[time - 1][int(pa)].accl < 0:
            can_accl = True
          elif delta_Vpa * limit > Dpap + 10 + 1.6:
            can_accl = True
          elif 0 < delta_Vpa:  # ここ要考察
            can_accl = True

      elif delta_Vpa < 0:  # 前方車両のほうが早い場合
        if Dpap < 0:
          if car[time - 1][int(pa)].accl > 0:
            can_accl = False
          elif car[time - 1][int(pa)].accl < 0:
            can_accl = True
          # if abs(delta_Vpa)*4 > abs(Dpap):
          #     can_accl=True

        else:
          if abs(delta_Vpa) * (limit - 4) < Dpap - 1.6:
            can_accl = True

      else:
        if Dpap > 1.6:
          can_accl = True

  # 変更先の後方車両との車間を調べる処理
  if can_accl is True and lane_destination == 2:
    Dppb = 1000  # とりあえず1000入れてみる
    # Vpb=1#1を入れてみる

    for k in run_car_list:
      if car[time][k].lane == lane_destination:  # 変更先の車線かどうか
        # 最小値が後ろの車との車間
        car_distance_tmp = car[time][number].front - \
            car[time][k].front  # 前方位置同士を引き算
        if car_distance_tmp >= 0 and car_distance_tmp < Dppb:  # 0以上の最小値を調べている
          Dppb = car_distance_tmp  # 車間距離更新(前方位置同士から算出した)
          pb = car[time][k].id
          # Vpb=car[time][k][4]

    # 今度は後方位置を考慮した車間距離を求める。
    if not pb == -1:
      Dppb = car[time][number].back - \
          car[time][int(pb)].front  # 自分の後方から相手の前方を引き算
      delta_Vpb = car[time][number].vel - \
          car[time][int(pb)].vel  # 後方車両との速度差

      if delta_Vpb > 0:  # 後方車両のほうが遅い場合
        if Dppb < 0:
          if car[time - 1][int(pb)].accl > 0:  # 並走してる車両が加速してる場合加速しない
            can_accl = False

      elif delta_Vpb < 0:  # 後方車両のほうが早い場合
        if Dppb > 0:
          if delta_Vpa == 0:
            delta_Vpa = 0.01
          # 最低車間距離－1.6削除
          if limit < Dpap / delta_Vpa and 1.6 < Dpap - (delta_Vpa * limit):
            can_accl = True
          else:
            can_accl = False
        else:
          can_accl = False
        if car[time - 1][int(pb)].accl == -0.3:
          can_accl = True
      else:  # 速度差がない場合加速する
        can_accl = True

  return can_accl


def change_lane(car, time, run_car_list, number, lane_destination):
  """
  車線変更の条件の判断している
  """
  pa = -1
  pb = -1
  can_change_lane = 0
  if not car[time][number].lane == lane_destination:  # 今いる車線が変更先車線でないとき
    # 変更先の先行車両との車間を調べる処理
    Dpap = 9999  # とりあえず1000入れてみる
    Vpa = 200  # とりあえず200入れてみる
    for k in run_car_list:
      if car[time][k].lane == lane_destination:  # 変更先の車線かどうか
        car_distance_tmp = car[time][k].front - \
            car[time][number].front  # 前方位置同士を引き算する
        if car_distance_tmp >= 0 and car_distance_tmp < Dpap:  # 0以上の最小値を調べている
          Dpap = car_distance_tmp  # 車間距離更新(前方位置同士から算出した)
          pa = car[time][k].id
          Vpa = car[time][k].vel

    # 今度は後方位置を考慮した車間距離を求める。
    if not pa == -1:
      Dpap = car[time][int(pa)].back - \
          car[time][number].front  # 相手の後方から自分の前方を引き算

    # 変更先の後方車両との車間を調べる処理
    Dppb = 1000  # とりあえず1000入れてみる
    Vpb = 1  # 1を入れてみる

    for k in run_car_list:
      if car[time][k].lane == lane_destination:  # 変更先の車線かどうか
        # 最小値が後ろの車との車間
        car_distance_tmp = car[time][number].front - \
            car[time][k].front  # 前方位置同士を引き算
        if car_distance_tmp >= 0 and car_distance_tmp < Dppb:  # 0以上の最小値を調べている
          Dppb = car_distance_tmp  # 車間距離更新(前方位置同士から算出した)
          pb = car[time][k].id
          Vpb = car[time][k].vel

    # 今度は後方位置を考慮した車間距離を求める。
    if not pb == -1:
      Dppb = car[time][number].back - \
          car[time][int(pb)].front  # 自分の後方から相手の前方を引き算

    Vp = car[time][number].vel
    # 車線変更可能車間距離
    if Vpb - Vp > 0:  # 自分の方が遅い場合
      can_lane_change_distance = (Vpb - Vp) * (Vpb - Vp) / 3.8 / 2 + 1.6
    else:
      can_lane_change_distance = 0

    if (Vp <= 1 or car[time][number].accl < 0) and (Vp * 3.6 / 2 < Dpap and Vp * 3.6 / 2 < Dppb) and (Vpa > Vp) and (can_lane_change_distance < Dppb):
      can_change_lane = 1
    # print(Vp==0 or car[time][number][5]<0,Vp*3.6/2 < Dpap and Vp*3.6/2 < Dppb,Vpa>Vp,ttc<2)
  return can_change_lane


def merging_lane(car, time, run_car_list, number, lane_destination):
  """
  最初に採用していた合流時の条件式
  """
  pa = -1
  pb = -1
  can_merge_lane = 0
  if not car[time][number].lane == lane_destination:  # 今いる車線が変更先車線でないとき
    Vp = car[time][number].vel
    # 変更先の先行車両との車間を調べる処理
    Dpap = 9999  # とりあえず9999入れてみる 車間距離
    Vpa = 200  # とりあえず200入れてみる　速度
    for k in run_car_list:
      if car[time][k].lane == lane_destination:  # 変更先の車線かどうか
        car_distance_tmp = car[time][k].front - car[time][number].front  # 前方位置同士を引き算する
        if car_distance_tmp >= 0 and car_distance_tmp < Dpap:  # 0以上の最小値を調べている
          Dpap = car_distance_tmp  # 車間距離更新(前方位置同士から算出した)
          pa = car[time][k].id
          Vpa = car[time][k].vel
    # 今度は後方位置を考慮した車間距離を求める。
    if not pa == -1:
      Dpap = car[time][int(pa)].back - car[time][number].front  # 相手の後方から自分の前方を引き算

    # 車線変更可能車間距離
    if Vp - Vpa > 0:  # 自分の方が速い場合
      can_lane_change_distance_a = (
          Vp - Vpa) * (Vp - Vpa) / 3.8 / 2 + 1.6
    else:
      can_lane_change_distance_a = 0

    # 変更先の後方車両との車間を調べる処理
    Dppb = 1000  # とりあえず1000入れてみる
    Vpb = 1  # 1を入れてみる
    for k in run_car_list:
      if car[time][k].lane == lane_destination:  # 変更先の車線かどうか
        # 最小値が後ろの車との車間
        car_distance_tmp = car[time][number].front - \
            car[time][k].front  # 前方位置同士を引き算
        if car_distance_tmp >= 0 and car_distance_tmp < Dppb:  # 0以上の最小値を調べている
          Dppb = car_distance_tmp  # 車間距離更新(前方位置同士から算出した)
          pb = car[time][k].id
          Vpb = car[time][k].vel
    # 今度は後方位置を考慮した車間距離を求める。
    if not pb == -1:
      Dppb = car[time][number].back - car[time][int(pb)].front

    # 車線変更可能車間距離算出
    if Vpb - Vp > 0:  # 自分の方が遅い場合
      can_lane_change_distance_b = (Vpb - Vp) * (Vpb - Vp) / 3.8 / 2 + 1.6
    else:
      can_lane_change_distance_b = 0
    # 比較
    if can_lane_change_distance_a < Dpap and can_lane_change_distance_b < Dppb:
      can_merge_lane = 1
  return can_merge_lane


def merging_lane2(car, time, run_car_list, number, lane_destination):  # TTCで判断する
  """
  加速車線から本線に合流するときのみ(TTCで判断する)
  車線変更の判断を行っており合流可能なときtrue　それ以外－1
  """
  pa = -1
  pb = -1
  can_merge_lane = 0
  if not car[time][number].lane == lane_destination:  # 今いる車線が変更先車線でないとき
    Vp = car[time][number].vel
    # 変更先の先行車両との車間を調べる処理
    Dpap = 9999  # とりあえず1000入れてみる
    Vpa = 200  # とりあえず200入れてみる
    for k in run_car_list:
      if car[time][k].lane == lane_destination:  # 変更先の車線かどうか
        car_distance_tmp = car[time][k].front - \
            car[time][number].front  # 前方位置同士を引き算する
        if car_distance_tmp >= 0 and car_distance_tmp < Dpap:  # 0以上の最小値を調べている
          Dpap = car_distance_tmp  # 車間距離更新(前方位置同士から算出した)
          pa = car[time][k].id
          Vpa = car[time][k].vel
    # 今度は後方位置を考慮した車間距離を求める。
    if not pa == -1:
      Dpap = car[time][int(pa)].back - \
          car[time][number].front  # 相手の後方から自分の前方を引き算
    # 車間距離が0の場合はttcを0にする
    if Dpap == 0:
      ttc_a = 0
    else:
      if (Vp - Vpa) <= 0:  # 前方車両のほうが速い
        ttc_a = 9999
      else:
        ttc_a = Dpap / (Vp - Vpa)
    # 変更先の後方車両との車間を調べる処理
    Dppb = 1000  # とりあえず1000入れてみる
    Vpb = 1  # 1を入れてみる
    for k in run_car_list:
      if car[time][k].lane == lane_destination:  # 変更先の車線かどうか
        # 最小値が後ろの車との車間
        car_distance_tmp = car[time][number].front - \
            car[time][k].front  # 前方位置同士を引き算
        if car_distance_tmp >= 0 and car_distance_tmp < Dppb:  # 0以上の最小値を調べている
          Dppb = car_distance_tmp  # 車間距離更新(前方位置同士から算出した)
          pb = car[time][k].id
          Vpb = car[time][k].vel
    # 今度は後方位置を考慮した車間距離を求める。
    if not pb == -1:
      Dppb = car[time][number].back - car[time][int(pb)].front

    if Dppb == 0:
      ttc_b = 0
    else:
      if (Vpb - Vp) <= 0:  # 自車が後ろより速い場合
        ttc_b = 9999
      else:
        ttc_b = Dppb / (Vpb - Vp)

    if ttc_a > 2 and ttc_b > 2 and Dpap > 1.6 and Dppb > 1.6:
      can_merge_lane = 1
  return can_merge_lane

# 前の車のIDと車間を調べる関数


def calculate_car_distance(car, time, car_id, car_lane, lane1_list, lane2_list, lane3_list, acceleration_lane_end):
  """
  前の車両のIDと車間を調べる関数
  """
  if car_lane == 1:
    if lane1_list.index(car_id) == 0:  # 前に車がいないとき
      front_car = -1
      car_distance = acceleration_lane_end - \
          car[time][car_id].front  # change by kino
    else:
      front_car = int(lane1_list[lane1_list.index(car_id) - 1])
      car_distance = car[time][front_car].back - car[time][car_id].front
  elif car_lane == 2:
    if lane2_list.index(car_id) == 0:  # 前に車がいないとき
      front_car = -1
      car_distance = 9999
    else:
      front_car = int(lane2_list[lane2_list.index(car_id) - 1])
      car_distance = car[time][front_car].back - car[time][car_id].front
  else:
    if lane3_list.index(car_id) == 0:  # 前に車がいないとき
      front_car = -1
      car_distance = 9999
    else:
      front_car = int(lane3_list[lane3_list.index(car_id) - 1])
      car_distance = car[time][front_car].back - car[time][car_id].front
  return front_car, car_distance


def desired_vehicle_distance(s0, v, T, Treac, delta_v, a, b):
  """
  希望車間距離
  """
  ss = round(s0 + v * (T + Treac) + ((v * delta_v) / (((a * b)**0.5) * 2)), 1)
  return ss


def calculate_accl(a, v, ss, s, vd):
  """
  idmの計算式
  """
  if s == 0:
    s = 0.1
  if ss < 0:
    ss = 0

  accl = round(a * min(1 - (v / vd)**4, 1 - (ss / s)**2), 1)
  if accl < -3.8:
    accl = -3.8
  return accl


def return_lane_list(car, run_car_list, time):
  """
  車線ごとに前方位置順にIDを並べる（降順）
  """
  lane1_list_tmp = []
  lane2_list_tmp = []
  lane3_list_tmp = []
  lane1_list, lane2_list, lane3_list = [], [], []
  if len(run_car_list) > 0:

    for j in run_car_list:  # 車両の数だけループ
      if car[time][j].lane == 1:
        lane1_list_tmp += [[car[time][j].id, car[time][j].front]]
      elif car[time][j].lane == 2:
        lane2_list_tmp += [[car[time][j].id, car[time][j].front]]
      elif car[time][j].lane == 3:
        lane3_list_tmp += [[car[time][j].id, car[time][j].front]]

    lane1_list_tmp = sorted(
        lane1_list_tmp, key=lambda x: x[1], reverse=True)  # ソート
    lane2_list_tmp = sorted(
        lane2_list_tmp, key=lambda x: x[1], reverse=True)
    lane3_list_tmp = sorted(
        lane3_list_tmp, key=lambda x: x[1], reverse=True)

    for j in lane1_list_tmp:
      lane1_list += [j[0]]
    for j in lane2_list_tmp:
      lane2_list += [j[0]]
    for j in lane3_list_tmp:
      lane3_list += [j[0]]

  return lane1_list, lane2_list, lane3_list
