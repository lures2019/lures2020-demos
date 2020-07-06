# include<iostream>
using namespace std;
int main() {
	int n,sum=0;
	cin >> n;
	for (int i = 0; i < n; i++) {
		sum += pow(2, i);
	}
	cout << "幂次数和是：" << sum << endl;
	return 0;
}