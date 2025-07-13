"""
This is a boilerplate pipeline 'data_ingestion'
generated using Kedro 0.19.14
"""

import logging
import time
from typing import Dict, List

import pandas as pd
import requests

logger = logging.getLogger(__name__)


def fetch_kmb_routes() -> List[Dict]:
    """
    Fetch all KMB routes from the official API

    Returns:
        List of route dictionaries
    """
    try:
        url = "https://data.etabus.gov.hk/v1/transport/kmb/route"

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()
        if data["type"] == "RouteList":
            routes = data["data"]
            logger.info(f"Successfully fetched {len(routes)} routes from KMB API")
            return routes
        else:
            logger.error(f"Unexpected API response type: {data.get('type')}")
            return []

    except Exception as e:
        logger.error(f"Error fetching KMB routes: {e}")
        return []


def fetch_kmb_stops() -> List[Dict]:
    """
    Fetch all KMB stops from the official API

    Returns:
        List of stop dictionaries
    """
    try:
        url = "https://data.etabus.gov.hk/v1/transport/kmb/stop"

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()
        if data["type"] == "StopList":
            stops = data["data"]
            # Filter to Hong Kong area only
            hk_stops = []
            for stop in stops:
                lat = float(stop.get("lat", 0))
                lng = float(stop.get("long", 0))
                if 22.15 <= lat <= 22.6 and 113.8 <= lng <= 114.5:
                    hk_stops.append(stop)

            logger.info(f"Successfully fetched {len(hk_stops)} HK stops from KMB API")
            return hk_stops
        else:
            logger.error(f"Unexpected API response type: {data.get('type')}")
            return []

    except Exception as e:
        logger.error(f"Error fetching KMB stops: {e}")
        return []


def fetch_route_stops_sample(routes: List[Dict], max_routes: int = 50) -> List[Dict]:
    """
    Fetch route-stop mappings for a sample of routes

    Args:
        routes: List of route dictionaries
        max_routes: Maximum number of routes to process

    Returns:
        List of route-stop mapping dictionaries
    """
    try:
        route_stops = []
        processed = 0

        for route in routes[:max_routes]:
            route_id = route["route"]
            service_type = route.get("service_type", 1)

            # Fetch for both directions
            for bound in ["O", "I"]:  # Outbound, Inbound
                try:
                    url = f"https://data.etabus.gov.hk/v1/transport/kmb/route-stop/{route_id}/{bound}/{service_type}"

                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        if data["type"] == "RouteStopList" and data["data"]:
                            route_stops.extend(data["data"])

                    # Small delay to avoid overwhelming the API
                    time.sleep(0.1)

                except Exception as e:
                    logger.warning(
                        f"Error fetching route-stops for {route_id}-{bound}: {e}"
                    )
                    continue

            processed += 1
            if processed % 10 == 0:
                logger.info(f"Processed {processed}/{max_routes} routes...")

        logger.info(f"Successfully fetched {len(route_stops)} route-stop mappings")
        return route_stops

    except Exception as e:
        logger.error(f"Error fetching route-stops: {e}")
        return []
