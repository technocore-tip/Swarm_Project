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
#include <webots/inertial_unit.h>
static int node_no=5;

int wb_emitter_send(WbDeviceTag tag, const void *data, int size);
/* Device stuff */


#define LEDS_NUMBER 10
static WbDeviceTag leds[LEDS_NUMBER];
static bool leds_values[LEDS_NUMBER];
static const char *leds_names[LEDS_NUMBER] = {"led0", "led1", "led2", "led3", "led4", "led5", "led6", "led7", "led8", "led9"};

static WbDeviceTag left_motor, right_motor,emitters,imu,receivers;

#define LEFT 0
#define RIGHT 1
#define MAX_SPEED 6.28
/* Breitenberg stuff */

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
  int i;

  for (i = 0; i < LEDS_NUMBER; i++)
    leds[i] = wb_robot_get_device(leds_names[i]);


  // get a handler to the motors and set target position to infinity (speed control).
  receivers = wb_robot_get_device("receiver");
  left_motor = wb_robot_get_device("left wheel motor");
  right_motor = wb_robot_get_device("right wheel motor");
  emitters = wb_robot_get_device("emitter");
  imu = wb_robot_get_device("inertial_unit");
  
  wb_receiver_enable(receivers, 60);
  wb_inertial_unit_enable(imu,get_time_step());
  wb_motor_set_position(left_motor, INFINITY);
  wb_motor_set_position(right_motor, INFINITY);
  wb_motor_set_velocity(left_motor, 0.0);
  wb_motor_set_velocity(right_motor, 0.0);
 
  step();
}


static void blink_leds() {
  static int counter = 0;
  counter++;
  leds_values[(counter / 10) % LEDS_NUMBER] = true;
}

static void turn_left() {
  wb_motor_set_velocity(left_motor, -MAX_SPEED/4);
  wb_motor_set_velocity(right_motor, MAX_SPEED/4);
  passive_wait(0.2);
}

static void turn_right() {
  wb_motor_set_velocity(left_motor, MAX_SPEED/4);
  wb_motor_set_velocity(right_motor,-MAX_SPEED/4);
  passive_wait(0.2);
}

static float orientation_angle(){
const double *orientation = wb_inertial_unit_get_roll_pitch_yaw(imu);
float angle=0;
  if(orientation[2]<0)
  {
      angle=orientation[2]+ (2*3.14159265358979323846);
  }
  else
  {
    angle=orientation[2];
  }
return angle;
}
static void send_message(){
  char message[128];
  sprintf(message, "%d_", node_no);
  wb_emitter_send(emitters, message, strlen(message) + 1);
  passive_wait(0.2);
}

int main(int argc, char **argv) {
  wb_robot_init();
  printf("Default controller of the e-puck robot started...\n");
  init_devices();
  step();
  
  while (true) {
    send_message();
    while (wb_receiver_get_queue_length(receivers) > 0) 
      {
         char *message = wb_receiver_get_data(receivers);
         char * token = strtok(message, " ");
         int message_counter=0,node_id=0;
         float magnitude=0,angle=0;         
         while( token != NULL ) {

            if(message_counter==0)
            {
              if(atoi(token)==node_no)
              {
                node_id=atoi(token);
               }
            }
            if(message_counter==3)
            {
               magnitude=atof(token);
            }      
            if(message_counter==4)
            {
               angle=atof(token);          
            }               
            token = strtok(NULL, " ");
            message_counter++;
         }
         if(node_id == node_no)
         {
           float current_angle = orientation_angle();
           //printf("current angle %f\n",current_angle);
           while((current_angle > angle+0.2)||(current_angle < angle-0.2))
           {
               if((current_angle > angle+0.2)||(current_angle > angle-0.2)) //rotate  clockwise
               {
                 turn_right();
                 step();
               }
               if((current_angle < angle+0.2)||(current_angle < angle-0.2)) // rotate  counter clockwise
               {
                   turn_left();
                   step();
               }
             current_angle = orientation_angle();
             //printf("current angle %f\n",current_angle);
//             printf("target angle %f\n",angle);
            }
            //printf("magnitude : %f",magnitude);
            wb_motor_set_velocity(left_motor, 0);
            wb_motor_set_velocity(right_motor,0);
            step();
            //float t= magnitude/(12.874*0.1);
            wb_motor_set_velocity(left_motor,2.44*magnitude);
            wb_motor_set_velocity(right_motor,2.44*magnitude);
            passive_wait(0.2);
            wb_motor_set_velocity(left_motor, 0);
            wb_motor_set_velocity(right_motor,0);
         }
         message_counter=0;
         magnitude=0;
         node_id=0;
         wb_receiver_next_packet(receivers);
         blink_leds();
         step();
      }
  };

  return EXIT_SUCCESS;
}
