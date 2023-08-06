/**
 * @license
 * Visual Blocks Language
 *
 * Copyright 2012 Google Inc.
 * https://developers.google.com/blockly/
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * @fileoverview Generating JavaScript for text blocks.
 * @author fraser@google.com (Neil Fraser)
 */
"use strict";

goog.provide("Blockly.JavaScript.zumi");

goog.require("Blockly.JavaScript");

Blockly.JavaScript["zumi_turn_degree_junior"] = function(block) {
  var arg0 = block.getFieldValue("NUM0");
  return "Engine.turnDegree(" + arg0 + ");\n";
};

Blockly.JavaScript["zumi_turn_left_junior"] = function(block) {
  return "Engine.turnLeft();\n";
};

Blockly.JavaScript["zumi_turn_right_junior"] = function(block) {
  return "Engine.turnRight();\n";
};

Blockly.JavaScript["zumi_forward_junior"] = function(block) {
  return "Engine.forward();\n";
};

Blockly.JavaScript["zumi_forward_duration_junior"] = function(block) {
  var arg0 = block.getFieldValue("NUM0");
  return "Engine.forward(" + arg0 + ");\n";
};

Blockly.JavaScript["zumi_reverse_junior"] = function(block) {
  return "Engine.reverse();\n";
};

Blockly.JavaScript["zumi_reverse_duration_junior"] = function(block) {
  var arg0 = block.getFieldValue("NUM0");
  return "Engine.reverse(" + arg0 + ");\n";
};

Blockly.JavaScript["zumi_stop_junior"] = function(block) {
  return "Engine.stop();\n";
};

Blockly.JavaScript["zumi_get_distance_junior"] = function(block) {
  var arg0 = block.getFieldValue("TYPE");
  return [
    "Infrared.getDistance(" + arg0 + ")",
    Blockly.JavaScript.ORDER_FUNCTION_CALL
  ];
};

Blockly.JavaScript["zumi_play_sound_junior"] = function(block) {
  return "await play_sound();\n";
};

Blockly.JavaScript["zumi_smile_detected_junior"] = function(block) {
  return "await smileDetected();\n";
};

Blockly.JavaScript["zumi_face_detected_junior"] = function(block) {
  return ["faceDetected()", Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript["zumi_track_face_junior"] = function(block) {
  return "await trackFace();\n";
};

Blockly.JavaScript["zumi_collect_smile_junior"] = function(block) {
  var arg0 = block.getFieldValue("EMOTION");
  return "await collectSmile();\n";
};

Blockly.JavaScript["zumi_turn_degree_senior"] = function(block) {
  var arg0 = block.getFieldValue("NUM0");
  return "Engine.turnDegree(" + arg0 + ");\n";
};

Blockly.JavaScript["zumi_turn_left_senior"] = function(block) {
  return "Engine.turnLeft();\n";
};

Blockly.JavaScript["zumi_turn_right_senior"] = function(block) {
  return "Engine.turnRight();\n";
};

Blockly.JavaScript["zumi_forward_senior"] = function(block) {
  return "Engine.forward();\n";
};

Blockly.JavaScript["zumi_forward_duration_senior"] = function(block) {
  var arg0 = block.getFieldValue("NUM0");
  return "Engine.forward(" + arg0 + ");\n";
};

Blockly.JavaScript["zumi_reverse_senior"] = function(block) {
  return "Engine.reverse();\n";
};

Blockly.JavaScript["zumi_reverse_duration_senior"] = function(block) {
  var arg0 = block.getFieldValue("NUM0");
  return "Engine.reverse(" + arg0 + ");\n";
};

Blockly.JavaScript["zumi_stop_senior"] = function(block) {
  return "Engine.stop();\n";
};

Blockly.JavaScript["zumi_get_distance_senior"] = function(block) {
  var arg0 = block.getFieldValue("TYPE");
  return [
    "Infrared.getDistance(" + arg0 + ")",
    Blockly.JavaScript.ORDER_FUNCTION_CALL
  ];
};

Blockly.JavaScript["zumi_play_sound_senior"] = function(block) {
  return "await play_sound();\n";
};

Blockly.JavaScript["zumi_personality_act_junior"] = function(block) {
  var arg0 = block.getFieldValue("EMOTION");
  if (arg0 === "Emotion.HAPPY") {
    return "personality.happy_zumi()\n";
  } else if (arg0 === "Emotion.SAD") {
    return "personality.sad_zumi()\n";
  }
  return "personality.excited_zumi()\n";
};

Blockly.JavaScript["zumi_personality_act_senior"] = function(block) {
  var arg0 = block.getFieldValue("EMOTION");
  if (arg0 === "Emotion.HAPPY") {
    return "personality.happy_zumi()\n";
  } else if (arg0 === "Emotion.SAD") {
    return "personality.sad_zumi()\n";
  }
  return "personality.excited_zumi()\n";
};

Blockly.JavaScript["zumi_smile_detected_senior"] = function(block) {
  return "await smileDetected();\n";
};

Blockly.JavaScript["zumi_face_detected_senior"] = function(block) {
  return ["faceDetected()", Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript["zumi_track_face_senior"] = function(block) {
  return "await trackFace();\n";
};

Blockly.JavaScript["zumi_collect_smile_senior"] = function(block) {
  var arg0 = block.getFieldValue("EMOTION");
  return "await collectSmile();\n";
};

Blockly.JavaScript["zumi_take_photo_junior"] = function(block) {
  return "await takePhoto();\n";
};

Blockly.JavaScript["zumi_take_photo_senior"] = function(block) {
  return "await takePhoto();\n";
};

Blockly.JavaScript["zumi_camera_show_junior"] = function(block) {
  return "await show();\n";
};

Blockly.JavaScript["zumi_camera_show_senior"] = function(block) {
  return "await show();\n";
};

Blockly.JavaScript["zumi_engine_set_speed_junior"] = function(block) {
  var arg0 = block.getFieldValue("NUM0");
  return "setSpeed(" + arg0 + ");\n";
};

Blockly.JavaScript["zumi_engine_set_speed_senior"] = function(block) {
  var arg0 = block.getFieldValue("NUM0");
  return "setSpeed(" + arg0 + ");\n";
};

Blockly.JavaScript["zumi_lights_on_junior"] = function(block) {
  return "turnOn();\n";
};

Blockly.JavaScript["zumi_lights_on_senior"] = function(block) {
  return "turnOn();\n";
};

Blockly.JavaScript["zumi_lights_off_junior"] = function(block) {
  return "turnOff();\n";
};

Blockly.JavaScript["zumi_lights_off_senior"] = function(block) {
  return "turnOff();\n";
};

Blockly.JavaScript["zumi_jedi_drive_junior"] = function(block) {
  return "jediDrive();\n";
};

Blockly.JavaScript["zumi_jedi_drive_senior"] = function(block) {
  return "jediDrive();\n";
};

Blockly.JavaScript["zumi_wait_junior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  return "wait(" + arg0 + ");\n";
};

Blockly.JavaScript["zumi_wait_junior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  return "wait(" + arg0 + ");\n";
};

Blockly.JavaScript["zumi_parallel_park_junior"] = function(block) {
  return "zumi.parallel_park();\n";
};

Blockly.JavaScript["zumi_brake_junior"] = function(block) {
  return "zumi.hard_brake();\n";
};

Blockly.JavaScript["zumi_reverse_seconds_junior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  return "zumi.reverse(" + arg0 + ");\n";
};

Blockly.JavaScript["zumi_forward_seconds_junior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  return "zumi.forward(" + arg0 + ");\n";
};

Blockly.JavaScript["zumi_turn_left_junior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("ANGLE"));
  return "zumi.turn_left(" + arg0 + ");\n";
};

Blockly.JavaScript["zumi_turn_right_junior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("ANGLE"));
  return "zumi.turn_right(" + arg0 + ");\n";
};

Blockly.JavaScript["zumi_left_u_turn_junior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  return "zumi.left_u_turn(speed=" + arg0 + ", step=4, delay=0.02);\n";
};

Blockly.JavaScript["zumi_right_u_turn_junior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  return "zumi.right_u_turn(speed=" + arg0 + ", step=4, delay=0.02);\n";
};

Blockly.JavaScript["zumi_circle_junior"] = function(block) {
  var arg0 = block.getFieldValue("CIRCLE");
  return "zumi.circle("+ arg0 + ");\n";
};

Blockly.JavaScript["zumi_triangle_junior"] = function(block) {
  var arg0 = block.getFieldValue("TRIANGLE");
  return "zumi.triangle("+ arg0 + ");\n";
};

Blockly.JavaScript["zumi_square_junior"] = function(block) {
  var arg0 = block.getFieldValue("SQUARE");
  return "zumi.square("+ arg0 + ");\n";
};

Blockly.JavaScript["zumi_rectangle_junior"] = function(block) {
  return "zumi.rectangle(direction=-1);\n";
};

Blockly.JavaScript["zumi_figure_8_junior"] = function(block) {
  return "zumi.figure_8();\n";
};

Blockly.JavaScript["zumi_j_turn_junior"] = function(block) {
  return "zumi.j_turn();\n";
};

Blockly.JavaScript["zumi_sleep_junior"] = function(block) {
  return "eyes.sleep()\n";
};

Blockly.JavaScript["zumi_sleep_senior"] = function(block) {
  return "eyes.sleep()\n";
};

Blockly.JavaScript["zumi_wakeup_junior"] = function(block) {
  return "eyes.wakeUp()\n";
};

Blockly.JavaScript["zumi_wakeup_senior"] = function(block) {
  return "eyes.wakeUp()\n";
};

Blockly.JavaScript["zumi_blink_junior"] = function(block) {
  return "eyes.blink()\n";
};

Blockly.JavaScript["zumi_blink_senior"] = function(block) {
  return "eyes.blink()\n";
};

Blockly.JavaScript["zumi_excited_junior"] = function(block) {
  return "eyes.excited()\n";
};

Blockly.JavaScript["zumi_excited_senior"] = function(block) {
  return "eyes.excited()\n";
};

Blockly.JavaScript["zumi_look_left_junior"] = function(block) {
  return "eyes.lookLeft()\n";
};

Blockly.JavaScript["zumi_look_left_senior"] = function(block) {
  return "eyes.lookLeft()\n";
};

Blockly.JavaScript["zumi_look_right_junior"] = function(block) {
  return "eyes.lookRight()\n";
};

Blockly.JavaScript["zumi_look_right_senior"] = function(block) {
  return "eyes.lookRight()\n";
};

Blockly.JavaScript["zumi_sad_junior"] = function(block) {
  return "eyes.sad()\n";
};

Blockly.JavaScript["zumi_sad_senior"] = function(block) {
  return "eyes.sad()\n";
};

Blockly.JavaScript["zumi_hello_junior"] = function(block) {
  return "eyes.hello()\n";
};

Blockly.JavaScript["zumi_hello_senior"] = function(block) {
  return "eyes.hello()\n";
};

Blockly.JavaScript["zumi_glimmer_junior"] = function(block) {
  return "eyes.glimmer()\n";
};

Blockly.JavaScript["zumi_glimmer_senior"] = function(block) {
  return "eyes.glimmer()\n";
};

Blockly.JavaScript["zumi_happy_junior"] = function(block) {
  return "eyes.happy()\n";
};

Blockly.JavaScript["zumi_happy_senior"] = function(block) {
  return "eyes.happy()\n";
};
