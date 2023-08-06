class Topics:
    
    advertisement = "advertisement" # data is dictionary {
    #  name: string
    #  rssi: int
    #  address: string   # mac address
    #  serviceUUID: string
    #  serviceData: {
    #    opCode:                       int
    #    dataType:                     int
    #    stateOfExternalCrownstone:    int    # adv contains state of external crownstone
    #    hasError:                     bool   # this crownstone has an error
    #    setupMode:                    bool   # is in setup mode
    #    id:                           int    # crownstone id (0-255)
    #    switchState:                  int    # raw switch state (uint8)
    #    flagsBitmask:                 int
    #    temperature:                  int    # chip temp
    #    powerFactor:                  int    # factor between real and apparent
    #    powerUsageReal:               int    # usage in watts (W)
    #    powerUsageApparent:           int    # usage in VA
    #    accumulatedEnergy:            int
    #    timestamp:                    int    # time on Crownstone seconds since epoch with locale correction
    #    dimmerReady:                  bool   # dimming is available for use (it is not in the first 60 seconds after boot)
    #    dimmingAllowed:               bool   # this Crownstone can dim
    #    switchLocked:                 bool   # this Crownstone is switch-locked
    #    errorMode:                    bool   # advertisement type errorMode : the errors JSON is valid. This alternates with normal advertisements
    #    errors: {
    #        overCurrent:              bool
    #        overCurrentDimmer:        bool
    #        temperatureChip:          bool
    #        temperatureDimmer:        bool
    #        dimmerOnFailure:          bool
    #        dimmerOffFailure:         bool
    #        bitMask:                  int
    #    }
    #    uniqueElement:                int    # something that identifies this advertisement uniquely. Can be used to skip duplicate payloads
    #    timeIsSet:                    bool   # this crownstone knows what time it is
    #  }

    newDataAvailable = "newDataAvailable"  # data is dictionary {
    #   id:                           int    # crownstone id (0-255)
    #   setupMode:                    bool   # is in setup mode
    #   switchState:                  int    # raw switch state (uint8)
    #   temperature:                  int    # chip temp in Celcius
    #   powerFactor:                  int    # factor between real and apparent
    #   powerUsageReal:               int    # power usage in watts (W)
    #   powerUsageApparent:           int    # power usage in VA
    #   accumulatedEnergy:            int
    #   timestamp:                    int    # time on Crownstone seconds since epoch with locale correction
    #   dimmerReady:                  bool   # dimming is available for use (it is not in the first 60 seconds after boot)
    #   dimmingAllowed:               bool   # this Crownstone can dim
    #   switchLocked:                 bool   # this Crownstone is switch-locked
    #   hasError:                     bool   # this crownstone has an error, if the crownstone has an error, the errors: {} dict is only valid if errorMode: true. This boolean is always valid.
    #   errorMode:                    bool   # summary type errorMode : the errors JSON is valid. This alternates with normal advertisements
    #   errors: {
    #       overCurrent:              bool
    #       overCurrentDimmer:        bool
    #       temperatureChip:          bool
    #       temperatureDimmer:        bool
    #       dimmerOnFailure:          bool
    #       dimmerOffFailure:         bool
    #       bitMask:                  int
    #   }
    #   timeIsSet:                    bool   # this crownstone knows what time it is
    # }

