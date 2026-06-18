from libs import *
from plyer import notification as notify


def notificate(title: str, text: str) -> None:
    notify.notify(
        title=title,
        message=text,
        app_name="JoblessSimulator",
        app_icon="icon/catho.ico",
        timeout=3,
    )


def notificate_and_wait(title: str, text: str) -> None:
    notify.notify(
        title=title,
        message=text,
        app_name="JoblessSimulator",
        app_icon="icon/catho.ico",
    )

    print("Pressione Enter para continuar...")
    input()