import threading

from interface.run_interface import run_interface


def main():
    interface_thread = threading.Thread(target=run_interface)
    interface_thread.start()

    # from database.database_crud import create_database
    # create_database()


if __name__ == "__main__":
    main()
