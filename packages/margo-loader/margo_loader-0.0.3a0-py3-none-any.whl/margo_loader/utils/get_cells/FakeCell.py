"""
TODO - Just use the class in nbformat that is used for cells. 
I am not familiar with the code base so I couldn't quickly 
find its definition and this was faster for now.

"""


class FakeCell:
    def __init__(self):
        self.cell_type = "code"
        self.source = ""

    def append_source(self, source: str):
        self.source += source

    def __str__(self):
        return self.source
