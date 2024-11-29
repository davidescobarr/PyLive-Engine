# installer.py

import subprocess
import sys


def install_package(package_name):
    """Устанавливает пакет через pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"Установка {package_name} завершена успешно.")
    except subprocess.CalledProcessError:
        print(f"Ошибка при установке {package_name}.")


def main():
    """Главная функция для установки пакетов."""
    packages = ["pyside6", "pygame", "pyinstaller"]
    for package in packages:
        install_package(package)


if __name__ == "__main__":
    main()
