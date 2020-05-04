/*
 * Copyright 1996-2020 Cyberbotics Ltd.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/*
 * Description:  Default controller of the e-puck robot
 */

/* include headers */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <webots/device.h>
#include <webots/distance_sensor.h>
#include <webots/led.h>
#include <webots/motor.h>
#include <webots/nodes.h>
#include <webots/robot.h>
#include <webots/emitter.h>
#include <webots/receiver.h>


static WbDeviceTag tag;


static int get_time_step() {
  static int time_step = -1;
  if (time_step == -1)
    time_step = (int)wb_robot_get_basic_time_step();
  return time_step;
}

static void step() {
  if (wb_robot_step(get_time_step()) == -1) {
    wb_robot_cleanup();
    exit(EXIT_SUCCESS);
  }
}

static void passive_wait(double sec) {
  double start_time = wb_robot_get_time();
  do {
    step();
  } while (start_time + sec > wb_robot_get_time());
}

static void init_devices() {
  tag = wb_robot_get_device("receiver");
  wb_receiver_enable(tag, 60);
  step();
}

int main(int argc, char **argv) {
  wb_robot_init();
  printf("Default controller of the e-puck robot started...\n");

  init_devices();

  while (true) {

while (wb_receiver_get_queue_length(tag) > 0) {
  const char *message = wb_receiver_get_data(tag);
  const double *dir = wb_receiver_get_emitter_direction(tag);
  double signal = wb_receiver_get_signal_strength(tag);
  printf("reference_node1: %s (signal=%g, dir=[%g %g %g])\n",
         message, signal, dir[0], dir[1], dir[2]);
  wb_receiver_next_packet(tag);
}
passive_wait(0.2);
    step();
  };

  return EXIT_SUCCESS;
}
