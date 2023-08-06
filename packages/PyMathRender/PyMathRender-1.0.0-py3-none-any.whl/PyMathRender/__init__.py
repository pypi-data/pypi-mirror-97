from matplotlib.pyplot import figure, plot, show
from matplotlib.animation import FuncAnimation
i, y, fig, x = [], [], figure(figsize = (12.8, 9.6)), 0
def process(color: str):
    if color == "blue": return 'b-'
    elif color == "green": return 'g-'
    elif color == "red": return 'r-'
    elif color == "cyan": return 'c-'
    elif color == "magenta": return 'm-'
    elif color == "yellow": return 'y-'
    elif color == "black": return 'k-'
    elif color == "white": return 'w-'
    else: return "-"
def main(Input, Text = "", LineColor = "", TextColor = "white", start = 0, end = 10, step = .001, required = []):
    if required:
        for r in required: exec("import " + r, globals())
    color = process(LineColor)
    def animate(ii):
        global x
        x = ii * step
        i.append(x)
        if callable(Input): y.append(Input(x))
        else: y.append(eval(Input))
        plot(i, y, color)
    fig.text(0.05, 0.95, Text, bbox = dict(facecolor = TextColor, alpha = 0.5))
    anim = FuncAnimation(fig, animate, range(int(start / step), int(end / step)))
    show()