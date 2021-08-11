import unittest
import sys
import os

from src.aggregator import aggregate_success_rate

class Test_Backend_Traffic_Analyzer(unittest.TestCase):
    """
    """
    def test_aggregator(self):
        aggregated_success_rate = {
            "Webapp1":{
                "1.0.1":{
                    "total_req_count": 10000,
                    "total_success_count": 8000,
                    "success_rate_%": 80.0
                },
                "1.1.0":{
                    "total_req_count": 2000,
                    "total_success_count": 1000,
                    "success_rate_%": 50.0
                }
            },
            "Cache1":{
                "1.0.0":{
                    "total_req_count": 1000,
                    "total_success_count": 700,
                    "success_rate_%": 70.0
                }
            }
        }
        
        status_response = {
            "Application":"Webapp1",
            "Version":"1.0.1",
            "Uptime":20000000,
            "Request_Count":3000,
            "Error_Count":1000,
            "Success_Count":2000
        }
        
        logger = "Fake_logger"
        out = aggregate_success_rate(aggregated_success_rate, status_response, logger)
        print(out)
        assert out == {
            "Webapp1":{
                "1.0.1":{
                    "total_req_count": 13000,
                    "total_success_count": 10000,
                    "success_rate_%": 76.92
                },
                "1.1.0":{
                    "total_req_count": 2000,
                    "total_success_count": 1000,
                    "success_rate_%": 50.0
                }
            },
            "Cache1":{
                "1.0.0":{
                    "total_req_count": 1000,
                    "total_success_count": 700,
                    "success_rate_%": 70.0
                }
            }
        }

