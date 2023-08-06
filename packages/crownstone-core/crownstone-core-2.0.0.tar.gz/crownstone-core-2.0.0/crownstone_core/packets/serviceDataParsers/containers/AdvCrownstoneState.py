from crownstone_core.packets.serviceDataParsers.containers.elements.AdvTypes import AdvType


class AdvCrownstoneState:
    def __init__(self):
        self.type = AdvType.CROWNSTONE_STATE

        self.crownstoneId              = None
        self.switchState               = None
        self.flags                     = None
        self.globalFlags               = None
        self.temperature               = None
        self.powerFactor               = None
        self.powerUsageReal            = None
        self.powerUsageApparent        = None
        self.accumulatedEnergy         = None
        self.timestamp                 = None
        self.uniqueIdentifier          = None
        self.validation                = None

    def __str__(self):
        return f"{self.type}\n"\
           f"crownstoneId:         {self.crownstoneId      }\n" \
           f"switchState:          {self.switchState       }\n" \
           f"flags:                {self.flags             }\n" \
           f"globalFlags:          {self.globalFlags       }\n" \
           f"temperature:          {self.temperature       }\n" \
           f"powerFactor:          {self.powerFactor       }\n" \
           f"powerUsageReal:       {self.powerUsageReal    }\n" \
           f"powerUsageApparent:   {self.powerUsageApparent}\n" \
           f"accumulatedEnergy:    {self.accumulatedEnergy }\n" \
           f"timestamp:            {self.timestamp         }\n" \
           f"uniqueIdentifier:     {self.uniqueIdentifier  }\n" \
           f"validation:           {self.validation        }\n"