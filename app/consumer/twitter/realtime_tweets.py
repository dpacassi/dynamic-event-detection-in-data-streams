from api import api

stream = api.GetStreamSample()

for message in stream:
    print(message)
