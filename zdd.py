import sys
from color import Color
from collections import defaultdict

# https://qiita.com/cabernet_rock/items/01c48dd06178ba0768f9
def find_longest_route_zdd(edges_with_weights):
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
	# 最長経路の端点と辺と長さと保持する変数
	longest_path_info = ({}, [], -1)

		# 辺を1本ずつ処理する
	for u, v in sorted_edges:
		weight = weights[(u, v)]
		new_states = {}

		for mate_frozenset, (cost, path_edges) in states.items():
			# 新規の辺 {u, v} を使わない場合
			if mate_frozenset not in new_states or cost > new_states[mate_frozenset][0]:
				new_states[mate_frozenset] = (cost, path_edges)

			# 新規の辺 {u, v} を使う場合
			mate = dict(mate_frozenset)
			# 現在のパスにおける u, v の次数を計算
			degree_u = sum(1 for edge in path_edges if u in edge)
			degree_v = sum(1 for edge in path_edges if v in edge)

			# 辺を追加すると次数が3以上になる頂点は単純経路に反するためスキップ
			if degree_u >= 2 or degree_v >= 2:
				continue
			# 辺 {u, v} を追加することで、単純なサイクルが完成する場合
			if mate.get(u) == v:
				#完成する単純なサイクル以外にパス断片が存在する場合はスキップ
				if(len(mate) > 2):
					continue
				new_cost = cost + weight
				new_path_edges = path_edges + [(u, v)]

				if new_cost > longest_path_info[2]:
					longest_path_info = ({}, new_path_edges, new_cost)
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
				new_mate[u_remote] = v
				new_mate[v] = u_remote
			elif v_is_endpoint and not u_is_endpoint:
				v_remote = new_mate.pop(v)
				new_mate[u] = v_remote
				new_mate[v_remote] = u

			# 2つの異なるパスを連結
			else: #u_is_endpoint and v_is_endpoint
				u_remote = new_mate.pop(u)
				v_remote = new_mate.pop(v)
				new_mate[u_remote] = v_remote
				new_mate[v_remote] = u_remote

			new_cost = cost + weight
			new_path_edges = path_edges + [(u, v)]

			new_mate_frozenset = frozenset(new_mate.items())
			# 圧縮:同じ接続状態なら、コストが最大のものを代表にする
			if new_mate_frozenset not in new_states or new_cost > new_states[new_mate_frozenset][0]:
				new_states[new_mate_frozenset] = (new_cost, new_path_edges)

		states = new_states

	# すべての状態の中から、一本道の単純経路（mate配列の要素数が2）で、
	# かつコストが最大のものを見つける
	for mate_frozenset, (cost, path_edges) in states.items():
		if len(mate_frozenset) == 2: # 端点が2つ = 一本道
			if cost > longest_path_info[2]:
				longest_path_info = (dict(mate_frozenset), path_edges, cost)

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

		if u == v:
			print(f"{Color.RED}Error:自己ループを含んでいます{Color.RESET}", file=sys.stderr)
			sys.exit(1)

		edges_with_weights.append((u, v, weight))

	if len(edges_with_weights) == 0:
		print(f"{Color.RED}Error:値を入力してください{Color.RESET}", file=sys.stderr)
		sys.exit(1)

	return edges_with_weights

def print_path(longest_path_info):
	mate_dict, path_edges, length = longest_path_info

	adj = defaultdict(list)
	for u, v in path_edges:
		adj[u].append(v)
		adj[v].append(u)

	ordered_path = []
	if not mate_dict:
		start_node = path_edges[0][0] # 任意の一点を始点とする
		current_node = start_node
		prev_node = -1

		while True:
			ordered_path.append(current_node)
			neighbors = adj[current_node]
			next_node = neighbors[0] if neighbors[0] != prev_node else neighbors[1]
			prev_node = current_node
			current_node = next_node
			if current_node == start_node:
				break

		ordered_path.append(start_node)

	else:
		start_node, end_node = mate_dict.keys()
		current_node = start_node
		prev_node = -1

		while True:
			ordered_path.append(current_node)
			if current_node == end_node:
				break
			neighbors = adj[current_node]
			next_node = neighbors[0] if neighbors[0] != prev_node else neighbors[1]
			prev_node = current_node
			current_node = next_node

	answer = "\r\n".join(map(str, ordered_path))
	print(f"{Color.GREEN}{answer}{Color.RESET}")
	print(f"{Color.GREEN}経路: {path_edges}{Color.RESET}")
	print(f"{Color.GREEN}長さ: {length}{Color.RESET}")


if __name__ == '__main__':
	edges_with_weights = read_graph()
	longest_path_info = find_longest_route_zdd(edges_with_weights)
	print_path(longest_path_info)

