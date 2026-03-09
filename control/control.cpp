#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <stdio.h>
#include <unistd.h>
#include <termios.h>

// 键值定义
#define KEY_UP    65 // ⬆
#define KEY_DOWN  66 // ⬇
#define KEY_LEFT  68 // ⬅
#define KEY_RIGHT 67 // ➡
#define KEY_W     119
#define KEY_S     115
#define KEY_A     97
#define KEY_D     100
#define KEY_Q     113
#define KEY_SPACE 32

// 获取键盘输入的非阻塞模式设置
int getch() {
    static struct termios oldt, newt;
    tcgetattr(STDIN_FILENO, &oldt); // 获取当前终端设置
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO); // 关闭行缓冲和回显
    tcsetattr(STDIN_FILENO, TCSANOW, &newt); // 应用新设置

    int ch = getchar(); // 读取字符
    
    tcsetattr(STDIN_FILENO, TCSANOW, &oldt); // 恢复旧设置
    return ch;
}

int main(int argc, char** argv) {
    ros::init(argc, argv, "simple_teleop_node");
    ros::NodeHandle nh;

    // 发布速度话题 /cmd_vel
    ros::Publisher pub = nh.advertise<geometry_msgs::Twist>("/cmd_vel", 10);

    geometry_msgs::Twist twist;
    double linear_speed = 0.5;
    double angular_speed = 1.0;

    printf("====================================\n");
    printf("   Simple Keyboard Teleop Node\n");
    printf("------------------------------------\n");
    printf(" Use Arrow Keys or WASD to move:\n");
    printf("   Up/W    : Move Forward\n");
    printf("   Down/S  : Move Backward\n");
    printf("   Left/A  : Turn Left\n");
    printf("   Right/D : Turn Right\n");
    printf("   Space   : Stop\n");
    printf("   Q       : Quit\n");
    printf("====================================\n");

    bool running = true;
    while(ros::ok() && running) {
        int c = getch(); // 获取按键

        // 如果是转义序列 (方向键通常是 \033[A 这种)
        if (c == 27) {
            getch(); // 跳过 [
            c = getch(); // 获取方向码
        }

        // 重置速度
        twist.linear.x = 0;
        twist.angular.z = 0;

        switch(c) {
            case KEY_UP:
            case KEY_W:
                twist.linear.x = linear_speed;
                printf("\rForward \n");
                break;
            case KEY_DOWN:
            case KEY_S:
                twist.linear.x = -linear_speed;
                printf("\rBackward\n");
                break;
            case KEY_LEFT:
            case KEY_A:
                twist.angular.z = angular_speed;
                printf("\rLeft    \n");
                break;
            case KEY_RIGHT:
            case KEY_D:
                twist.angular.z = -angular_speed;
                printf("\rRight   \n");
                break;
            case KEY_SPACE:
                // 停止
                printf("\rStop    \n");
                break;
            case KEY_Q:
                running = false;
                break;
            default:
                break;
        }

        pub.publish(twist);
        ros::spinOnce();
    }

    return 0;
}