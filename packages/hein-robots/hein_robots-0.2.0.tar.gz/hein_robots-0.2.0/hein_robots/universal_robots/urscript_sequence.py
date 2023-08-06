from typing import Dict, List, Tuple
from collections import OrderedDict
import re
import math
from hein_robots.robotics import Location, Orientation, Cartesian
from hein_robots.grids import LocationGroup


class URScriptSequence(LocationGroup):
    LOCATION_REGEX = re.compile('global (\w+)_p=p\[(.*)\]')
    JOINT_REGEX = re.compile('global (\w+)_q=\[(.*)\]')

    @classmethod
    def parse_sequence_file(cls, file_path: str) -> Tuple[Dict[str, Location], Dict[str, List[float]]]:
        with open(file_path) as sequence_file:
            locations = OrderedDict()
            joints = OrderedDict()

            for line in sequence_file:
                location_match = cls.LOCATION_REGEX.search(line)
                if location_match:
                    name, location_str = location_match.groups()
                    location_list = [float(n) for n in location_str.split(', ')]
                    position = Cartesian(*location_list[:3])
                    rotation_vector = Cartesian(*location_list[3:])
                    locations[name] = Location(position, Orientation.from_rotation_vector(rotation_vector)).convert_m_to_mm()

                joint_match = cls.JOINT_REGEX.search(line)
                if joint_match:
                    name, joint_str = joint_match.groups()
                    joint_list = [math.degrees(float(n)) for n in joint_str.split(', ')]
                    joints[name] = joint_list

        return locations, joints

    def __init__(self, sequence_json_file: str):
        self.locations, self.joints = self.parse_sequence_file(sequence_json_file)

    def __len__(self):
        return len(self.locations)

    def __getitem__(self, item):
        return self.locations[item]

    def indexes(self) -> List[str]:
        return list(self.locations.keys())
