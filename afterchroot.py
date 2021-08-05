from commands import CommandExecuter
import os
import fileinput
import pwd
from getpass import getpass


def is_uefi() -> bool:
    return os.path.isdir('/sys/firmware/efi')


def install_packages() -> None:
    packages = [
        "grub"
        "dhcpcd"
        "iwd"
        "iw"
        "neovim"
        "intel-ucode"
        "sudo"
        "networkmanager"
        "efibootmgr"
        "dosfstools"
        "os-prober"
        "mtools"
    ]

    CommandExecuter(
        f"pacman --noconfirm --needed -S {' '.join(packages)}")


def set_default_timezone():
    CommandExecuter(
        "ln -sf /usr/share/zoneinfo/Europe/Istanbul /etc/localtime")
    CommandExecuter("hwclock --systohc")


def set_timezone() -> None:

    continents = [
        "Africa",
        "America",
        "Antarctica",
        "Arctic",
        "Asia",
        "Atlantic",
        "Australia",
        "Europe",
        ""
    ]

    while not ((continent := input("Please enter a valid continent name(Enter for default values): ")) in continents):
        pass

    if not continent:
        set_default_timezone()
        return

    cities = os.listdir(f"/usr/share/zoneinfo/{continent}")

    print(f"Available cities in the {continent}:")
    for i, c in enumerate(cities):
        if i % 5 == 4 and i != 0:
            print(c)
        else:
            print(c.ljust(10, " "), end="\t")

    print()
    while not((city := input("Please enter a valid city name: ")) in cities):
        pass

    zoneinfo = f"/usr/share/zoneinfo/{continent}/{city}"
    CommandExecuter(f"ln -sf {zoneinfo} /etc/localtime")
    CommandExecuter("hwclock --systohc")


def set_locals() -> None:
    print("Uncommenting `en_US.UTF-8 UTF-8` line at `/etc/locale.gen`.")
    with fileinput.input("/etc/locale.gen", inplace=True) as f:
        for line in f:
            new_line = line.replace("#en_US.UTF-8 UTF-8", "en_US.UTF-8 UTF-8")
            print(new_line, end="")
    CommandExecuter("locale-gen")
    print("Creating `/etc/locale.conf` file to set locals...")
    with open("/etc/locale.conf", "w+") as local_file:
        local_file.write("LANG=en_US.UTF-8")


def configure_network() -> None:
    hostname = input("Enter a hostname: ")
    print("Creating `/etc/hostname` file...")
    with open("/etc/hostname", "w+") as hostname_file:
        hostname_file.write(hostname)

    print("Editing the `/etc/hosts` file...")
    with open("/etc/hosts", "w+") as hosts_file:
        hosts_file.write(
            f"127.0.0.1\tlocalhost\n::1\t\tlocalhost\n127.0.1.1\t{hostname}.localdomain {hostname}")


def install_bootloader() -> None:
    if is_uefi():
        opts = "--target=x86_64-efi --bootloader-id=grub_uefi --recheck"
    else:
        opts = "/dev/sda"

    CommandExecuter(f"grub-install {opts}")
    print("Creating grub config file...")
    CommandExecuter("grub-mkconfig -o /boot/grub/grub.cfg")


def finish() -> None:
    print("Starting NetworkManager service...")
    CommandExecuter("systemctl enable --now NetworkManager")
    CommandExecuter("exit")


def main() -> None:
    install_packages()
    set_timezone()
    set_locals()
    configure_network()
    user_operations()
    install_bootloader()
    finish()
