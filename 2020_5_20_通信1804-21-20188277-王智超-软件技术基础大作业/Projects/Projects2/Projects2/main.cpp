#include<iostream>
using namespace std;

void print(int arr[], int n)
{
	for (int j = 0; j<n; j++)
	{
		cout << arr[j] << "  ";
	}
	cout << endl;
}

int main()
{
	int s[10] = { 8,1,9,7,2,4,5,6,10,3 };
	int n = 10;
	cout << "初始序列是：";
	print(s, 10);
	for (int i = 0; i < n - 1; i++) {
		for (int j = 0; j < n - 1 - i; j++) {
			if (s[j] > s[j + 1]) {
				int temp = s[j];
				s[j] = s[j + 1];
				s[j + 1] = temp;
			}
		}
	}
	cout << "排序结果是：";
	print(s, 10);
	return 0;
}