class Status:
    def __init__(self, data):
        self.online: bool = data.get("online")
        self.players: StatusPlayers = StatusPlayers(data)


class StatusPlayers:
    def __init__(self, data):
        self.online: int = data.get("onlinePlayers", 0)
        self.max: int = data.get("maxPlayers", 0)


class Player:
    def __init__(self, data):
        self.uuid: str = data.get("uuid")
        self.username = self.name = data.get("username")
        self.town: int = data.get("town")
        self.nation: int = data.get("nation")
        self.tokens: int = data.get("tokens", 0)
        self.role: str = data.get("role", None)
        self.paid: bool = data.get("paid", False)
        self.deaths: int = data.get("deaths", 0)
        self.kills: int = data.get("kills", 0)
        self.chunks_travelled: int = data.get("chunks_travelled", 0)
        self.discord: int = data.get("discord")


class Nation:
    def __init__(self, data):
        self.id: int = data.get("id")
        self.name: str = data.get("name")
        self.longname: str = data.get("longname")
        self.formatted: str = f"{self.longname} ({self.name})" if bool(self.longname) else self.name
        self.bank: int = data.get("bank")
        self.ideology: str = data.get("ideology")
        self.color: int = int(data.get("color", "000000"), 16) if data.get("color") else None
        self.founded: str = data.get("founded")
        self.joinable: bool = bool(data.get("joinable"))
        self.pollexpiry: int = data.get("pollexpiry")
        self.webhook: str = data.get("webhook")
        self.proto: bool = data.get("proto")
        self.members: list = [NationMember(member) for member in data.get("members")]


class NationMember:
    def __init__(self, data):
        self.uuid = data.get("uuid")
        self.username = self.name = data.get("username")


class Town:
    def __init__(self, data):
        self.id: int = data.get("id")
        self.name: str = data.get("name")
        self.bank: int = data.get("int")
        self.mayor: str = data.get("mayor")
        self.nation: int = data.get("nation")
        self.province: bool = data.get("province")
        self.permissions: TownPermissions = TownPermissions(data.get("permissions"))


class TownPermissions:
    def __init__(self, data):
        self.build: str = data.get("build")
        self.break_blocks: str = data.get("break")  # python keywords go brr
        self.switch: str = data.get("switch")
        self.purchasable: str = data.get("purchasable")
        self.grace: str = data.get("grace")
