import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
from enum import Enum
from math import sin, cos, radians

#%matplotlib inline
#np.set_printoptions(precision=3, suppress=True)

plt.rcParams["figure.figsize"] = [12, 12]

class Rotation(Enum):
    ROLL = 0
    PITCH = 1
    YAW = 2  


class EulerRotation:
    
    def __init__(self, rotations):
        """
        `rotations` is a list of 2-element tuples where the
        first element is the rotation kind and the second element
        is angle in degrees.
        
        Ex:
        
            [(Rotation.ROLL, 45), (Rotation.YAW, 32), (Rotation.PITCH, 55)]
            
        """
        self._rotations = rotations
        self._rotation_map = {Rotation.ROLL : self.roll, Rotation.PITCH : self.pitch, Rotation.YAW : self.yaw}

    def roll(self, phi):
        """Returns a rotation matrix along the roll axis"""
        return np.array([
            [1, 0, 0],
            [0, cos(phi), -sin(phi)],
            [0, sin(phi), cos(phi)]
        ])
    
    def pitch(self, theta):
        """Returns the rotation matrix along the pitch axis"""
        return np.array([
            [cos(theta), 0, sin(theta)],
            [0, 1, 0],
            [-sin(theta), 0, cos(theta)]
        ])

    def yaw(self, psi):
        """Returns the rotation matrix along the yaw axis"""
        return np.array([
            [cos(psi), -sin(psi), 0],
            [sin(psi), cos(psi), 0],
            [0, 0, 1]
        ])

    def rotate(self):
        """Applies the rotations in sequential order"""
        t = np.eye(3)
        for rot in self._rotations:
            r = self._rotation_map[rot[0]](radians(rot[1]))
            t = np.dot(r, t)
        return t

# return roll, pitch, yaw
def quat2euler(a, b, c, d):
    return np.arctan2(2*(a*b + c*d), (1-2*(b*b+c*c))), np.arcsin(2*(a*c-d*b)), np.arctan2(2*(a*d+b*c), (1-2*(c*c+d*d)))

# roll, pitch, yaw
def euler2quat(phi, theta, psi):
    return [
        np.cos(phi/2)*np.cos(theta/2)*np.cos(psi/2) + np.sin(phi/2)*np.sin(theta/2)*np.sin(psi/2),
        np.sin(phi/2)*np.cos(theta/2)*np.cos(psi/2) - np.cos(phi/2)*np.sin(theta/2)*np.sin(psi/2),
        np.cos(phi/2)*np.sin(theta/2)*np.cos(psi/2) + np.sin(phi/2)*np.cos(theta/2)*np.sin(psi/2),
        np.cos(phi/2)*np.cos(theta/2)*np.sin(psi/2) - np.sin(phi/2)*np.sin(theta/2)*np.cos(psi/2)        
    ]

#######################################################################

def plot():
    v = np.array([1, 0, 0])
    R1 = EulerRotation([(Rotation.ROLL, 25), (Rotation.PITCH, 75), (Rotation.YAW, 90)]).rotate()
    R2 = EulerRotation([(Rotation.PITCH, 75),(Rotation.ROLL, 25), (Rotation.YAW, 90)]).rotate()
    R3 = EulerRotation([(Rotation.YAW, 90), (Rotation.ROLL, 25), (Rotation.PITCH, 75)]).rotate()

    rv1 = np.dot(R1, v)
    rv2 = np.dot(R2, v)
    rv3 = np.dot(R3, v)
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # axes (shown in black)
    ax.quiver(0, 0, 0, 1.5, 0, 0, color='black', arrow_length_ratio=0.15)
    ax.quiver(0, 0, 0, 0, 1.5, 0, color='black', arrow_length_ratio=0.15)
    ax.quiver(0, 0, 0, 0, 0, 1.5, color='black', arrow_length_ratio=0.15)

    # Original Vector (shown in blue)
    ax.quiver(0, 0, 0, v[0], v[1], v[2], color='blue', arrow_length_ratio=0.15)

    # Rotated Vectors (shown in red)
    ax.quiver(0, 0, 0, rv1[0], rv1[1], rv1[2], color='red', arrow_length_ratio=0.15)
    ax.quiver(0, 0, 0, rv2[0], rv2[1], rv2[2], color='purple', arrow_length_ratio=0.15)
    ax.quiver(0, 0, 0, rv3[0], rv3[1], rv3[2], color='green', arrow_length_ratio=0.15)

    ax.set_xlim3d(-1, 1)
    ax.set_ylim3d(1, -1)
    ax.set_zlim3d(1, -1)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()    

def test_rotation():
    rotations = [
        (Rotation.ROLL, 25),
        (Rotation.PITCH, 75),
        (Rotation.YAW, 90),
    ]

    R = EulerRotation(rotations).rotate()
    R = np.round_(R, 3)
    assert(
        np.array_equal(R, np.array([
            [0, -0.906, 0.423],
            [.259, 0.408, 0.875],
            [-.966, 0.109, 0.235]
        ]))
    )

def test_quat2euler():
    quat = (0.683, 0.683, 0.183, -0.183,)
    euler = quat2euler(*quat)
    euler = list(map(lambda n: np.round(n, 3), euler))
    gt = list(map(lambda d: np.round(d, 3), [np.deg2rad(90), np.deg2rad(30), np.deg2rad(0)]))
    assert(euler == gt)

def test_euler2quat():
    euler = (np.deg2rad(90), np.deg2rad(30), np.deg2rad(0),)
    quat = euler2quat(*euler)
    quat = list(map(lambda n: np.round(n, 3), quat))
    assert(quat == [0.683, 0.683, 0.183, -0.183])
    
if '__main__' == __name__:
    test_rotation()
    test_quat2euler()
    test_euler2quat()
    #plot()
