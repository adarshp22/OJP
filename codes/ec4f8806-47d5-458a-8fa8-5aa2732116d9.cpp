#include <iostream>
#include <vector>
#include <unordered_map>

using namespace std;

vector<int> twoSum(const vector<int>& nums, int target) {
    unordered_map<int, int> numToIndex;  // number -> index

    for (int i = 0; i < nums.size(); i++) {
        int complement = target - nums[i];
        // Check if complement is already in map
        if (numToIndex.find(complement) != numToIndex.end()) {
            return {numToIndex[complement], i};
        }
        // Store current number and its index
        numToIndex[nums[i]] = i;
    }
    // Since the problem guarantees one solution, this line may never be reached
    return {};
}

int main() {
    int n, target;
    cout << "Enter number of elements: ";
    cin >> n;

    vector<int> nums(n);
    cout << "Enter the elements separated by spaces: ";
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }

    cout << "Enter target: ";
    cin >> target;

    vector<int> result = twoSum(nums, target);

    if (!result.empty()) {
        cout  << result[0] << " " << result[1];
    } else {
        cout << "No solution found.\n";
    }

    return 0;
}