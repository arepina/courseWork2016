class HierarchyBuilder:

    def calculate_average_semantic_distance_ideal_tree(self, db):
        row_semantic_distance_ideal = db.cursor_semantic_distance_ideal.execute('SELECT * FROM Distance').fetchone()
        avg = 0
        count = 0
        while row_semantic_distance_ideal is not None:
            count += 1
            avg += float(row_semantic_distance_ideal[2])
            row_semantic_distance_ideal = db.cursor_semantic_distance_ideal.fetchone()

    def build_hierachy(self):
        # find free nodes
        # for each node iterate through all aspects list pairs with this node
        # add as children those whose semantic distance is less them average distance in ideal tree
        pass
