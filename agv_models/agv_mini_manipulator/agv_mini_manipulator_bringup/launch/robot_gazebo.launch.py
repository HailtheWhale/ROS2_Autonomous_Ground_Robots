from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
import os
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_path

def generate_launch_description():

    urdf_path = os.path.join(get_package_share_path('agv_mini_manipulator_description'), 
                             'urdf', 'robot.urdf.xacro')

    rviz_config_path = os.path.join(get_package_share_path('agv_mini_manipulator_bringup'),
                                    'rviz', 'mobile_base_display.rviz')
    
    gz_world_path = os.path.join(get_package_share_path('agv_sim_gz'),
                                      'worlds', 'test_world.sdf')

    gz_bridge_config_path = os.path.join(get_package_share_path('agv_mini_manipulator_bringup'),
                                      'config', 'gazebo_bridge_robot.yaml')


    robot_description = ParameterValue(Command(['xacro ', urdf_path]),value_type=str)

    # Nodes
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_path]
    )

    # Gazebo
    gz_node = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [os.path.join(get_package_share_path('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
                    launch_arguments={'gz_args': ['-r -v4 ', gz_world_path], 'on_exit_shutdown': 'true'}.items()
             )

    gz_spawn_robot_node = Node(package='ros_gz_sim', executable='create',
                            arguments=['-topic', 'robot_description'],
                            output='screen')


    # Launch node list
    return LaunchDescription([
        robot_state_publisher_node,
        rviz2_node,
        gz_node,  
        gz_spawn_robot_node,
    ])
