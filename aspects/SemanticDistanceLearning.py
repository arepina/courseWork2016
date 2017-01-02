

class SemanticDistanceLearning:

    def ground_truth_distance(self):
        import os
        path = os.getcwd()
        filenames = os.listdir(path + "/../productTrees/Subcategories old")
        os.chdir(path + "/../productTrees/Subcategories old")
        for filename in filenames:
            with open(filename) as f:
                lines = f.readlines()
            f = open(filename, 'w')
            for line in lines:
                str = line + ";2"
                f.write(str)

            #tree = self.build_tree(lines)