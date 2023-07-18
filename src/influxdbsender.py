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


class DataCollectorAndSender:
    def __init__(self, config_file_path):
        config = configparser.ConfigParser()
        config.read(config_file_path)
        self.config = config

        self.influx_url = config.get('influxDb', 'url')
        self.influx_token = config.get('influxDb', 'token')
        self.influx_org = config.get('influxDb', 'org')
        self.influx_bucket = config.get('influxDb', 'bucketName')
        self.printer_id = config.get('Printer', 'id')

        self.max_retries = config.getint('SendDataSettings', 'max_retries')
        self.retry_delay = config.getint('SendDataSettings', 'retry_delay')
        self.min_send_interval = config.getfloat('SendDataSettings', 'min_send_interval')
        self.loop_sleep = config.getfloat('SendDataSettings', 'loop_sleep')

        self.value_ranges = [
            range(6001, 6013),
            range(6015, 6033),
            range(6034, 6041),
            range(6042, 6049),
            range(6052, 6172),
        ]

        self.last_sent_values = {}

        # Set up InfluxDB client
        self.write_client = influxdb_client.InfluxDBClient(url=self.influx_url, token=self.influx_token, org=self.influx_org)
        # Define the write api
        self.write_api = self.write_client.write_api(write_options=SYNCHRONOUS)

    async def _fetch_from_opcua(self):
        for attempt in range(self.max_retries):
            try:
                return await get_values()
            except asyncio.exceptions.TimeoutError:
                logging.warning(f"Connection attempt {attempt + 1} failed. Retrying...")
                await asyncio.sleep(self.retry_delay)
        else:
            logging.error(f"Could not establish connection after {self.max_retries} attempts.")
            return None

    def _format_data_dict(self, values):
        return {
            f"value{i}": {
                "printer_id": self.printer_id,
                "unit": "nounit",
                "value": values.get(f"value{i}"),
            }
            for r in self.value_ranges for i in r
        }

    async def main(self):

        while True:
            try:
                logging.info("Prepare values to send to InfluxDB")

                values = await self._fetch_from_opcua()
                if values is None:
                    continue

                data = self._format_data_dict(values)

                # Get current time
                current_time = time.time()

                points_to_send = []

                for key, value in data.items():
                    last_sent = self.last_sent_values.get(key, {})
                    last_sent_value = last_sent.get('value')
                    last_sent_time = last_sent.get('time')

                    # Check if data has changed or 3 minutes have passed
                    if last_sent_value != value[
                        'value'] or last_sent_time is None or current_time - last_sent_time >= self.min_send_interval:
                        points_to_send.append(
                            Point(key).tag("printer_id", value["printer_id"]).field(value["unit"], value["value"]))
                        # Update the last sent value and time for the key
                        self.last_sent_values[key] = {'value': value['value'], 'time': current_time}

                if points_to_send:
                    self.write_api.write(bucket=self.influx_bucket, org=self.influx_org, record=points_to_send)
                    logging.info("__________________values sent!__________________")

                await asyncio.sleep(self.loop_sleep)

            except Exception as e:
                logging.error(f"Error occurred: {e}")

if __name__ == "__main__":
    config_file_path = 'config.ini'
    collector = DataCollectorAndSender(config_file_path)
    asyncio.run(collector.main())
