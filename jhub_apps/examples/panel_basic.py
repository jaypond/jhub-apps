"""We can use this to test the bokeh_root_cmd"""
import panel as pn

pn.extension(sizing_mode="stretch_width")


def test_panel_app():
    """Returns a Panel test app that has been marked `.servable()`

    Returns:
        pn.Column: A Column based Panel app
    """
    slider = pn.widgets.FloatSlider(name="Slider")
    return pn.template.FastListTemplate(
        title="Panel Test App", sidebar=[slider], main=[slider.param.value]
    ).servable()


if __name__.startswith("bokeh"):
    test_panel_app()
