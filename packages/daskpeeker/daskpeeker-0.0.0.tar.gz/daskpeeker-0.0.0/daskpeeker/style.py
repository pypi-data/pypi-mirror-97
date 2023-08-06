DEFAULT_VIEW_NAME = "Unnamed View"

LEFT_COLOR = "#00AEF9"
RIGHT_COLOR = "#F9AE00"
colors = [LEFT_COLOR, RIGHT_COLOR]

sidebar_w = 45
content_l_m = 0
navb_h = 50  # 62.5

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": navb_h,
    "left": 0,
    "bottom": 0,
    "width": f"{sidebar_w}rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    # "padding": "0.5rem 1rem",
    "background-color": "#f8f9fa",
}

SIDEBAR_HIDDEN = {
    **SIDEBAR_STYLE,
    "left": f"-{sidebar_w}rem",
    "padding": "0rem 0rem",
}


CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": f"{content_l_m + sidebar_w}rem",
    # "margin-right": "2rem",
    "padding": "4rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE_HIDDEN = {
    **CONTENT_STYLE,
    "margin-left": f"{content_l_m}rem",
}
