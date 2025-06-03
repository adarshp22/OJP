#include<iostream>
#include<bits/stdc++.h>
using namespace std;

int main(){
	
	int n; cin>>n;
	vector<int>v(n);
	for(int i=0; i< n;i++) cin>>v[i];
	int t; cin>>t;
	sort(v.begin(),v.end());
	int i=0,j=n-1;
	while(i<j){
		if(v[i] + v[j] > t) {
			j--;
		}
		else if(v[i] + v[j] < t){
			i++;
		}
		else{
			cout<<i<<" "<<j<<endl;
			break;
		}
	}

	
	
	
	
	
	
	
	
	
	return 0;
}