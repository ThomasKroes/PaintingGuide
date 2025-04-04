class DebugPrintMixin:
    def __init__(self, *args, **kwargs):
        self.verbose = True  # or False to disable output
        super().__init__(*args, **kwargs)

        self.print_index = -1

    def set_print_index(self, print_index : int):
        """Set print index."""

        self.print_index = print_index

    def print(self, message: str):
        if self.verbose:
            if self.print_index >= 0:
                print(f"[{self.__class__.__name__} { self.print_index }] {message}")
            else:
                print(f"[{self.__class__.__name__}] {message}")