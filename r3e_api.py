import sys
import mmap
import ctypes
import re
import json
import copy

import orjson as oj

from pprint import pprint as pp

from r3e_types import *

from ctypes_json import *


def main():

    _obj = Shared.from_buffer(mmap.mmap(-1, ctypes.sizeof(Shared), tagname='$R3E'))

    CD = CDataJSONEncoder()
    CDdefault = CD.default

    #pp( _obj.__dict__ )
    #te = oj.dumps(_obj, default=CDdefault, option=oj.OPT_INDENT_2)
    #pp('{}'.format(te.decode('utf-8')))
    #tes = json.dumps(_obj, cls=CDataJSONEncoder, indent=2)
    #pp(tes)


    #pp(_obj.Player)


    printR3Evar(_obj, 'TrackName')
    printR3Evar(_obj, 'LayoutName')

    printR3Evar(_obj, 'SessionType')
    printR3Evar(_obj, 'SessionPhase')

    printR3Evar(_obj, 'SessionType')
    printR3Evar(_obj, 'SessionPhase')
    printR3Evar(_obj, 'PitWindowStatus')
    printR3Evar(_obj, 'FinishStatus')
    printR3Evar(_obj, 'ControlType')
    printR3Evar(_obj, 'TireTypeFront')
    printR3Evar(_obj, 'TireTypeRear')
    printR3Evar(_obj, 'TireSubtypeFront')
    printR3Evar(_obj, 'TireSubtypeRear')
    printR3Evar(_obj, 'TireOnMtrl')

    printR3Evar(_obj.Player, 'SuspensionDeflection')
    printR3Evar(_obj.Player, 'SuspensionVelocity')





    quit()


    printR3Evar(_obj.DriverData[0].DriverInfo, 'Name')
    printR3Evar(_obj.DriverData[1].DriverInfo, 'Name')
    printR3Evar(_obj.DriverData[2].DriverInfo, 'Name')
    printR3Evar(_obj.DriverData[3].DriverInfo, 'Name')
    printR3Evar(_obj.DriverData[4].DriverInfo, 'Name')

    quit()



    for at in dir(_obj):
        reg = re.search("^[a-zA-Z].*", str(at))
        if reg:
            printR3Evar(_obj, at)


def printR3Evar(_obj, at):

    obj = copy.deepcopy(_obj)

    vects = [
        'Position',
        'Velocity',
        'LocalVelocity',
        'Acceleration',
        'LocalAcceleration',
        'Orientation',
        'Rotation',
        'AngularAcceleration',
        'AngularVelocity',
        'LocalAngularVelocity',
        'LocalGforce',
        'SectorStartFactors',
        'RaceSessionLaps',
        'RaceSessionMinutes',
        'SectorYellow',
        'SectorTimesSessionBestLap',
        'SectorTimesBestSelf',
        'SectorTimesPreviousSelf',
        'SectorTimesCurrentSelf',
        'BestIndividualSectorTimeSelf',
        'BestIndividualSectorTimeLeader',
        'BestIndividualSectorTimeLeaderClass',
        'CarCgLocation',
        'CarOrientation',
        'LocalAcceleration',
    ]

    vect4 = [
        'SuspensionDeflection' ,
        'SuspensionVelocity' ,
        'Camber' ,
        'RideHeight' ,
        'TireRps',
        'TireSpeed',
        'TireGrip',
        'TireWear',
        'TireFlatspot',
        'TirePressure',
        'TireDirt',
        'BrakePressure',
        'TireOnMtrl',
        'TireLoad',
    ]

    strings = [
        'TrackName',
        'LayoutName',
        'veh_Name',
        'PlayerName',
        'drv_Name',
    ]

    structs = [
        'VehicleInfo',
        'Player',
        'DriverInfo',
        'Penalties',
    ]



    if at == 'DriverData':
        for dd in getattr(obj, at):
            pp(dd)
            for a in dir(dd):
                reg = re.search("^[a-zA-Z].*", str(a))
                if reg:
                    printR3Evar(dd, a)
                    #pp( '{} : {}'.format( '{}_{}'.format(at,a).ljust(40), getattr(dd, a) ) )


    if at in structs:
        tobj = getattr(obj, at)
        for a in dir(tobj):
            reg = re.search("^[a-zA-Z].*", str(a))
            if reg:
                printR3Evar(tobj, a)
                #pp( '{} : {}'.format( '{}_{}'.format(at,a).ljust(40), getattr(tobj, a) ) )


    elif at in vects:
        try:
            x, y, z = getattr(obj, at)
            pp( '{} ['.format(str(at)) )
            pp( '{:<5} {:<23} {:<23} {:<23}'.format('', x,y,z) )
            pp( ']' )
        except Exception as e:
            pp(e)

    elif at in vect4:
        try:
            FL, FR, RL, RR = getattr(obj, at)
            pp( '{} ['.format(str(at)) )
            pp( '{:<5} {:<30} {:<30}'.format('', FL.__str__(), FR.__str__()) )
            pp( '{:<5} {:<30} {:<30}'.format('', RL.__str__(), RR.__str__()) )
            pp( ']' )
        except Exception as e:
            pp(e)

    elif at in strings:
        pp( '{} : {}'.format( at.ljust(30), getattr(obj, at).__str__() ) )

    else:
        pp( '{} : {}'.format( at.ljust(30), getattr(obj, at).__str__() ) )


if __name__ == '__main__':
    main()

