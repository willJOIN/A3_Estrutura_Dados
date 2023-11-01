from collections import deque

SYMBOL_TABLE = {
    'i': 1,
    'v': 5,
    'x': 10,
    'l': 50,
    'c': 100,
    'd': 500,
    'm': 1000
}


def rom_parse(val):
  val = val.lower().strip()
  if val == 'n':
    return 0
  running_sum = 0
  largest_place = 0
  previous_vals = deque(maxlen=3)
  for i in range(-1, -1 * (len(val) + 1), -1):
    # iterate from right to left
    c = val[i]
    # get numeric value assigned to this character
    numeric_val = SYMBOL_TABLE.get(c)
    if not numeric_val:
      # raise exception if invalid character provided
      raise ValueError('Unable to parse invalid roman numeral "' + val +
                       '", found illegal character "' + c + '"')

    if len(previous_vals) == 3 and all(n == c for n in previous_vals):
      # this is now the 4th matching character in a row
      raise ValueError('Unable to parse invalid roman numeral "' + val +
                       '", found more than 3 repeating instances of "' + c +
                       '" in a row')

    if len(previous_vals) > 0:
      most_recent = SYMBOL_TABLE.get(previous_vals[-1])
      if most_recent <= numeric_val:
        running_sum += numeric_val
        if numeric_val > largest_place:
          largest_place = numeric_val
        elif numeric_val < largest_place:
          raise ValueError(
              'Unable to parse invalid roman numeral "' + val +
              '", invalid ordering. Irregular subtractive notation not allowed.'
          )
      else:  # most_recent > numeric_val
        running_sum -= numeric_val
    else:
      running_sum += numeric_val
      largest_place = numeric_val
    previous_vals.append(c)  # always appened to deque when done
  return running_sum
