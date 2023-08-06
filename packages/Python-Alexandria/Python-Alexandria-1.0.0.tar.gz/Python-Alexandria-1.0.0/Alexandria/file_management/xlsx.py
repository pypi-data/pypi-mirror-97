import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

from mpl_plotter.two_d import line
from mpl_plotter.three_d import line as line3

from constructs.list import chain_words


class Worksheet:
    def __init__(self, wb, s):
        self.s = s
        self.ws = wb[s]

    def get_header_names(self):
        rows = self.ws.iter_rows(min_row=1, max_row=1)
        first_row = next(rows)
        self.headings = [c.value for c in first_row]
        return self.headings

    def column_values(self, n_col):
        c = []
        for row in tuple(self.ws.rows):
            c.append(row[n_col].value)
        del c[0]
        c = pd.Series(c)
        pd.to_numeric(c, errors='coerce')
        c.dropna()
        return c

    def plot_col(self, col1, col2, i, n, args_x, args_y, cmap='inferno', last=False, fig=None):
        try:
            c = mpl.cm.get_cmap(cmap)
            line(self.column_values(self.headings.index(col1)),
                 self.column_values(self.headings.index(col2)),
                 fig=fig,
                 line_width=2, color=c(i / n), title_size=16,
                 x_label=col1.capitalize(),
                 y_label=col2.capitalize(),
                 x_label_size=18, y_label_rotation=90, y_label_size=18,
                 x_label_pad=args_x[0], x_upper_bound=args_x[1][1], x_lower_bound=args_x[1][0], custom_x_tick_labels=args_x[2], x_tick_number=args_x[3],
                 y_label_pad=args_y[0], y_upper_bound=args_y[1][1], y_lower_bound=args_y[1][0], custom_y_tick_labels=args_y[2], y_tick_number=args_y[3],
                 grid=True, grid_color='lightgrey', tick_ndecimals=2,
                 title='{} vs {}'.format(chain_words(col2.split(' ')[:-1]).capitalize(), chain_words(col1.split(' ')[:-1]).capitalize()),
                 plot_label=self.s.replace('_', ' ')[:-2],
                 legend=True, legend_size=12 if not isinstance(fig, type(None)) else 10, legend_ncol=2,
                 more_subplots_left=not last,
                 backend=None)
        except ValueError:
            print("Probable errors:\n" +
                  "     Plot axis limits -> NaN, inf\n" +
                  "     Sheet {}: time [s] is not in column name list:\n     {}\n".format(self.s, self.headings) +
                  "If error impedes desired function comment out try-except statement at lines 39-54")
        except TypeError:
            print("Probable error:\n"
                  "     Missing legend string. Check line 57")
        return self

    def save(self, name, dpi):
        plt.tight_layout()
        plt.savefig(name, dpi=dpi)
        plt.show()

    def plot_col_3d(self, col1, col2, x, last=False):
        """
        Deprecated
        """
        try:
            y = self.column_values(self.headings.index(col1))
            z = self.column_values(self.headings.index(col2))
            xx = x*np.ones(y.shape)
            line3(x=xx,
                  y=y,
                  z=z,
                  x_label='Wind', x_label_pad=10,
                  y_label=col1, y_label_pad=10, y_label_rotation=90,
                  z_label=col2, z_label_pad=10, z_label_rotation=90,
                  x_label_size=16, y_label_size=16, title_size=16,
                  line_width=2, color=((x+10)/24)*np.ones(3),
                  x_bounds=[-10, 10],
                  y_bounds=[0, 600],
                  z_bounds=[0, 5],
                  grid=True, grid_color='lightgrey',
                  title='Stratos IV flight profile: {} vs {}'.format(col2.split(' ', 1)[0], col1.split(' ', 1)[0]),
                  legend=True, legend_size=9.5, legend_ncol=2,
                  more_subplots_left=not last)
        except ValueError:
            print('Sheet {}: time [s] is not in column name list:\n{}'.format(self.s, self.headings))
        return self
