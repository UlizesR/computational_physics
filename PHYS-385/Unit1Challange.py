# import necessary libraries
import numpy as np                                  # For numerical computing     
import scipy as sp                                  # For signal processing           
from scipy import signal                            # For signal processing
import matplotlib.pyplot as plt                     # For plotting
from matplotlib.gridspec import GridSpec            # For creating subplots
from matplotlib.animation import FuncAnimation      # For animation
from matplotlib.widgets import Button, Slider       # For buttons, sliders

# font stuff
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.linewidth'] = 3

FPS = 16                    # frames per second
ASPECT = 5                  # aspect ratio
LIM = 1.5                   # limits
WP_POS = 45                 # position of the wave plate
N = 100                     # number of points
WP_OFFSET = N//10           # offset of the wave plate
BOUNDS = N - 1              

# Defining Class for Jones Vectors and Matrices
class Jones:
    def __init__(self):
        self.hP = np.array([1, 0])                   # horizontal polarization
        self.vP = np.array([0, 1])                   # vertical polarization
        self.p45 = (1/np.sqrt(2))*np.array([1, 1])   # 45 degree polarization
        self.m45 = (1/np.sqrt(2))*np.array([1, -1])  # -45 degree polarization
        self.rC = (1/np.sqrt(2))*np.array([1, 1j])   # right circular polarization
        self.lC = (1/np.sqrt(2))*np.array([1, -1j])  # left circular polarization

        # create dictionary for the Jones vectors
        self.jones_vectors = {
            'hP': self.hP,
            'vP': self.vP, 
            'p45': self.p45, 
            'm45': self.m45, 
            'rC': self.rC, 
            'lC': self.lC
        }

    # Methods for Jones Matrices
        
    # Jones matrix for a horizontal Polarizer
    def jH(self) -> np.ndarray:
        return np.array([[1, 0], [0, 0]])
    
    # Jones matrix for a vertical Polarizer
    def jV(self) -> np.ndarray:
        return np.array([[0, 0], [0, 1]])
    
    # Jones matrix for a Linear Polarizer at some angle theta
    def jTheta(self, theta: float) -> np.ndarray:
        return np.array([
            [np.cos(theta)**2, np.sin(theta)*np.cos(theta)], 
            [np.sin(theta)*np.cos(theta), np.sin(theta)**2]
        ])
    
    # Jones matrix for a half Wave Plate at some fast axis angle theta w.r.t horizontal
    def jHWP(self, theta: float) -> np.ndarray:
        return np.array([
            [np.cos(2*theta), np.sin(2*theta)], 
            [np.sin(2*theta), -np.cos(2*theta)]
        ])
    
    # Jones matrix for a quarter Wave Plate at some fast axis angle theta w.r.t horizontal
    def jQWP(self, theta: float) -> np.ndarray:
        return np.array([
            [np.cos(theta)**2 + 1j*np.sin(theta)**2, (1-1j)*np.sin(theta)*np.cos(theta)], 
            [(1-1j)*np.sin(theta)*np.cos(theta), np.sin(theta)**2 + 1j*np.cos(theta)**2]
        ])
    

# Create a gridspec
gs = GridSpec(4, 2, height_ratios=[1, 1, 1, 1], width_ratios=[3, 1])  # 4 rows, 2 columns

fig = plt.figure(figsize=(12, 7))  # setting the size of the figure

# Add a 3D subplot to the figure
ax1 = fig.add_subplot(gs[:, 0], projection='3d')  # This plot spans all rows and the first column

# Add three 2D subplots
ax2 = fig.add_subplot(gs[0, 1])  # This plot is in the first row and second column
ax3 = fig.add_subplot(gs[1, 1])  # This plot is in the second row and second column
ax4 = fig.add_subplot(gs[2, 1])  # This plot is in the third row and second column

# Set aspect ratio to be equal so the figure is square
ax2.set_aspect('equal', adjustable='box')
ax3.set_aspect('equal', adjustable='box')
ax4.set_aspect('equal', adjustable='box')

plt.tight_layout()

# adjust the main plot to make room for the sliders and buttons
fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, hspace=0.5)

z = np.linspace(0, N, N)                        # z-axis values

# Had to set values of the y-axis to that of the z-axis because Matplotlib's 3D plot uses z-axis as the vertical axis
ax1.set_box_aspect([1, ASPECT, 1])       # aspect ratio
ax1.set_xlabel('X')                      # x-axis label
ax1.set_ylabel('Z')                      # y-axis label
ax1.set_zlabel('Y')                      # z-axis label
ax1.set_xticks([])                       # remove x-axis ticks
# ax1.set_yticks([])                     # remove y-axis ticks
ax1.set_zticks([])                       # remove z-axis ticks  

# set the limits of the plots
ax1.set_xlim(-LIM, LIM)                  # x-axis limits
ax1.set_ylim(0, z[BOUNDS])               # y-axis limits
ax1.set_zlim(-LIM, LIM)                  # z-axis limits
ax2.set_xlim(-LIM, LIM)                  # x-axis limits
ax2.set_ylim(-LIM, LIM)                  # y-axis limits
ax3.set_xlim(-LIM, LIM)                  # x-axis limits
ax3.set_ylim(-LIM, LIM)                  # y-axis limits
ax4.set_xlim(-LIM, LIM)                  # x-axis limits
ax4.set_ylim(-LIM, LIM)                  # y-axis limits

# draw a box in the middle of the plot in the y-z plane
# this box represents a polarizer
def draw_polarizer():
    # bottom square
    ax1.plot([-1.25, 1.25], [WP_POS, WP_POS], [-1.25, -1.25], 'k', linewidth=1)
    ax1.plot([-1.25, 1.25], [WP_POS, WP_POS], [1.25, 1.25], 'k', linewidth=1)
    ax1.plot([-1.25, -1.25], [WP_POS, WP_POS], [-1.25, 1.25], 'k', linewidth=1)
    ax1.plot([1.25, 1.25], [WP_POS, WP_POS], [-1.25, 1.25], 'k', linewidth=1)
    
    # top square
    ax1.plot([-1.25, 1.25], [WP_POS+WP_OFFSET, WP_POS+WP_OFFSET], [-1.25, -1.25], 'k', linewidth=1)
    ax1.plot([-1.25, 1.25], [WP_POS+WP_OFFSET, WP_POS+WP_OFFSET], [1.25, 1.25], 'k', linewidth=1)
    ax1.plot([-1.25, -1.25], [WP_POS+WP_OFFSET, WP_POS+WP_OFFSET], [-1.25, 1.25], 'k', linewidth=1)
    ax1.plot([1.25, 1.25], [WP_POS+WP_OFFSET, WP_POS+WP_OFFSET], [-1.25, 1.25], 'k', linewidth=1)
    
    # vertical lines
    ax1.plot([-1.25, -1.25], [WP_POS, WP_POS+WP_OFFSET], [-1.25, -1.25], 'k', linewidth=1)
    ax1.plot([-1.25, -1.25], [WP_POS, WP_POS+WP_OFFSET], [1.25, 1.25], 'k', linewidth=1)
    ax1.plot([1.25, 1.25], [WP_POS, WP_POS+WP_OFFSET], [-1.25, -1.25], 'k', linewidth=1)
    ax1.plot([1.25, 1.25], [WP_POS, WP_POS+WP_OFFSET], [1.25, 1.25], 'k', linewidth=1)

draw_polarizer()


# Make a vertically oriented slider to control the velocity of the wave
axvel = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
vel_slider = Slider(
    ax=axvel,
    label="Wave Velocity",
    valmin=0,
    valmax=1,
    valinit=0.1,
    orientation="vertical"
)

# Make a horizontal slider to control the angle of the wave plate or linear polarizer
axAngle = fig.add_axes([0.3, 0.2, 0.45, 0.0225])
# The slider object
angle_slider = Slider(
    ax=axAngle,
    label='Angle [rads]',
    valmin=0,
    valmax=2*np.pi,
    valinit=np.pi/4
)

# Create axes for the buttons
hPBtn = plt.axes([0.05, 0.01, 0.14, 0.05])
vPBtn = plt.axes([0.2, 0.01, 0.14, 0.05])
rCBtn = plt.axes([0.35, 0.01, 0.14, 0.05])
lCBtn = plt.axes([0.5, 0.01, 0.14, 0.05])
p45Btn = plt.axes([0.65, 0.01, 0.14, 0.05])
m45Btn = plt.axes([0.8, 0.01, 0.14, 0.05])

# Create axes for the buttons
jHBtn = plt.axes([0.125, 0.1, 0.14, 0.05])
jVBtn = plt.axes([0.275, 0.1, 0.14, 0.05])
linBtn = plt.axes([0.425, 0.1, 0.14, 0.05])
qwpBtn = plt.axes([0.575, 0.1, 0.14, 0.05])
hwpBtn = plt.axes([0.725, 0.1, 0.14, 0.05])

# Create buttons
hp_button = Button(hPBtn, 'hP')
vp_button = Button(vPBtn, 'vP')
p45_button = Button(p45Btn, 'p45')
m45_button = Button(m45Btn, 'm45')
rc_button = Button(rCBtn, 'rC')
lc_button = Button(lCBtn, 'lC')

# Create buttons
jh_button = Button(jHBtn, 'jH')
jv_button = Button(jVBtn, 'jV')
lin_button = Button(linBtn, 'jLiniar')
qwp_button = Button(qwpBtn, 'jQWP')
hwp_button = Button(hwpBtn, 'jHWP')

# Create a class for the buttons on click functions
class Index:
    def __init__(self):
        self.state = 'hP'
        self.polarizer = 'jH'
        self.jones = Jones()
        self.k = 1/24

    def hP(self, event):
        self.state = 'hP'
        self.update()

    def vP(self, event):
        self.state = 'vP'
        self.update()

    def p45(self, event):
        self.state = 'p45'
        self.update()

    def m45(self, event):
        self.state = 'm45'
        self.update()

    def rC(self, event):
        self.state = 'rC'
        self.update()

    def lC(self, event):
        self.state = 'lC'
        self.update()

    def jH(self, event):
        self.polarizer = 'jH'
        self.update()

    def jV(self, event):
        self.polarizer = 'jV'
        self.update()

    def jLiniar(self, event):
        self.polarizer = 'jLiniar'
        self.update()

    def jQWP(self, event):
        self.polarizer = 'jQWP'
        self.update()

    def jHWP(self, event):
        self.polarizer = 'jHWP'
        self.update()

    def update(self):
        global pol_state
        pol_state = np.full(N, self.state)
        ani.new_frame_seq()

# create an instance of the Index class
callback = Index()

# set the on click functions for the buttons
hp_button.on_clicked(callback.hP)
vp_button.on_clicked(callback.vP)
p45_button.on_clicked(callback.p45)
m45_button.on_clicked(callback.m45)
rc_button.on_clicked(callback.rC)
lc_button.on_clicked(callback.lC)

# set the on click functions for the buttons
jh_button.on_clicked(callback.jH)
jv_button.on_clicked(callback.jV)
lin_button.on_clicked(callback.jLiniar)
qwp_button.on_clicked(callback.jQWP)
hwp_button.on_clicked(callback.jHWP)

# set the quiver data
quiver = ax1.quiver([], [], [], [], [], [], color='black',linewidth=1, alpha=0.2)

# set the x and y values for the curves
xcurve, = ax1.plot([], [], [], 'tab:red', linewidth=1, alpha=0.4)
ycurve, = ax1.plot([], [], [], 'tab:green', linewidth=1, alpha=0.4)


# Initialize the electric field to be a 2D array of zeros 
# each array represents the x and y components of the electric field
E = np.zeros((N, 2), dtype=complex)
# initialize the electric field values 
# in this case the electric field is just a horizontal line across the z-axis

"""
    Since k = 1/v and w = 1 and we usually set v = 1, then k = 1
    E = Re[E_0 * exp(i(kz - wt)) * eps]
"""
# I need to divide 2pi by 18 because otherwise the wave will be too big
# if the divisor is too small, the wave becomes jagged
xs = np.real(E[:,0] * np.exp(1j * z * (2 * np.pi) / 18 ))
ys = np.real(E[:,1] * np.exp(1j * z * (2 * np.pi) / 18 ))

# plot the initial curve 
curve, = ax1.plot(xs, z, ys, 'tab:blue', linewidth=1)

# add vectors to the 2D plots
# each subplot will have a 3 vectors representing the x, y and 2D electric field
ax2_qx = ax2.quiver(0, 0, 1, 0, color='tab:red', scale=1, scale_units='xy', angles='xy', lw=2)
ax2_qy = ax2.quiver(0, 0, 0, 1, color='tab:blue', scale=1, scale_units='xy', angles='xy', lw=2)
ax2_qe = ax2.quiver(0, 0, 1, 1, color='black', scale=1, scale_units='xy', angles='xy', lw=2)

ax3_qx = ax3.quiver(0, 0, 1, 0, color='tab:red', scale=1, scale_units='xy', angles='xy', lw=2)
ax3_qy = ax3.quiver(0, 0, 0, 1, color='tab:blue', scale=1, scale_units='xy', angles='xy', lw=2)
ax3_qe = ax3.quiver(0, 0, 1, 1, color='black', scale=1, scale_units='xy', angles='xy', lw=2)

ax4_qx = ax4.quiver(0, 0, 1, 0, color='tab:red', scale=1, scale_units='xy', angles='xy', lw=2)
ax4_qy = ax4.quiver(0, 0, 0, 1, color='tab:blue', scale=1, scale_units='xy', angles='xy', lw=2)
ax4_qe = ax4.quiver(0, 0, 1, 1, color='black', scale=1, scale_units='xy', angles='xy', lw=2)


# a dictionsry for the titles
pol_state_title = {
    'hP': 'Horizontal Polarization',
    'vP': 'Vertical Polarization',
    'p45': '45 Degree Polarization',
    'm45': '-45 Degree Polarization',
    'rC': 'Right Circular Polarization',
    'lC': 'Left Circular Polarization'
}

pol_type_title = {
    'jH': 'Horizontal Polarizer',
    'jV': 'Vertical Polarizer',
    'jLiniar': 'Linear Polarizer',
    'jQWP': 'Quarter Wave Plate',
    'jHWP': 'Half Wave Plate'
}

# set the title of the plot
title = ax1.set_title('')

ax2.set_title('Entering Polarizer')
ax3.set_title('In Polarizer')
ax4.set_title('Exiting Polarizer')

b, a = signal.butter(2, 0.01)
E = signal.filtfilt(b, a, E, axis=0)

# the update function for the animation
def update(i):
    state = callback.state

    # set the title of the plot based on the current state
    if title.get_text() != pol_state_title[state] + ' - ' + pol_type_title[callback.polarizer]:
        title.set_text(pol_state_title[state] + ' - ' + pol_type_title[callback.polarizer])

    # calculate the electric field for each point
    for k in range(WP_POS):
        # calculate the electric field before the passing through the polarizer
        E[k] = callback.jones.jones_vectors[state] 
    for k in range(WP_POS + WP_OFFSET, N):
        # calculate the electric field after the passing through the polarizer
        if callback.polarizer == 'jH':
            E[k] = np.dot(callback.jones.jH(), callback.jones.jones_vectors[state])
        elif callback.polarizer == 'jV':
            E[k] = np.dot(callback.jones.jV(), callback.jones.jones_vectors[state])
        elif callback.polarizer == 'jLiniar':
            E[k] = np.dot(callback.jones.jTheta(angle_slider.val), callback.jones.jones_vectors[state])
        elif callback.polarizer == 'jHWP':
            E[k] = np.dot(callback.jones.jHWP(angle_slider.val), callback.jones.jones_vectors[state])
        elif callback.polarizer == 'jQWP':
            E[k] = np.dot(callback.jones.jQWP(angle_slider.val), callback.jones.jones_vectors[state])
    for k in range(WP_POS, WP_POS + 10):
        # calculate the electric field after the passing through the polarizer
        if callback.polarizer == 'jH':
            E[k] = np.dot(callback.jones.jH(), callback.jones.jones_vectors[state])
        elif callback.polarizer == 'jV':
            E[k] = np.dot(callback.jones.jV(), callback.jones.jones_vectors[state])
        elif callback.polarizer == 'jLiniar':
            E[k] = np.dot(callback.jones.jTheta(angle_slider.val + k * callback.k), callback.jones.jones_vectors[state])
        elif callback.polarizer == 'jHWP':
            E[k] = np.dot(callback.jones.jHWP(angle_slider.val * k * callback.k), callback.jones.jones_vectors[state])
        elif callback.polarizer == 'jQWP':
            E[k] = np.dot(callback.jones.jQWP(angle_slider.val * k * callback.k), callback.jones.jones_vectors[state])


    _x = np.real(E[:,0] * np.exp(1j * ((z * (2 * np.pi / 18)) - i * vel_slider.val) ))
    _y = np.real(E[:,1] * np.exp(1j * ((z * (2 * np.pi / 18)) - i * vel_slider.val) ))

    # update the x and y values of the curve
    curve.set_data_3d(_x, z, _y)
    # update the x and y values of the x and y curves
    xcurve.set_data_3d(_x, z, np.ones_like(_x)-2.5)
    ycurve.set_data_3d(np.ones_like(_y)-2.5, z, _y)
    # update the quiver data
    quiver.set_segments([np.array([[0, z[k], 0], [_x[k], z[k], _y[k]]]) for k in range(N)])  # switch y and z

    # update the 2D plots
    # update the x, y and 2D electric field vectors
    # as it enters the polarizer
    ax2_qx.set_UVC(_x[WP_POS], 0)
    ax2_qy.set_UVC(0, _y[WP_POS])
    ax2_qe.set_UVC(_x[WP_POS], _y[WP_POS])

    # as it passes through the polarizer
    ax3_qx.set_UVC(_x[WP_POS+WP_OFFSET // 2], 0)
    ax3_qy.set_UVC(0, _y[WP_POS+WP_OFFSET // 2])
    ax3_qe.set_UVC(_x[WP_POS+WP_OFFSET // 2], _y[WP_POS+WP_OFFSET // 2])

    # as it exits the polarizer
    ax4_qx.set_UVC(_x[WP_POS+WP_OFFSET], 0)
    ax4_qy.set_UVC(0, _y[WP_POS+WP_OFFSET])
    ax4_qe.set_UVC(_x[WP_POS+WP_OFFSET], _y[WP_POS+WP_OFFSET])
    return ()

# animate the plot
ani = FuncAnimation(fig, update, interval=1000/FPS, save_count=N, blit=True)

# show the plot
plt.show()