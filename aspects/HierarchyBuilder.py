import codecs

import math


class HierarchyBuilder:
    @staticmethod
    def calculate_average_semantic_distance_ideal_tree(db):
        row_semantic_distance_ideal = db.cursor_semantic_distance_ideal.execute('SELECT * FROM Distance').fetchone()
        avg = 0
        count = 0
        while row_semantic_distance_ideal is not None:
            count += 1
            avg += float(row_semantic_distance_ideal[2])
            row_semantic_distance_ideal = db.cursor_semantic_distance_ideal.fetchone()
        average_semantic_distance_ideal = avg / count
        return average_semantic_distance_ideal

    def process(self, db, average_semantic_distance_ideal):
        db.create_hierarchy_db()
        self.build_hierarchy(db, average_semantic_distance_ideal)

    def build_hierarchy(self, db, average_semantic_distance_ideal):
        free_nodes = self.find_free_nodes()
        for node in free_nodes:
            row_semantic_distance = db.cursor_semantic_distance.execute(
                'SELECT * FROM Distance WHERE aspect1 = ? OR aspect2 = ?', (node, node,)).fetchone()
            while row_semantic_distance is not None:
                # add as children those whose semantic distance is less them average distance in ideal tree
                if row_semantic_distance[2] <= math.sqrt(average_semantic_distance_ideal):
                    aspect1 = row_semantic_distance[0]
                    aspect2 = row_semantic_distance[1]
                    if aspect1 == node:
                        db.add_hierarchy(node, aspect2)
                        free_nodes.append(aspect2)
                    else:
                        db.add_hierarchy(node, aspect1)
                        free_nodes.append(aspect1)
                row_semantic_distance = db.cursor_semantic_distance.fetchone()
            db.conn_hierarchy.commit()

    @staticmethod
    def find_free_nodes():
        import os
        free_nodes = []
        path = os.getcwd()
        filenames = os.listdir(path + "/../productTrees/Tree")
        os.chdir(path + "/../productTrees/Tree")
        filenames.remove(".DS_Store")
        filenames.remove("Subcategories.txt")
        for filename in filenames:
            lines = codecs.open(filename, 'r', 'cp1251').readlines()
            max_ind = 2  # max depth index of file
            for line in lines:
                arr = line.split(";")
                arr[2] = arr[2].replace("\r\n", "")
                if str(max_ind) in arr and arr[0] not in free_nodes:  # the node is the free one for concrete file
                    free_nodes.append(arr[0])
        return free_nodes
