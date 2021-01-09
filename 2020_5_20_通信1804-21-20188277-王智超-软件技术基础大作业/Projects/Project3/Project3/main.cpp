#include <stdio.h>
#include <stdlib.h>
//���ṹ��
typedef struct BiTNode {
	char data;//����
	struct BiTNode * lchild, *rchild;//���Һ���ָ��
}BiTNode, *BiTree;
//��ʼ���������Ķ�������T
void Create_BiTree(BiTree * T) {
	char ch;
	ch = getchar();
	//@ ��ʾ�˴��޽�㣬Ϊ����
	if (ch == '@') {
		*T = NULL;
	}
	//# ��ʾ�������
	else if (ch == '#') {
		return;
	}
	//�ų����������������Ϊ�����ݵĽ�㣬������й���
	else {
		*T = (BiTree)malloc(sizeof(BiTNode));
		(*T)->data = ch;
		//�������������Һ��ӽ��
		Create_BiTree(&(*T)->lchild);
		Create_BiTree(&(*T)->rchild);
	}
}
//�������������
void InOrder(BiTree T) {
	if (T) {
		//������������ȱ������ӣ�Ȼ�����������ݣ��ڱ����Һ���
		InOrder(T->lchild);
		printf("%3c", T->data);
		InOrder(T->rchild);
	}
}

int main() {
	BiTree T;
	printf("input PreOrder str:");
	//���������
	Create_BiTree(&T);
	printf("\n");
	//��������ʽ����������
	printf("\nInOrder list of T :");
	InOrder(T);
}