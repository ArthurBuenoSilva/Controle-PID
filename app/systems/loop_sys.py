from control import TimeResponseData, TimeResponseList


class LoopSystem:
    def __init__(
        self,
        t: TimeResponseList,
        p: TimeResponseData,
        overshoot: float = None,
        rise_time: float = None,
        kp: float = None,
        ti: float = None,
        td: float = None,
    ):
        self.t = t
        self.p = p
        self.overshoot = overshoot
        self.rise_time = rise_time
        self.kp = kp
        self.ti = ti
        self.td = td


class CloseLoopSystem(LoopSystem):
    def __init__(
        self,
        t: TimeResponseList,
        p: TimeResponseData,
        overshoot: float = None,
        rise_time: float = None,
        kp: float = None,
        ti: float = None,
        td: float = None,
    ):
        super().__init__(t, p, overshoot, rise_time, kp, ti, td)


class OpenLoopSystem(LoopSystem):
    def __init__(
        self,
        t: TimeResponseList,
        p: TimeResponseData,
        overshoot: float = None,
        rise_time: float = None,
        kp: float = None,
        ti: float = None,
        td: float = None,
    ):
        super().__init__(t, p, overshoot, rise_time, kp, ti, td)
