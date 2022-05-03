import os
import tarfile
import shutil
import requests
from os import system

NOTES_URL = "https://github.com/HicaroD/Notes"
DOTFILES_URL = "https://github.com/HicaroD/dotfiles"
HOME_PATH = os.path.expanduser("~")


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
        local_filename = url.split("/")[-1]
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename

    @staticmethod
    def install_golang():
        go_tarfile_name = "go1.18.linux-amd64.tar.gz"
        go_directory = "/usr/local/go"
        go_url = "https://go.dev/dl/go1.18.linux-amd64.tar.gz"

        if not os.path.exists(go_tarfile_name):
            print(f"Downloading Go from {go_url}")
            Builder.download_file(go_url)

        if os.path.exists(go_directory):
            print("Removing existent /usr/local/go folder")
            shutil.rmtree(go_directory)

        if os.path.exists(go_tarfile_name):
            print("Extracting Go tarball on /usr/local")
            go_tarfile = tarfile.open(go_tarfile_name, "r|*")
            go_tarfile.extractall(path="/usr/local")
            go_tarfile.close()
            os.remove(go_tarfile_name)
        else:
            print("Go tarball not found.")
            exit()

    @staticmethod
    def install_rust():
        system("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")

    @staticmethod
    def configure_git():
        print("Configuring Git")
        email = input("Enter e-mail: ")
        system(f'git config --global user.email "{email}"')

        username = input("Enter username: ")
        system(f'git config --global user.name "{username}"')

        system(f'git config --global core.editor "neovim"')
        system(f'git config --global commit.verbose true')

    @staticmethod
    def configure_neovim():
        print("Configuring Neovim")

        system(f"git clone {DOTFILES_URL}")

        neovim_dotfiles_path = "dotfiles/init.vim"
        neovim_folder_configuration = os.path.expanduser("~") + "/.config/nvim"

        if os.path.exists(neovim_dotfiles_path):
            if not os.path.exists(neovim_folder_configuration):
                print("Creating Neovim folder")
                os.mkdir(neovim_folder_configuration)

            os.rename(neovim_dotfiles_path, neovim_folder_configuration + "init.vim")
            shutil.rmtree("dotfiles")

        else:
            print("dotfiles folder not found")
            exit()

    @staticmethod
    def configure_neovim_plugins():
        # Vim-plug
        system("sh -c 'curl -fLo \"${XDG_DATA_HOME:-$HOME/.local/share}\"/nvim/site/autoload/plug.vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'")

    @staticmethod
    def get_personal_notes():
        print("Downloading personal notes")
        system(f"git clone {NOTES_URL} " + + "/Documents/Notes")

    @staticmethod
    def append_aliases_to_zshrc():
        zshrc_file_path = HOME_PATH + "/.zshrc"
        if os.path.exists(zshrc_file_path):
            print("Appending aliases to .zshrc")
            with open(zshrc_file_path, "a") as zshrc_file:
                zshrc_file.write("alias notes=\"nvim ~/Documents/Notes/\"\n")
                zshrc_file.write("alias vimrc=\"nvim ~/.config/nvim/init.vim\"")
        else:
            print(".zshrc doesn't exist!")
            exit()

    @staticmethod
    def run():
        Builder.update_system()
        Builder.install_base_packages()
        Builder.install_golang()
        Builder.install_rust()
        Builder.configure_git()
        Builder.configure_neovim()
        Builder.configure_neovim_plugins()
        Builder.get_personal_notes()
        Builder.append_aliases_to_zshrc()


def main():
    Builder.run()


if __name__ == "__main__":
    main()
