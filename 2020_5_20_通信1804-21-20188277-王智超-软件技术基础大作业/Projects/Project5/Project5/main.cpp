# include<iostream>
using namespace std;
int main() {
	int n,sum=0;
	cin >> n;
	for (int i = 0; i < n; i++) {
		if (pow(2, i) < n) {
			sum += pow(2, i);
		}
	}
	cout << "�ݴ������ǣ�" << sum << endl;
	return 0;
}