import pytest
import sys
from pprint import pprint
from unittest import TestCase

import requests


class TestApiV3(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.print_debug_objects = True

    def make_request(self, method, url, json=None):
        try:
            response = requests.request(method, url, json=json)
        except:
            print("Failed to connect to server", file=sys.stderr)
            assert False

        return response

    def get_gpus(self):
        response = self.make_request("GET", "http://localhost:8000/api/v3/gpus")
        if response.status_code == 204:
            print("No GPUs found", file=sys.stderr)
            assert False

        return response.json()["response"]

    def get_gpuchips(self):
        response = self.make_request("GET", "http://localhost:8000/api/v3/gpuchips")
        if response.status_code == 204:
            print("No GPU Chips found", file=sys.stderr)
            assert False

        return response.json()["response"]

    def test_gpus_get(self):
        response = self.make_request("GET", "http://localhost:8000/api/v3/gpus")

        assert response.status_code in [200, 204]

        if response.status_code == 204:
            if self.print_debug_objects:
                print("No GPUs found")
            return

        try:
            data = response.json()
        except:
            assert False

        assert data["status"]
        assert data["message"]
        assert "response" in data

        if self.print_debug_objects:
            pprint(data)

    def test_gpus_post(self):
        existing_gpu = self.get_gpus()[0]
        existing_chip = existing_gpu["chip"]
        non_existent_chip = existing_chip.copy()
        non_existent_chip["id"] = "000000000000000000000000"

        new_gpu = {
            "modelName": "Test Model",
            "manufacturer": "Test Manufacturer",
            "chip": existing_chip,
            "launchDate": "2021-01-01",
            "launchPrice": "100",
            "memory": 8,
            "computeUnits": 16,
            "performance": 100
        }

        response = self.make_request("POST", "http://localhost:8000/api/v3/gpus", json=new_gpu)
        assert response.status_code == 201

        response_gpu = response.json()["response"]
        for key in new_gpu:
            assert new_gpu[key] == response_gpu[key]

        if self.print_debug_objects:
            print("\n====================================" * 2)
            print("Response GPU:")
            pprint(response_gpu)

        new_gpu["chip"] = non_existent_chip
        response = self.make_request("POST", "http://localhost:8000/api/v3/gpus", json=new_gpu)
        assert response.status_code == 400
        if self.print_debug_objects:
            print("\n====================================" * 2)
            print("Non existent chip response:")
            pprint(response.json())

        new_gpu["memory"] = "incorrect_value"
        response = self.make_request("POST", "http://localhost:8000/api/v3/gpus", json=new_gpu)
        assert response.status_code == 400
        if self.print_debug_objects:
            print("\n====================================" * 2)
            print("Incorrect GPU response:")
            pprint(response.json())

    def test_gpus_other_methods(self):
        methods = ["PUT", "PATCH", "DELETE"]
        for method in methods:
            response = self.make_request(method, "http://localhost:8000/api/v3/gpus")
            assert response.status_code == 501

            if self.print_debug_objects:
                print("\n====================================" * 2)
                print(f"Response for {method}:")
                pprint(response.json())

    def test_gpus_single_get(self):
        existing_gpu = self.get_gpus()[0]

        response = self.make_request("GET", f"http://localhost:8000/api/v3/gpus/{existing_gpu['id']}")
        assert response.status_code == 200

        try:
            data = response.json()
        except:
            assert False

        assert data["status"]
        assert data["message"]
        assert "response" in data

        if self.print_debug_objects:
            print("\n====================================" * 2)
            print("Single GPU response:")
            pprint(data)

        non_existent_id = "000000000000000000000000"

        response = self.make_request("GET", f"http://localhost:8000/api/v3/gpus/{non_existent_id}")
        assert response.status_code == 404

        if self.print_debug_objects:
            print("\n====================================" * 2)
            print("Non existent GPU response:")
            pprint(response.json())

    def test_gpus_single_put(self):
        existing_gpu = self.get_gpus()[0]
        existing_chip = existing_gpu["chip"]
        non_existent_chip = existing_chip.copy()
        non_existent_chip["id"] = "000000000000000000000000"

        new_gpu = {
            "id": existing_gpu["id"],
            "modelName": "Test Model",
            "manufacturer": "Test Manufacturer",
            "chip": existing_chip,
            "launchDate": "2021-01-01",
            "launchPrice": "100",
            "memory": 8,
            "computeUnits": 16,
            "performance": 100
        }

        response = self.make_request(
            "PUT", f"http://localhost:8000/api/v3/gpus/{existing_gpu['id']}", json=new_gpu
        )
        assert response.status_code == 200

        response_gpu = response.json()["response"]
        for key in new_gpu:
            assert new_gpu[key] == response_gpu[key]

        if self.print_debug_objects:
            print("\n====================================" * 2)
            print("Response GPU:")
            pprint(response_gpu)

        new_gpu["chip"] = non_existent_chip
        response = self.make_request(
            "PUT", f"http://localhost:8000/api/v3/gpus/{existing_gpu['id']}", json=new_gpu
        )
        assert response.status_code == 400
        if self.print_debug_objects:
            print("\n====================================" * 2)
            print("Non existent chip response:")
            pprint(response.json())

        new_gpu["memory"] = "incorrect_value"
        response = self.make_request(
            "PUT", f"http://localhost:8000/api/v3/gpus/{existing_gpu['id']}", json=new_gpu
        )
        assert response.status_code == 400
        if self.print_debug_objects:
            print("\n====================================" * 2)
            print("Incorrect GPU response:")
            pprint(response.json())

    def test_gpus_single_delete(self):
        existing_gpu = self.get_gpus()[0]

        response = self.make_request("DELETE", f"http://localhost:8000/api/v3/gpus/{existing_gpu['id']}")
        assert response.status_code == 200

        try:
            data = response.json()
        except:
            assert False

        assert data["status"]
        assert data["message"]
        assert "response" in data

        if self.print_debug_objects:
            print("\n====================================" * 2)
            print("Single GPU response:")
            pprint(data)

        non_existent_id = "000000000000000000000000"

        response = self.make_request("DELETE", f"http://localhost:8000/api/v3/gpus/{non_existent_id}")
        assert response.status_code == 404

        if self.print_debug_objects:
            print("\n====================================" * 2)
            print("Non existent GPU response:")
            pprint(response.json())

    def test_gpus_single_other_methods(self):
        existing_gpu = self.get_gpus()[0]
        non_existent_id = "000000000000000000000000"

        methods = ["POST", "PATCH"]
        for method in methods:
            response = self.make_request(method, f"http://localhost:8000/api/v3/gpus/{existing_gpu['id']}")
            assert response.status_code == 501

            if self.print_debug_objects:
                print("\n====================================" * 2)
                print(f"Response for {method}:")
                pprint(response.json())

    def test_gpuchips_get(self):
        response = self.make_request("GET", "http://localhost:8000/api/v3/gpuchips")

        assert response.status_code in [200, 204]

        if response.status_code == 204:
            if self.print_debug_objects:
                print("No GPU Chips found")
            return

        try:
            data = response.json()
        except:
            assert False

        assert data["status"]
        assert data["message"]
        assert "response" in data

        if self.print_debug_objects:
            pprint(data)

    def test_gpuchips_post(self):
        existing_chip = self.get_gpuchips()[0]
        new_chip = {
            "chipName": "Test Chip",
            "architecture": "Test Architecture",
            "fab": "Test Fab",
            "transistors": 100,
            "dieSize": 100
        }

        response = self.make_request("POST", "http://localhost:8000/api/v3/gpuchips", json=new_chip)
        assert response.status_code == 201

        response_chip = response.json()["response"]
        for key in new_chip:
            assert new_chip[key] == response_chip[key]

        if self.print_debug_objects:
            print("\n====================================" * 2)
            print("Response Chip:")
            pprint(response_chip)

    def test_gpuchips_other_methods(self):
        methods = ["PUT", "PATCH", "DELETE"]
        for method in methods:
            response = self.make_request(method, "http://localhost:8000/api/v3/gpuchips")
            assert response.status_code == 501

            if self.print_debug_objects:
                print("\n====================================" * 2)
                print(f"Response for {method}:")
                pprint(response.json())

    def test_gpuchips_single_get(self):
        existing_chip = self.get_gpuchips()[0]

        response = self.make_request("GET", f"http://localhost:8000/api/v3/gpuchips/{existing_chip['id']}")
        assert response.status_code == 200

        try:
            data = response.json()
        except:
            assert False

        assert data["status"]
        assert data["message"]
        assert "response" in data

        if self.print_debug_objects:
            print("\n====================================" * 2)
            print("Single Chip response:")
            pprint(data)

        non_existent_id = "000000000000000000000000"

        response = self.make_request("GET", f"http://localhost:8000/api/v3/gpuchips/{non_existent_id}")
        assert response.status_code == 404

        if self.print_debug_objects:
            print("\n====================================" * 2)
            print("Non existent Chip response:")
            pprint(response.json())

    def test_gpuchips_single_put(self):
        existing_chip = self.get_gpuchips()[0]
        new_chip = {
            "id": existing_chip["id"],
            "chipName": "Test Chip",
            "architecture": "Test Architecture",
            "fab": "Test Fab",
            "transistors": 100,
            "dieSize": 100
        }

        response = self.make_request(
            "PUT", f"http://localhost:8000/api/v3/gpuchips/{existing_chip['id']}", json=new_chip
        )
        assert response.status_code == 200

        response_chip = response.json()["response"]
        for key in new_chip:
            assert new_chip[key] == response_chip[key]

        if self.print_debug_objects:
            print("\n====================================" * 2)
            print("Response Chip:")
            pprint(response_chip)

    def test_gpuchips_single_delete(self):
        existing_chip = self.get_gpuchips()[0]

        response = self.make_request("DELETE", f"http://localhost:8000/api/v3/gpuchips/{existing_chip['id']}")
        assert response.status_code == 200

        try:
            data = response.json()
        except:
            assert False

        assert data["status"]
        assert data["message"]
        assert "response" in data

        if self.print_debug_objects:
            print("\n====================================" * 2)
            print("Single Chip response:")
            pprint(data)

        non_existent_id = "000000000000000000000000"

        response = self.make_request("DELETE", f"http://localhost:8000/api/v3/gpuchips/{non_existent_id}")
        assert response.status_code == 404

        if self.print_debug_objects:
            print("\n====================================" * 2)
            print("Non existent Chip response:")
            pprint(response.json())

    def test_gpuchips_single_other_methods(self):
        existing_chip = self.get_gpuchips()[0]
        non_existent_id = "000000000000000000000000"

        methods = ["POST", "PATCH"]
        for method in methods:
            response = self.make_request(method, f"http://localhost:8000/api/v3/gpuchips/{existing_chip['id']}")
            assert response.status_code == 501

            if self.print_debug_objects:
                print("\n====================================" * 2)
                print(f"Response for {method}:")
                pprint(response.json())

    def test_gpuchips_single_gpus_get(self):
        existing_chip = self.get_gpuchips()[0]

        response = self.make_request(
            "GET", f"http://localhost:8000/api/v3/gpuchips/{existing_chip['id']}/gpus"
        )
        assert response.status_code in [200, 204]

        if response.status_code == 204:
            if self.print_debug_objects:
                print("No GPUs found for chip")
            return

        try:
            data = response.json()
        except:
            assert False

        assert data["status"]
        assert data["message"]
        assert "response" in data

        if self.print_debug_objects:
            pprint(data)
