
class AvailabilityZone:
    def __init__(self, zone_name, price_history):
        self.zone_name = zone_name
        self.price_history = price_history

    @property
    def current_price(self):
        if self.price_history:
            return float(self.price_history[0]['SpotPrice'])
        else:
            return None

    def __repr__(self):
        price = str(self.current_price)
        zone_name = self.zone_name
        return "%s for $%s/hr" % (zone_name, price)
