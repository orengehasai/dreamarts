
def find_all_pairs_longest_path(edges_with_weights):
    # 辺の正規化 (u < v)
    weights = {}
    for u, v, w in edges_with_weights:
        edge = tuple(sorted((u, v)))
        weights[edge] = w

    # 辺をソートして処理順序を固定
    sorted_edges = sorted(list(weights.keys()))

    # 状態を管理する辞書
    # keyとして使用するためfrozenset
    # value: (コスト, 辺のリスト)
    states = {frozenset(): (0, [])}
    # 最長経路の辺と長さを保持する変数
    longest_path_info = ([], -1)

    # 辺を1本ずつ処理する
    for u, v in sorted_edges:
        weight = weights[(u, v)]
        new_states = states.copy()  # 「この辺を使わない」場合の全状態をコピー

        for mate_frozenset, (cost, path_edges) in states.items():

            # --- この辺 {u, v} を「使う」場合の処理 ---

            # 現在のパスにおける u, v の次数を計算
            degree_u = sum(1 for edge in path_edges if u in edge)
            degree_v = sum(1 for edge in path_edges if v in edge)

            # 辺を追加すると次数が3以上になる頂点は単純経路に反するためスキップ
            if degree_u >= 2 or degree_v >= 2:
                continue

            # uとvが既に同じパスの端点の場合、サイクルが形成されるためスキップ
            # if mate.get(u) == v:
            #     continue

            mate = dict(mate_frozenset)

            # 辺 {u, v} を追加することで、単純なサイクルが完成する場合
            if mate.get(u) == v:
                #完成する単純なサイクル以外にパス断片が存在する場合はスキップ
                if(len(mate) > 2):
                    continue
                new_cost = cost + weight
                new_path_edges = path_edges + [(u, v)]

                # 全体の最長記録を更新
                if new_cost > longest_path_info[1]:
                    longest_path_info = (new_path_edges, new_cost)
                # 単純サイクルを形成した状態は、これ以上伸長できないため、new_statesには追加せず、枝刈りする
                continue


            new_mate = mate.copy()
            u_is_endpoint = u in new_mate # uが既にパスの端点か
            v_is_endpoint = v in new_mate # vが既にパスの端点か

            # パス断片を追加
            if not u_is_endpoint and not v_is_endpoint:
                new_mate[u] = v
                new_mate[v] = u

            # 既存のパスを伸長
            elif u_is_endpoint and not v_is_endpoint:
                u_remote = new_mate.pop(u)
                # new_mate.pop(u_remote)
                new_mate[u_remote] = v
                new_mate[v] = u_remote
            elif v_is_endpoint and not u_is_endpoint:
                v_remote = new_mate.pop(v)
                # new_mate.pop(v_remote)
                new_mate[u] = v_remote
                new_mate[v_remote] = u

            # 2つの異なるパスを連結
            else: #u_is_endpoint and v_is_endpoint
                u_remote = new_mate.pop(u)
                v_remote = new_mate.pop(v)
                # new_mate.pop(u_remote)
                # new_mate.pop(v_remote)
                new_mate[u_remote] = v_remote
                new_mate[v_remote] = u_remote

            new_cost = cost + weight
            new_path_edges = path_edges + [(u, v)]

            # e) 圧縮: 同じ接続状態(mate)なら、コストが最大のものを残す
            new_mate_frozenset = frozenset(new_mate.items())

            if new_mate_frozenset not in new_states or new_cost > new_states[new_mate_frozenset][0]:
                new_states[new_mate_frozenset] = (new_cost, new_path_edges)

        states = new_states

    # すべての状態の中から、一本道の単純経路（mate配列の要素数が2）で、
    # かつコストが最大のものを見つける
    for mate_frozenset, (cost, path_edges) in states.items():
        if len(mate_frozenset) == 2: # 端点が2つ = 一本道
            if cost > longest_path_info[1]:
                longest_path_info = (path_edges, cost)

    return longest_path_info

def read_graph():
	edges_with_weights = []
	while True:
		line = input()
		if len(line) == 0:
			break
		parts = line.replace(' ', '').split(',')
		u = int(parts[0])
		v = int(parts[1])
		weight = float(parts[2])

		edges_with_weights.append((u, v, weight))

	return edges_with_weights

if __name__ == '__main__':

	edges_with_weights = read_graph()
	path, length = find_all_pairs_longest_path(edges_with_weights)


	print(f"  経路: {path}")
	print(f"  長さ: {length}")

