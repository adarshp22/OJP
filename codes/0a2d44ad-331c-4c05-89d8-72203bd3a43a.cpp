#include <iostream>
#include <vector>
#include <unordered_map>

using namespace std;

int main() {
    int n;
    cin >> n;
    
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    int target;
    cin >> target;
    
    unordered_map<int, int> num_map;
    for (int i = 0; i < n; ++i) {
        int complement = target - nums[i];
        if (num_map.find(complement) != num_map.end()) {
            cout << num_map[complement] << " " << i << "\n";
            break;
        }
        num_map[nums[i]] = i;
    }
    
    return 0;
}