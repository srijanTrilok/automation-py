from ..modals.tsv.intelliChat import intelliChat


def intent_process(event):
    slots = event["currentIntent"]["slots"]
    msg = "Sorry no record found!"

    if slots['downup'] is not None and slots['country'] is not None:
        downup_slot = slots['downup'].lower()
        country = slots['country'].lower()

        downup = intelliChat(country=country)

        if downup_slot == 'downgrade':
            machines = downup.machineToDowngrade()

        if downup_slot == 'upgrade':
            machines = downup.machineToUpgrade()
        msg = "%s machines can be %s in %s" % (machines, downup_slot, country)

    return msg