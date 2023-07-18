import asyncio
import influxdb_client
import configparser
import logging
import time
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from opcuaclient import get_values

# Set up logging
logging.basicConfig(level=logging.INFO)


class DataCollector:
    def __init__(self, config):
        self.config = config

        self.url = config.get('influxDb', 'url', fallback='')
        self.token = config.get('influxDb', 'token', fallback='')
        self.org = config.get('influxDb', 'org', fallback='')
        self.bucket = config.get('influxDb', 'bucketName', fallback='')
        self.printer_id = config.get('Printer', 'id', fallback='')

        self.max_retries = config.getint('Settings', 'max_retries', fallback=5)
        self.retry_delay = config.getint('Settings', 'retry_delay', fallback=2)
        self.send_interval = config.getfloat('Settings', 'send_interval', fallback=180)
        self.loop_sleep = config.getfloat('Settings', 'loop_sleep', fallback=0.1)

        self.ranges = [
            range(6001, 6013),
            range(6015, 6033),
            range(6034, 6041),
            range(6042, 6049),
            range(6052, 6172),
        ]

        self.last_sent_values = {}

    async def _fetch_values(self):
        for attempt in range(self.max_retries):
            try:
                return await get_values()
            except asyncio.exceptions.TimeoutError:
                logging.warning(f"Connection attempt {attempt + 1} failed. Retrying...")
                await asyncio.sleep(self.retry_delay)
        else:
            logging.error(f"Could not establish connection after {self.max_retries} attempts.")
            return None

    def _prepare_data_dict(self, values):
        return {
            f"value{i}": {
                "printer_id": self.printer_id,
                "unit": "nounit",
                "value": values.get(f"value{i}"),
            }
            for r in self.ranges for i in r
        }

    async def main(self):
        # Set up InfluxDB client
        write_client = influxdb_client.InfluxDBClient(url=self.url, token=self.token, org=self.org)
        # Define the write api
        write_api = write_client.write_api(write_options=SYNCHRONOUS)

        while True:
            try:
                logging.info("______________prepare values to send____________")

                values = await self._fetch_values()
                if values is None:
                    continue

                data = self._prepare_data_dict(values)

                # Get current time
                current_time = time.time()

                points_to_send = []

                for key, value in data.items():
                    last_sent = self.last_sent_values.get(key, {})
                    last_sent_value = last_sent.get('value')
                    last_sent_time = last_sent.get('time')

                    # Check if data has changed or 3 minutes have passed
                    if last_sent_value != value[
                        'value'] or last_sent_time is None or current_time - last_sent_time >= self.send_interval:
                        points_to_send.append(
                            Point(key).tag("printer_id", value["printer_id"]).field(value["unit"], value["value"]))
                        # Update the last sent value and time for the key
                        self.last_sent_values[key] = {'value': value['value'], 'time': current_time}

                if points_to_send:
                    write_api.write(bucket=self.bucket, org=self.org, record=points_to_send)
                    logging.info("__________________values sent!__________________")

                await asyncio.sleep(self.loop_sleep)

            except Exception as e:
                logging.error(f"Error occurred: {e}")

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    collector = DataCollector(config)
    asyncio.run(collector.main())
