#include <iostream>
using namespace std;

int main() {
	int d[] = { 9, 6, 7, 5, 13, 6, 2 };
	int n = 7;
	int max = d[0];
	int min = d[0];
	bool flag = false;
	if (n % 2) {
		n--;
		flag = true;
	}
	for (int i = 0; i < n - 1; i += 2) {
		if (d[i] <= d[i + 1]) {
			if (d[i] < min)
				min = d[i];
			if (d[i + 1] > max)
				max = d[i + 1];
		}
		else {
			if (d[i] > max)
				max = d[i];
			if (d[i + 1] < min)
				min = d[i + 1];
		}
	}
	//若数组长度为奇数，还需要和最后一个数作比较 
	if (flag) {
		if (d[n] < min)
			min = d[n];
		if (d[n] > max)
			max = d[n];
	}
	cout << "The max value of the array is: " << max << endl;
	cout << "The min value of the array is: " << min << endl;
}