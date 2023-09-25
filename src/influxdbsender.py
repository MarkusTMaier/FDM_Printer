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
        6001, 6002, 6003, 6004, 6005, 6007, 6013, 6014,
        6015, 6016, 6017, 6018, 6019, 6020, 6021, 6022, 6023, 6024, 6025, 6026,
        6027, 6028, 6029, 6030, 6031, 6032, 6033, 6034, 6035, 6036, 6037, 6038, 6039,
        6040, 6041, 6042, 6043, 6044, 6045, 6046, 6047, 6048, 6049, 6050, 6052, 6053, 6054, 6055,
        6056, 6057, 6058, 6059, 6060, 6061, 6062, 6063, 6064, 6065, 6066, 6067,
        6068, 6069, 6070, 6071, 6072, 6073, 6074, 6075, 6076, 6077, 6078, 6079,
        6080, 6081, 6082, 6083, 6084, 6085, 6086, 6087, 6088, 6089, 6090, 6091,
        6092, 6093, 6094, 6095, 6096, 6097, 6098, 6099, 6100, 6101, 6102, 6103,
        6104, 6105, 6106, 6107, 6108, 6109, 6110, 6111, 6112, 6113, 6114, 6115,
        6116, 6117, 6118, 6119, 6120, 6121, 6122, 6123, 6124, 6125, 6126, 6127,
        6128, 6129, 6130, 6131, 6132, 6133, 6134, 6135, 6136, 6137, 6138, 6139,
        6140, 6141, 6142, 6143, 6144, 6145, 6146, 6147, 6148, 6149, 6150, 6151,
        6152, 6153, 6154, 6155, 6156, 6157, 6158, 6159, 6160, 6161, 6162, 6163,
        6164, 6165, 6166, 6167, 6168, 6169, 6170, 6171
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
            for i in self.value_ranges
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