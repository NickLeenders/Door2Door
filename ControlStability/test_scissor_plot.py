from scissor_plot import create_plot,control_curve,stability_curve
import numpy as np

control_value = control_curve(1)
stability_value = stability_curve(1)
x_cg = np.linspace(0, 0.4, num=10)
create_plot(x_cg)
pass

