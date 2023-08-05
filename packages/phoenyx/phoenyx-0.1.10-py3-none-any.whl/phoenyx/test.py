from phoenyx import *

from renderer import *  # type: ignore
from menu import *  # type: ignore
from slider import *  # type: ignore
from button import *  # type: ignore

renderer = Renderer(600, 600)

menu: object
slider: object


def setup() -> None:
    global menu, slider
    slider = renderer.create_slider(100, 100, "slider", 0, 10, 1, 0, length=300, shape="SQUARE")

    renderer.create_button(
        100,
        300,
        "hide slider",
        action=slider.hide,
        height=50,
        width=100,
        color=70,
        stroke="red",
        shape="ELLIPSE",
    )
    renderer.create_button(
        100,
        400,
        "reveal slider",
        action=slider.reveal,
        height=50,
        width=100,
        color=70,
        stroke="green",
        shape="ELLIPSE",
    )

    menu = renderer.create_menu(
        "menu",
        side="RIGHT",
        test=lambda: print("menu activated"),
        other_test=lambda: print("yo"),
        third_test=lambda: print("no inspiration"),
        # wow_this_line_is_long_and_it_will_force_the_menu_to_have_a_big_width=lambda: print("long"),
        blob=lambda: print("blob"),
        blob2=lambda: print("blob2 lol"),
        last_one_i_swear=lambda: print("not sure though"))

    renderer.new_keypress(renderer.keys.K_SPACE, lambda: print("space"), behaviour="HOLD")
    renderer.new_keypress(renderer.keys.K_a, lambda: print("a"), behaviour="PRESSED")
    renderer.update_keypress(renderer.keys.K_SPACE, lambda: print("space but updated"))

    renderer.text_size = 15


def draw() -> None:
    global menu, slider
    renderer.background(51)

    renderer.text(10, 10, f"fps : {round(renderer.fps)}")
    renderer.text(10, 30, f"value of slider : {slider.value}")
    renderer.text(10, 50, f"state of menu : {('unflod', 'fold')[menu.is_fold],menu.tick_count}")


if __name__ == "__main__":
    renderer.run(draw, setup=setup)
