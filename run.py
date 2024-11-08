from opendating import create_app, socketio, add_cmdline_options

def main():
    app = create_app()
    socketio.run(app, port=8080)

if __name__ == "__main__":
    main()
