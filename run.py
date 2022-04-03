from app import Config, create_app

if __name__ == "__main__":
    config = Config()
    app = create_app(config)
    app.run(config.host, config.port, debug=config.debug)
