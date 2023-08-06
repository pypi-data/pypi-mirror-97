import numpy as np
from scipy.integrate import quad
from scipy.interpolate import interp1d


def dt_v(t):
    dt_v = np.array(list([t[i + 1] - t[i]] for i in range(t.size - 1)))
    dt_v = np.append(dt_v, np.array([t[-2] - t[-1]]))
    return dt_v


class two_d:

    def Q_interp1d(self, x1, x2, target, log=False):
        """
        :param x1:
        :param x2:
        :param target:
        :param log:
        :return:
        """

        # Integral about x_p axis
        int_z = np.empty(target.shape[1])

        for i in range(x1.size):
            spl_x2 = interp1d(x2, target[:, i])
            int_z[i] = quad(spl_x2, x2.min(), x2.max())[0]*1000

        # Integral about z_p axis
        spl_x1 = interp1d(x1, int_z)
        int_x1 = quad(spl_x1, x1[1], x1[-2])[0]

        if log:
            print(f"Maximum value of target distribution:    {target.max():.5f}")
            print(f"Average value over x2 axis:              {np.mean(target):.5f}")
            print(f"Integral over x1, x2 axes:               {int_z:.5f}")

        return int_x1, spl_x1
