# pil_resize

![PyPI - package version](https://img.shields.io/pypi/v/pil_resize?logo=pypi&style=flat-square)
![PyPI - license](https://img.shields.io/pypi/l/pil_resize?label=package%20license&style=flat-square)
![PyPI - python version](https://img.shields.io/pypi/pyversions/pil_resize?logo=pypi&style=flat-square)
![PyPI - downloads](https://img.shields.io/pypi/dm/pil_resize?logo=pypi&style=flat-square)

![GitHub - last commit](https://img.shields.io/github/last-commit/kkristof200/py_resize_image?style=flat-square)
![GitHub - commit activity](https://img.shields.io/github/commit-activity/m/kkristof200/py_resize_image?style=flat-square)

![GitHub - code size in bytes](https://img.shields.io/github/languages/code-size/kkristof200/py_resize_image?style=flat-square)
![GitHub - repo size](https://img.shields.io/github/repo-size/kkristof200/py_resize_image?style=flat-square)
![GitHub - lines of code](https://img.shields.io/tokei/lines/github/kkristof200/py_resize_image?style=flat-square)

![GitHub - license](https://img.shields.io/github/license/kkristof200/py_resize_image?label=repo%20license&style=flat-square)

## Description

E

## Install

~~~~bash
pip install pil_resize
# or
pip3 install pil_resize
~~~~

## Usage

~~~~python
from pil_resize_aspect_ratio import Resizer, FillType

p_org_img_bg  = 'bg.png'
p_overlay_img = 'fg.png'
path_out = 'final.png'

resized_bg_image = Resizer.resize_keep_aspect_ratio(
    image=p_org_img_bg,
    fill_type=FillType.Fill,
    target_size=(1920, 1080),
    return_image_instead_of_success=False
)

print(
    Resizer.paste_and_fit(
        background_image=resized_bg_image,
        foreground_image=p_overlay_img,
        path_out=path_out
    )
)
~~~~

## Dependencies

[noraise](https://pypi.org/project/noraise), [Pillow](https://pypi.org/project/Pillow)