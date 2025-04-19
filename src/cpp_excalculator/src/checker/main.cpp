// src/arithmetic/main.cpp

#include "../include/checker/checker.h"

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);

    auto checker_node = std::make_shared<Checker>();

    // 10.0까지 누적 합산을 수행하도록 목표 전송
    checker_node->send_goal_total_sum(10.0f);

    rclcpp::spin(checker_node);
    rclcpp::shutdown();
    return 0;
}
