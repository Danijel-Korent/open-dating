from app import app, socketio, add_cmdline_options


def main():
    socketio.run(app, port=8080, debug=True)


if __name__ == "__main__":
    main()
