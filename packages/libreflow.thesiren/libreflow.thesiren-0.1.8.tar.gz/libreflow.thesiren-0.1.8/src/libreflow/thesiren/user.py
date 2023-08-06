from kabaret import flow


class MyBookmarks(flow.DynamicMap):
    pass

class User(flow.Object):
    who_am_i = flow.Computed()
    my_bookmarks = flow.Child(MyBookmarks)