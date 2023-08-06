def saurify(pilot: str):
  pilot_array = pilot.split(" ")
  pilot_array.reverse()
  saurified_pilot = " ".join(pilot_array)
  return saurified_pilot
