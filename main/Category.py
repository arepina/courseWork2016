class Category(object):
    def __init__(self, name, parentId, uniqName, offersNum, visual, modelsNum, childrenCount, type, advertisingModel,
                 link, id):
        self.name = name
        self.parentId = parentId
        self.uniqName = uniqName
        self.offersNum = offersNum
        self.visual = visual
        self.modelsNum = modelsNum
        self.childrenCount = childrenCount
        self.type = type
        self.advertisingModel = advertisingModel
        self.link = link
        self.id = id
