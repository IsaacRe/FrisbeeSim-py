from math import sin, cos, pi, exp, log
import tensorflow as tf

# define constants for frisbee flight
g = -9.8
m = 0.175
RHO = 1.23
AREA = 0.0558
CLO = 0.1
CLA = 1.4
CDO = 0.08
CDA = 2.72
ALPHA0 = -4
e = exp(1)

disc_rendering_size = 5


def simple_trajectory(distance, direction, lift=0.02):
    """
    Simple approximation function of a frisbee trajectory outputting position given time, scaled linearly for total
        distance and total time of flight
    """

    # define constants
    T = 50.0
    C = 0.34
    D = 9.4
    L = 3.0

    # scale t by total time
    # TODO get flight time from distance and lift
    t = t * T / distance
    x_scaled = tf.log(1.0 + t)

    # unscale return value
    x = x_scaled * distance * C

    # scale x by total distance
    x_scaled = x_scaled * D / L
    y = distance * lift * C * (x_scaled - tf.exp(x_scaled - 7.0)) + 1.0

    return x, y


class SimpleDisc:

    def __init__(self, t, window, sess):
        # all beginning with _ are tf vars
        self.sess = sess
        self.t = t
        self.x, self.y, self.z = 0.0, 0.0, 0.0
        self.rendering = window.add_object(disc_rendering_size, 0, 0)

        # initialize flight variables
        self._position = None
        self._start_coords = None
        self._direction = None
        self._target_coords = None
        self._flight_distance = None
        self.t_elapsed = None
        self.in_flight = False

    def begin_flight(self, position, direction, distance):
        # manage flight variables
        self._start_coords = position
        self._direction = direction
        self._flight_distance = distance
        self._target_coords = position + distance * tf.stack([tf.cos(direction), tf.sin(direction)])
        self.t_elapsed = 0.0
        self.in_flight = True
        self._position = position

        # get flight trajectory
        # TODO change simple_trajectory to output tensor

        # update position
        # TODO update x, y, and z

        # update rendering
        self.rendering.move_to(self.x, self.z)

    def update_flight(self):
        assert self.in_flight

        # update time and get trajectory position
        self.t_elapsed += self.t
        d, y = simple_trajectory(self.t_elapsed, self.flight_distance)

        # update position
        self.x, self.z = d * cos()


class Disc:

    def __init__(self, t):
        self.t = t
        self.cl, self.cd, self.direction = 0, 0, 0
        [self.x, self.y, self.z, self.vxz, self.vy] = [0] * 5

    # update velocity and position of disc during the given time-step
    def update_flight(self):

        # change in x as a result of drag
        self.vxz -= RHO * pow(self.vxz, 2) * AREA * self.cd * self.t

        # change in y as a result of lift and gravity
        self.vy += (RHO * pow(self.vxz, 2) * AREA * self.cl/2/m + g) * self.t

        # update coords
        self.x += cos(self.direction) * self.vxz * self.t
        self.y += self.vy * self.t
        self.z += sin(self.direction) * self.vxz * self.t

    # set initial position and velocity and flight constants
    def begin_flight(self, pos, angles, veloc):

        # set initial position
        [self.x, self.y, self.z] = pos

        # set initial velocity
        [self.vxz, self.vy] = veloc

        # store initial direction of throw
        [self.direction, tilt] = angles

        # set drag and lift constants for the flight
        self.cl = CLO + CLA * tilt * pi / 180
        self.cd = CDO + CDA * pow( (tilt - ALPHA0) * pi / 180, 2)
