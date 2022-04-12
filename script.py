import os
import tarfile
import shutil
import requests
from os import system

NOTES_URL = "https://github.com/HicaroD/Notes"
DOTFILES_URL = "https://github.com/HicaroD/dotfiles-neovim"


class Builder:
    @staticmethod
    def install_package(package_name: str):
        system(f"sudo pacman -S {package_name}")

    @staticmethod
    def update_system():
        system("sudo pacman -Syu")

    @staticmethod
    def install_base_packages():
        packages = ["git", "zsh", "neovim", "curl"]
        for package in packages:
            Builder.install_package(package)

        # Oh My Zsh
        system(
            'sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"'
        )

    @staticmethod
    # Credits: https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests#16696317
    def download_file(url):
        local_filename = url.split('/')[-1]
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename

    @staticmethod
    def install_golang():
        go_tarfile_name = 'go1.18.linux-amd64.tar.gz'
        go_directory = '/usr/local/go'
        go_url = 'https://go.dev/dl/go1.18.linux-amd64.tar.gz'

        print(f"Downloading Go from {go_url}")

        if not os.path.exists(go_tarfile_name):
            Builder.download_file(go_url)

        if os.path.exists(go_directory):
            print("Removing existent /usr/local/go folder")
            shutil.rmtree(go_directory)

        if os.path.exists(go_tarfile_name):
            print("Extracting Go tarball on /usr/local")
            go_tarfile = tarfile.open(go_tarfile_name, 'r|*')
            go_tarfile.extractall(path='/usr/local')
            go_tarfile.close()
            os.remove(go_tarfile_name)
        else:
            print("Go tarball not found.")
            exit()

    @staticmethod
    def run():
        #Builder.update_system()
        #Builder.install_base_packages()
        Builder.install_golang()


def main():
    Builder.run()


if __name__ == "__main__":
    main()
