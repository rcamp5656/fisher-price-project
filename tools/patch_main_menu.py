
# patch_main_menu.py

def add_play_live_button(make_nav, switch_screen_callback):
    """
    Appends a 'Play Live' button to a navigation row.
    Use this inside your main screen's navigation logic.
    """
    nav = [
        ('Prev', lambda *_: switch_screen_callback('prev')),
        ('Next', lambda *_: switch_screen_callback('next')),
        ('Play', lambda *_: switch_screen_callback('play')),
        ('Pause', lambda *_: switch_screen_callback('pause')),
        ('Stop', lambda *_: switch_screen_callback('stop')),
        ('Show Converted', lambda *_: switch_screen_callback('converted')),
        ('Play Live', lambda *_: switch_screen_callback('play_live')),
        ('Live Input', lambda *_: switch_screen_callback('live')),
        ('Exit', lambda *_: switch_screen_callback('exit')),
    ]
    return make_nav(nav)
