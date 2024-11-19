import cal


def keisan1(q_lane1, q_lane2, q_lane3, ratio, seed):
  time_max = 600  # シミュレーションを行う時間の長さ[秒]
  acceleration_lane_start = 300  # 加速車線の始まる位置
  acceleration_lane_end = acceleration_lane_start + 300  # 加速車線の終わる位置
  if ratio > 0:
    use_base_station = 1  # 制御なし=0,制御あり(速度調節のみ)=1,制御あり(速度調節+車線変更)=2
    cal.simulation(time_max, q_lane1, q_lane2, q_lane3, acceleration_lane_start, acceleration_lane_end, use_base_station, ratio, seed)
  elif ratio == 0:
    use_base_station = 0  # 基地局なし=0,制御あり(速度調節のみ)=1,制御あり(速度調節+車線変更)=2
    cal.simulation(time_max, q_lane1, q_lane2, q_lane3, acceleration_lane_start, acceleration_lane_end, use_base_station, ratio, seed)


def keisan2(ratio, seed):  # ratioは譲る車両の割合
  # ####シミュレーション設定#####

  # keisan1(10,10,10,ratio,seed)

  # keisan1(50,190,190,ratio,seed)
  # keisan1(50,195,195,ratio,seed)
  # keisan1(50,200,200,ratio,seed)
  # keisan1(50,205,205,ratio,seed)
  # keisan1(50,210,210,ratio,seed)
  # keisan1(50,215,215,ratio,seed)
  # keisan1(50,220,220,ratio,seed)
  # keisan1(50,225,225,ratio,seed)
  # keisan1(50,230,230,ratio,seed)
  # keisan1(50,235,235,ratio,seed)
  # keisan1(50,240,240,ratio,seed)
  keisan1(50, 245, 245, ratio, seed)

# for i in range(1,2):#繰り返し実行する時
#     keisan2(0,i)
  # keisan2(10,i)
  # keisan2(30,i)
  # keisan2(50,i)
  # keisan2(100,i)


keisan2(0, 1)
# keisan2(40,1)
# keisan2(100,1)

# filereader.filereading()

print("終了")
