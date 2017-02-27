void dfs(const vector<vector<int> > &a, vector<bool> &visited, int s) {
    visited[s] = true;
    // 进行操作
    for (int i = 0; i < a[s].size(); ++i) {
        if (!visited[a[s][i]])
            dfs(a, visited, a[s]);
    }
    visited[s] = false;
}

void dfs(const vector<vector<int> > &a, int s) {
    vector<bool> visited(a.size(), false);
    dfs(a, visited, s);
}



void bfs(const vector<vector<int> > &a, int s) {
    queue<int> q;
    vector<bool> visited(a.size(), false);
    q.push(s);
    int v;
    while (!q.empty()) {
        v = q.top();
        q.pop();
        visited[v] = true;
        // 进行操作
        for (int i = 0; i < a[s].size(); ++i) {
            if (!visited(a[s][i]))
                q.push(a[s][i])
        }
    }
}