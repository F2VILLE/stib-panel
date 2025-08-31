import requests as req
import json
from datetime import datetime
import os
import enum

API_KEY = os.getenv("STIB_API_KEY")

class Dataset(enum.Enum):
    WAITING_TIME = "waiting-time"
    STOP_DETAILS = "stop-details"
    LINE_DETAILS = "gtfs-routes"

class API:
    def __init__(self):
        self.base_url = "https://stibmivb.opendatasoft.com/api/explore/v2.1"
        self.sets = {}
        self.sets[Dataset.WAITING_TIME] = "waiting-time-rt-production"
        self.sets[Dataset.STOP_DETAILS] = "stop-details-production"
        self.sets[Dataset.LINE_DETAILS] = "gtfs-routes-production"

    def get_dataset(self, name: Dataset) -> str:
        return self.sets.get(name, "")

    def get_base_url(self) -> str:
        return self.base_url
    
    def query(self, dataset: Dataset, params: dict) -> dict:
        response = req.get(
            f"{self.base_url}/catalog/datasets/{self.get_dataset(dataset)}/records",
            params={**params, "apikey": API_KEY}
        )
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")
        return response.json()

class Line:
    def __init__(self, id: str, destination: str, arrival: str):
        self.api = API()
        self.id = id
        self.destination = destination
        self.arrival = arrival
        self.time_arrival = datetime.fromisoformat(arrival)
        details = self.get_details(id)
        self.color = "#" + details.get("color", "333333")
        self.type = details.get("type", "")

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

    def get_details(self, line_id: str) -> dict:
        response = self.api.query(Dataset.LINE_DETAILS, {
            "where": f"route_short_name = '{line_id}'"
        })
        if not response["results"]:
            return {}
        details = {
            "color": response["results"][0].get("route_color"),
            "type": response["results"][0].get("route_type")
        }
        return details

class STIB:
    def __init__(self, stop_name: str):
        self.stop_name = stop_name
        self.api = API()
        stop_details = self.api.query(Dataset.STOP_DETAILS, {
            "where": f"name LIKE '%{stop_name}%'"
        })
        ids = [result['id'] for result in stop_details['results']]
        self.stop_ids = ids

    @property
    def next_lines(self) -> list[Line]:
        waiting_time_data = self.api.query(Dataset.WAITING_TIME, {
            "where": f"pointid IN {tuple(self.stop_ids)}"
        })
        lines = waiting_time_data['results']

        lines = waiting_time_data['results']

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
