```python
from manim import *

class ExplainXSquared(Scene):
    def construct(self):
        # Title
        title = Text("Understanding x²", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Introduction
        intro_text = Text("The function f(x) = x² maps each number to its square", 
                         font_size=32)
        intro_text.next_to(title, DOWN, buff=0.5)
        self.play(Write(intro_text))
        self.wait(2)
        self.play(FadeOut(intro_text))
        
        # Setting up the coordinate system
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 9, 1],
            axis_config={"color": BLUE},
            x_axis_config={"numbers_to_include": list(range(-3, 4))},
            y_axis_config={"numbers_to_include": list(range(0, 10, 1))},
        )
        
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        self.play(Create(axes), Write(axes_labels))
        self.wait(1)
        
        # Create the parabola
        parabola = axes.plot(lambda x: x**2, color=YELLOW)
        parabola_label = MathTex("f(x) = x^2").next_to(parabola, UP+RIGHT)
        
        self.play(Create(parabola), Write(parabola_label))
        self.wait(2)
        
        # Demonstrate squaring with geometric representation
        for x_val in [-2, -1, 0, 1, 2]:
            # Create dot on x-axis and vertical line
            x_dot = Dot(axes.c2p(x_val, 0), color=GREEN)
            x_label = MathTex(f"x = {x_val}").next_to(x_dot, DOWN)
            
            # Calculate y value
            y_val = x_val**2
            
            # Create dot for result
            result_dot = Dot(axes.c2p(x_val, y_val), color=RED)
            
            # Vertical line
            vert_line = Line(
                axes.c2p(x_val, 0),
                axes.c2p(x_val, y_val),
                stroke_width=2,
                color=BLUE_D
            )
            
            # Result label
            result_label = MathTex(f"{x_val}^2 = {y_val}").next_to(result_dot, RIGHT)
            
            # Show the process
            self.play(
                FadeIn(x_dot),
                Write(x_label)
            )
            self.wait(0.5)
            
            self.play(
                Create(vert_line),
                FadeIn(result_dot),
                Write(result_label)
            )
            self.wait(1)
            
            # Emphasize the corresponding square
            if x_val != 0:  # Skip the square for x=0 as it would be invisible
                square = Square(side_length=abs(x_val))
                square.set_stroke(color=GREEN_B, width=2)
                square.set_fill(color=GREEN_B, opacity=0.3)
                square.next_to(axes.c2p(3.5, y_val/2), RIGHT)
                
                area_label = MathTex(f"\\text{{Area}} = {abs(x_val)} \\times {abs(x_val)} = {y_val}")
                area_label.next_to(square, RIGHT)
                
                self.play(Create(square), Write(area_label))
                self.wait(1)
                self.play(FadeOut(square), FadeOut(area_label))
            
            # Clean up for next iteration
            self.play(
                FadeOut(x_dot),
                FadeOut(x_label),
                FadeOut(result_dot),
                FadeOut(result_label),
                FadeOut(vert_line)
            )
        
        # Show key properties
        properties = VGroup(
            Text("Key Properties of f(x) = x²:", font_size=36),
            Text("1. Always outputs non-negative values (y ≥ 0)", font_size=28),
            Text("2. Symmetric about the y-axis", font_size=28),
            Text("3. Has its minimum at (0,0)", font_size=28),
            Text("4. Grows more rapidly as |x| increases", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        properties.to_edge(DOWN, buff=0.5)
        
        self.play(Write(properties[0]))
        
        # Highlight non-negative property
        self.play(Write(properties[1]))
        highlight_region = Rectangle(
            width=axes.x_range[1] - axes.x_range[0],
            height=0.5,
            color=GREEN
        ).move_to(axes.c2p(0, -0.25))
        self.play(Create(highlight_region))
        self.wait(1)
        self.play(FadeOut(highlight_region))
        
        # Show symmetry
        self.play(Write(properties[2]))
        symmetry_line = axes.get_vertical_line(axes.c2p(0, 0), line_config={"dashed_ratio": 0.5})
        symmetry_line.set_color(PURPLE)
        self.play(Create(symmetry_line))
        
        # Animate points to show symmetry
        for x_val in [1, 2]:
            left_dot = Dot(axes.c2p(-x_val, x_val**2), color=RED)
            right_dot = Dot(axes.c2p(x_val, x_val**2), color=RED)
            symmetry_arrow = DoubleArrow(left_dot.get_center(), right_dot.get_center(), color=PURPLE)
            
            self.play(
                FadeIn(left_dot),
                FadeIn(right_dot),
                Create(symmetry_arrow)
            )
            self.wait(0.5)
            self.play(
                FadeOut(left_dot),
                FadeOut(right_dot),
                FadeOut(symmetry_arrow)
            )
        
        self.play(FadeOut(symmetry_line))
        
        # Show minimum at origin
        self.play(Write(properties[3]))
        min_point = Dot(axes.c2p(0, 0), color=YELLOW, radius=0.1)
        min_label = Text("Minimum", font_size=24).next_to(min_point, DOWN)
        
        self.play(Create(min_point), Write(min_label))
        self.wait(1)
        self.play(FadeOut(min_point), FadeOut(min_label))
        
        # Show rapid growth
        self.play(Write(properties[4]))
        growth_arrows = VGroup()
        for x in [-3, -2, -1, 0, 1, 2]:
            if x != 0:
                start_point = axes.c2p(x, x**2)
                end_point = axes.c2p(x+1, (x+1)**2)
                arrow = Arrow(start_point, end_point, color=RED_B)
                growth_arrows.add(arrow)
        
        self.play(LaggedStart(*[Create(arrow) for arrow in growth_arrows], lag_ratio=0.3))
        self.wait(1)
        self.play(FadeOut(growth_arrows))
        
        # Applications
        self.play(FadeOut(properties))
        
        applications = Text(
            "Applications of x²:\n" +
            "• Area calculations\n" +
            "• Projectile motion\n" +
            "• Economics (quadratic cost functions)\n" +
            "• Machine learning optimization",
            font_size=32,
            line_spacing=1.5
        )
        applications.to_edge(DOWN, buff=0.8)
        
        self.play(Write(applications))
        self.wait(2)
        
        # Final summary
        self.play(
            FadeOut(applications),
            FadeOut(parabola),
            FadeOut(parabola_label),
            FadeOut(axes),
            FadeOut(axes_labels)
        )
        
        summary = Text(
            "The function f(x) = x² is one of the most\n" +
            "fundamental functions in mathematics,\n" +
            "forming the basis for many mathematical models.",
            font_size=36,
            line_spacing=1.2
        )
        
        self.play(Write(summary))
        self.wait(2)
        
        self.play(FadeOut(summary), FadeOut(title))
        
        final_equation = MathTex("f(x) = x^2", font_size=72)
        self.play(Write(final_equation))
        self.wait(1)
        self.play(FadeOut(final_equation))
        self.wait(1)
```
