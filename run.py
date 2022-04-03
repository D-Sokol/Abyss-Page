from app import Config, create_app

config = Config()
app = create_app(config)

if __name__ == "__main__":
    app.run(config.HOST, config.PORT, debug=config.DEBUG)
