# python-dsf(ddsf)

## installation
```
pip install ddsf
```

## usage

```
# inititate connection
dsf = Ddsf(url, user, password)
```

### rooms
```
# get all rooms
rooms = dsf.rooms()

# print room attributes
for room in dsf.rooms():
    print(room.data)
    # OR
    print(room.pretty())

# edit room attributes
for room in dsf.rooms():
    room.RoomName = "NewName"
    room.update()
```

