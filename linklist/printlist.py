import gdb
import struct


class node:
    def __init__(self, addr):
        self.addr = addr

        self.sizeof = 0
        self.data = 0
        self.data_offset = 0
        self.data_sizeof = 0

        self.next = 0
        self.next_offset = 0
        self.next_sizeof = 0

        inferior = gdb.inferiors()[0]
        self.sizeof = gdb.lookup_type("struct node").sizeof
        mem = inferior.read_memory(addr, self.sizeof)
        (self.data, _, self.next) = struct.unpack("<IIQ", mem)

        self.data_offset = gdb.parse_and_eval("(int)&((struct node *)0)->data")
        assert(self.data_offset == 0)
        assert(gdb.lookup_type("struct node").fields()[0].name == "data")
        self.data_sizeof = gdb.lookup_type("struct node").fields()[0].type.sizeof
        assert(self.data_sizeof == 4)
        assert(gdb.lookup_type("struct node").fields()[0].type.code == gdb.TYPE_CODE_INT)

        self.next_offset = gdb.parse_and_eval("(int)&((struct node *)0)->next")
        assert(self.next_offset == 8)
        assert(gdb.lookup_type("struct node").fields()[1].name == "next")
        self.next_sizeof = gdb.lookup_type("struct node").fields()[1].type.sizeof
        assert(self.next_sizeof == 8)
        assert(gdb.lookup_type("struct node").fields()[1].type.code == gdb.TYPE_CODE_PTR)
        

    def get_next(self):
        return self.next

    def get_data(self):
        return self.data


class print_list(gdb.Command):
    def __init__(self):
        super(print_list, self).__init__("print_list", gdb.COMMAND_DATA, gdb.COMPLETE_NONE)

    def invoke(self, arg, from_tty):
        h = gdb.parse_and_eval("l->next").cast(gdb.lookup_type('unsigned long long'))
        while True:
            if h == 0:
                break

            newnode = node(h)
            print newnode.get_data()
            h = newnode.get_next()


print_list() 
