# rosbag record commands

### eveything
rosbag record --split --size=1024 --duration=4 -b 0 -a

### 2 camerainfoRGB + camerainfoDepth
rosbag record --split --size=1024 -b 0 /abretesesamo/rgb/camera_info /ervilhamigalhas/rgb/camera_info /ervilhamigalhas/depth/camera_info /abretesesamo/depth/camera_info

### 1 rgb + camera_params
rosbag record --split --size=1024 -b 0 /abretesesamo/rgb/image_color /abretesesamo/rgb/camera_info

### 2 rgb 
rosbag record --split --size=1024 -b 0 /abretesesamo/rgb/image_color /ervilhamigalhas/rgb/image_color

### 1 rgb + depth
rosbag record --split --size=1024 -b 0 /camera/depth_registered/image_raw  /camera/rgb/image_color /camera/depth/camera_info /camera/rgb/camera_info

### 2 pc2
rosbag record --split --size=1024 -b 0 /ervilhamigalhas/depth_registered/points /abretesesamo/depth_registered/points

### 2 rgb + depth
rosbag record --split --size=1024 -b 0 /ervilhamigalhas/depth_registered/image_raw /abretesesamo/depth_registered/image_raw /ervilhamigalhas/rgb/image_color /abretesesamo/rgb/image_color

### 2 rgb + depth + pc2
rosbag record --split --size=2048 -b 0 /ervilhamigalhas/depth_registered/image_raw /abretesesamo/depth_registered/image_raw /ervilhamigalhas/rgb/image_color /abretesesamo/rgb/image_color /ervilhamigalhas/depth_registered/points /abretesesamo/depth_registered/points

