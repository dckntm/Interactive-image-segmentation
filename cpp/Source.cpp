/*
4 5
1 2 10000
1 3 10000
2 3 1
3 4 10000
2 4 10000
*/

#include <iostream>
#include <vector>
#include <set>
#include <map>
#include <queue>
#include <algorithm>

using namespace std;

struct cmp {
	bool operator() (const pair<int, int> &a, const pair<int, int> &b){
		return a.second > b.second;
	}
};

vector<vector<int>> graph, straight, reversed;
multiset<pair<int, int>, cmp> vertices;
vector<int> height, excess;
map<pair<int, int>, int> capacity;
int source = -1, runoff = -1;
int opt = 0;
int n, m, u, v, c;

void bfs() {
	vector<int> dist(graph.size(), -1), dist1(graph.size(), -1);
	vector<bool> used(graph.size(), false);
	queue<int> q;
	q.push(runoff);
	used[runoff] = true;
	dist[runoff] = 0;
	while (!q.empty()) {
		for (auto i : reversed[q.front()]) {
			if (!used[i] && capacity[make_pair(i, q.front())]) {
				used[i] = true;
				q.push(i);
				dist[i] = dist[q.front()] + 1;
			}
		}
		q.pop();
	}
	q.push(source);
	used.assign(graph.size(), false);
	used[source] = true;
	dist1[source] = 0;
	while (!q.empty()) {
		for (auto i : straight[q.front()]) {
			if (!used[i] && capacity[make_pair(i, q.front())]) {
				used[i] = true;
				q.push(i);
				dist1[i] = dist1[q.front()] + 1;
			}
		}
		q.pop();
	}
	for (int i = 0; i < dist.size(); ++i) {
		if (dist[i] == -1) {
			dist[i] = dist1[i];
		}
	}
	dist[source] = graph.size();
	height = dist;
	vertices.clear();
	for (int i = 0; i < graph.size() - 1; ++i) {
		if (excess[i] != 0) {
			vertices.insert({ i, height[i] });
		}
	}
}

void f() {
	while (!vertices.empty()) {
		if (opt == m) {
			bfs();
			opt = 0;
		}
		pair<int, int> tmp = *vertices.begin();
		for (auto i : graph[tmp.first]) {
			if (height[i] == height[tmp.first] - 1) {
				int flow = min(excess[tmp.first], capacity[make_pair(tmp.first, i)]);
				excess[tmp.first] -= flow;
				excess[i] += flow;
				if (flow != 0 && i != runoff && excess[i] == flow) {
					vertices.insert(make_pair(i, height[i]));
				}
				capacity[make_pair(tmp.first, i)] -= flow;
				capacity[make_pair(i, tmp.first)] += flow;
			}
		}
		int min_height = graph.size();
		for (auto i : graph[tmp.first]) {
			if (capacity[make_pair(tmp.first, i)] > 0)
				min_height = min(min_height, height[i]);
		}
		vertices.erase(vertices.begin());
		height[tmp.first] = min_height + 1;
		tmp.second = height[tmp.first];
		if (height[tmp.first] == graph.size() + 1) {
			excess[tmp.first] = 0;
		}
		if (excess[tmp.first] != 0) {
			vertices.insert(tmp);
		}
		++opt;
	}
}


int main() {
	cin >> n >> m;
	graph.resize(n);
	straight.resize(n);
	reversed.resize(n);
	height.resize(n, 0);
	excess.resize(n, 0);
	for (int i = 0; i < m; ++i) {
		cin >> u >> v >> c;
		graph[u - 1].push_back(v - 1);
		graph[v - 1].push_back(u - 1);
		straight[u - 1].push_back(v - 1);
		reversed[v - 1].push_back(u - 1);
		capacity[make_pair(u - 1, v - 1)] = c;
		capacity[make_pair(v - 1, u - 1)] = 0;
	}
	for (int i = 0; i < n; ++i) {
		if (straight[i].size() == 0)
			runoff = i;
		if (reversed[i].size() == 0)
			source = i;
	}
	height[source] = n;
	for (auto i : graph[source]) {
		excess[i] = capacity[make_pair(source, i)];
		if (i != runoff) {
			vertices.insert(make_pair(i, height[i]));
		}
		swap(capacity[make_pair(i, source)], capacity[make_pair(source, i)]);
	}
	int x = 0;
	f();
	cout << excess[runoff] << '\n';
}