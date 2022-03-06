import numpy as np

def init_HLU():
    H = np.array([1.0, 0.0, 0.0])
    L = np.array([0.0, 0.0, 1.0])
    U = np.cross(H, L)
    HLU = np.array((H, L, U)).T

    return HLU

def R2d(v, alpha):
    M = np.array(((np.cos(alpha), -np.sin(alpha)),
                  (np.sin(alpha),  np.cos(alpha))))
    return M.dot(v)

def RU(HLU, alpha):
    M = np.array((( np.cos(alpha), np.sin(alpha), 0.0),
                  (-np.sin(alpha), np.cos(alpha), 0.0),
                  (0.0, 0.0, 1.0)))
    return HLU.dot(M)

def RL(HLU, alpha):
    M = np.array(((np.cos(alpha), 0.0, -np.sin(alpha)),
                  (0.0, 1.0, 0.0),
                  (np.sin(alpha), 0.0, np.cos(alpha))))
    return HLU.dot(M)

def RH(HLU, alpha):
    M = np.array(((1.0, 0.0, 0.0),
                 (0.0, np.cos(alpha), -np.sin(alpha)),
                 (0.0, np.sin(alpha), np.cos(alpha))))

    return HLU.dot(M)
