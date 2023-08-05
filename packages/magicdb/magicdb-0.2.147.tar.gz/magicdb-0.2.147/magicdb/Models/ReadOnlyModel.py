from magicdb.Models import MagicModelSpeed


class ReadOnlyModel(MagicModelSpeed):
    def save(self, *args, **kwargs):
        print("READ ONLY MODEL SO SAVE WILL NOT WORK.")

    def update(self, *args, **kwargs):
        print("READ ONLY MODEL SO UPDATE WILL NOT WORK.")

    def delete(self, *args, **kwargs):
        print("READ ONLY MODEL SO DELETE WILL NOT WORK.")
