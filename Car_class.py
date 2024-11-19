class Car_info():
    def __init__(self, ID):
        self.id = ID  # 0:ID
        self.max_accl = 0  # 1:最大加速度
        self.desired_Deceleration = 0  # 2:希望減速度
        self.passing_time = 0  # 3:安全車頭時間
        self.driver_reaction_time = 0  # 4:反応時間
        self.dis_stop = 0  # 5:停止時最低車間距離
        self.v_init = 0  # 6:初期速度
        self.vd = 0  # 7:希望速度
        self.kindness = 0  # 8優しいかどうか
        self.occur_time = 0  # 9車両発生時刻
        self.acc_on_cross = 0  # 10合流部での加速するか否か

    def put_vars(self):
        print(vars(self))

    def num_to_vars(self, i, num):
        if 0 <= i and i <= 10:
            if i == 0:
                self.id = num
            elif i == 1:
                self.max_accl = num
            elif i == 2:
                self.desired_Deceleration = num
            elif i == 3:
                self.passing_time = num
            elif i == 4:
                self.driver_reaction_time = num
            elif i == 5:
                self.dis_stop = num
            elif i == 6:
                self.v_init = num
            elif i == 7:
                self.vd = num
            elif i == 8:
                self.kindness = num
            elif i == 9:
                self.occur_time = num
            elif i == 10:
                self.acc_on_cross = num

            return True
        else:
            return False

    def ls_to_vars(self, ls):
        if type(ls) == list:
            if len(ls) <= 11:
                for i, num in enumerate(ls):
                    self.num_to_vars(i, num)

    def vars_to_ls(self):
        return [self.id,
                self.max_accl,
                self.desired_Deceleration,
                self.passing_time,
                self.driver_reaction_time,
                self.dis_stop,
                self.v_init,
                self.vd,
                self.kindness,
                self.occur_time,
                self.acc_on_cross
                ]


class Car():
    def __init__(self, ID):
        self.id = ID  # 0ID代入
        self.front = 0  # 1前方位置代入
        self.back = 0  # 2後方位置代入
        self.lane = 0  # 3車線代入
        self.vel = 0  # 4速度代入
        self.accl = 0  # 5加速度代入
        self.distance = 0  # 6車間距離代入
        self.delta_v = 0  # 7相対速度
        self.front_car_id = 0  # 8前方車両ID
        self.shift_lane = 0  # 9車線変更してる途中かどうか
        self.shift_lane_to = 0  # 10どこの車線に変更しようとしてるか
        self.shift_begin = 0  # 11車線変更開始時間
        self.shift_distance_go = 0  # 12車線変更先車間距離
        self.shift_id_go = 0  # 13車線変更先前方車両ID
        self.target_id = 0  # 14目標車両ID

    def put_vars(self):
        print(vars(self))

    def num_to_vars(self, i, num):
        if i == 0:
            self.id = num  # 0ID代入
        elif i == 1:
            self.front = num  # 1前方位置代入
        elif i == 2:
            self.back = num  # 2後方位置代入
        elif i == 3:
            self.lane = num  # 3車線代入
        elif i == 4:
            self.vel = num  # 4速度代入
        elif i == 5:
            self.accl = num  # 5加速度代入
        elif i == 6:
            self.distance = num  # 6車間距離代入
        elif i == 7:
            self.delta_v = num  # 7相対速度
        elif i == 8:
            self.front_car_id = num  # 8前方車両ID
        elif i == 9:
            self.shift_lane = num  # 9車線変更してる途中かどうか
        elif i == 10:
            self.shift_lane_to = num  # 10どこの車線に変更しようとしてるか
        elif i == 11:
            self.shift_begin = num  # 11車線変更開始時間
        elif i == 12:
            self.shift_distance_go = num  # 12車線変更先車間距離
        elif i == 13:
            self.shift_id_go = num  # 13車線変更先前方車両ID
        elif i == 14:
            self.target_id = num  # 14目標車両ID

    def ls_to_vars(self, ls):
        if type(ls) == list:
            if len(ls) <= 15:
                for i, num in enumerate(ls):
                    self.num_to_vars(i, num)

    def vars_to_list(self):
        return [self.id, self.front, self.back, self.lane, self.vel, self.accl, self.distance, self.delta_v, self.front_car_id, self.shift_lane, self.shift_lane_to, self.shift_begin, self.shift_distance_go, self.shift_id_go, self.target_id]


def make_car_info(CAR_MAX):
    car_info = {}
    for i in range(CAR_MAX):
        car_info[i] = Car_info(i)
    return car_info


def make_car(time, CAR_MAX):
    car = [[Car(id) for id in range(CAR_MAX)]for time in range(time)]
    return car
