First Page:
  -> List all the doctors (get Doctors API)
  -> List the filters  (get Filters API)
Second Page (Selected a doctor): 
  -> List Available Slots (get availibility slots) 
      params: Doctor id, start date time, end date time(Optional, Default would be start_time + 1 month)
      return: {
        "time_slots": [
            {
                "start_time":"",
                "end_time":"",
                "Day":"",
                "slot_length":""
            },
            ...
        ]
      }
Third Page (Selected a Slot)
    -> Fill out the paitent form 
    -> Book Apointment (book_apointment API)
        params: paitent_id, Doctor_id , start_time, end_time
