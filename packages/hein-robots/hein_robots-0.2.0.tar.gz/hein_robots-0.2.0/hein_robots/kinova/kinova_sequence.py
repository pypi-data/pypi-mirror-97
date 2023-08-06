from typing import Dict, List
import json
from hein_robots.robotics import Location
from hein_robots.grids import LocationGroup


class KinovaSequence(LocationGroup):
    @staticmethod
    def parse_sequence_file(sequence_file_path: str) -> Dict[str, Location]:
        with open(sequence_file_path) as sequence_file:
            locations = {}
            data = json.load(sequence_file)
            tasks = data['sequences']['sequence'][0]['tasks']

            for task in tasks:
                if 'reachPose' in task['action']:
                    pose = task['action']['reachPose']['targetPose']
                    location = Location(pose['x'], pose['y'], pose['z'], pose['thetaX'], pose['thetaY'], pose['thetaZ'])
                    locations[task['action']['name']] = location.convert_m_to_mm()

            return locations

    def __init__(self, sequence_json_file: str):
        self.locations = self.parse_sequence_file(sequence_json_file)

    def __len__(self):
        return len(self.locations)

    def __getitem__(self, item):
        return self.locations[item]

    def indexes(self) -> List[str]:
        return list(self.locations.keys())
