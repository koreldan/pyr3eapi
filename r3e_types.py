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


class Session(IntEnum):
    Unavailable = -1
    Practice = 0
    Qualify = 1
    Race = 2
    Warmup = 3


class SessionPhase(IntEnum):
    Unavailable = -1
    Garage = 1
    Gridwalk = 2
    Formation = 3
    Countdown = 4
    Green = 5
    Checkered = 6


class Control(IntEnum):
    Unavailable = -1
    Player = 0
    AI = 1
    Remote = 2
    Replay = 3


class PitWindow(IntEnum):
    Unavailable = -1
    Disabled = 0
    Closed = 1
    Open = 2
    Stopped = 3
    Completed = 4


class PitStopStatus(IntEnum):
    Unavailable = -1
    UnservedTwoTyres = 0
    UnservedFourTyres = 1
    Served = 2


class FinishStatus(IntEnum):
    Unavailable = -1
    null = 0
    Finished = 1
    DNF = 2
    DNQ = 3
    DNS = 4
    DQ = 5


class SessionLengthFormat(IntEnum):
    Unavailable = -1
    TimeBased = 0
    LapBased = 1
    TimeAndLapBased = 2


class PitMenuSelection(IntEnum):
    Unavailable = -1
    Preset = 0

    # Pit menu actions
    Penalty = 1
    Driverchange = 2
    Fuel = 3
    Fronttires = 4
    Reartires = 5
    Frontwing = 6
    Rearwing = 7
    Suspension = 8

    # Pit menu buttons
    ButtonTop = 9
    ButtonBottom = 10

    # Pit menu nothing selected
    Max = 11


class TireType(IntEnum):
    Unavailable = -1
    Option = 0
    Prime = 1


class TireSubtype(IntEnum):
    Unavailable = -1
    Primary = 0
    Alternate = 1
    Soft = 2
    Medium = 3
    Hard = 4


class MtrlType(IntEnum):
    Unavailable = -1
    null = 0
    Tarmac = 1
    Grass = 2
    Dirt = 3
    Gravel = 4
    Rumble = 5


class EngineType(IntEnum):
    Combustion = 0
    Electric = 1
    Hybrid = 2




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


class DriverData(StructureWithEnums):
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

    _map = {
        'FinishStatus' : FinishStatus ,
        'TireTypeFront' : TireType ,
        'TireTypeRear' : TireType ,
        'TireSubtypeFront' : TireSubtype ,
        'TireSubtypeRear' : TireSubtype ,
    }


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




class Shared(StructureWithEnums):
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

    _map = {
        'SessionType' : Session,
        'SessionPhase' : SessionPhase,
        'PitWindowStatus' : PitWindow ,
        'FinishStatus' : FinishStatus ,
        'ControlType' : Control ,
        'TireTypeFront' : TireType ,
        'TireTypeRear' : TireType ,
        'TireSubtypeFront' : TireSubtype ,
        'TireSubtypeRear' : TireSubtype ,
        'TireOnMtrl' : MtrlType ,
    }
