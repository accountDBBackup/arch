from commands import CommandExecuter
import os
import fileinput
from getpass import getpass


def check_password_is_set(username: str) -> bool:
    return CommandExecuter(
        f"passwd --status {username}").result.split(" ")[1] == "P"


def check_user_exists(username: str) -> bool:
    return not CommandExecuter(f"id -u {username}").is_stderr()


def create_user(username: str) -> None:
    if check_user_exists(username):
        if not check_password_is_set(username):
            password = verify_passwor()
            CommandExecuter(f"usermod --password {password} {username}")
    else:
        print(f"Creating user {username}...")
        add_user_with_password(username)


def verify_password() -> str:
    while password := getpass(prompt="Enter your password: "):
        password_verification = getpass(
            prompt="Enter your password one more time: ")
        if password == password_verification:
            return password

        print("Password verification failed!")
        continue


def add_user_with_password(username: str, password: str = verify_password()):
    CommandExecuter(f"useradd -m {username} -p {password}")


def set_user_groups(username: str):
    print(f"Setting the group permissions for the user `{username}`...")
    CommandExecuter(
        f"usermod -aG wheel,audio,storage,optical,video {username}")


def set_root_password(password: str = verify_password()) -> None:
    CommandExecuter(f"echo {password} | passwd root")


def user_operations() -> None:
    if not check_password_is_set("root"):
        set_root_password()
    username = input("Please enter name for the new user: ")
    create_user(username)
    set_user_groups(username)


def edit_sudoers() -> None:
    print("Editing sudoers file...")
    with fileinput.input("/etc/sudoers", inplace=True) as f:
        for line in f:
            new_line = line.replace(
                "# %wheel ALL=(ALL) ALL", "%wheel ALL=(ALL) ALL")
            print(new_line, end="")
