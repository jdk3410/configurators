// C program to write Cisco ASA firewall configs on Linux. Santized for external use. Written by github/jdk3410
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

#define KRED  "\x1B[31m"
#define KNRM  "\x1B[0m"
#define MAX_DATA 100


void print_cats()

{
	printf(KRED ".----------------------------------------------.\n");
	printf("|                                              |\n");
	printf("|                                              |\n");
	printf("|                       \\`\\  F    Cisco        |\n");
	printf("|            /./././.   | |  i    Advanced     |\n");
	printf("|          /        `/. | |  r    Terminal     |\n");
	printf("|         /     __    `/'/'  e                 |\n");
	printf("|      /\\__/\\ /'  `\\    /    w                 |\n");
	printf("|     |  00  |      `.,.|    a                 |\n");
	printf("|      \\Vvvv/        ||||    l                 |\n");
	printf("|        ||||        ||||    l                 |\n");
	printf("|        ||||        ||||                      |\n");
	printf("|        `'`'        `'`'                      |\n");
	printf(".----------------------------------------------.\n");
	printf(KNRM "\n");


}

void passwd()
{
unsigned short int length = 12;
srand ((unsigned int) time(0) + getpid());

while(length--) {
	putchar(rand() % 94 + 33);
	srand(rand());
}

}

void main_loop()
{
	char password[] = "passwd";

	char hostname[MAX_DATA];
	char ext_ip[MAX_DATA];
	char int_ip[MAX_DATA];

	printf("Enter Cisco hostname: ");
	scanf("%s", hostname);
	printf("Enter external IP: ");
	scanf("%s", ext_ip);
	printf("Enter internal IP: ");
	scanf("%s", int_ip);
	printf("Password will be %s", password);

	printf("conf t\n");

	printf("hostname %s\n", hostname);
	printf("\n");
	printf("domain-name nothing.com\n");
	printf("no dhcpd enable inside\n");
	printf("no dhcpd address 192.168.1.5-192.168.1.36 inside\n");
	printf("no dhcpd address 192.168.1.2-192.168.1.33 inside\n");
	printf("no dhcpd auto_config outside\n");
	printf("crypto key generate rsa modulus 2048 noconfirm\n");
	printf("\n");
	printf("int vlan1\n");
	printf("ip address %s\n", int_ip);
	printf("no shut\n");
	printf("exit\n");
	printf("\n");
	printf("int vlan2\n");
	printf("ip address %s\n", ext_ip);
	printf("no shut\n");
	printf("exit\n");
	printf("\n");

}


int main(void)
{

	print_cats();
	main_loop();
	return 0;
}
