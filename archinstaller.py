import os
import subprocess
import fileinput
import pwd
import afterchroot

def welcome():
    print("Welcome to to the Arch Installer!")
    system_clock_sync = "timedatectl set-ntp true"
    print(f"Running `{system_clock_sync}` command to sync the system clock!")
    subprocess.run(system_clock_sync, shell=True)


def format_disks():
    pass


def mount_partitions():
    pass


def update_mirrors():
    print("Refreshing mirrorlist...")
    subprocess.run(
        "reflector --latest 30 --sort rate --save /etc/pacman.d/mirrorlist", shell=True)


def install_arch_essentails():
    kernels = ["linux", "linux-lts", "linux linux-lts"]
    while not ((choice :=
                input("\t(1) linux\n\t(2) linux-lts\n\t(3) both\nChose a kernel: ")) in [1, 2, 3]):
        pass

    choice = int(choice)
    print(f"Installing: {kernels[choice-1].replace(' ', ' and ')}")
    subprocess.run(
        f"pacstrap /mnt base {kernels[choice -1]} linux-firmware", shell=True)


def generate_fstab():
    subprocess.run("genfstab -U /mnt >> /mnt/etc/fstab", shell=True)


def chroot():
    subprocess.run("arch-chroot /mnt /bin/bash", shell=True)

def main():
	afterchroot.main()
    


if __name__ == "__main__":
    main()
