import gdb
import struct


class node:
    def __init__(self, addr):
        self.addr = addr
        self.data = 0
        self.next = 0

        inferior = gdb.inferiors()[0]

        mem = inferior.read_memory(addr, 16);
        (self.data, _, self.next) = struct.unpack("<IIQ", mem)

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
