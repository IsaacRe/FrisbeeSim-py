from disc import Disc
from graphics import *

TICK_TIME = 0.1
pix_ratio = 2


class GameManager:

    def test(self, pos, angles, veloc):
        print("Starting simulation...")

        window = GraphWin("Frisbee Sim", 500, 500)
        
        disc = Disc(TICK_TIME)

        disc.begin_flight(pos, angles, veloc)
        disc_draw = Circle(Point(250, 250), 10)
        disc_draw.draw(window)
        disc_draw.setFill('red')

        while disc.y > 0.0:
            disc.update_flight()
            disc_draw.move((disc.x - disc_draw.getCenter().x + 250) * pix_ratio, (disc.z - disc_draw.getCenter().y + 250) * pix_ratio)

            time.sleep(0.05)

        window.getMouse()
        window.close()
