# -*- coding: utf-8 -*-
"""
A python module to support analytic cycling with a power meter.
Created on Tue Oct 29 12:35:40 2013
@author: christophernst
"""

import datetime

import numpy as np

# set your own with velo.FTP = my_value
FTP = 290
zones = [0, 55, 75, 90, 105, 120, 150]
sst = [88, 94]
__kjoule_to_kcal__ = 0.2388


def show_state():
    """
    prints the current configuration (FTP) and the resulting training zones
    """
    print("velo loaded - FTP: %.f, MAP: %.f, Zones: %s" % (
        FTP, maximum_aerobic_power(), str(["{:.0f}".format(watts_ftp(i)) for i in zones])))


def ftp_watts(power):
    """
    Return percent of ``FTP`` for the given power in Watts.
    """
    return power / float(FTP) * 100


def map_watts(power):
    """
    Return percent of ``MAP`` for the given power in Watts.
    """
    return power / float(maximum_aerobic_power()) * 100


def maximum_aerobic_power():
    """
    Return the MAP
    """
    return FTP / 0.85


def zone_watts(power):
    """
    Return the index of ``zones`` where the given power fits in.
    """
    p_rel = ftp_watts(power)
    for zone in zones:
        if p_rel < zone:
            return zones.index(zone)
    return len(zones)


def sst_watt_zone():
    """
    Display the watt values of the SST range
    """
    return [x * FTP / 100 for x in sst]


def show_watts(power):
    """
    Return a summary of the given power containing percent FTP, percent MAP and zone.
    """
    return ["L{}".format(zone_watts(power)), "{:.1f} %FTP".format(ftp_watts(power)),
            "{:.1f} %MAP".format(map_watts(power))]


def watts_ftp(percent):
    """
    Return the power in Watts for the given percents of ``FTP``.
    """
    return float(percent) / 100. * FTP


def watts_map(percent):
    """
    Return the power in Watts for the given percents of ``MAP``.
    """
    return float(percent) / 100. * maximum_aerobic_power()


def vo2_max(normalized_power, average_hr, weight=71, hr_rest=40, hr_max=175):
    """
    https://alancouzens.com/blog/VO2Scores.html
    - raises (slightly) with hr_max and hr_rest(!)
    - raises proportionally with NP
    - falls with average_hr
    ~ efficiency, based on HR reserve / weight
    """
    if (average_hr > 10) & (normalized_power > 10):
        return (normalized_power / 75 * 1000 / weight) / ((average_hr - hr_rest) / (hr_max - hr_rest))
    return np.nan


###################################################

def kjoule_workout(workout):
    """
    Calculate the energy in KJoule for the given workout.

    Parameters
    ----------
    workout : List of durations and power of intervals
        The expected format is (minutes, watts, minutes, watts...)

    >>> kjoule_workout((60,200,10,320))

    returns the work of 60 minutes at 200 Watts + 10 minutes at 320 W
    """
    seconds = np.array(workout).reshape(-1, 2)[:, 0] * 60.
    kwatts = np.array(workout).reshape(-1, 2)[:, 1] / 1000.
    return np.dot(seconds, kwatts)


def avgp_workout(workout):
    """
    Calculate the average power in W for the given workout.

    Parameters
    ----------
    workout : List of durations and power of intervals
        The expected format is (minutes, watts, minutes, watts...)

    >>> avgp_workout((60,200,10,320))

    returns the average power  of 60 minutes at 200 Watts + 10 minutes at 320 W
    """
    times = np.array(workout).reshape(-1, 2)[:, 0]
    watts = np.array(workout).reshape(-1, 2)[:, 1]
    return np.dot(times, watts) / sum(times * 1.)


def tss_workout(workout):
    """
    Calculate the TSS (Training Stress Score) for the given workout.

    Parameters
    ----------
    workout : List of durations and power of intervals
        The expected format is (minutes, watts, minutes, watts...)

    >>> tss_workout((60, 200, 10, 320))

    returns the TSS of 60 minutes at 200 Watts + 10 minutes at 320 W
    """
    hours = np.array(workout).reshape(-1, 2)[:, 0] / 60.
    intensity2 = (np.array(workout).reshape(-1, 2)[:, 1] / float(FTP)) ** 2
    return np.dot(hours, intensity2) * 100


def kcal_workout(workout, efficiency=0.23):
    """
    Calculate an estimation for the calories burned during the given workout.

    Parameters
    ----------
    workout : List of durations and power of intervals
        The expected format is (minutes, watts, minutes, watts...)
    efficiency : factor for the physiological efficiency (default=0.23)
        You typically only get 1/4 of your energy consumed to the road.
        The rest ist lost as general warmth, friction etc. The range for the efficiency is
        typically given between 0.22 an 0.25, where 0.25 means very efficient.
        If you measure power at the cranks or on the pedals you should choose a lower value
        to account for drive train efficiency.

    see kjoule_workout
    """
    return kjoule_workout(workout) * __kjoule_to_kcal__ / efficiency


###################################################

def tss_impact(tss, k, days):
    """
    Return the impact of the training stress after given amount of days.

    Parameters
    ----------
    tss : TSS of a workout on day 0
    k : decay constant
        (typical values: 7 for short term stress (fatigue) and 42
        for long term stress (fitness)
    days : days after the workout
        (if days < 0 zero impact is returned)
    """
    return tss * (1 - np.exp(-1 / k)) * np.exp(-days / k) \
        if days >= 0 else 0


def tss_decay(tss, k, days):
    """
    Return what is left of a training load after given days and given decay constant.
    see tss_impact
    """
    return tss * np.exp(-days / k)


def pmc(ctl, atl, workouts=None, days=8):
    """
    Return the future performance manager chart.

    Parameters
    ----------
    ctl : current chronic training load

    atl : current acute training load

    workouts :  array of TSS values.
        Element ``i`` represents the TSS on day ``i``

    days : How long to look ahead.

    Return
    ------
    An array, each day as a row, columns=workouts, CTL, ATL, and TSB
    """

    if workouts is None:
        workouts = []
    size_workouts = len(workouts)
    if size_workouts > days:
        days = size_workouts
    day_array = np.arange(0, days)

    # append 0
    no_workouts = np.zeros(days - size_workouts)
    workout_array = np.append(workouts, no_workouts)

    # calculate decay of current CTL/ATL and sum up impacts of planned workouts and sum all
    # do that for CTL and ATL
    ctl_base = np.vectorize(lambda i: tss_decay(ctl, 42, i))(np.array(day_array))
    ctl_impacts = np.array([[tss_impact(workout, 42, (day - i)) for day in day_array]
                            for i, workout in enumerate(workout_array)])
    ctl_array = ctl_base + ctl_impacts.sum(axis=0)

    atl_base = np.vectorize(lambda i: tss_decay(atl, 7, i))(np.array(day_array))
    atl_impacts = np.array([[tss_impact(workout, 7, (day - i)) for day in day_array]
                            for i, workout in enumerate(workout_array)])
    atl_array = atl_base + atl_impacts.sum(axis=0)

    return np.array(list(zip(workout_array, ctl_array, atl_array, ctl_array - atl_array)))


######################################################

def time_segment(distance, velocity):
    """
    Return the time (HH:mm:ss) required to pass the given distance with the given velocity.

    Parameters
    ----------
    distance : float
        distance in km
    velocity : float
        speed in km/h

    Time savings over 40 km:
    P1=300;str(velo.time_segment(40, velo.Speed(cda=0.35).v(P1,0))-velo.time_segment(40, velo.Speed(cda=0.34).v(P1,0)))
    """
    time_in_seconds = 3600 * distance / float(velocity)
    return datetime.timedelta(seconds=time_in_seconds)


def t_to_close_gap(v_group, v_rider, t_break=1 / 60):
    """
    How long does it take to close the gap to a group after taking a short break? (in h)

    Parameters
    ----------
    v_group : float
        speed of group in km/h
    v_rider : float
        rider's speed to chase back in km/h
    t_break : float
        duration of break in h (default: 1 min)

    >>> import velopy
    >>> t_to_close_gap(velopy.Speed().velocity(260,0),velopy.Speed().velocity(300,0))*60
    Group riding at 260 W, rider at 300 W in the flat: it takes nearly 19 min
    """
    return v_group * t_break / (v_rider - v_group)


def speed_cadence(cadence, gearing, circumference=2.100):
    """
    Return the speed (km/h) for given cadence and gearing

    Parameters
    ----------
    cadence : float
        cadence in rpm
    gearing : float
        gearing in chain teeth / cog teeth
    circumference : float
        distance covered by one turn of the wheel (2 * pi * wheel radius)
    >>> speed_cadence((90, 39/12)

    returns the speed when pedaling with 90 rpm on a 39x12 gearing
    """
    return cadence * gearing * circumference * 60 / 1000.


def cadence_speed(speed, gearing, circumference=2.100):
    """
    Return the cadence required to reach a certain speed with a certain gearing

    Parameters
    ----------
    speed : float
        speed in km/h
    gearing : float
        gearing in chain teeth / cog teeth
    circumference : float
        distance covered by one turn of the wheel (2 * pi * wheel radius)
    >>> cadence_speed((90, 39/12)

    returns the speed when pedaling with 90 rpm on a 39x12 gearing
    """
    return speed / (gearing * circumference * 60 / 1000.)


######################################################

class Speed:
    """ Convert speed to power (P(v)) and power to speed (v(P))

    Parameters
    ----------
    rho : float
        air density in kg/m**3
    cda : float
        drag coefficient times frontal Area in m**2
    crr : float
        coefficient of rolling resistance
    M : float
        total system mass: rider + clothes + bottles&stuff + bike

    """
    _g = 9.80665  # standard acceleration of gravity

    def __init__(self, **kwargs):
        self.rho = kwargs.pop('rho', 1.192)
        self.cda = kwargs.pop('cda', 0.35)
        self.crr = kwargs.pop('crr', 0.004)
        self.mass = kwargs.pop('M', 82.0)

    def power_air(self, velocity):
        """
        Return the Power required to overcome the air resistance
        """
        v_k = velocity / 3.6
        return 0.5 * self.rho * self.cda * v_k ** 3

    def power_wheel(self, velocity):
        """
        Return the Power required to overcome the rolling resistance
        """
        v_k = velocity / 3.6
        return self.crr * self.mass * self._g * v_k

    def power_climb(self, velocity, slope):
        """
        Return the Power required to overcome the gravity
        Parameters
        ----------
        velocity : float
            Speed in km/h
        slope : float
            slope. eg. 0.08 for an 8% climb
        """
        v_k = velocity / 3.6
        return slope * self.mass * self._g * v_k

    def power_total(self, velocity, slope):
        """
        Return the total power needed to hold the given speed on the given slope
        ----------
        velocity : float
            Speed in km/h
        slope : float
            slope. eg. 0.08 for an 8% climb
        """
        return self.power_air(velocity) + self.power_wheel(velocity) + self.power_climb(velocity, slope)

    def velocity(self, p, slope):
        """
        Return the velocity reached when pushing the given power up to hill of given slope
        ----------
        p : float
            Power in Watts
        slope : float
            slope. eg. 0.08 for an 8% climb
        """
        a = 0.5 * self.rho * self.cda
        b = (self.crr + slope) * self.mass * self._g

        return -3.6 * (np.sqrt(p ** 2 / (4 * a ** 2) + b ** 3 / (27 * a ** 3)) - p / (2 * a)) ** (1 / 3.0) \
               + 1.2 * b / (a * (np.sqrt(p ** 2 / (4 * a ** 2) + b ** 3 / (27 * a ** 3)) - p / (2 * a)) ** (1 / 3.0))


######################################################

class Gearing:
    """ Some helper functions around shifting
    in progress
    >>> gears = Gearing()
    >>> print(gears.rings)
    """
    _52x36 = (52, 36)
    _52x39 = (52, 39)
    _11_11x25 = (11, 12, 13, 14, 15, 17, 19, 21, 23, 25, 28)
    _11_11x28 = (11, 12, 13, 14, 15, 17, 19, 21, 23, 25, 28)
    _11_12x28 = (12, 13, 14, 15, 16, 17, 19, 21, 23, 25, 28)

    # http://www.j-berkemeier.de/Ritzelrechner.html?kb=36,52+rz=28,25,23,21,19,17,16,15,14,13,12+tf=90+ru=213+vr=1-1+ge=false+rt=false
    # http://www.j-berkemeier.de/Ritzelrechner.html?kb=36,52+rz=28,25,23,21,19,17,15,14,13,12,11+tf=90+ru=213+vr=1-1+ge=false+rt=false

    def __init__(self, **kwargs):
        self.rings = kwargs.pop('rings', Gearing._52x36)
        self.cogs = kwargs.pop('cogs', Gearing._11_11x28)

    def combinations(self):
        """
        experimental
        """
        return np.array(self.rings) * np.array(self.cogs)

# show_state()
