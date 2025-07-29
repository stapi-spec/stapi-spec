from datetime import datetime


def on_config(config, **kwargs) -> None:
    config.copyright = config.copyright.format(year=datetime.now().year)
