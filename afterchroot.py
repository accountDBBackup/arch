from commands import CommandExecuter
import os
import fileinput
import pwd


def is_uefi() -> bool:
    return os.path.isdir('/sys/firmware/efi')


def install_packages():
    CommandExecuter(
        "pacman --noconfirm --needed -S grub dhcpcd iwd iw neovim intel-ucode sudo networkmanager efibootmgr dosfstools os-prober mtools")


def set_time_zone():
    continents = [
        "Africa",
        "America",
        "Antarctica",
        "Arctic",
        "Asia",
        "Atlantic",
        "Australia",
        "Europe"
    ]

    while not ((continent := input("Please enter a valid continent name: ")) in continents):
        pass

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

    zone_info = f"/usr/share/zoneinfo/{continent}/{city}"
    CommandExecuter(f"ln -sf {zone_info} /etc/localtime")
    CommandExecuter("hwclock --systohc")


def set_locals():
    print("Uncommenting `en_US.UTF-8 UTF-8` line at `/etc/locale.gen`.")
    with fileinput.input("/etc/locale.gen", inplace=True) as f:
        for line in f:
            new_line = line.replace("#en_US.UTF-8 UTF-8", "en_US.UTF-8 UTF-8")
            print(new_line, end="")
    CommandExecuter("locale-gen")
    print("Creating `/etc/locale.conf` file to set locals...")
    with open("/etc/locale.conf", "w+") as local_file:
        local_file.write("LANG=en_US.UTF-8")


def configure_network():
    myhostname = input("Enter a hostname: ")
    print("Creating `/etc/hostname` file...")
    with open("/etc/hostname", "w+") as hostname:
        hostname.write(myhostname)

    print("Editing the `/etc/hosts` file...")
    with open("/etc/hosts", "w+") as hosts:
        hosts.write(
            f"127.0.0.1\tlocalhost\n::1\t\tlocalhost\n127.0.1.1\t{myhostname}.localdomain {myhostname}")


def check_password_is_set(user: str) -> bool:
    stdout = CommandExecuter(
        f"passwd --status {user}").stdout.split(" ")
    return stdout[1] == "P"


def check_user_exists(user: str) -> bool:
    try:
        pwd.getpwnam(user)
    except KeyError:
        return False

    return True


def create_user(user: str):
    if check_user_exists(user):
        if check_password_is_set(user):
            pass
        else:
            CommandExecuter(f"passwd {user}")

    else:
        print(f"Creating user {user}...")
        CommandExecuter(f"useradd -m {user}")
        CommandExecuter(f"passwd {user}")


def user_operations():
    if not check_password_is_set("root"):
        print("Select a root password!")
        CommandExecuter("passwd")
    new_user = input("Please enter name for the new user: ")
    create_user(new_user)
    print(f"Setting the group permissions for the user `{new_user}`...")
    CommandExecuter(
        f"usermod -aG wheel,audio,storage,optical,video {new_user}")


def edit_sudoers():
    print("Editing sudoers file...")
    with fileinput.input("/etc/sudoers", inplace=True) as f:
        for line in f:
            new_line = line.replace(
                "# %wheel ALL=(ALL) ALL", "%wheel ALL=(ALL) ALL")
            print(new_line, end="")


def install_bootloader():
	if is_uefi():
		CommandExecuter(
			"grub-install --target=x86_64-efi --bootloader-id=grub_uefi --recheck")
	else:
		CommandExecuter("grub-install /dev/sda")

    print("Creating grub config file...")
    CommandExecuter("grub-mkconfig -o /boot/grub/grub.cfg")


def finish():
    print("Starting NetworkManager service...")
    CommandExecuter("systemctl enable --now NetworkManager")
    CommandExecuter("exit")


def main():
    install_packages()
    set_time_zone()
    set_locals()
    configure_network()
    user_operations()
    install_bootloader()
    finish()
