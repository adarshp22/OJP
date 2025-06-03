#include<iostream>
#include<bits/stdc++.h>
using namespace std;

int main(){
	
	int n; cin>>n;
	vector<int>v(n);
	int t; cin>>t;
	int i=0,j=n-1;
	sort(v.begin(),v.end());
	while(i<j){
		if(v[i] + v[j] > t) {
			j--;
		}
		else if(v[i] + v[j] < t) {
			i++;
		}
		else{
			cout<<i<<" "<<j<<endl;
			break;
		}
	}
	
	
	
	
	
	
	
	
	return 0;
}