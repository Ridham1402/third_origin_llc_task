import datetime
import pytz


class DateUtility:
    def __init__(
            self, 
            holidays_file : str
            ):
        """
        Initializes the DateUtility class with holidays data loaded from the specified file.
        :param holidays_file: Path to the holidays data file
        :type holidays_file: str
        """
        self.holidays = self.load_holidays(holidays_file)


    def load_holidays(
            self, 
            holidays_file : str
            ) -> dict:
        """
        Loads holidays data from the specified file and returns a dictionary of holidays.
        :param holidays_file: Path to the holidays data file
        :type holidays_file: str
        :return: Dictionary containing holidays data
        :rtype: dict
        """
        holidays = {}
        with open(holidays_file, 'r') as file:
            lines = file.readlines()[1:]  # Exclude header line
            for line in lines:
                timezone, date_str, holiday = line.strip().split(', ')
                date = datetime.datetime.strptime(date_str, "%Y%m%d").date()
                if timezone not in holidays:
                    holidays[timezone] = {}
                holidays[timezone][date] = holiday
        return holidays


    def convert_dt(
            self, 
            from_date : datetime.datetime, 
            from_date_TZ : str, 
            to_date_TZ : str
            ) -> datetime.datetime:
        """
        Converts a datetime from one timezone to another.
        :param from_date: The datetime to convert
        :type from_date: datetime.datetime
        :param from_date_TZ: Timezone of the source datetime
        :type from_date_TZ: str
        :param to_date_TZ: Timezone of the target datetime
        :type to_date_TZ: str
        :return: The converted datetime in the target timezone
        :rtype: datetime.datetime
        """
        from_timezone = pytz.timezone(from_date_TZ)
        to_timezone = pytz.timezone(to_date_TZ)
        from_date = from_timezone.localize(from_date)
        return from_date.astimezone(to_timezone)


    def add_dt(
            self, 
            from_date : datetime.datetime, 
            number_of_days: int
            ) -> datetime.datetime:
        """
        Adds the specified number of days to the given date.
        :param from_date: The starting datetime
        :type from_date: datetime.datetime
        :param number_of_days: The number of days to add
        :type number_of_days: int
        :return: The resulting datetime after adding the specified number of days
        :rtype: datetime.datetime
        """
        return from_date + datetime.timedelta(days=number_of_days)


    def sub_dt(
            self, 
            from_date : datetime.datetime, 
            number_of_days : int
            ) -> datetime.datetime:
        """
        Subtracts the specified number of days from the given date.
        :param from_date: The starting datetime
        :type from_date: datetime.datetime
        :param number_of_days: The number of days to subtract
        :type number_of_days: int
        :return: The resulting datetime after subtracting the specified number of days
        :rtype: datetime.datetime
        """
        return from_date - datetime.timedelta(days=number_of_days)


    def get_days(
            self, 
            from_date : datetime.datetime, 
            to_date : datetime.datetime
            ) -> int:
        """
        Calculates the number of days between two dates.
        :param from_date: The starting date
        :type from_date: datetime.datetime
        :param to_date: The ending date
        :type to_date: datetime.datetime
        :return: The number of days between the two dates
        :rtype: int
        """
        return (to_date - from_date).days


    def get_days_exclude_we(
            self, 
            from_date : datetime.datetime, 
            to_date : datetime.datetime
            ) -> int:
        """
        Calculates the number of days between two dates excluding weekends.
        :param from_date: The starting datetime
        :type from_date: datetime.datetime
        :param to_date: The ending datetime
        :type to_date: datetime.datetime
        :return: The number of days between the two dates excluding weekends
        :rtype: int
        """
        days = (to_date - from_date).days
        weekends = self.count_weekends(from_date, to_date)
        return days - weekends


    def count_weekends(
            self, 
            from_date : datetime.datetime, 
            to_date : datetime.datetime
            ) -> int:
        """
        Counts the number of weekends (Saturday and Sunday) between two dates.
        :param from_date: The starting datetime
        :type from_date: datetime.datetime
        :param to_date: The ending datetime
        :type to_date: datetime.datetime
        :return: The number of weekends between the two dates
        :rtype: int
        """
        weekends = 0
        current_date = from_date
        while current_date <= to_date:
            if current_date.weekday() >= 5:  # Saturday (5) or Sunday (6)
                weekends += 1
            current_date += datetime.timedelta(days=1)
        return weekends


    def get_days_since_epoch(
            self, 
            from_date : datetime.datetime
            ) -> int:
        """
        Calculates the number of days between the specified date and the epoch (January 1, 1970).
        :param from_date: The date to calculate the days since the epoch
        :type from_date: datetime.datetime
        :return: The number of days since the epoch
        :rtype: int
        """
        epoch = datetime.datetime.utcfromtimestamp(0)
        return (from_date - epoch).days


    def is_holiday(
            self, 
            date : datetime.datetime, 
            timezone : str
            ) -> bool:
        """
        Checks if the specified date is a holiday in the given timezone.
        :param date: The date to check
        :type date: datetime.datetime
        :param timezone: The timezone to consider for holidays
        :type timezone: str
        :return: True if the date is a holiday, False otherwise
        :rtype: bool
        """
        if timezone in self.holidays and date in self.holidays[timezone]:
            return True
        return False

    def get_business_days(
            self, 
            from_date : datetime.datetime, 
            to_date : datetime.datetime
            ) -> int:
        """
        Calculates the number of business days (excluding weekends and holidays) between two dates.
        :param from_date: The starting datetime
        :type from_date: datetime.datetime
        :param to_date: The ending datetime
        :type to_date: datetime.datetime
        :return: The number of business days between the two dates
        :rtype: int
        """
        current_date = from_date
        business_days = 0
        while current_date <= to_date:
            if current_date.weekday() < 5 and not self.is_holiday(current_date, "US/Eastern"):
                business_days += 1
            current_date += datetime.timedelta(days=1)
        return business_days




#Instance of above class "DateUtility" and its various functions

utility = DateUtility("holidays.dat")       #Mention the path of holidays file as argument while initiating the class

from_date = datetime.datetime(2022, 12, 22)
to_date = datetime.datetime(2023, 1, 2)

converted_date = utility.convert_dt(from_date, "UTC", "US/Eastern")
print("Converted Date:", converted_date)

added_date = utility.add_dt(from_date, 11)
print("Added Date:", added_date)

subtracted_date = utility.sub_dt(from_date, 33)
print("Subtracted Date:", subtracted_date)

days = utility.get_days(from_date, to_date)
print("Number of Days:", days)

days_exclude_we = utility.get_days_exclude_we(from_date, to_date)
print("Number of Days (excluding weekends):", days_exclude_we)

days_since_epoch = utility.get_days_since_epoch(from_date)
print("Days since EPOCH:", days_since_epoch)

business_days = utility.get_business_days(from_date, to_date)
print("Number of Business Days (excluding holidays):", business_days)
