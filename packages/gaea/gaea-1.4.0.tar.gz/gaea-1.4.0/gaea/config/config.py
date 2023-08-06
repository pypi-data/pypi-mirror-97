from dynaconf import Dynaconf

CONFIG = Dynaconf(
    envvar_prefix="AKB",
    settings_files=["config.yaml"],
    env_switcher="ENV",
    core_loaders=["YAML"],
    environments=True,
)
