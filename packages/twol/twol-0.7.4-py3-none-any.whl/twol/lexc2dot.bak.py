from collections import defaultdict
id_dict = {}
from_to_set = set()
from_to_targets_dict = defaultdict(set)
lex_name_lst = []
node_rank = defaultdict(int)
id_num = 0

def new_id(lex_name):
    global id_num
    id_num += 1
    id = "ID_" + str(id_num)
    id_dict[lex_name] = id
    lex_name_lst.append(lex_name)
    return id

def calc_ranks(node, rank):
    node_rank[node] = rank
    for target in from_to_targets_dict[node]:
        targ_rank = node_rank[target]
        if targ_rank == 0 or targ_rank > rank + 1:
            calc_ranks(target, rank + 1)
    return

def main():
    import argparse
    arpar = argparse.ArgumentParser("python3 lexc2dot.py")
    arpar.add_argument(
        "-i", "--input",
        action='store', nargs='+',
        help="list of LEXC files",
        default=["examples.pstr"])
    arpar.add_argument(
        "-o", "--output",
        help="file to which write the DOT source",
        default="")
    arpar.add_argument(
        "-v", "--verbosity",
        help="level of  diagnostic output",
        type=int, default=0)
    args = arpar.parse_args()


    import fileinput
    import re

    file_lex_lists = defaultdict(list)

    skip = True
    for line_nl in fileinput.input(args.input):
        filename = fileinput.filename()
        line = line_nl.rstrip()
        lst = re.split("\s+", line)
        if line.startswith("!"):
            continue
        if line.startswith("Multichar_Symbols"):
            skip = True
        elif line.startswith("Definitions"):
            skip = True
        elif line_nl.startswith("LEXICON "):
            skip = False
            if len(lst) >= 2:
                lex_name = lst[1]
                id = new_id(lex_name)
                file_lex_lists[filename].append(lex_name)
            else:
                exit("** {} ({}): {}".format(filename,
                                             fileinput.lineno(), line))
        elif not skip:
            if len(lst) >= 2:
                target = lst[1]
                from_to_set.add((lex_name, target))
                from_to_targets_dict[lex_name].add(target)
            else:
                exit("** {} ({}): {}".format(filename,
                                             fileinput.lineno(), line))

    for source, target in sorted(from_to_set):
        if source not in id_dict:
            src_id = new_id(source)
        if target not in id_dict:
            trg_id = new_id(target)

    print("Digraph {")
    print("\trankdir=LR;")
    print("\tranksep=2;")
    i = 0
    for filename, lex_lst in file_lex_lists.items():
        print("subgraph cluster_{} {{".format(i))
        i = i + 1
        print('label="{}";'.format(filename))
        id_lst = ['\t{} [label="{}"]'.format(id_dict[lex_name],
                                             lex_name)  for lex_name in lex_lst]
        s = ";\n\t".join(id_lst)
        print("\t{}".format(s))
        print("}")
    for lex_name in lex_name_lst:
        id = id_dict[lex_name]
        print('\t{} [label="{}"]'.format(id, lex_name))

    #calc_ranks("Root", 1)
    #for lex_name in lex_name_lst:
    #    if node_rank[lex_name] == 0:
    #        calc_ranks(lex_name, 30)
    #node_rank["Poss"] = 8
    #node_rank["Clit"] = 9
    #node_rank["End"] = 10

    #rank_node = defaultdict(set)
    #for node, rank in node_rank.items():
    #    rank_node[rank].add(node)
    #for rank, node_set in sorted(rank_node.items()):
    #    id_lst = [id_dict[n] for n in node_set]
    #    node_str = ", ".join(list(id_lst))
    #    print("\t{", "rank=same; {}".format(node_str), "}")
        
    for source, target in sorted(from_to_set):
        src_id = id_dict.get(source, source)
        trg_id = id_dict.get(target, target)
        print("\t{} -> {}".format(src_id, trg_id))

    print("}")
    ###print(from_to_targets_dict)
    ###print(node_rank)
    return

if __name__ == "__main__":
    main()
