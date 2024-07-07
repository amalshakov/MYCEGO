import os
from typing import List

from PIL import Image

from utils import (
    calculate_margins,
    determine_rows_and_columns,
    insert_images_into_new_image,
    scale_images,
)


def collect_png_to_tiff(input_folders: List[str]) -> None:
    """
    Создает TIFF файлы на основе PNG изображений,
    расположенных в указанных папках.

    Args:
        input_folders (List[str]): Список папок с файлами PNG.

    Raises:
        ValueError: Если список input_folders пустой.

    """
    # Константы для настроек TIFF файлов
    PAGE_SIZE = (
        3508,
        2480,
    )  # Размер страницы TIFF в пикселях (ширина, высота) - горизонтальный А4
    MIN_MARGIN_LR = 200  # Минимальные отступы слева и справа в пикселях
    MIN_MARGIN_TB = 300  # Минимальные отступы сверху и снизу в пикселях
    MARGIN_BETWEEN = 80  # Отступ между изображениями в пикселях

    # Проверка на корректность входных данных
    if len(input_folders) == 0:
        raise ValueError(
            "Функция должна принимать список с одним "
            "или несколькими элементами - папками с файлами PNG"
        )

    # Обработка каждой папки
    for i, input_folder in enumerate(input_folders, start=1):
        # Получить список всех PNG файлов в текущей папке
        png_files = [
            file for file in os.listdir(input_folder) if file.endswith(".png")
        ]

        # Сортировка файлов, чтобы порядок был предсказуемым
        png_files.sort()

        # Список изображений для сохранения в TIFF
        images = []

        # Открыть все изображения и добавить их в список
        for file_name in png_files:
            file_path = os.path.join(input_folder, file_name)
            image = Image.open(file_path)
            images.append(image)

        # Сохранить изображения в один TIFF файл на одной странице
        if images:
            # Размеры страницы A4 в пикселях
            page_width, page_height = PAGE_SIZE

            # Количество изображений
            num_images = len(images)

            # Определение количества строк и столбцов
            rows, cols = determine_rows_and_columns(num_images)

            # Масштабирование изображений
            scaled_images = scale_images(
                images,
                PAGE_SIZE[0],
                PAGE_SIZE[1],
                MIN_MARGIN_LR,
                MIN_MARGIN_TB,
                MARGIN_BETWEEN,
            )

            # Создать новое изображение с белым фоном
            new_image = Image.new(
                "RGB", (page_width, page_height), (255, 255, 255)
            )

            # Вычислить отступы и их значения
            left_margin, _, top_margin, _ = calculate_margins(
                scaled_images,
                cols,
                rows,
                page_width,
                page_height,
                MARGIN_BETWEEN,
            )

            # Вставить изображения в новое изображение
            insert_images_into_new_image(
                new_image,
                scaled_images,
                cols,
                rows,
                left_margin,
                top_margin,
                MARGIN_BETWEEN,
            )

            # Сохранить новое изображение в TIFF файл с уникальным именем
            output_file = f"Result{i}.tiff"
            new_image.save(output_file, compression="tiff_deflate")


if __name__ == "__main__":
    input_folders = [
        "C:/Dev/mycego/test_db/1369_12_Наклейки 3-D_3",
        "C:/Dev/mycego/test_db/1388_2_Наклейки 3-D_1",
        "C:/Dev/mycego/test_db/1388_6_Наклейки 3-D_2",
        "C:/Dev/mycego/test_db/1388_12_Наклейки 3-D_3",
    ]

    collect_png_to_tiff(input_folders)
