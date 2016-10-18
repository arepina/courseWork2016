class Review(object):
    def __init__(self, pro, text, contra, id, agree, grade, visibility, priceGrade,
                 anonymous, region, date, qualityGrade, convenienceGrade, reject, usageTime):
        self.pro = pro
        self.text = text
        self.contra = contra
        self.id = id
        self.agree = agree
        self.grade = grade
        self.visibility = visibility
        self.priceGrade = priceGrade
        self.anonymous = anonymous
        self.region = region
        self.date = date
        self.qualityGrade = qualityGrade
        self.convenienceGrade = convenienceGrade
        self.reject = reject
        self.usageTime = usageTime