class ModuleInput:

    def __init__(self, bbf=None):
        self.version = 1
        self.type = 1

        self.bbf = bbf if bbf else bytearray()
        self.pointer = 0

    def serialize(self, stdin, arguments, files):
        bbf_data = bytearray()
        bbf_data += self.version.to_bytes(1, 'big')
        bbf_data += self.type.to_bytes(1, 'big')

        bbf_data += len(stdin).to_bytes(8, 'big')

        argument_len = sum([len(arg.encode()) for arg in arguments]) + (2 * len(arguments))
        bbf_data += argument_len.to_bytes(4, 'big')

        file_data_len = sum([len(data) + len(path.encode()) for path, data in files.items()]) + (12 * len(files))
        bbf_data += file_data_len.to_bytes(8, 'big')

        bbf_data += stdin

        for argument in arguments:
            bbf_data += len(argument).to_bytes(2, 'big')
            bbf_data += argument.encode()

        for path, data in files.items():
            bbf_data += len(path.encode()).to_bytes(4, 'big')
            bbf_data += len(data).to_bytes(8, 'big')

            bbf_data += path.encode()
            bbf_data += data

        return bbf_data

    def get_data(self, offset, type='bytes'):
        bytes = self.bbf[self.pointer:self.pointer + offset]
        self.pointer += offset
        if type == 'str':
            return bytes.decode()
        elif type == 'int':
            return int.from_bytes(bytes, 'big')
        else:
            return bytes

    def deserialize(self):
        version = self.get_data(1, type='int')
        if version != self.version:
            raise Exception(f'Unsupported BioLib Binary Format version: Got {version} expected {self.version}')

        type = self.get_data(1, type='int')
        if type != self.type:
            raise Exception(f'Unsupported BioLib Binary Format type: Got {type} expected {self.type}')

        stdin_len = self.get_data(8, type='int')
        argument_data_len = self.get_data(4, type='int')
        files_data_len = self.get_data(8, type='int')
        stdin = self.get_data(stdin_len)

        end_of_arguments = self.pointer + argument_data_len
        arguments = []
        while self.pointer != end_of_arguments:
            argument_len = self.get_data(2, type='int')
            argument = self.get_data(argument_len, type='str')
            arguments.append(argument)

        end_of_files = self.pointer + files_data_len
        files = {}
        while self.pointer < end_of_files:
            path_len = self.get_data(4, type='int')
            data_len = self.get_data(8, type='int')
            path = self.get_data(path_len, type='str')
            data = self.get_data(data_len)
            files[path] = bytes(data)

        return {'stdin': stdin, 'arguments': arguments, 'files': files}
