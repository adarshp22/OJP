#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        vector<int> v;
        for(int i = 0 ; i < nums.size()-1; i++) {
            for(int j = i+1; j < nums.size(); j++) {
                if(nums[i] + nums[j] == target) {
                    v.push_back(i);
                    v.push_back(j);
                    return v; // return on first valid pair
                }
            }
        }
        return v; // returns empty if no such pair
    }
};

int main() {
    int t;
    cin >> t;
    
    while(t--) {
        int n, target;
        cin >> n;

        vector<int> nums(n);
        for(int i = 0; i < n; i++) {
            cin >> nums[i];
        }

        cin >> target;

        Solution sol;
        vector<int> result = sol.twoSum(nums, target);
        
        if(result.empty()) {
            cout << "No valid pair found" << endl;
        } else {
            cout << result[0] << " " << result[1] << endl;
        }
    }

    return 0;
}