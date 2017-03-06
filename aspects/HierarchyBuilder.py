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

    # def process_ideal(self, db):
    #     db.create_hierarchy_ideal_db()
    #     self.build_hierarchy_ideal(db)
    #
    # def build_hierarchy_ideal(self, db):
    #     pass

    def build_hierarchy(self, db, average_semantic_distance_ideal):
        free_nodes = self.find_free_nodes()
        for node in free_nodes:
            row_semantic_distance = db.cursor_semantic_distance.execute('SELECT * FROM Distance WHERE aspect1 = ? OR aspect2 = ?', (node, node,)).fetchone()
            while row_semantic_distance is not None:
                # add as children those whose semantic distance is less them average distance in ideal tree
                if row_semantic_distance[2] <= average_semantic_distance_ideal:
                    aspect1 = row_semantic_distance[0]
                    aspect2 = row_semantic_distance[1]
                    if aspect1 == node:
                        db.add_hierarchy(node, aspect2)
                    else:
                        db.add_hierarchy(node, aspect1)
                row_semantic_distance = db.cursor_semantic_distance.fetchone()
            db.conn_hierarchy.commit()

    @staticmethod
    def find_free_nodes():
        import os
        free_nodes = []
        path = os.getcwd()
        filenames = os.listdir(path + "/../productTrees/Tree")
        os.chdir(path + "/../productTrees/Tree")
        for filename in filenames:
            with open(filename) as f:
                lines = f.readlines()
            max_ind = 2  # max index of file 
            if 3 in lines:
                max_ind = 3
            for line in lines[0].split("\n"):
                arr = line.split(";")
                for val in arr:
                    if max_ind in arr and val not in free_nodes:  # the node is the free one for concrete file
                        free_nodes.append(val)
        return free_nodes




