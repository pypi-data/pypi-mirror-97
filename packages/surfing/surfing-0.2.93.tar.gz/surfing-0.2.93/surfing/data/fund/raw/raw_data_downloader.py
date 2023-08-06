
import traceback

# from .rq_raw_data_downloader import RqRawDataDownloader
from .em_raw_data_downloader import EmRawDataDownloader
from .web_raw_data_downloader import WebRawDataDownloader
from .oversea_data_downloader import OverseaDataUpdate
from .raw_data_helper import RawDataHelper


class RawDataDownloader:
    def __init__(self, rq_license=None):
        self._data_helper = RawDataHelper()
        # self.rq_downloader = RqRawDataDownloader(rq_license, self._data_helper)
        self.web_downloader = WebRawDataDownloader(self._data_helper)
        self.em_downloader = EmRawDataDownloader(self._data_helper)
        self.oversea_download = OverseaDataUpdate(update_period=10, data_per_page=5, data_helper=self._data_helper)
        
    def download(self, start_date, end_date):
        failed_tasks = []

        try:
            failed_tasks.extend(self.em_downloader.download_all(start_date, end_date))         
        except Exception as e:
            print(e)
            traceback.print_exc()
            failed_tasks.append('unknown in em_downloader')

        # If 'em_tradedates' in failed_tasks, there is no trading day between start_date and end_date
        # Stop and return
        if 'em_tradedates' in failed_tasks:
            return failed_tasks

        # try:
        #     failed_tasks.extend(self.rq_downloader.download_all(start_date, end_date))
        # except Exception as e:
        #     print(e)
        #     traceback.print_exc()
        #     failed_tasks.append('unknown in rq_downloader')

        try:
            failed_tasks.extend(self.web_downloader.download_all(start_date, end_date))
        except Exception as e:
            print(e)
            traceback.print_exc()
            failed_tasks.append('unknown in web_downloader')

        try:
            failed_tasks.extend(self.oversea_download.update_fund_nav())
        except Exception as e:
            print(e)
            traceback.print_exc()
            failed_tasks.append('oversea fund nav')

        return failed_tasks

    def get_updated_count(self):
        return self._data_helper._updated_count
