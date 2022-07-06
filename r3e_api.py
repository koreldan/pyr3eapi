import sys
import mmap
import ctypes
import re
import json

import orjson as oj

from pprint import pprint as pp

from r3e_types import *

from ctypes_json import *


def main():

    _obj = Shared.from_buffer(mmap.mmap(-1, ctypes.sizeof(Shared), tagname='$R3E'))

    CD = CDataJSONEncoder()
    CDdefault = CD.default

    # A - print a nested json about all data
    #te = oj.dumps(_obj, default=CDdefault, option=oj.OPT_INDENT_2)
    #pp(te)


    # B - per variable prints
    # single session -> practice -> 3 drivers + you
    pp(_obj.TrackName.__str__())
    pp(_obj.LayoutName.__str__())

    pp(_obj.DriverData[0].DriverInfo.Name.__str__())
    pp(_obj.DriverData[1].DriverInfo.Name.__str__())
    pp(_obj.DriverData[2].DriverInfo.Name.__str__())
    pp(_obj.DriverData[3].DriverInfo.Name.__str__())
    pp(_obj.DriverData[4].DriverInfo.Name.__str__()) # empty driver

    quit()

    # python print to view all data
    for at in dir(_obj):
        reg = re.search("^[a-zA-Z].*", str(at))
        if reg:

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
                'DriverInfo',
                'Penalties',
            ]

            if at == 'DriverData':
                for dd in getattr(_obj, at):
                    pp(dd)
                    for a in dir(dd):
                        reg = re.search("^[a-zA-Z].*", str(a))
                        if reg:
                            pp( '{} : {}'.format( '{}_{}'.format(at,a).ljust(40), getattr(dd, a) ) )


            if at in structs:
                tobj = getattr(_obj, at)
                for a in dir(tobj):
                    reg = re.search("^[a-zA-Z].*", str(a))
                    if reg:
                        pp( '{} : {}'.format( '{}_{}'.format(at,a).ljust(40), getattr(tobj, a) ) )


            elif at in vects:
                try:
                    x, y, z = getattr(_obj, at)
                    pp( '{} ['.format(str(at)) )
                    pp( '{:<5} {:<23} {:<23} {:<23}'.format('', x,y,z) )
                    pp( ']' )
                except Exception as e:
                    pp(v)
                    pp(e)

            elif at in vect4:
                try:
                    FL, FR, RL, RR = getattr(_obj, at)
                    pp( '{} ['.format(str(at)) )
                    pp( '{:<5} {:<30} {:<30}'.format('', FL, FR) )
                    pp( '{:<5} {:<30} {:<30}'.format('', RL, RR) )
                    pp( ']' )
                except Exception as e:
                    pp(v)
                    pp(e)

            elif at in strings:
                pp( '{} : {}'.format( at.ljust(30), str( getattr(_obj, at) ) ) )

            else:
                pp( '{} : {}'.format( at.ljust(30), getattr(_obj, at) ) )


if __name__ == '__main__':
    main()

