#-*- encoding: utf-8 -*-
class Cmd_spliter(object):
    elements = []

    def __init__(self, text):
        self.from_str(text)

    def from_str(self, str):
        parts = str.split("<<<name>>>")
        print(parts)
        self.clear()

        for each in parts:
            if '' != each:
                arr = each.split("<<<name/>>>\n")
                if arr == None:
                    pass
                elif len(arr) >= 2:
                    print(arr)
                    # print('name:', arr[0])
                    # print('value:', arr[1])
                    dict_ele = {}
                    dict_ele['name'] = arr[0]
                    dict_ele['value'] = arr[1]
                    self.elements.append(dict_ele)
                else:
                    pass
        print('len:', len(self.elements), self.elements)

    def count(self):
        # print(self.elements)
        return len(self.elements)

    def del_key(self, key):
        pass #TODO

    def add_key(self, key, text):
        # TODO: should check and delete same
        print(key, text)
        dict_ele={}
        dict_ele['name'] = key
        dict_ele['value'] = text
        print(dict_ele)
        self.elements.append(dict_ele)

    def text_by_key(self, key):
        return self.elements[key]

    def content(self):
        return self.elements #dict in list

    def clear(self):
        self.elements.clear()

    def to_str(self):
        text = ""
        for each in self.elements:
            print(each['name'], each['value'])
            text = text + "<<<name>>>" + each['name'] + "<<<name/>>>\n" + each['value']
        return text