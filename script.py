from os import system

NOTES_URL = "https://github.com/HicaroD/Notes"
DOTFILES_URL = "https://github.com/HicaroD/dotfiles-neovim"


class Builder():
    @staticmethod
    def install_package(package_name: str):
        system(f"sudo pacman -S {package_name}")

    @staticmethod
    def update_system():
        system("sudo pacman -Syu")

    @staticmethod
    def install_base_packages():
        packages = ["git", "python", "zsh", "neovim"]
        for package in packages:
            Builder.install_package(package)

        # Oh My Zsh
        system("sh -c \"$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)\"")

    @staticmethod
    def run():
        Builder.update_system()
        Builder.install_base_packages()

def main():
    Builder.run()


if __name__ == "__main__":
    main()
