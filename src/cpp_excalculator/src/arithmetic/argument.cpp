#include "rclcpp/rclcpp.hpp"
#include "rcl_interfaces/msg/set_parameters_result.hpp"
#include "ros_study_msgs/msg/arithmetic_argument.hpp"

#include <random>

class Argument : public rclcpp::Node
{
public:
    Argument() : Node("argument")
    {
        RCLCPP_INFO(this->get_logger(), "Argument init set start");

        // Declare parameters
        //this는 Argument의 포인터
        this->declare_parameter("qos_depth", 10); 
        this->declare_parameter("min_random_num", 0);
        this->declare_parameter("max_random_num", 9);

        qos_depth_ = this->get_parameter("qos_depth").as_int();
        min_random_num_ = this->get_parameter("min_random_num").as_int();
        max_random_num_ = this->get_parameter("max_random_num").as_int();

        RCLCPP_INFO(this->get_logger(), "qos_depth set %d", qos_depth_);
        RCLCPP_INFO(this->get_logger(), "min_random_num set %d", min_random_num_);
        RCLCPP_INFO(this->get_logger(), "max_random_num set %d", max_random_num_);

        // Parameter callback
        parameter_callback_handle_ = this->add_on_set_parameters_callback(
            std::bind(&Argument::on_parameter_changed, this, std::placeholders::_1));

        RCLCPP_INFO(this->get_logger(), "add_on_set_parameters_callback on");

        // QoS 설정
        rclcpp::QoS qos(rclcpp::QoSInitialization::from_rmw(rmw_qos_profile_default));
        qos.keep_last(qos_depth_);
        qos.reliability(RMW_QOS_POLICY_RELIABILITY_RELIABLE);
        qos.durability(RMW_QOS_POLICY_DURABILITY_VOLATILE);

        // Publisher 생성
        publisher_ = this->create_publisher<ros_study_msgs::msg::ArithmeticArgument>(
            "arithmetic_argument", qos);

        timer_ = this->create_wall_timer(
            std::chrono::seconds(1),
            std::bind(&Argument::publish_random_message, this));

        RCLCPP_INFO(this->get_logger(), "publish topic : arithmetic_argument_publisher");
        RCLCPP_INFO(this->get_logger(), "end init");
    }

private:

rclcpp::Publisher<ros_study_msgs::msg::ArithmeticArgument>::SharedPtr publisher_;
rclcpp::TimerBase::SharedPtr timer_;
OnSetParametersCallbackHandle::SharedPtr parameter_callback_handle_;

int qos_depth_;
int min_random_num_;
int max_random_num_;

    void publish_random_message()
    {
        ros_study_msgs::msg::ArithmeticArgument msg;
        msg.stamp = this->now();

        msg.argument_a = static_cast<float>(get_random(min_random_num_, max_random_num_));
        msg.argument_b = static_cast<float>(get_random(min_random_num_, max_random_num_));

        publisher_->publish(msg);

        RCLCPP_INFO(this->get_logger(), "Published argument a: %.1f", msg.argument_a);
        RCLCPP_INFO(this->get_logger(), "Published argument b: %.1f", msg.argument_b);
    }

    rcl_interfaces::msg::SetParametersResult on_parameter_changed(
        const std::vector<rclcpp::Parameter> &params)
    {
        RCLCPP_INFO(this->get_logger(), "start update_parameter");

        for (const auto &param : params)
        {
            if (param.get_name() == "min_random_num" && param.get_type() == rclcpp::ParameterType::PARAMETER_INTEGER)
            {
                min_random_num_ = param.as_int();
                RCLCPP_INFO(this->get_logger(), "self.min_random_num = %d", min_random_num_);
            }
            else if (param.get_name() == "max_random_num" && param.get_type() == rclcpp::ParameterType::PARAMETER_INTEGER)
            {
                max_random_num_ = param.as_int();
                RCLCPP_INFO(this->get_logger(), "self.max_random_num = %d", max_random_num_);
            }
        }

        rcl_interfaces::msg::SetParametersResult result;
        result.successful = true;
        return result;
    }

    int get_random(int min, int max)
    {
        static std::random_device rd;
        static std::mt19937 gen(rd());
        std::uniform_int_distribution<> dis(min, max);
        return dis(gen);
    }

};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<Argument>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
