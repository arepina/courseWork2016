

class SemanticDistanceLearning:

    def ground_truth_distance(self):
        import os
        path = os.getcwd()
        filenames = os.listdir(path + "\\..\\productTrees\\Subcategories old")
        os.chdir(path + "\\..\\productTrees\\Subcategories old")
        for filename in filenames:
            f = open(filename, 'r')
            lines = f.readlines()
            f.close()
            for line in lines:
                r = 42
                #tree = self.build_tree(lines)