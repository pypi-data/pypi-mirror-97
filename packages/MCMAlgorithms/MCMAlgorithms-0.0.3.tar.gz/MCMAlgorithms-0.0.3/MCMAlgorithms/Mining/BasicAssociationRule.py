import numpy as np


class Tool:

    def __init__(self, master, absolute_support=2, confidence=0.5):
        self.master = master
        self.master.absolute_support = absolute_support
        self.master.confidence = confidence

    def SetAbsoluteSupport(self, absolute_support):
        if absolute_support < 1:
            raise Exception
        self.master.absolute_support = absolute_support

    def SetConfidence(self, confidence):
        if confidence <= 0 or confidence > 1:
            raise Exception
        self.master.confidence = confidence

    def LoadData(self, item_order, dataset):
        # This function load the dataset,
        # item order shall be a list or tuple containing the order of the item for sorting
        # dataset shall be a list, each element of the list is a list or tuple containing an affair
        map_dict = dict.fromkeys(list(range(len(item_order))))
        anti_map_dict = dict.fromkeys(item_order)
        for idx in range(len(item_order)):
            map_dict[idx] = item_order[idx]
            anti_map_dict[item_order[idx]] = idx
        data = np.zeros((len(dataset), len(item_order)), dtype=np.int)
        for affair_idx in range(len(dataset)):
            affair = dataset[affair_idx]
            for item in affair:
                data[affair_idx, anti_map_dict[item]] = 1
        self.master.itemnum = len(item_order)
        self.master.map_dict = map_dict
        self.map_dict = map_dict
        self.master.data = data

    def GenerateRule(self):
        rules = dict()
        for depth in self.master.frequent_sets:
            frequent_sets, supports = self.master.frequent_sets[depth]
            # Calculate confidence
            for frequent_set_idx in range(frequent_sets.shape[0]):
                tabu = np.array([], dtype=np.int).reshape((0, self.master.itemnum))
                frequent_set = frequent_sets[frequent_set_idx, :]
                support = supports[frequent_set_idx, 0]
                # generate subset
                item_ptr = np.argwhere(frequent_set == 1).reshape(1, -1)
                frequent_set_num = 2 ** sum(frequent_set)
                frequent_set_ptr = [bin(x).replace('0b', '').rjust(sum(frequent_set), '0') for x in
                                    range(1, frequent_set_num - 1)]
                frequent_set_ptr = np.array([[int(char) for char in x] for x in frequent_set_ptr])
                for sub_idx in range(frequent_set_ptr.shape[0]):
                    # create subset
                    frequent_idx_choice = frequent_set_ptr[sub_idx, :]
                    to_choose_idx = (frequent_idx_choice * item_ptr).squeeze().tolist()
                    to_choose_idx = list(filter(lambda x: x, to_choose_idx))
                    subset = np.zeros((1, self.master.itemnum), dtype=np.int)
                    subset[0, to_choose_idx] = 1
                    diff_subset = np.bitwise_xor(frequent_set, subset)
                    # judge tabu
                    flag = False
                    for tabu_idx in range(tabu.shape[0]):
                        or_result = np.bitwise_or(tabu[tabu_idx, :], subset)
                        if np.all(or_result == tabu[tabu_idx, :]):
                            flag = True
                            break
                    if flag:
                        continue
                    # calculate confidence
                    subset_itemnum = np.sum(subset)
                    if not subset_itemnum:
                        continue
                    subset_candidate_table, subset_support_table = self.master.frequent_sets[subset_itemnum]
                    corresponding_idx = int(np.argwhere(np.all(subset_candidate_table == subset, axis=1)).squeeze())
                    subset_support = subset_support_table[corresponding_idx, 0]
                    confidence = support / subset_support
                    # judgement
                    if confidence >= self.master.confidence:
                        rules[tuple(subset.squeeze().tolist())] = tuple(diff_subset.squeeze().tolist())
                    else:
                        tabu = np.vstack((tabu, subset))
        self.master.rules = rules

    def OutputRule(self):
        output_rule = dict()
        for pair in self.master.rules.items():
            # transfer bin to real item
            front, back = pair
            front_items = tuple(filter(None, [self.master.map_dict[idx] if front[idx] else '' for idx in range(len(front))]))
            back_items = tuple(filter(None, [self.master.map_dict[idx] if back[idx] else '' for idx in range(len(back))]))
            output_rule[front_items] = back_items
        self.master.verbal_rules = output_rule


class Apriori:

    def __init__(self):
        self.tool = Tool(self)

    def SetAbsoluteSupport(self, absolute_support):
        self.tool.SetAbsoluteSupport(absolute_support)

    def SetConfidence(self, confidence):
        self.tool.SetConfidence(confidence)

    def LoadData(self, item_order, dataset):
        self.tool.LoadData(item_order, dataset)

    def Mining(self):
        tabu_list = np.array([], dtype=np.int).reshape(0, self.itemnum)
        candidate = np.array([], dtype=np.int).reshape(0, self.itemnum)
        supports = np.array([], dtype=np.int).reshape(0, 1)
        frequent_sets = dict()
        # First Scan
        first_cnt = np.sum(self.data, axis=0).squeeze()
        not_frequent_idx = np.argwhere(first_cnt < self.absolute_support).squeeze().tolist()
        if type(not_frequent_idx) != list:
            not_frequent_idx = [not_frequent_idx]
        for item_idx in range(self.itemnum):
            if item_idx in not_frequent_idx:
                buffer_tabu = np.zeros((1, self.itemnum), dtype=np.int)
                buffer_tabu[0, item_idx] = 1
                tabu_list = np.vstack((tabu_list, buffer_tabu))
            else:
                buffer_candidate = np.zeros((1, self.itemnum), dtype=np.int)
                buffer_candidate[0, item_idx] = 1
                candidate = np.vstack((candidate, buffer_candidate))
                supports = np.vstack((supports, first_cnt[item_idx]))
        frequent_sets[1] = (candidate, supports)
        cnt = 1
        # Repeat scanning dataset
        while candidate.shape[0]:
            # Concat for new subitemset
            round_candidate = np.array([], dtype=np.int).reshape(0, self.itemnum)
            for affair_idx in range(candidate.shape[0]):
                for compare_idx in range(affair_idx + 1, candidate.shape[0]):
                    xor_result = np.bitwise_xor(candidate[affair_idx, :], candidate[compare_idx, :])
                    if np.sum(xor_result) == 2:
                        new_set = np.bitwise_or(candidate[affair_idx, :], candidate[compare_idx, :])
                        # Check whether subset is in tabu list
                        tabu_flag = False
                        for tabu_idx in range(tabu_list.shape[0]):
                            if np.all(np.bitwise_and(new_set, tabu_list[tabu_idx, :]) == tabu_list[tabu_idx, :]):
                                tabu_flag = True
                                break
                        if tabu_flag:
                            continue
                        # Add to candidate
                        if round_candidate.shape[0]:
                            if not self.itemnum in np.sum(new_set == round_candidate, axis=1).tolist():
                                round_candidate = np.vstack((round_candidate, new_set))
                        else:
                            round_candidate = np.vstack((round_candidate, new_set))
            # Counting
            candidate = np.array([], dtype=np.int).reshape(0, self.itemnum)
            supports = np.array([], dtype=np.int).reshape(0, 1)
            for candidate_idx in range(round_candidate.shape[0]):
                this_candidate = round_candidate[candidate_idx, :]
                support = np.sum(np.all(np.bitwise_and(this_candidate, self.data) == this_candidate, axis=1))
                if support >= self.absolute_support:
                    candidate = np.vstack((candidate, this_candidate))
                    supports = np.vstack((supports, support))
                else:
                    tabu_list = np.vstack((tabu_list, this_candidate))
            cnt += 1
            if candidate.shape[0]:
                frequent_sets[cnt] = (candidate, supports)
        self.frequent_sets = frequent_sets

    def GenerateRule(self):
        self.tool.GenerateRule()

    def OutputRule(self):
        self.tool.OutputRule()
        return self.verbal_rules

    def MineRules(self):
        self.Mining()
        self.GenerateRule()
        return self.OutputRule()


class Eclat:

    def __init__(self):
        self.tool = Tool(self)

    def SetAbsoluteSupport(self, absolute_support):
        self.tool.SetAbsoluteSupport(absolute_support)

    def SetConfidence(self, confidence):
        self.tool.SetConfidence(confidence)

    def LoadData(self, item_order, dataset):
        self.tool.LoadData(item_order, dataset)

    def Mining(self):
        # First Scan
        candidate = np.array([], dtype=np.int).reshape(0, self.itemnum)
        supports = np.array([], dtype=np.int).reshape(0, 1)
        tabu_list = np.array([], dtype=np.int).reshape(0, self.itemnum)
        frequent_sets = dict()
        for item_idx in range(self.itemnum):
            new_set = np.zeros((1, self.itemnum), dtype=np.int)
            new_set[0, item_idx] = 1
            support = np.sum(self.data[:, item_idx]).reshape(-1, 1)
            if support < self.absolute_support:
                tabu_list = np.vstack((tabu_list, new_set))
            else:
                candidate = np.vstack((candidate, new_set))
                supports = np.vstack((supports, support))
        frequent_sets[1] = (candidate, supports)
        cnt = 1
        # Scanning Verticle dataset
        while candidate.shape[0]:
            # Concat and create new candidate
            round_candidate = np.array([], dtype=np.int).reshape(0, self.itemnum)
            supports = np.array([], dtype=np.int).reshape(0, 1)
            for each_candidate_idx in range(candidate.shape[0]):
                for another_candidate_idx in range(each_candidate_idx + 1, candidate.shape[0]):
                    xor_result = np.bitwise_xor(candidate[each_candidate_idx, :], candidate[another_candidate_idx, :])
                    if sum(xor_result) == 2:
                        new_set = np.bitwise_or(candidate[each_candidate_idx, :], candidate[another_candidate_idx, :])
                        # Check whether subset is in tabu list
                        tabu_flag = False
                        for tabu_idx in range(tabu_list.shape[0]):
                            if np.all(np.bitwise_and(new_set, tabu_list[tabu_idx, :]) == tabu_list[tabu_idx, :]):
                                tabu_flag = True
                                break
                        if tabu_flag:
                            continue
                        # Get the affair list and compare with absolute support
                        bench = np.ones((self.data.shape[0], 1), dtype=np.int).squeeze()
                        for item_idx in range(self.itemnum):
                            if new_set[item_idx]:
                                bench = np.bitwise_and(bench, self.data[:, item_idx])
                        support = np.array([np.sum(bench)]).reshape(-1, 1)
                        if support < self.absolute_support:
                            tabu_list = np.vstack((tabu_list, new_set))
                        else:
                            # Add to candidate
                            if round_candidate.shape[0]:
                                if not self.itemnum in np.sum(new_set == round_candidate, axis=1).tolist():
                                    round_candidate = np.vstack((round_candidate, new_set))
                                    supports = np.vstack((supports, support))
                            else:
                                round_candidate = np.vstack((round_candidate, new_set))
                                supports = np.vstack((supports, support))
            cnt += 1
            candidate = round_candidate
            if candidate.shape[0]:
                frequent_sets[cnt] = (candidate, supports)
        self.frequent_sets = frequent_sets

    def GenerateRule(self):
        self.tool.GenerateRule()

    def OutputRule(self):
        self.tool.OutputRule()
        return self.verbal_rules

    def MineRules(self):
        self.Mining()
        self.GenerateRule()
        return self.OutputRule()


class FPGrowth:

    class FPTreeLeafNode:

        def __init__(self, parent, itemnum, item):
            self.parent = parent
            self.children_nodes = []
            self.children_items = np.array([], dtype=np.int).reshape(0, itemnum)
            self.item = item
            self.cnt = 0

        def AddChildren(self, children_node):
            self.children_items = np.vstack((self.children_items, children_node.item))
            self.children_nodes.append(children_node)

        def PassWay(self):
            self.cnt += 1

    class FPTreeRootNode:

        def __init__(self, itemnum):
            self.parent = None
            self.children_nodes = []
            self.children_items = np.array([], dtype=np.int).reshape(0, itemnum)
            self.item = np.zeros((1, itemnum), dtype=np.int).squeeze()

        def AddChildren(self, children_node):
            self.children_nodes.append(children_node)
            self.children_items = np.vstack((self.children_items, children_node.item))

        def PassWay(self):
            pass

    def __init__(self):
        self.tool = Tool(self)

    def SetAbsoluteSupport(self, absolute_support):
        self.tool.SetAbsoluteSupport(absolute_support)

    def SetConfidence(self, confidence):
        self.tool.SetConfidence(confidence)

    def LoadData(self, item_order, dataset):
        self.tool.LoadData(item_order, dataset)

    def MineSubFPTree(self, item_nodes, target_item):
        item_nodes = item_nodes.copy()
        item_node = item_nodes[target_item]
        candidate = np.array([], dtype=int).reshape(0, self.itemnum)
        supports = np.array([], dtype=np.int).reshape(0, 1)
        # Check whether this point is a frequent set
        cnt = 0
        for each_node in item_node:
            cnt += each_node.cnt
        if cnt >= self.absolute_support:
            node_candidate = np.array(target_item).reshape(1, -1)
            candidate = np.vstack((candidate, node_candidate))
            supports = np.vstack((supports, cnt))
            # Construct Conditional FPTree dataset
            dataset = np.array([], dtype=np.int).reshape(0, self.itemnum)
            for each_node in item_node:
                bench = np.zeros((1, self.itemnum), dtype=np.int).squeeze()
                support = each_node.cnt
                tree_node = each_node.parent
                while tree_node.parent != None:
                    bench = np.bitwise_or(bench, tree_node.item)
                    tree_node = tree_node.parent
                if np.sum(bench):
                    bench = np.repeat(np.expand_dims(bench, axis=1), support, axis=1).T
                    dataset = np.vstack((dataset, bench))
            # Construct conditional FPTree
            root = self.FPTreeRootNode(self.itemnum)
            sub_item_nodes = dict()
            for affair_idx in range(dataset.shape[0]):
                affair = dataset[affair_idx, :]
                tree_ptr = root
                exist_flag = False
                for item_idx in range(self.itemnum):
                    if affair[item_idx]:
                        item = np.zeros((1, self.itemnum), dtype=np.int).squeeze()
                        item[item_idx] = 1
                        judgement = np.all(tree_ptr.children_items == item, axis=1).tolist()
                        if True in judgement:
                            idx = judgement.index(True)
                            tree_ptr = tree_ptr.children_nodes[idx]
                        else:
                            new_node = self.FPTreeLeafNode(tree_ptr, self.itemnum, item)
                            tree_ptr.AddChildren(new_node)
                            item = tuple(item.tolist())
                            sub_item_node = sub_item_nodes.get(item, [])
                            sub_item_node.append(new_node)
                            sub_item_nodes[item] = sub_item_node
                            tree_ptr = new_node
                        tree_ptr.PassWay()
            # recursively mine the sub tree
            for sub_sub_item in sub_item_nodes:
                sub_candidate, sub_support = self.MineSubFPTree(sub_item_nodes, sub_sub_item)
                for candidate_idx in range(sub_candidate.shape[0]):
                    subset = np.bitwise_or(np.array(target_item, dtype=np.int), sub_candidate[candidate_idx, :])
                    if not np.sum(np.all(candidate == subset, axis=1)):
                        candidate = np.vstack((candidate, subset))
                        supports = np.vstack((supports, np.array([[sub_support[candidate_idx, 0]]])))
        return candidate, supports

    def Mining(self):
        # Build FP Tree
        root = self.FPTreeRootNode(self.itemnum)
        item_nodes = dict()
        # Sort data
        sort_idx = np.argsort(np.sum(self.data, axis=0).squeeze()).squeeze()[::-1]
        temp_data = self.data[:, sort_idx]
        for affair_idx in range(self.data.shape[0]):
            affair = temp_data[affair_idx, :]
            tree_ptr = root
            exist_flag = False
            # recursive building tree
            for item_idx in range(self.itemnum):
                if affair[item_idx]:
                    item = np.zeros((1, self.itemnum), dtype=np.int).squeeze()
                    item[item_idx] = 1
                    judgement = np.all(tree_ptr.children_items == item, axis=1).tolist()
                    if True in judgement:
                        idx = judgement.index(True)
                        tree_ptr = tree_ptr.children_nodes[idx]
                    else:
                        new_node = self.FPTreeLeafNode(tree_ptr, self.itemnum, item)
                        tree_ptr.AddChildren(new_node)
                        item = tuple(item.tolist())
                        item_node = item_nodes.get(item, [])
                        item_node.append(new_node)
                        item_nodes[item] = item_node
                        tree_ptr = new_node
                    tree_ptr.PassWay()
        # Mine frequent set
        frequent_sets = dict()
        candidate = np.array([], dtype=np.int).reshape(0, self.itemnum)
        supports = np.array([], dtype=np.int).reshape(0, 1)
        for item in item_nodes:
            sub_candidate, sub_support = self.MineSubFPTree(item_nodes, item)
            for candidate_idx in range(sub_candidate.shape[0]):
                if not sum(np.all(sub_candidate[candidate_idx, :] == candidate, axis=1)):
                    candidate = np.vstack((candidate, sub_candidate[candidate_idx, :]))
                    supports = np.vstack((supports, np.array([[sub_support[candidate_idx, 0]]])))
        length = np.sum(candidate, axis=1)
        # Shift back and form the frequent set
        candidate = candidate[:, np.argsort(sort_idx)]
        try:
            for layer in range(1, np.max(length) + 1):
                frequent_sets[layer] = (candidate[length == layer, :], supports[length == layer, :])
        except:
            pass
        self.frequent_sets = frequent_sets

    def GenerateRule(self):
        self.tool.GenerateRule()

    def OutputRule(self):
        self.tool.OutputRule()
        return self.verbal_rules

    def MineRules(self):
        self.Mining()
        self.GenerateRule()
        return self.OutputRule()
