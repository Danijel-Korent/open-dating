from app import create_app, socketio, add_cmdline_options

app = create_app()


def main():
    socketio.run(app, port=8080)


if __name__ == "__main__":
    main()
