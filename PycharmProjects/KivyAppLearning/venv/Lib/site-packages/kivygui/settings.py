import os
from os.path import join as j

here = os.path.dirname(__file__)
f = os.path.abspath(j(here, 'fonts'))

KIVY_FONTS = [
    # {
        # "name": "SourceSansPro",
        # "fn_regular": j(f, "SourceSansPro-Regular"),
        # "fn_bold": j(f, "SourceSansPro-Bold"),
        # "fn_italic": j(f, "SourceSansPro-Italic"),
        # "fn_bolditalic": j(f, "SourceSansPro-BoldItalic"),
    # },
    {
        "name": "Raleway",
        "fn_regular": j(f, "Raleway-Regular.ttf"),
        "fn_bold": j(f, "Raleway-Bold.ttf"),
        "fn_italic": j(f, "Raleway-Italic.ttf"),
        "fn_bolditalic": j(f, "Raleway-BoldItalic.ttf"),
    },
    {
        "name": "Ubuntu",
        "fn_regular": j(f, "Ubuntu-Regular.ttf"),
        "fn_bold": j(f, "Ubuntu-Bold.ttf"),
        "fn_italic": j(f, "Ubuntu-Italic.ttf"),
        "fn_bolditalic": j(f, "Ubuntu-BoldItalic.ttf"),
    },
    {
        "name": "SourceCodePro",
        "fn_regular": j(f, "SourceCodePro-Regular.ttf"),
        "fn_bold": j(f, "SourceCodePro-Bold.ttf"),
    },
    {
        "name": "Inconsolata",
        "fn_regular": j(f, "Inconsolata-Regular.ttf"),
        "fn_bold": j(f, "Inconsolata-Bold.ttf"),
    },
    {
        "name": "RobotoCondensed",
        "fn_regular": j(f, "RobotoCondensed-Light.ttf"),
        "fn_bold": j(f, "RobotoCondensed-Regular.ttf"),
        "fn_italic": j(f, "RobotoCondensed-LightItalic.ttf"),
        "fn_bolditalic": j(f, "RobotoCondensed-Italic.ttf"),
    }
]

from kivy.core.text import LabelBase
for font in KIVY_FONTS:
    LabelBase.register(**font)
