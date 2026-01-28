from datetime import datetime,date
class Util():
    INPUT_FORMAT = "%H:%M"
    OUTPUT_FORMAT = "%I:%M %p"
    @staticmethod
    def convertDate(datev,fmt='%d-%m-%Y'):
       if datev is None:
            return
       if isinstance(datev, (date, datetime)):
            return datev.strftime(fmt)
   

   

    @classmethod
    def to_ampm(cls, slot: str) -> str:
        """
        Converts '11:00-13:00' -> '11:00 AM - 01:00 PM'
        """
        if not slot or "-" not in slot:
            return ""

        try:
            start, end = slot.split("-")

            start_time = datetime.strptime(start.strip(), cls.INPUT_FORMAT)
            end_time = datetime.strptime(end.strip(), cls.INPUT_FORMAT)

            return f"{start_time.strftime(cls.OUTPUT_FORMAT)} - {end_time.strftime(cls.OUTPUT_FORMAT)}"

        except ValueError:
            return slot  # fallback to original if parsing fails
   
