import json

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import scipy


def open_json(filename):
    with open(filename, "r", encoding="utf-8") as read_file:
        data = json.load(read_file)
    return data


class Person:
    def __init__(self, dictionary):
        self.id = dictionary['id']
        self.name = dictionary['name']
        self.shortname = dictionary['shortname']
        self.gender = dictionary['gender']
        if 'pids' in dictionary.keys():
            self.pids = dictionary['pids']
        else:
            self.pids = []
        if 'mid' in dictionary.keys():
            self.mid = dictionary['mid']
        else:
            self.mid = -1
        if 'fid' in dictionary.keys():
            self.fid = dictionary['fid']
        else:
            self.fid = -1
        self.cids = []
        if 'date' in dictionary.keys():
            self.date = dictionary['date']
        else:
            self.date = "-"
        if 'x' in dictionary.keys():
            self.x = dictionary['x']
        else:
            self.x = -1
        if 'y' in dictionary.keys():
            self.y = dictionary['y']
        else:
            self.y = -1
        self.rank = -1

    def __repr__(self):
        result = str(self.id) + ', ' + self.name + ', ' + self.gender
        result += ', ' + str(self.pids)
        result += ', ' + str(self.mid)
        result += ', ' + str(self.fid)
        result += ', ' + str(self.cids)
        result += ', ' + str(self.rank)
        return '{' + result + '}'

    def get_data(self):
        data = {'id': self.id,
                'pids': self.pids,
                'mid': self.mid,
                'fid': self.fid,
                'name': self.name,
                'gender': self.gender,
                'shortname': self.shortname,
                'date': self.date,
                'rank': self.rank,
                'type': 'person',
                'x': self.x,
                'y': self.y}
        if not data['pids']:
            data.pop('pids')
        if data['mid'] == -1:
            data.pop('mid')
        if data['fid'] == -1:
            data.pop('fid')
        if data['x'] == -1:
            data.pop('x')
        if data['y'] == -1:
            data.pop('y')
        return data


class Family:
    def __init__(self, id, sid1, sid2, cids):
        self.id = id
        self.sid1 = sid1
        self.sid2 = sid2
        self.cids = cids

    def __repr__(self):
        result = str(self.id) + ', ' + str(self.sid1) + ', ' + str(self.sid2) + ', ' + str(self.cids)
        return '{' + result + '}'

    def __eq__(self, other):
        if ((self.sid1 == other.sid1 and self.sid2 == other.sid2) or (
                self.sid2 == other.sid1 and self.sid1 == other.sid2)) and self.cids == other.cids:
            return True
        else:
            return False

    def get_data(self):
        data = {'id': self.id,
                'type': 'family',
                'sid1': self.sid1,
                'sid2': self.sid2,
                'cids': self.cids}
        return data


class FamilyTree:
    def __init__(self, tree_list):
        self.tree = {}
        self.families = {}
        if type(tree_list) is list:
            for node in tree_list:
                if type(node) is dict:
                    if 'x' in tree_list[0].keys():
                        if node['type'] == 'person':
                            person = Person(node)
                            self.tree.update({person.id: person})
                        else:
                            family = Family(node.id, node.sid1, node.sid2, node.cids)
                            self.tree.update({family.id: family})
                            self.families.update()
                    else:
                        person = Person(node)
                        self.tree.update({person.id: person})
                else:
                    print("List must contains dict!")
        else:
            print("Tree must be list!")
        self.__add_children()
        self.__add_rank()
        self.__add_families()

    def __add_children(self):
        result = self.tree
        for i in self.tree:
            if self.tree[i].mid != -1:
                result[self.tree[i].mid].cids.append(self.tree[i].id)
            if self.tree[i].fid != -1:
                result[self.tree[i].fid].cids.append(self.tree[i].id)
        self.tree = result

    def __add_rank(self):
        result = self.tree

        def add_rank_node(node, rank):
            if node.rank == -1:
                node.rank = str(rank)
                for n in node.pids:
                    add_rank_node(result[n], rank)
            else:
                rank += 1
                for n in node.cids:
                    add_rank_node(result[n], rank)

        add_rank_node(result[1], 0)
        self.tree = result

    def __add_families(self):
        i = 0
        for person in self.tree.values():
            for pid in person.pids:
                family = Family('f' + str(i), person.id, pid, list(set(person.cids) & set(self.tree[pid].cids)))
                if family not in self.families.values():
                    self.families.update({family.id: family})
                    i += 1

    def get_all_attr(self, attr_name):
        result = []
        for person in self.tree.values():
            result.append(getattr(person, attr_name))
        return result

    def get_dataframe(self):
        df_dict = {}
        for attr in ['id', 'name', 'gender', 'pids', 'mid', 'fid', 'cids', 'rank']:
            df_dict.update({attr: self.get_all_attr(attr)})
        df = pd.DataFrame.from_dict(df_dict)
        df.set_index('id', inplace=True)
        return df

    def get_persons_df(self):
        df_dict = {}
        for attr in ['id', 'name', 'gender', 'rank']:
            df_dict.update({attr: self.get_all_attr(attr)})
        df = pd.DataFrame.from_dict(df_dict)
        df.set_index('id', inplace=True)
        return df

    def get_links_df(self):
        df_dict = {}
        for attr in ['id', 'pids', 'cids']:
            df_dict.update({attr: self.get_all_attr(attr)})
        df = pd.DataFrame.from_dict(df_dict)
        df.set_index('id', inplace=True)
        return df

    def get_links_pair_df(self):
        df_dict = {'source_id': [], 'target_id': [], 'color': []}
        for person in self.tree.values():
            for pid in person.pids:
                if self.tree[pid].id not in df_dict['source_id'] and person.id not in df_dict['target_id']:
                    df_dict['source_id'].append(person.id)
                    df_dict['target_id'].append(self.tree[pid].id)
                    df_dict['color'].append('green')
            for cid in person.cids:
                df_dict['source_id'].append(person.id)
                df_dict['target_id'].append(self.tree[cid].id)
                df_dict['color'].append('blue')
        df = pd.DataFrame.from_dict(df_dict)
        return df

    def get_links_pair_families_df(self):
        #до делать
        df_dict = {'source_id': [], 'target_id': [], 'color': []}

        for family in self.families.values():
            df_dict['source_id'].append(family.sid1)
            df_dict['target_id'].append(family.id)
            df_dict['color'].append('green')
            df_dict['source_id'].append(family.sid2)
            df_dict['target_id'].append(family.id)
            df_dict['color'].append('green')
            for cid in family.cids:
                df_dict['source_id'].append(family.id)
                df_dict['target_id'].append(cid)
                df_dict['color'].append('blue')

        df = pd.DataFrame.from_dict(df_dict)
        return df

    def get_tree_family(self):
        tree_family = {}
        tree_family.update(self.tree)
        tree_family.update(self.families)
        return tree_family

    def get_networkx_graph(self):
        df = self.get_links_pair_families_df()
        G = nx.from_pandas_edgelist(df, 'source_id', 'target_id')
        for obj in self.get_tree_family().values():
            G.nodes[obj.get_data()['id']].update(obj.get_data())
        return G


# family_tree = FamilyTree(open_json('data/tree3_simple.json'))
# d = dict(family_tree.get_networkx_graph().nodes(data=True))
# print(d)
# print(list(d)[0])
# print(nx.adjacency_matrix(family_tree.get_networkx_graph()).toarray())