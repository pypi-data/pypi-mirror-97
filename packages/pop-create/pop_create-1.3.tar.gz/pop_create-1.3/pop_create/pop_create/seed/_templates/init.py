def __init__(hub):
    # Remember not to start your app in the __init__ function
    # This function should just be used to set up the plugin subsystem
    # Add another function to call from your run.py to start the app
    for dyne in [R__DYNES__]:
        hub.pop.sub.add(dyne_name=dyne)


def cli(hub):
    hub.pop.config.load(["R__CLEAN_NAME__", R__DYNES__], cli="R__CLEAN_NAME__")
    # Your app's options can now be found under hub.OPT.R__NAME__
    print("R__NAME__ works!")
