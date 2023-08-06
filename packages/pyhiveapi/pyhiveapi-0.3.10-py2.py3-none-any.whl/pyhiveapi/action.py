"""Hive Action Module."""


class Action:
    """Hive Action Code."""

    actionType = "Actions"

    def __init__(self, session=None):
        """Initialise Action."""
        self.session = session

    def getAction(self, device):
        """Get smart plug current power usage."""
        dev_data = {}

        if device["hiveID"] in self.data["action"]:
            dev_data = {
                "hiveID": device["hiveID"],
                "hiveName": device["hiveName"],
                "hiveType": device["hiveType"],
                "haName": device["haName"],
                "haType": device["haType"],
                "status": {"state": self.getState(device)},
                "power_usage": None,
                "deviceData": {},
                "custom": device.get("custom", None),
            }

            self.session.devices.update({device["hiveID"]: dev_data})
            return self.session.devices[device["hiveID"]]
        else:
            exists = self.session.data.actions.get("hiveID", False)
            if exists is False:
                return "REMOVE"
            return device

    def getState(self, device):
        """Get action state."""
        final = None

        try:
            data = self.session.data.actions[device["hiveID"]]
            final = data["enabled"]
        except KeyError as e:
            self.session.log.error(e)

        return final

    def turnOn(self, device):
        """Set action turn on."""
        import json

        final = False

        if device["hiveID"] in self.session.data.actions:
            self.session.hiveRefreshTokens()
            data = self.session.data.actions[device["hiveID"]]
            data.update({"enabled": True})
            send = json.dumps(data)
            resp = self.session.api.setAction(device["hiveID"], send)
            if resp["original"] == 200:
                final = True
                self.session.getDevices(device["hiveID"])

        return final

    def turnOff(self, device):
        """Set action to turn off."""
        import json

        final = False

        if device["hiveID"] in self.session.data.actions:
            self.session.hiveRefreshTokens()
            data = self.session.data.actions[device["hiveID"]]
            data.update({"enabled": False})
            send = json.dumps(data)
            resp = self.session.api.setAction(device["hiveID"], send)
            if resp["original"] == 200:
                final = True
                self.session.getDevices(device["hiveID"])

        return final
