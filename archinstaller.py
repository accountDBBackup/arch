import os
import subprocess
import fileinput


def welcome():
    print("Welcome to to the Arch Installer!")
    system_clock_sync = "timedatectl set-ntp true"
    print(f"Running `{system_clock_sync}` command to sync the system clock!")
    subprocess.run(system_clock_sync, shell=True)


def format_disks():
    pass


def mount_partitions():
    pass


def install_arch_essentails():
    kernels = ["linux", "linux-lts", "linux linux-lts"]
    choice = int(
        input("Chose a kernel:\n (1) linux\n(2) linux-lts\n(3) both")) - 1
    print(f"Installing: {kernels[choice].replace(' ', ' and ')}")
    subprocess.run(
        f"pacstrap /mnt base {kernels[choice]} linux-firmware", shell=True)


def generate_fstab():
    subprocess.run("genfstab -U /mnt >> /mnt/etc/fstab", shell=True)


def chroot():
    subprocess.run("arch-chroot /mnt /bin/bash", shell=True)
    subprocess.run(
        "pacman --noconfirm -S grub dhcpcd iwd id neovim intel-ucode sudo networkmanager efibootmgr dosfstools os-prober mtools", shell=True)


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

    print(f"Available cities in {continent}:")
    for i, c in enumerate(cities):
        if i % 5 == 4 and i != 0:
            print(c)
        else:
            print(c.ljust(10, " "), end="\t")

    print()
    while not((city := input("Please enter a valid city name: ")) in cities):
        pass

    zone_info = f"/usr/share/zoneinfo/{continent}/{city}"
    subprocess.run(f"ln -sf {zone_info} /etc/localtime", shell=True)
    subprocess.run("hwclock --systohc", shell=True)


def set_locals():
    print("Uncommenting `en_US.UTF-8 UTF-8` line at `/etc/locale.gen`.")
    with fileinput.input("/etc/locale.gen", inplace=True) as f:
        for line in f:
            new_line = line.replace("#en_US.UTF-8 UTF-8", "en_US.UTF-8 UTF-8")
            print(new_line, end="")
    subprocess.run("locale-gen", shell=True)
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


# def create_user():
# 	print("Select a root password!")
# 	os.system("passwd")
#     new_user = input("Please enter name for the new user: ")
#     print("Creating user {new_user}...")
#     os.system("useradd -m {new_user}")
#     os.system("passwd {new_user}")
#     print("Setting the group permissions for the user `{new_user}`...")
#     os.system("usermod -aG wheel,audio,storage,optical,video {new_user}")

# def install_bootloader():
# 	os.system("grub-install --target=x86_64-efi --bootloader-id=grub_uefi --recheck")
# 	print("Creating grub config file...")
# 	os.system("grub-mkconfig -o /boot/grub/grub.cfg")

# def finish():
# 	print("Starting NetworkManager service...")
# 	os.system("systemctl enable NetworkManager")
# 	os.system("systemctl start NetworkManager")
# 	os.system("exit")
# 	print("Rebooting now..")
# 	os.system("reboot now")

def main():
    # welcome()
    # format_disks()
    # mount_partitions()
    # install_arch_essentails()
    # set_time_zone()
    # set_locals()
    configure_network()


if __name__ == "__main__":
    main()
