# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, Tuple, Union
import os

# Pip
from PIL import Image, ImageFile
from noraise import noraise

# Local
from .enums import FillType

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ class: Resizer ------------------------------------------------------------ #

class Resizer:

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def resize_keep_aspect_ratio(
        cls,
        image: Union[str, Image.Image], # accepts both image path and PIL.Image.Image
        fill_type: FillType,
        target_size: Tuple[int, int] = (1920, 1080),
        path_out: Optional[str] = None,
        return_image_instead_of_success: bool = False
    ) -> Union[Image.Image, bool]:
        if isinstance(image, str):
            image = Image.open(open(image, 'rb')).convert('RGBA')

        target_width, target_height = target_size
        w, h = image.size
        ratio = min(float(target_width)/float(w), float(target_height)/float(h))

        if fill_type == FillType.Fill:
            ratio = max(float(target_width)/float(w), float(target_height)/float(h))

        image = image.resize((int(float(w)*ratio), int(float(h)*ratio)))
        nw, nh = image.size

        if fill_type == FillType.Fill:
            x = int((float(nw) - float(target_width)) / 2)
            y = int((float(nh) - float(target_height)) / 2)

            area = (x, y, x+target_width, y+target_height)
            image = image.crop(area)

        if path_out:
            save_res = cls.save_image(image, path_out)

            if not return_image_instead_of_success:
                return save_res

        return image

    @classmethod
    def paste_and_fit(
        cls,
        background_image: Union[str, Image.Image], # accepts both image path and PIL.Image.Image
        foreground_image: Union[str, Image.Image], # accepts both image path and PIL.Image.Image
        use_foreground_image_size: bool = False,
        path_out: Optional[str] = None,
        return_image_instead_of_success: bool = False
    ) -> Union[Image.Image, bool]:
        ImageFile.LOAD_TRUNCATED_IMAGES = True

        if isinstance(foreground_image, str):
            foreground_image = Image.open(open(foreground_image, 'rb')).convert('RGBA')

        target_size = foreground_image.size if use_foreground_image_size else background_image.size
        background_image = background_image.copy()

        if background_image.size != target_size:
            background_image = cls.resize_keep_aspect_ratio(background_image, FillType.Fill, target_size=target_size)

        if foreground_image.size != target_size:
            foreground_image = foreground_image.copy()
            foreground_image = cls.resize_keep_aspect_ratio(foreground_image, FillType.Fit, target_size=target_size)

        overlay_x = int((float(background_image.size[0]) - float(foreground_image.size[0]))/2)
        overlay_y = int((float(background_image.size[1]) - float(foreground_image.size[1]))/2)

        background_image.paste(
            foreground_image,
            (
                overlay_x,
                overlay_y,
                overlay_x + foreground_image.size[0],
                overlay_y + foreground_image.size[1]
            )
        )

        if path_out:
            save_res = cls.save_image(background_image, path_out)

            if not return_image_instead_of_success:
                return save_res

        return background_image

    @staticmethod
    @noraise(default_return_value=False)
    def save_image(
        image: Image,
        path: str
    ) -> bool:
        out_file = open(path, 'wb' )
        image.save(out_file, path.split('.')[-1].lower().replace('jpg', 'jpeg'))  # Must specify desired format here
        out_file.flush()
        out_file.close()

        return os.path.exists(path)


# ---------------------------------------------------------------------------------------------------------------------------------------- #