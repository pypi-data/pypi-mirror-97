import sys
sys.path.append('')
from libra_core.config import *
from libra_core.log import *
from libra_core.influxd import InfluxDBClinet


def test_config():
    init_config()
    print(config("log_path"))
    print(config("log", "logging.level.com.apus"))
    print(config("channel_country_config"))

def test_influxdb():
    influxdb_client = InfluxDBClinet(config("influxdb.host"), 
                                     config("influxdb.port"), 
                                     config("influxdb.username"), 
                                     config("influxdb.password"), 
                                     config("influxdb.database"))
    sql_str = 'select sum(*) from libra_spider_detail where time< 1613788350000000000 and time > 1613540690000000000 group by time(1d)'
    print(influxdb_client.query(sql_str))

if __name__ == "__main__":
    test_config()
    test_influxdb()
