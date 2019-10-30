# Copyright 2019 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import launch
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    os.environ["PX4_HOME_LAT"] = "37.7332531";
    os.environ["PX4_HOME_LON"] = "-119.5616378";
    os.environ["PX4_HOME_ALT"] = "2800.4";

    gazebo_dir = get_package_share_directory('gazebo_ros')
    included_launch = launch.actions.IncludeLaunchDescription(
                launch.launch_description_sources.PythonLaunchDescriptionSource(gazebo_dir + '/launch/gazebo.launch.py'),
                launch_arguments={'world': 'worlds/yosemite.world',
                                  'paused': 'false',
                                  'physics': 'ode'}.items()
                )
    return LaunchDescription([
        Node(package='sitl_launcher', node_executable='launch_drone_ros2.py', output='screen'),
        included_launch,
    ])
