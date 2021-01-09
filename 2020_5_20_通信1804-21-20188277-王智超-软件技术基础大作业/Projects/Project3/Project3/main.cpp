#include <stdio.h>
#include <stdlib.h>
//结点结构体
typedef struct BiTNode {
	char data;//数据
	struct BiTNode * lchild, *rchild;//左右孩子指针
}BiTNode, *BiTree;
//初始化二叉树的二叉链表T
void Create_BiTree(BiTree * T) {
	char ch;
	ch = getchar();
	//@ 表示此处无结点，为虚结点
	if (ch == '@') {
		*T = NULL;
	}
	//# 表示构造结束
	else if (ch == '#') {
		return;
	}
	//排除以上两种情况，则为有数据的结点，对其进行构造
	else {
		*T = (BiTree)malloc(sizeof(BiTNode));
		(*T)->data = ch;
		//继续构造其左右孩子结点
		Create_BiTree(&(*T)->lchild);
		Create_BiTree(&(*T)->rchild);
	}
}
//中序遍历二叉树
void InOrder(BiTree T) {
	if (T) {
		//中序遍历，即先遍历左孩子，然后输出结点数据，在遍历右孩子
		InOrder(T->lchild);
		printf("%3c", T->data);
		InOrder(T->rchild);
	}
}

int main() {
	BiTree T;
	printf("input PreOrder str:");
	//构造二叉树
	Create_BiTree(&T);
	printf("\n");
	//按照中序方式遍历二叉树
	printf("\nInOrder list of T :");
	InOrder(T);
}