#-*- encoding: utf-8 -*-
class Cmd_spliter(object):
    elements = {}

    def __init__(self, text):
        self.from_str(text)

    def from_str(self, str):
        parts = str.split("<<<name>>>")
        print(parts)

        for each in parts:
            if '' != each:
                arr = each.split("<<<name/>>>\n")
                if arr == None:
                    pass
                elif len(arr) >= 2:
                    print(arr)
                    # print('name:', arr[0])
                    # print('elements:', arr[1])
                    self.elements[arr[0]] = arr[1]
                else:
                    pass
        print(self.elements)

    def count(self):
        # print(self.elements)
        return len(self.elements)

    def del_key(self, key):
        self.elements.pop(key)

    def add_key(self, key, text):
        # TODO: should check and delete same
        self.elements[key] = text

    def text_by_key(self, key):
        return self.elements[key]

    def content(self):
        return self.elements #dict

    def clear(self):
        return self.elements.clear()

    def to_str(self):
        text = ""
        for key, value in self.elements.items():
            print(key, value)
            text = text + "<<<name>>>" + key + "<<<name/>>>\n" + value
        return text