import datetime
import os
import os.path

from SapphireQuant.Core.Bar import Bar
from SapphireQuant.Core.CSharpUtils import CSharpUtils
from SapphireQuant.Core.Enum.EnumBarType import EnumBarType
from SapphireQuant.DataProcessing import BinaryWriter
from SapphireQuant.DataProcessing.BinaryReader import BinaryReader
from SapphireQuant.DataProcessing.FileHeader import FileHeader


class BinaryMinBarStream(object):
    """
    分钟读写流
    """
    BarLength = 88
    SimpleDayBarCountThreshold = 18

    def __init__(self, market, instrument_id, file_path):
        self._file_stream = None
        self._file_header = FileHeader()
        self._file_extension = ".min"
        self._instrument_id = ""
        self._file_path = ""

        self._file_header.file_version = "MQ 1.0"
        self._file_header.period = 1
        self._file_header.market = market
        self._file_header.bar_type = EnumBarType.minute
        self._file_path = file_path

        if file_path.strip() == '':
            raise Exception("Invalid Config File Path!")

        extension = os.path.splitext(file_path)[1].lower()
        if extension != self._file_extension:
            raise Exception("Invalid File Extension!")

        create_new = not os.path.exists(file_path)
        self._instrument_id = instrument_id.split('.')[0]
        self._file_stream = open(file_path, 'rb+')

        if not create_new:
            if os.path.getsize(file_path) == 0:
                raise Exception("Invalid File Length!")
            if self._file_header is None:
                self._file_header = FileHeader()

    def _read_bar(self, reader):
        """
        读取Bar
        :param reader:
        :return:
        """
        bar = Bar()
        bar.begin_time = CSharpUtils.convert_c_sharp_ticks_to_py_date_time(reader.read_int64())
        bar.end_time = CSharpUtils.convert_c_sharp_ticks_to_py_date_time(reader.read_int64())
        bar.trading_date = CSharpUtils.convert_c_sharp_ticks_to_py_date_time(reader.read_int64())
        bar.open = reader.read_double()
        bar.close = reader.read_double()
        bar.high = reader.read_double()
        bar.low = reader.read_double()
        bar.pre_close = reader.read_double()
        bar.volume = reader.read_double()
        bar.turnover = reader.read_double()
        bar.open_interest = reader.read_double()
        bar.instrument_id = self._instrument_id
        # bar.IsCompleted = True

        return bar

    def read_all(self, bar_series):
        """

        :param bar_series:
        :return:
        """
        if bar_series is None:
            raise Exception("BarSeries Is Empty.")

        reader = BinaryReader(self._file_stream)
        self._file_header.read(reader)
        begin_date = self._file_header.begin_trading_day
        end_date = self._file_header.end_trading_day

        return self.read_trading_days(bar_series, begin_date, end_date)

    def read_trading_day(self, bar_series, trading_day):
        """
        按照交易日读取分钟线数据
        :param bar_series:分钟线数据
        :param trading_day:交易日
        :return:
        """
        if bar_series is None:
            raise Exception("BarSeries Is Empty.")

        if not isinstance(trading_day, datetime.date):
            raise Exception("Trading Day Param Error")

        read_count = 0
        trading_day = datetime.datetime(trading_day.year, trading_day.month, trading_day.day)
        reader = BinaryReader(self._file_stream)
        self._file_header.read(reader)
        if (trading_day < self._file_header.begin_trading_day) or (trading_day > self._file_header.end_trading_day):
            return False

        data = self._file_header.trading_day_indices.try_get(trading_day)
        found = data[0]
        start_offset = data[1]
        count = data[2]
        if found:
            reader.stream.seek(start_offset, 0)
            while count > 0:
                bar = self._read_bar(reader)
                bar_series.append(bar)
                count -= 1
                read_count += 1

        return read_count > 0

    def read_trading_days(self, bar_series, begin_trading_day, end_trading_day):
        """
        按照交易日区间读取分钟线数据
        :param bar_series:分钟线数据
        :param begin_trading_day:开始交易日
        :param end_trading_day:结束交易日
        :return:
        """
        if bar_series is None:
            raise Exception("BarSeries Is Empty.")

        if not isinstance(begin_trading_day, datetime.date):
            raise Exception("BeginTradingDay Param Error.")

        if not isinstance(end_trading_day, datetime.date):
            raise Exception("EndTradingDay Param Error.")

        begin_trading_day = datetime.datetime(begin_trading_day.year, begin_trading_day.month, begin_trading_day.day)
        end_trading_day = datetime.datetime(end_trading_day.year, end_trading_day.month, end_trading_day.day)

        if begin_trading_day > end_trading_day:
            raise Exception("EndTradingDay Must Be Larger Than BeginTradingDay")

        if begin_trading_day == end_trading_day:
            return self.read_trading_day(bar_series, begin_trading_day)

        read_count = 0
        reader = BinaryReader(self._file_stream)
        self._file_header.read(reader)
        if (end_trading_day < self._file_header.begin_trading_day) or (begin_trading_day > self._file_header.end_trading_day):
            return False

        if begin_trading_day < self._file_header.begin_trading_day:
            begin_trading_day = self._file_header.begin_trading_day

        if end_trading_day > self._file_header.end_trading_day:
            end_trading_day = self._file_header.end_trading_day

        data = self._file_header.trading_day_indices.get_trading_day_offsets(begin_trading_day, end_trading_day)
        found = data[0]
        start_offset = data[1]
        end_offset = data[2]
        start_count = data[3]
        end_count = data[4]
        if found:
            end_offset += self.BarLength * end_count
            reader.stream.seek(start_offset, 0)
            while reader.stream.tell() < end_offset:
                bar = self._read_bar(reader)
                bar_series.append(bar)
                read_count += 1

        return read_count > 0

    def _update_file_header(self, bar_series, start, length):
        start_bar = bar_series[start]
        end_bar = bar_series[start + length - 1]
        if self._file_header.begin_time == datetime.datetime.max or start_bar.begin_time < self._file_header.begin_time:
            self._file_header.begin_time = start_bar.begin_time
            self._file_header.mark_as_dirty(True)

        if self._file_header.end_time == datetime.datetime.max or start_bar.end_time > self._file_header.end_time:
            self._file_header.end_time = end_bar.end_time
            self._file_header.mark_as_dirty(True)
        self._file_header.bar_count += length

    def _write(self, bar_series, start, length, offset):
        if bar_series is None:
            raise Exception("Argument Null Exception:bar_series")
        if length < 0:
            raise Exception("Argument Null Exception:length")
        if start < 0 or (start + length > len(bar_series)):
            raise Exception("Argument Null Exception:start")
        writer = BinaryWriter(self._file_stream)
        writer.stream.seek(offset, 0)
        self._writer_bars(writer, bar_series, 0, length)

    def _writer_bars(self, writer, bar_series, start, length):
        for i in range(start, length, 1):
            bar = bar_series[i]
            trading_date = datetime.datetime(bar.trading_date.year, bar.trading_date.month, bar.trading_date.day)
            if self._file_header.begin_trading_day == datetime.datetime.max or trading_date < self._file_header.begin_trading_day:
                self._file_header.begin_trading_day = trading_date
                self._file_header.mark_as_dirty(True)
            if self._file_header.end_trading_day == datetime.datetime.max or trading_date > self._file_header.end_trading_day:
                self._file_header.end_trading_day = trading_date
                self._file_header.mark_as_dirty(True)
            offset = writer.stream.tell()
            self._file_header.natural_day_indices.add(bar.begin_time, offset)
            self._file_header.trading_day_indices.add(bar.trading_date, offset)
            writer.write_int64(CSharpUtils.get_c_sharp_ticks(bar.begin_time))
            writer.write_int64(CSharpUtils.get_c_sharp_ticks(bar.end_time))
            writer.write_int64(CSharpUtils.get_c_sharp_ticks(bar.trading_date))
            writer.write_double(bar.open)
            writer.write_double(bar.close)
            writer.write_double(bar.high)
            writer.write_double(bar.low)
            writer.write_double(bar.pre_close)
            writer.write_double(bar.volume)
            writer.write_double(bar.turnover)
            writer.write_double(bar.open_interest)
        self._file_header.write(writer)

    def writer(self, bar_series):
        self._write(bar_series, 0, len(bar_series), FileHeader.FileHeaderTotalSize)