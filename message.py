# takes a single string (name) and arbitrarily long list of strings (args)
# that compose a protocol message, and roll them into a single string
# delimited by underscores that can be sent over the socket connection.
def make_msg(name, *args):
    msg = name
    for arg in args:
        msg = msg + "_" + arg
    return msg

# split our single long string into a list of msg_entries representing
# the protocol message type (HELLO, AUTH_FAIL, etc) and any potential
# additional information the message may be carrying (such as a client-ID)
def unwind_msg(message):
    print(message)
    entries = message.split("_")
    return entries
