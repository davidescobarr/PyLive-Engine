import os
import subprocess
import sys
from core.Settings import Settings
from core.StartGame import StartGame


def compile_with_pyinstaller(settings: Settings):
    # Проверка основного скрипта
    main_script_path = sys.modules[StartGame().__class__.__module__].__file__
    if not os.path.exists(main_script_path):
        return f"Main script not found: {main_script_path}"

    # Директории, которые нужно включить
    directories_to_include = [
        settings.folder
    ]

    data_files = []

    for folder in directories_to_include:
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder):
                for file in files:
                    full_path = os.path.join(root, file)

                    # Предполагается, что base_path - это корневой каталог проекта
                    base_path = settings.folder
                    relative_path = os.path.relpath(full_path, start=base_path)

                    target_folder = os.path.join('files', os.path.dirname(relative_path))
                    data_files.append(f'--add-data={base_path + "/" + relative_path};{target_folder}')
        else:
            return f"Warning: Directory {folder} does not exist and will be skipped."

    # Сборка команды для PyInstaller
    compile_command = [sys.executable, '-m', 'PyInstaller',
                       '--onefile', "-w", main_script_path] + data_files

    try:
        # Запуск PyInstaller
        subprocess.run(compile_command, check=True)
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}\nOutput: {e.output}\nError Output: {e.stderr}"

    return "0"