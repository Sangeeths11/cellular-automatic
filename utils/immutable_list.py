class ImmutableList[T]:
    """
    List which cannot be modified, inspired by https://stackoverflow.com/questions/23474648/python-read-only-lists-using-the-property-decorator
    """
    def __init__(self, data: list[T]):
        """
        :param data: list to be wrapped
        """
        self._data = data

    def __getitem__(self, index: int) -> T:
        return self._data[index]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)