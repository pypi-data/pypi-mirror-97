"""
``hdrs`` module for HTTP header parsing functions.
"""

__all__ = [
  "is_user_agent"
]

from python_http_parser.__private import trim_and_lower

def is_user_agent(hdr_line):
  """Return whether the ``hdr_line`` argument contains a User-Agent header.

  This function only checks the first 10 characters of ``hdr_line``;
  no newlines are allowed.
  """
  if type(hdr_line) is not str:
    raise TypeError('hdr_line is not a string!')
  elif len(hdr_line) < 18:
    # Let's pretend that a User-Agent header must be at least 18
    # characters long.
    return False

  first_10_chars = trim_and_lower(hdr_line[:11])

  if first_10_chars == 'user-agent':
    return True

  return False
