from time import strftime


def get_card():
    return "<h1>Test card</h1>Server time at the time of test card generation:<br>{0}".format(strftime("%Y-%m-%d %H:%M:%S"))
