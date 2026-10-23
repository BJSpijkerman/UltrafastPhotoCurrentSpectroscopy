from LabControl.experiments.LockIn import LockIn
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

port_name = ""
baudrate = 9600
internal_ref = True
gain = 26
tau = 4

lockin = LockIn()
lockin.set_baudrate(baudrate)
lockin.connect(port_name)
lockin.set_reference(internal_ref)
lockin.set_gain(gain)
lockin.set_tau(tau)
lockin.Configure()

print(lockin.Aquire("X"))

fig = plt.figure(figsize=(9, 5))
ax = fig.add_subplot()

line_X, = ax.plot([], [])
line_Y, = ax.plot([], [])

t = []
X = []
Y = []
def update(i):
	t.append(i)
	result = lockin.AquireSnap()
	X.append(result["X"])
	Y.append(result["Y"])
	line_X.set_data(t, X)
	line_Y.set_data(t, Y)
	ax.relin()
	ax.autoscale_view()

ani = FuncAnimation(fig, update)
plt.show()
