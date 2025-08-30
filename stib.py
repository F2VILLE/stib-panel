import requests as req
import json
from datetime import datetime
import os

API_KEY = os.getenv("STIB_API_KEY")

base_url = "https://stibmivb.opendatasoft.com/api/explore/v2.1"

wt = "waiting-time-rt-production"
sd = "stop-details-production"

class Line:
    def __init__(self, id: str, destination: str, arrival: str):
        self.id = id
        self.destination = destination
        self.arrival = arrival
        # parse the arrival time to a datetime object
        self.time_arrival = datetime.fromisoformat(arrival)

    def __str__(self):
        now = datetime.now().astimezone()
        delta = int((self.time_arrival - now).total_seconds() / 60)
        if delta < 1:
            return f"[{self.id}] {self.destination} - Arriving now"
        return f"[{self.id}] {self.destination} - {delta} min"
    
    def time_left(self) -> str:
        now = datetime.now().astimezone()
        delta = int((self.time_arrival - now).total_seconds() / 60)
        if delta < 1:
            return "Arriving now"
        return f"{delta} min"

class STIB:
    def __init__(self, stop_name: str):
        self.stop_name = stop_name
        response = req.get(
            f"{base_url}/catalog/datasets/{sd}/records",
            params={"where": f"name LIKE '%{stop_name}%'", "apikey": API_KEY}
        )
        stop_details = response.json()
        ids = [result['id'] for result in stop_details['results']]
        self.stop_ids = ids

    @property
    def next_lines(self) -> list[Line]:
        response = req.get(
            f"{base_url}/catalog/datasets/{wt}/records",
            params={"where": f"pointid IN {tuple(self.stop_ids)}", "apikey": API_KEY}
        )
        data = response.json()

        lines = data['results']

        result_lines: list[Line] = []

        for line in lines:
            passing_times = line['passingtimes']
            passing_times = json.loads(passing_times)

            for t in passing_times:
                if 'destination' not in t:
                    continue
                result_lines.append(Line(
                    t['lineId'],
                    t['destination']['fr'],
                    t['expectedArrivalTime']
                ))
        result_lines.sort(key=lambda x: x.time_arrival)
        return result_lines
