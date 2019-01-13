class IntermediateDataWriter:
    def __init__(self, write_file_name, url, collection_name, films_list):
        self.file_name = 'raw_data/{0}.py'.format(write_file_name)
        self.url = url
        self.collection_name = collection_name
        self.films_list = films_list
        return

    def perform(self):
        file = open(self.file_name, 'w')
        file.write("LINK = '{0}'\n".format(self.url))
        file.write("NAME = '{0}'\n".format(self.collection_name))
        file.write('MOVIES = [\n')
        for file_dict in self.films_list:
            file.write('   {0},\n'.format(str(file_dict)))
        file.write(']\n')
        file.close()
        print('Data to {0} successfully written'.format(self.file_name))
        return
