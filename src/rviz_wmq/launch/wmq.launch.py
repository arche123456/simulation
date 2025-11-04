import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory#获取功能包下share目录路径
#from 模块或包名 import 类名或函数名 后续可以直接调用类名或函数名不需要加模块或包名
#import可以直接引入模块和包名，然后通过模块名.类名或函数名来使用
def generate_launch_description():
    #package包名   executable可执行文件   name节点名称   output输出方式
    #ros2 launch rviz_wmq wmq.launch.py model:=$(ros2 pkg prefix --share rviz_wmq)/urdf_wmq/urdf/xxxx.urdf

    #ParameterValue将一个值封装成可识别的参数值类型，command捕获输出作为参数值，
    urdf_file_path = os.path.join(
        get_package_share_directory('rviz_wmq'),
        'urdf_wmq', 'urdf', 'wmq_robot.urdf'
    )
    model = DeclareLaunchArgument(
        name="model",
        default_value = urdf_file_path
    )

    #rviz配置文件路径，可直接打开配置好的rviz文件
    rviz_file_path = os.path.join(
        get_package_share_directory('rviz_wmq'),
        'rviz', 'wmq_box.rviz'
    )


    # 使用ParameterValue和Command封装URDF描述,用作节点的参数值
    robot_description = ParameterValue(
        Command(['xacro ', LaunchConfiguration("model")]),
    )

    #前者为实例的节点名称，可以自定，后者为功能包名称和可执行文件名称必须与功能包robot_state_publisher的一致
    #通过初始化列表将robot_description赋给robot_state_publisher节点的robot_description参数
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{"robot_description":robot_description}]
        )
    
    #joint_state_publisher节点用于发布动态关节状态信息
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher'
    )
    
    #rviz2节点用于可视化
    rviz2 = Node(package='rviz2',
                 executable='rviz2', 
                 arguments=['-d', rviz_file_path],
                 output='screen')

    return LaunchDescription([model, robot_state_publisher, joint_state_publisher, rviz2])