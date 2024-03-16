import threading

from interface.run_interface import run_interface


def main():
    interface_thread = threading.Thread(target=run_interface)
    interface_thread.start()


if __name__ == "__main__":
    main()
