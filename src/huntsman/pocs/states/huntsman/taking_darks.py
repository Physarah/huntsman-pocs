def on_enter(event_data):

    pocs = event_data.model
    pocs.next_state = 'starting'

    # Take bias frames
    pocs.say("Taking bias frames.")
    pocs.observatory.take_dark_observation(bias=True)

    # Take dark frames
    pocs.say("Taking dark frames.")
    pocs.observatory.take_dark_observation()
