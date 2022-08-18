from cv2 import LineSegmentDetector, transform
from manim import *


class AtwoodMachine(Scene):
    def construct(self):
        self.edge = 1
        self.left_rope_length = 3
        self.right_rope_length = 1
        self.left_block_rope = 0.75
        self.right_block_rope = 0.5
        
        self.init_blocks()
        self.init_pulley()
        self.move_blocks()
    
    def init_blocks(self):
        self.m_big = Square(1.5, color=PURPLE, fill_color=PURPLE, fill_opacity=1).set_x(-self.edge).set_y(-self.left_block_rope)
        self.m_small = Square(1, color=PURPLE, fill_color=PURPLE, fill_opacity=1).set_x(self.edge).set_y(-self.right_block_rope)
        
        self.play(Create(self.m_big), Create(self.m_small))

    def init_pulley(self):
        # Left rope
        self.p1 = Dot([-self.edge, 2, 0])
        self.left_rope = always_redraw(lambda: Line(self.p1, self.m_big.get_top()).set_color(BLUE))
        # Right rope
        self.p2 = Dot([self.edge, 2, 0])
        self.right_rope = always_redraw(lambda: Line(self.p2, self.m_small.get_top()).set_color(BLUE))

        self.pulley = Circle(self.edge, color=RED, fill_color=RED, fill_opacity=1).set_x(0).set_y(2)

        self.play(Create(self.left_rope), Create(self.right_rope))
        self.play(DrawBorderThenFill(self.pulley))
        self.add_foreground_mobject(self.pulley)
    
    def move_blocks(self):
        self.left_arrow = always_redraw(lambda: Arrow(start=self.m_big.get_bottom(), end=self.m_big.get_bottom() - [0, 1, 0]))
        self.right_arrow = always_redraw(lambda: Arrow(start=self.m_small.get_top() + [0.25, 0, 0], end=self.m_small.get_top() + [0.25, 1, 0]))

        def move_up(x, y, z, t):
            return (x, y + t, z)
        def move_down(x, y, z, t):
            return (x, y - t, z)
        translate_big = Homotopy(move_down, self.m_big, run_time=3, rate_func=rate_functions.ease_in_quad)
        translate_small = Homotopy(move_up, self.m_small, run_time=3, rate_func=rate_functions.ease_in_quad)

        self.play(GrowArrow(self.left_arrow), GrowArrow(self.right_arrow))
        self.add(self.left_rope, self.right_rope)
        self.play(translate_big, translate_small) # Lines move dependent to this
        self.wait(5)