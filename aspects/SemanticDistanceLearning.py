

class SemanticDistanceLearning:

    def ground_truth_distance(self, db):
        import os
        path = os.getcwd()
        filenames = os.listdir(path + "\\..\\productTrees\\Subcategories old")
        os.chdir(path + "\\..\\productTrees\\Subcategories")
        all_files_content = []
        for filename in filenames:  # load the aspects from all files
            with open(filename) as f:
                all_files_content.append(f.readlines())
        os.chdir(path + "\\..\\productTrees\\Subcategories old")
        i = 0
        for filename in filenames:  # iterate through all the files to calculate the path weights
            f = open(filename)
            file_content = str(all_files_content[i]).split(";")
            for i in range(0, len(file_content)):
                node = file_content[i]
                for j in range(i + 1, len(file_content)):
                    next_node = file_content[j]
                    path_weight = self.find_path(node, next_node, filename)
                    try_to_find_same_row = db.cursor_path_weight.execute("SELECT * FROM Weight WHERE aspect1 = ? AND aspect2 = ?", (node, next_node,))
                    if try_to_find_same_row is None:
                        db.add_path_weight(node, next_node, path_weight)
                    else:
                        # compare the deep and overwrite the min
                        r = 42
            i += 1
            f.close()

    def find_path(self, node, next_node, filename):
        with open(filename) as f:
            content = f.readlines()
        parent_name = ""
        parent_name_next = ""
        deep_num_node = 0
        deep_num_node_next = 0
        for line in content:
            arr = line.split(";")
            word1 = arr[0]
            word2 = arr[1]
            deep_num = arr[2]
            if node == word1:
                parent_name = word2
                deep_num_node = deep_num
            if next_node == word1:
                parent_name_next = word2
                deep_num_node_next = deep_num
        if len(parent_name) == 0:
            deep_num_node = 1
        if len(parent_name_next) == 0:
            deep_num_node_next = 1
        if parent_name == parent_name_next:
            return 2
        else:
            return deep_num_node + deep_num_node_next