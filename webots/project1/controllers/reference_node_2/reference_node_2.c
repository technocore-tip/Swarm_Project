#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <webots/motor.h>
#include <webots/nodes.h>
#include <webots/robot.h>
#include <webots/emitter.h>
#include <webots/receiver.h>
#include <webots/emitter.h>

int wb_emitter_send(WbDeviceTag tag, const void *data, int size);

static WbDeviceTag tag,emitters;


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
  emitters = wb_robot_get_device("emitter");
  wb_receiver_enable(tag, 60);
  
  step();
}
static void send_message(char *signal_strength){
  //char message[128];
  //sprintf(message, "node%d", 2);
    wb_emitter_send(emitters, signal_strength, strlen(signal_strength) + 1);
    printf("%s\n",signal_strength);
passive_wait(0.2);
}

int main(int argc, char **argv) {
  wb_robot_init();
  printf("Initializing Receiver Node 2 loc (-1,1,0)\n");
  init_devices();
  int channel=wb_receiver_get_channel(tag);
 // printf("channel: %d\n",channel);

while (true)
{
  char signal_streng[150]="ref_node2:";
  char temp[9] =" ";
  //signal_strength="a";
  while (wb_receiver_get_queue_length(tag) > 0) 
  {
  
    const char *message = wb_receiver_get_data(tag);
    const double *dir = wb_receiver_get_emitter_direction(tag);
    double signal = wb_receiver_get_signal_strength(tag);
 //   printf("reference_node1: %s (signal=%g, dir=[%g %g %g])\n",
 //          message, signal, dir[0], dir[1], dir[2]);
    wb_receiver_next_packet(tag);
    sprintf(temp, "%f", signal);
    strcat(signal_streng,message);
    strcat(signal_streng,temp);
    strcat(signal_streng," ");
    //strcat(signal_streng,temp);
  //  printf("next packet\n");
  }
 // printf("all signal: %s \n",signal_streng);
  //printf("packet complete\n");
  send_message(signal_streng);
  passive_wait(0.2);
  memset(signal_streng, 0, 150);
  memset(temp, 0,9);
      step();
};

  return EXIT_SUCCESS;
}
