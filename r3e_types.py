from ctypes import LittleEndianStructure, c_int, c_float, Array, wintypes, c_double, c_wchar
from enum import IntEnum


class ShortWord(Array):
    _type_ = wintypes.WORD
    _length_ = 15

    def __str__(self):
        try:
            return bytes(self).decode('utf-16-le').rstrip('\x00')
        except UnicodeDecodeError as e:
            return ""


class Word(Array):
    _type_ = wintypes.WORD
    _length_ = 33

    def __str__(self):
        try:
            return bytes(self).decode('utf-16-le').rstrip('\x00')
        except UnicodeDecodeError as e:
            return ""

class LongWord(Array):
    _type_ = wintypes.WORD
    _length_ = 32

    def __str__(self):
        try:
            return bytes(self).decode('windows-1252').rstrip('\x00')
        except UnicodeDecodeError as e:
            return ""


# https:#gist.github.com/christoph2/9c390e5c094796903097
class StructureWithEnums(LittleEndianStructure):
    """Add missing enum feature to ctypes Structures.
    """
    _map = {}

    def __getattribute__(self, name):
        _map = LittleEndianStructure.__getattribute__(self, '_map')
        value = LittleEndianStructure.__getattribute__(self, name)
        if name in _map:
            EnumClass = _map[name]
            if isinstance(value, Array):
                return [EnumClass(x) for x in value]
            else:
                return EnumClass(value)
        else:
            return value

    def __str__(self):
        result = []
        result.append("struct {0} {{".format(self.__class__.__name__))
        for field in self._fields_:
            attr, attrType = field
            if attr in self._map:
                attrType = self._map[attr]
            value = getattr(self, attr)
            result.append("    {0} [{1}] = {2!r};".format(attr, attrType.__name__, value))
        result.append("};")
        return '\n'.join(result)

    __repr__ = __str__


class ACC_FLAG_TYPE(IntEnum):
    ACC_NO_FLAG = 0
    ACC_BLUE_FLAG = 1
    ACC_YELLOW_FLAG = 2
    ACC_BLACK_FLAG = 3
    ACC_WHITE_FLAG = 4
    ACC_CHECKERED_FLAG = 5
    ACC_PENALTY_FLAG = 6
    ACC_GREEN_FLAG = 7
    ACC_ORANGE_FLAG = 8

class ACC_PENALTY_TYPE(IntEnum):
    ACC_None = 0
    ACC_DriveThrough_Cutting = 1
    ACC_StopAndGo_10_Cutting = 2
    ACC_StopAndGo_20_Cutting = 3
    ACC_StopAndGo_30_Cutting = 4
    ACC_Disqualified_Cutting = 5
    ACC_RemoveBestLaptime_Cutting = 6
    ACC_DriveThrough_PitSpeeding = 7
    ACC_StopAndGo_10_PitSpeeding = 8
    ACC_StopAndGo_20_PitSpeeding = 9
    ACC_StopAndGo_30_PitSpeeding = 10
    ACC_Disqualified_PitSpeeding = 11
    ACC_RemoveBestLaptime_PitSpeeding = 12
    ACC_Disqualified_IgnoredMandatoryPit = 13
    ACC_PostRaceTime = 14
    ACC_Disqualified_Trolling = 15
    ACC_Disqualified_PitEntry = 16
    ACC_Disqualified_PitExit = 17
    ACC_Disqualified_Wrongway = 18
    ACC_DriveThrough_IgnoredDriverStint = 19
    ACC_Disqualified_IgnoredDriverStint = 20
    ACC_Disqualified_ExceededDriverStintLimit = 21

class ACC_SESSION_TYPE(IntEnum):
    ACC_UNKNOWN = -1
    ACC_PRACTICE = 0
    ACC_QUALIFY = 1
    ACC_RACE = 2
    ACC_HOTLAP = 3
    ACC_TIMEATTACK = 4
    ACC_DRIFT = 5
    ACC_DRAG = 6
    ACC_HOTSTINT = 7
    ACC_HOTSTINTSUPERPOLE = 8

class ACC_STATUS(IntEnum):
    ACC_OFF = 0
    ACC_REPLAY = 1
    ACC_LIVE = 2
    ACC_PAUSE = 3

class ACC_WHEELS_TYPE(IntEnum):
    ACC_FrontLeft = 0
    ACC_FrontRight = 1
    ACC_RearLeft = 2
    ACC_RearRight = 3

class ACC_TRACK_GRIP_STATUS(IntEnum):
    ACC_GREEN = 0
    ACC_FAST = 1
    ACC_OPTIMUM = 2
    ACC_GREASY = 3
    ACC_DAMP = 4
    ACC_WET = 5
    ACC_FLOODED = 6

class ACC_RAIN_INTENSITY(IntEnum):
    ACC_NO_RAIN = 0
    ACC_DRIZZLE = 1
    ACC_LIGHT_RAIN = 2
    ACC_MEDIUM_RAIN = 3
    ACC_HEAVY_RAIN = 4
    ACC_THUNDERSTORM = 5


class SPageFileGraphic(StructureWithEnums):
    _fields_ = [
        ("packetId", c_int),
        ("status", c_int),
        ("session", c_int),
        ("currentTime", ShortWord),
        ("lastTime", ShortWord),
        ("bestTime", ShortWord),
        ("split", ShortWord),
        ("completedLaps", c_int),
        ("position", c_int),
        ("iCurrentTime", c_int),
        ("iLastTime", c_int),
        ("iBestTime", c_int),
        ("sessionTimeLeft", c_float),
        ("distanceTraveled", c_float),
        ("isInPit", c_int),
        ("currentSectorIndex", c_int),
        ("lastSectorTime", c_int),
        ("numberOfLaps", c_int),
        ("tyreCompound", Word),
        ("replayTimeMultiplier", c_float),
        ("normalizedCarPosition", c_float),
        ("activeCars", c_int),
        ("carCoordinates", c_float * 3 * 60),
        ("carID", c_int * 60),
        ("playerCarID", c_int),
        ("penaltyTime", c_float),
        ("flag", c_int),
        ("penalty", c_int),
        ("idealLineOn", c_int),
        ("isInPitLane", c_int),
        ("surfaceGrip", c_float),
        ("mandatoryPitDone", c_int),
        ("windSpeed", c_float),
        ("windDirection", c_float),
        ("isSetupMenuVisible", c_int),
        ("mainDisplayIndex", c_int),
        ("secondaryDisplayIndex", c_int),
        ("TC", c_int),
        ("TCCut", c_int),
        ("EngineMap", c_int),
        ("ABS", c_int),
        ("fuelXLap", c_int),
        ("rainLights", c_int),
        ("flashingLights", c_int),
        ("lightsStage", c_int),
        ("exhaustTemperature", c_float),
        ("wiperLV", c_int),
        ("DriverStintTotalTimeLeft", c_int),
        ("DriverStintTimeLeft", c_int),
        ("rainTyres", c_int),
        ("sessionIndex", c_int),
        ("usedFuel", c_float),
        ("deltaLapTime", ShortWord),
        ("iDeltaLapTime", c_int),
        ("estimatedLapTime", ShortWord),
        ("iEstimatedLapTime", c_int),
        ("isDeltaPositive", c_int),
        ("iSplit", c_int),
        ("isValidLap", c_int),
        ("fuelEstimatedLaps", c_float),
        ("trackStatus", Word),
        ("missingMandatoryPits", c_int),
        ("Clock", c_float),
        ("directionLightsLeft", c_int),
        ("directionLightsRight", c_int),
        ("GlobalYellow", c_int),
        ("GlobalYellow1", c_int),
        ("GlobalYellow2", c_int),
        ("GlobalYellow3", c_int),
        ("GlobalWhite", c_int),
        ("GlobalGreen", c_int),
        ("GlobalChequered", c_int),
        ("GlobalRed", c_int),
        ("mfdTyreSet", c_int),
        ("mfdFuelToAdd", c_float),
        ("mfdTyrePressureLF", c_float),
        ("mfdTyrePressureRF", c_float),
        ("mfdTyrePressureLR", c_float),
        ("mfdTyrePressureRR", c_float),
        ("trackGripStatus", c_int),
        ("rainIntensity", c_int),
        ("rainIntensityIn10min", c_int),
        ("rainIntensityIn30min", c_int),
        ("currentTyreSet", c_int),
        ("strategyTyreSet", c_int),
        ("gapAhead", c_int),
        ("gapBehind", c_int),
    ]
    _map = {
        "status": ACC_STATUS,
        "session": ACC_SESSION_TYPE,
        "flag": ACC_FLAG_TYPE,
        "penalty": ACC_PENALTY_TYPE,
        "trackGripStatus": ACC_TRACK_GRIP_STATUS,
        "rainIntensity": ACC_RAIN_INTENSITY,
        "rainIntensityIn10min": ACC_RAIN_INTENSITY,
        "rainIntensityIn30min": ACC_RAIN_INTENSITY,
    }





class DriverInfo(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Name', LongWord),
        ('CarNumber', c_int),
        ('ClassId', c_int),
        ('ModelId', c_int),
        ('TeamId', c_int),
        ('LiveryId', c_int),
        ('ManufacturerId', c_int),
        ('UserId', c_int),
        ('SlotId', c_int),
        ('ClassPerformanceIndex', c_int),
        ('EngineType', c_int),
        ('Unused1', c_int),
        ('Unused2', c_int),
    ]


class CutTrackPenalties(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('DriveThrough', c_int) ,
        ('StopAndGo', c_int) ,
        ('PitStop', c_int) ,
        ('TimeDeduction', c_int) ,
        ('SlowDown', c_int) ,
    ]


class DriverData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        # DriverInfo
        ('DriverInfo', DriverInfo),

        ('FinishStatus', c_int),
        ('Place', c_int),
        ('PlaceClass', c_int),
        ('LapDistance', c_float),
        ('Position', c_float * 3),
        ('TrackSector', c_int ),
        ('CompletedLaps', c_int ),
        ('CurrentLapValid', c_int ),
        ('LapTimeCurrentSelf', c_float),
        ('SectorTimeCurrentSelf', c_float * 3),
        ('SectorTimePreviousSelf', c_float * 3),
        ('SectorTimeBestSelf', c_float * 3),
        ('TimeDeltaFront', c_float),
        ('TimeDeltaBehind', c_float),
        ('PitStopStatus', c_int ),
        ('InPitlane', c_int ),
        ('NumPitstops', c_int ),

        ('Penalties', CutTrackPenalties),

        ('CarSpeed', c_float ),
        ('TireTypeFront', c_int ),
        ('TireTypeRear', c_int ),
        ('TireSubtypeFront', c_int ),
        ('TireSubtypeRear', c_int ),
        ('BasePenaltyWeight', c_float ),
        ('AidPenaltyWeight', c_float ),
        ('DrsState', c_int ),
        ('PtpState', c_int ),

        ('PenaltyType', c_int ),
        ('PenaltyReason', c_int ),
        ('EngineState', c_int ),

        ('Unused1', c_int ),
        ('Unused2', c_float ),
        ('Unused3', c_float ),
    ]


class PlayerData(LittleEndianStructure):
    # PlayerData (high precision)
    _pack_ = 1
    _fields_ = [
        ('GameSimulationTicks' , c_int ),
        ('GameSimulationTime' , c_double ),
        ('Position' , c_double * 3 ),
        ('Velocity' , c_double * 3 ),
        ('LocalVelocity' , c_double * 3 ),
        ('Acceleration' , c_double * 3 ),
        ('LocalAcceleration' , c_double * 3 ),
        ('Orientation' , c_double * 3 ),
        ('Rotation' , c_double * 3 ),
        ('AngularAcceleration' , c_double * 3 ),
        ('AngularVelocity' , c_double * 3 ),
        ('LocalAngularVelocity' , c_double * 3 ),
        ('LocalGforce' , c_double * 3 ),
        ('SteeringForce' , c_double ),
        ('SteeringForcePercentage' , c_double ),
        ('EngineTorque' , c_double ),
        ('CurrentDownforce' , c_double ),
        ('Voltage' , c_double ),
        ('ErsLevel' , c_double ),
        ('PowerMguH' , c_double ),
        ('PowerMguK' , c_double ),
        ('TorqueMguK' , c_double ),

        ('SuspensionDeflection' , c_double * 4 ),
        ('SuspensionVelocity' , c_double * 4 ),
        ('Camber' , c_double * 4 ),
        ('RideHeight' , c_double * 4 ),

        ('FrontWingHeight' , c_double ),
        ('FrontRollAngle' , c_double ),
        ('RearRollAngle' , c_double ),
        ('ThirdSpringSuspensionDeflectionFront' , c_double ),
        ('ThirdSpringSuspensionVelocityFront' , c_double ),
        ('ThirdSpringSuspensionDeflectionRear' , c_double ),
        ('ThirdSpringSuspensionVelocityRear' , c_double ),
        ('Unused1' , c_double ),
    ]




class Shared(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('VersionMajor', c_int ),
        ('VersionMinor', c_int ),
        ('AllDriversOffset', c_int ),
        ('DriverDataSize', c_int ),
        ('GamePaused', c_int ),
        ('GameInMenus', c_int ),
        ('GameInReplay', c_int ),
        ('GameUsingVr', c_int ),

        ('GameUnused1', c_int ),
        # offset issue, was working on 06/07/2022 ... no more on 07/07/2022  ¯\_(ツ)_/¯

        ('Player' , PlayerData ),

        ('TrackName' , LongWord ),
        ('LayoutName' , LongWord ),

        ('TrackId', c_int ),
        ('LayoutId', c_int ),

        ('LayoutLength', c_float ),

        ('SectorStartFactors', c_float * 3 ),
        ('RaceSessionLaps', c_int * 3 ),
        ('RaceSessionMinutes', c_int * 3 ),

        ('EventIndex', c_int ),
        ('SessionType', c_int ),
        ('SessionIteration', c_int ),
        ('SessionLengthFormat', c_int ),
        ('SessionPitSpeedLimit', c_float ),
        ('SessionPhase', c_int ),
        ('StartLights', c_int ),
        ('TireWearActive', c_int ),
        ('FuelUseActive', c_int ),
        ('NumberOfLaps', c_int ),
        ('SessionTimeDuration', c_float ),
        ('SessionTimeRemaining', c_float ),
        ('MaxIncidentPoints', c_int ),
        ('EventUnused2', c_float ),
        ('PitWindowStatus', c_int ),
        ('PitWindowStart', c_int ),
        ('PitWindowEnd', c_int ),
        ('InPitlane', c_int ),
        ('PitMenuSelection', c_int ),

        # PitMenuState
        ('Preset', c_int) ,
        ('Penalty', c_int) ,
        ('Driverchange', c_int) ,
        ('Fuel', c_int) ,
        ('FrontTires', c_int) ,
        ('RearTires', c_int) ,
        ('FrontWing', c_int) ,
        ('RearWing', c_int) ,
        ('Suspension', c_int) ,
        ('ButtonTop', c_int) ,
        ('ButtonBottom', c_int) ,
        # PitMenuState END


        ('PitState', c_int ),

        ('PitTotalDuration', c_float ),
        ('PitElapsedTime', c_float ),
        ('PitAction', c_int ),
        ('NumPitstopsPerformed', c_int ),
        ('PitMinDurationTotal', c_float ),
        ('PitMinDurationLeft', c_float ),


        # FLAGS
        ('Yellow', c_int ),
        ('YellowCausedIt', c_int ),
        ('YellowOvertake', c_int ),
        ('YellowPositionsGained', c_int ),
        ('SectorYellow', c_int * 3 ),
        ('ClosestYellowDistanceIntoTrack', c_float ),
        ('Blue', c_int ),
        ('Black', c_int ),
        ('Green', c_int ),
        ('Checkered', c_int ),
        ('White', c_int ),
        ('BlackAndWhite', c_int ),
        # FLAGS END


        ('gridPosition', c_int ),
        ('PositionClass', c_int ),
        ('FinishStatus', c_int ),
        ('CutTrackWarnings', c_int ),

        ('Penalties', CutTrackPenalties),

        ('NumPenalties', c_int ),

        ('CompletedLaps', c_int ),
        ('CurrentLapValid', c_int ),
        ('TrackSector', c_int ),
        ('LapDistance', c_float ),
        ('LapDistanceFraction', c_float ),
        ('LapTimeBestLeader', c_float ),
        ('LapTimeBestLeaderClass', c_float ),

        ('SectorTimesSessionBestLap', c_float * 3 ),

        ('LapTimeBestSelf', c_float ),
        ('SectorTimesBestSelf', c_float * 3 ),

        ('LapTimePreviousSelf', c_float ),
        ('SectorTimesPreviousSelf', c_float * 3 ),

        ('LapTimeCurrentSelf', c_float ),
        ('SectorTimesCurrentSelf', c_float * 3 ),

        ('LapTimeDeltaLeader', c_float ),
        ('LapTimeDeltaLeaderClass', c_float ),
        ('TimeDeltaFront', c_float ),
        ('TimeDeltaBehind', c_float ),
        ('TimeDeltaBestSelf', c_float ),


        ('BestIndividualSectorTimeSelf', c_float * 3 ),
        ('BestIndividualSectorTimeLeader', c_float * 3 ),
        ('BestIndividualSectorTimeLeaderClass', c_float * 3 ),

        ('IncidentPoints', c_int ),

        ('LapValidState', c_int ),

        ('ScoreUnused1', c_float ),
        ('ScoreUnused2', c_float ),


        ('VehicleInfo', DriverInfo),

        ('PlayerName', LongWord),

        ('ControlType', c_int ),
        ('CarSpeed', c_float ),
        ('EngineRps', c_float ),
        ('MaxEngineRps', c_float ),
        ('UpshiftRps', c_float ),
        ('Gear', c_int ),
        ('NumGears', c_int ),

        ('CarCgLocation', c_float * 3 ),

        ('CarOrientation', c_float * 3 ),

        ('LocalAcceleration', c_float * 3 ),

        ('TotalMass', c_float ),
        ('FuelLeft', c_float ),
        ('FuelCapacity', c_float ),
        ('FuelPerLap', c_float ),
        ('EngineWaterTemp', c_float ),
        ('EngineOilTemp', c_float ),
        ('FuelPressure', c_float ),
        ('EngineOilPressure', c_float ),
        ('TurboPressure', c_float ),
        ('Throttle', c_float ),
        ('ThrottleRaw', c_float ),
        ('Brake', c_float ),
        ('BrakeRaw', c_float ),
        ('Clutch', c_float ),
        ('ClutchRaw', c_float ),
        ('SteerInputRaw', c_float ),
        ('SteerLockDegrees', c_int ),
        ('SteerWheelRangeDegrees', c_int ),

        # AidSettings
        ('aid_Abs', c_int),
        ('aid_Tc', c_int),
        ('aid_Esp', c_int),
        ('aid_Countersteer', c_int),
        ('aid_Cornering', c_int),


        # DRS
        ('drs_Equipped', c_int),
        ('drs_Available', c_int),
        ('drs_NumActivationsLeft', c_int),
        ('drs_Engaged', c_int),


        ('PitLimiter', c_int ),

        # PushToPass
        ('p2p_Available', c_int),
        ('p2p_Engaged', c_int),
        ('p2p_AmountLeft', c_int),
        ('p2p_EngagedTimeLeft', c_float),
        ('p2p_WaitTimeLeft', c_float),

        ('BrakeBias', c_float ),
        ('DrsNumActivationsTotal', c_int ),
        ('PtpNumActivationsTotal', c_int ),


        ('VehicleUnused1', c_float ),
        ('VehicleUnused2', c_float ),
        ('VehicleUnused3', c_float * 3 ),


        ('TireType', c_int ),
        ('TireRps', c_float * 4 ),
        ('TireSpeed', c_float * 4 ),
        ('TireGrip', c_float * 4 ),
        ('TireWear', c_float * 4 ),
        ('TireFlatspot', c_int * 4 ),
        ('TirePressure', c_float * 4 ),
        ('TireDirt', c_float * 4 ),

        ('TireTemp', c_float * 6 * 4 ),

        ('TireTypeFront', c_int ),
        ('TireTypeRear', c_int ),

        ('TireSubtypeFront', c_int ),
        ('TireSubtypeRear', c_int ),

        ('BrakeTemp', c_float * 4 * 4 ),
        ('BrakePressure', c_float * 4 ),

        ('TractionControlSetting', c_int ),
        ('EngineMapSetting', c_int ),
        ('EngineBrakeSetting', c_int ),

        ('TractionControlPercent', c_float ),

        ('TireOnMtrl', c_int * 4 ),
        ('TireLoad', c_float * 4 ),

        ('CarDamage', c_float * 6 ),

        ('NumCars', c_int ),

        ('DriverData', DriverData * 128),

    ]
