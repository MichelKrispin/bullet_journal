class EscapeCode:
    def __init__(self, enter_code: str = "", exit_code: str = "") -> None:
        self.enter_code = f"\x1b{enter_code}"
        self.exit_code = f"\x1b{exit_code}"

    def __call__(self, msg: str) -> None:
        print(msg, end="")

    def __enter__(self):
        print(self.enter_code, end="")
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        print(self.exit_code, end="")


class Strikethrough(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[9m", "[29m")


class Bold(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[1m", "[22m")


class Dim(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[2m", "[22m")


class Italic(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[3m", "[23m")


class Underline(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[4m", "[24m")


class Black(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[30m", "[39m")


class Red(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[31m", "[39m")


class Green(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[32m", "[39m")


class Yellow(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[33m", "[39m")


class Blue(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[34m", "[39m")


class Magenta(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[35m", "[39m")


class Cyan(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[36m", "[39m")


class White(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[37m", "[39m")


class RedBackground(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[41m", "[49m")


class BlackBackground(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[40m", "[49m")


class RedBackground(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[41m", "[49m")


class GreenBackground(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[42m", "[49m")


class YellowBackground(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[43m", "[49m")


class BlueBackground(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[44m", "[49m")


class MagentaBackground(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[45m", "[49m")


class CyanBackground(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[46m", "[49m")


class WhiteBackground(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[47m", "[49m")


class DefaultBackground(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[49m", "[49m")


class BrightBlack(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[90m", "[39m")


class BrightRed(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[91m", "[39m")


class BrightGreen(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[92m", "[39m")


class BrightYellow(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[93m", "[39m")


class BrightBlue(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[94m", "[39m")


class BrightMagenta(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[95m", "[39m")


class BrightCyan(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[96m", "[39m")


class BrightWhite(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[97m", "[39m")


class BrightBlackBackground(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[100m", "[49m")


class BrightRedBackground(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[101m", "[49m")


class BrightGreenBackground(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[102m", "[49m")


class BrightYellowBackground(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[103m", "[49m")


class BrightBlueBackground(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[104m", "[49m")


class BrightMagentaBackground(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[105m", "[49m")


class BrightCyanBackground(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[106m", "[49m")


class BrightWhiteBackground(EscapeCode):
    def __init__(self) -> None:
        super().__init__("[107m", "[49m")


if __name__ == "__main__":
    # Test
    if False:
        with Strikethrough() as p:
            p("Hello")
        with BrightMagenta() as p:
            p(" you")
        with BlueBackground() as p:
            p("!!!")
        print("\nHello")
        with Bold() as p:
            p("Hello\n")
        with Italic(), Underline(), Strikethrough(), Bold(), Red():
            print("Hello")
        print("Hello")
        with RedBackground() as p:
            p("Hello")
        print("")

    # Migration
    if False:
        with Bold() as p:
            p("Migration")
        print(" of ", end="")
        with Underline() as p:
            p(f"{5}")
        print(" unfinished tasks.")

        # Migration request
        priority = 0
        title = "Read something nice"
        state = "due"
        date = "15.06.24"
        with Bold() as p:
            p("Migrate ")
        if priority > 0:
            with BrightRed() as p:
                p(f"[{priority}]")
        print(f"[{priority}]", end="")
        with Italic() as p:
            p(f" {title}")
        print(f" from {date}? [y/n] ", end="")
        answer = input("")
        with BrightRedBackground() as p:
            p('For yes type "y", for no type "n"')
        print("")

    # Showing tasks of today
    records = [
        [2, "Task 1", "due", "16.06.24", 12],
        [4, "Another task", "ignored", "16.06.24", 13],
        [0, "Yet another task", "done", "16.06.24", 10],
        [0, "Final task", "migrated", "16.06.24", 11],
    ]

    def print_line(priority, title, date, task_id):
        if priority > 0:
            with BrightRed() as p:
                p(f"({priority:2d})")
        else:
            print("    ", end="")
        print(" ", end="")
        with Italic() as p:
            p(f"{title:30}")
        print(f" from {date} ", end="")
        with BrightBlack():
            print(f"[id={task_id}]")

    for row in records:
        task_id = row[4]
        title = row[1]
        priority = row[0]
        state = row[2]
        date = row[3]
        if state == "done":
            with Bold(), Green() as p:
                p("[x] ")
                print_line(priority, title, date, task_id)
        elif state == "due":
            with Bold() as p:
                p("[ ] ")
            print_line(priority, title, date, task_id)
        elif state == "migrated":
            with Dim() as p:
                p("[>] ")
                print_line(priority, title, date, task_id)
        elif state == "ignored":
            with Strikethrough() as p:
                p("[ ] ")
                print_line(priority, title, date, task_id)
