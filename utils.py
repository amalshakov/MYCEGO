import math
from typing import List, Tuple

from PIL import Image


def determine_rows_and_columns(num_images: int) -> Tuple[int, int]:
    """
    Определяет количество строк и столбцов
    в зависимости от количества изображений.

    Args:
        num_images (int): Количество изображений.

    Returns:
        Tuple[int, int]: Кортеж из двух значений: количество строк и столбцов.
    """
    if num_images <= 2:
        rows, cols = 1, num_images
    elif num_images <= 4:
        rows, cols = 2, 2
    elif num_images == 6:
        rows, cols = 2, 3
    elif num_images == 8:
        rows, cols = 2, 4
    elif num_images == 12:
        rows, cols = 3, 4
    else:
        cols = min(num_images, 4)  # Максимум 4 столбца
        rows = math.ceil(num_images / cols)
    return rows, cols


def scale_images(
    images: List[Image.Image],
    page_width: int,
    page_height: int,
    MIN_MARGIN_LR: int,
    MIN_MARGIN_TB: int,
    MARGIN_BETWEEN: int,
) -> List[Image.Image]:
    """
    Масштабирует список изображений
    с учетом заданных параметров страницы и отступов.

    Args:
        images (List[Image.Image]): Список объектов изображений PIL.Image.
        page_width (int): Ширина страницы в пикселях.
        page_height (int): Высота страницы в пикселях.
        MIN_MARGIN_LR (int): Минимальные отступы слева и справа в пикселях.
        MIN_MARGIN_TB (int): Минимальные отступы сверху и снизу в пикселях.
        MARGIN_BETWEEN (int): Отступ между изображениями в пикселях.

    Returns:
        List[Image.Image]: Список масштабированных изображений.
    """
    scaled_images = []
    num_images = len(images)
    rows, cols = determine_rows_and_columns(num_images)

    max_image_width = (
        page_width - 2 * MIN_MARGIN_LR - (cols - 1) * MARGIN_BETWEEN
    ) // cols
    max_image_height = (
        page_height - 2 * MIN_MARGIN_TB - (rows - 1) * MARGIN_BETWEEN
    ) // rows

    for img in images:
        img_width, img_height = img.size
        scale_ratio = min(
            max_image_width / img_width, max_image_height / img_height
        )
        new_size = (
            int(img_width * scale_ratio),
            int(img_height * scale_ratio),
        )
        scaled_images.append(img.resize(new_size, Image.Resampling.NEAREST))

    return scaled_images


def calculate_margins(
    scaled_images: List[Image.Image],
    cols: int,
    rows: int,
    page_width: int,
    page_height: int,
    MARGIN_BETWEEN: int,
) -> Tuple[int, int, int, int]:
    """
    Вычисляет отступы слева, справа, сверху и снизу
    на основе масштабированных изображений.

    Args:
        scaled_images (List[Image.Image]): Список масштабированных изображений.
        cols (int): Количество столбцов.
        rows (int): Количество строк.
        page_width (int): Ширина страницы в пикселях.
        page_height (int): Высота страницы в пикселях.
        MARGIN_BETWEEN (int): Отступ между изображениями в пикселях.

    Returns:
        Tuple[int, int, int, int]: Кортеж из четырех значений:
            - left_margin: отступ слева,
            - right_margin: отступ справа,
            - top_margin: отступ сверху,
            - bottom_margin: отступ снизу.
    """
    total_images_width = (
        sum(img.size[0] for img in scaled_images[:cols])
        + (cols - 1) * MARGIN_BETWEEN
    )
    left_margin = (page_width - total_images_width) // 2

    total_images_height = (
        sum(img.size[1] for img in scaled_images[:rows])
        + (rows - 1) * MARGIN_BETWEEN
    )
    top_margin = (page_height - total_images_height) // 2

    right_margin = page_width - total_images_width - left_margin
    bottom_margin = page_height - total_images_height - top_margin

    return left_margin, right_margin, top_margin, bottom_margin


def insert_images_into_new_image(
    new_image: Image.Image,
    scaled_images: List[Image.Image],
    cols: int,
    rows: int,
    left_margin: int,
    top_margin: int,
    MARGIN_BETWEEN: int,
) -> None:
    """
    Вставляет масштабированные изображения в новое изображение
    с учетом заданных параметров.

    Args:
        new_image (Image.Image): Новое изображение,
            в которое вставляются изображения.
        scaled_images (List[Image.Image]): Список масштабированных изображений.
        cols (int): Количество столбцов для размещения изображений.
        rows (int): Количество строк для размещения изображений.
        left_margin (int): Отступ слева в пикселях.
        top_margin (int): Отступ сверху в пикселях.
        MARGIN_BETWEEN (int): Отступ между изображениями в пикселях.
    """
    x_offset = left_margin
    y_offset = top_margin
    col_count = 0
    for img in scaled_images:
        new_image.paste(img, (x_offset, y_offset))
        x_offset += img.size[0] + MARGIN_BETWEEN
        col_count += 1
        if col_count == cols:
            x_offset = left_margin
            y_offset += img.size[1] + MARGIN_BETWEEN
            col_count = 0
