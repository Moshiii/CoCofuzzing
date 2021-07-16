class MutateData:
    exit_keywords = ['exit', 'quit', 'q']

    def __init__(self, dataPath):
        self.snippetsList = open(dataPath).readlines()

    def getSnippetByIdx(self, idx):
        return self.snippetsList[idx]

    def getSnippetCount(self):
        return len(self.snippetsList)
