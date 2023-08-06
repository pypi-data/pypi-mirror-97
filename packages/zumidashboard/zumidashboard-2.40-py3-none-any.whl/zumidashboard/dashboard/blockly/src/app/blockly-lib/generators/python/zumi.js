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
 * @fileoverview Generating Python for logic blocks.
 * @author q.neutron@gmail.com (Quynh Neutron)
 */
"use strict";

goog.provide("Blockly.Python.zumi");

goog.require("Blockly.Python");

Blockly.Python["zumi_turn_degree_junior"] = function(block) {
  var arg0 = block.getFieldValue("NUM0");
  return "engine.turn_degree(" + arg0 + ")\n";
};

Blockly.Python["zumi_turn_degree_senior"] = function(block) {
  var arg0 = block.getFieldValue("NUM0");
  return "engine.turn_degree(" + arg0 + ")\n";
};

Blockly.Python["zumi_turn_left_junior"] = function(block) {
  return "engine.left()\n";
};

Blockly.Python["zumi_turn_left_senior"] = function(block) {
  return "engine.left()\n";
};

Blockly.Python["zumi_turn_right_junior"] = function(block) {
  return "engine.right()\n";
};

Blockly.Python["zumi_turn_right_senior"] = function(block) {
  return "engine.right()\n";
};

Blockly.Python["zumi_forward_junior"] = function(block) {
  return "engine.forward()\n";
};

Blockly.Python["zumi_forward_senior"] = function(block) {
  return "engine.forward()\n";
};

Blockly.Python["zumi_forward_seconds_junior"] = function(block) {
  var arg0 = block.getFieldValue("NUM0");
  return "zumi.forward(duration=" + arg0 + ")\n";
};


Blockly.Python["zumi_parallel_park_junior"] = function(block) {
  return "zumi.parallel_park()\n";
};

Blockly.Python["zumi_brake_junior"] = function(block) {
  return "zumi.hard_brake()\n";
};

Blockly.Python["zumi_reverse_seconds_junior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  return "zumi.reverse(duration=" + arg0 + ")\n";
};

Blockly.Python["zumi_turn_left_junior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("ANGLE"));
  return "zumi.turn_left(desired_angle=" + arg0 +", duration=1)\n";
};

Blockly.Python["zumi_turn_right_junior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("ANGLE"));
  return "zumi.turn_right(desired_angle=" + arg0 +", duration=1)\n";
};

Blockly.Python["zumi_left_u_turn_junior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  return "zumi.left_u_turn(speed=" + arg0 + ", step=4, delay=0.02)\n";
};

Blockly.Python["zumi_right_u_turn_junior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  return "zumi.right_u_turn(speed=" + arg0 + ", step=4, delay=0.02)\n";
};

Blockly.Python["zumi_circle_junior"] = function(block) {
  var arg0 = block.getFieldValue("CIRCLE");
  return "zumi.circle("+ arg0 + ")\n";
};

Blockly.Python["zumi_triangle_junior"] = function(block) {
  var arg0 = block.getFieldValue("TRIANGLE");
  return "zumi.triangle("+ arg0 + ")\n";
};

Blockly.Python["zumi_square_junior"] = function(block) {
  var arg0 = block.getFieldValue("SQUARE");
  return "zumi.square("+ arg0 + ")\n";
};

Blockly.Python["zumi_rectangle_junior"] = function(block) {
  return "zumi.rectangle(direction=-1)\n";
};

Blockly.Python["zumi_figure_8_junior"] = function(block) {
  return "zumi.figure_8()\n";
};

Blockly.Python["zumi_j_turn_junior"] = function(block) {
  return "zumi.j_turn()\n";
};

Blockly.Python["zumi_draw_text_junior"] = function(block) {
  var arg0 = block.getFieldValue("TEXT");
  return "zumi.draw_text_center(\"" + arg0 + "\")\n";
};

Blockly.Python["zumi_sad_junior"] = function(block) {
  return "zumi.sad()\n";
};

Blockly.Python["zumi_closed_eyes_junior"] = function(block) {
  return "zumi.close_eyes()\n";
};

Blockly.Python["zumi_sleepy_eyes_junior"] = function(block) {
  return "zumi.sleepy_eyes()\n";
};

Blockly.Python["zumi_happy_eyes_junior"] = function(block) {
  return "zumi.happy()\n";
};

Blockly.Python["zumi_glimmer_eyes_junior"] = function(block) {
  return "zumi.glimmer()\n";
};

Blockly.Python["zumi_glimmer_eyes_junior"] = function(block) {
  return "zumi.angry()\n";
};

Blockly.Python["zumi_open_eyes_junior"] = function(block) {
  return "zumi.hello()\n";
};

Blockly.Python["zumi_blinking_eyes_junior"] = function(block) {
  return "zumi.blink()\n";
};

Blockly.Python["zumi_forward_duration_senior"] = function(block) {
  var arg0 = block.getFieldValue("NUM0");
  return "engine.forward(" + arg0 + ")\n";
};

Blockly.Python["zumi_reverse_junior"] = function(block) {
  return "engine.reverse()\n";
};

Blockly.Python["zumi_reverse_senior"] = function(block) {
  return "engine.reverse()\n";
};

Blockly.Python["zumi_reverse_duration_junior"] = function(block) {
  var arg0 = block.getFieldValue("NUM0");
  return "engine.reverse(" + arg0 + ")\n";
};

Blockly.Python["zumi_reverse_duration_senior"] = function(block) {
  var arg0 = block.getFieldValue("NUM0");
  return "engine.reverse(" + arg0 + ")\n";
};

Blockly.Python["zumi_stop_junior"] = function(block) {
  return "engine.stop()\n";
};

Blockly.Python["zumi_stop_senior"] = function(block) {
  return "engine.stop()\n";
};

Blockly.Python["zumi_get_distance_junior"] = function(block) {
  var arg0 = block.getFieldValue("TYPE");
  return [
    "infrared.get_distance(" + arg0 + ")",
    Blockly.Python.ORDER_FUNCTION_CALL
  ];
};

Blockly.Python["zumi_play_sound_junior"] = function(block) {
  return "speaker.play()\n";
};

Blockly.Python["zumi_personality_act_junior"] = function(block) {
  var arg0 = block.getFieldValue("EMOTION");
  if (arg0 === "Emotion.HAPPY") {
    return "personality.happy_zumi()\n";
  } else if (arg0 === "Emotion.SAD") {
    return "personality.sad_zumi()\n";
  }
  return "personality.excited_zumi()\n";
};

Blockly.Python["zumi_personality_act_senior"] = function(block) {
  var arg0 = block.getFieldValue("EMOTION");
  if (arg0 === "Emotion.HAPPY") {
    return "personality.happy_zumi()\n";
  } else if (arg0 === "Emotion.SAD") {
    return "personality.sad_zumi()\n";
  }
  return "personality.excited_zumi()\n";
};

Blockly.Python["zumi_face_detected_junior"] = function(block) {
  return ["camera.face_detected()", Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python["zumi_track_face_junior"] = function(block) {
  return "camera.track_face()\n";
};

Blockly.Python["zumi_take_photo_junior"] = function(block) {
  return "camera.take_photo()\n";
};

Blockly.Python["zumi_smile_detected_junior"] = function(block) {
  return "DeepLearning.smile_detected()\n";
};

Blockly.Python["zumi_collect_smile_junior"] = function(block) {
  var arg0 = block.getFieldValue("EMOTION");
  return "DeepLearning.collect_smile()\n";
};

Blockly.Python["zumi_get_distance_senior"] = function(block) {
  var arg0 = block.getFieldValue("TYPE");
  return [
    "infrared.get_distance(" + arg0 + ")",
    Blockly.Python.ORDER_FUNCTION_CALL
  ];
};

Blockly.Python["zumi_play_sound_senior"] = function(block) {
  var arg0 = block.getFieldValue("SOUND");
  return "speaker.play()\n";
};

Blockly.Python["zumi_face_detected_senior"] = function(block) {
  return ["camera.face_detected()", Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python["zumi_track_face_senior"] = function(block) {
  return "camera.track_face()\n";
};

Blockly.Python["zumi_take_photo_senior"] = function(block) {
  return "camera.take_photo()\n";
};

Blockly.Python["zumi_smile_detected_senior"] = function(block) {
  return "DeepLearning.smile_detected()\n";
};

Blockly.Python["zumi_collect_smile_senior"] = function(block) {
  var arg0 = block.getFieldValue("EMOTION");
  return "DeepLearning.collect_smile()\n";
};

Blockly.Python["zumi_camera_show_junior"] = function(block) {
  return "camera.show()\n";
};

Blockly.Python["zumi_camera_show_senior"] = function(block) {
  return "camera.show()\n";
};

Blockly.Python["zumi_engine_set_speed_junior"] = function(block) {
  var arg0 = block.getFieldValue("NUM0");
  return "engine.set_speed(" + arg0 + ")\n";
};

Blockly.Python["zumi_engine_set_speed_senior"] = function(block) {
  var arg0 = block.getFieldValue("NUM0");
  return "engine.set_speed(" + arg0 + ")\n";
};

Blockly.Python["zumi_lights_on_junior"] = function(block) {
  return "lights.turn_on()\n";
};

Blockly.Python["zumi_lights_on_senior"] = function(block) {
  return "lights.turn_on()\n";
};

Blockly.Python["zumi_lights_off_junior"] = function(block) {
  return "lights.turn_off()\n";
};

Blockly.Python["zumi_lights_off_senior"] = function(block) {
  return "lights.turn_off()\n";
};

Blockly.Python["zumi_jedi_drive_junior"] = function(block) {
  return "infrared.jedi_drive()\n";
};

Blockly.Python["zumi_jedi_drive_senior"] = function(block) {
  return "infrared.jedi_drive()\n";
};

Blockly.Python["zumi_wait_junior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  return "timer.wait(" + arg0 + ")\n";
};

Blockly.Python["zumi_wait_junior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  return "timer.wait(" + arg0 + ")\n";
};

Blockly.Python["zumi_sleep_junior"] = function(block) {
  return "eyes.sleep()\n";
};

Blockly.Python["zumi_sleep_senior"] = function(block) {
  return "eyes.sleep()\n";
};

Blockly.Python["zumi_wakeup_junior"] = function(block) {
  return "eyes.wake_up()\n";
};

Blockly.Python["zumi_wakeup_senior"] = function(block) {
  return "eyes.wake_up()\n";
};

Blockly.Python["zumi_blink_junior"] = function(block) {
  return "eyes.blink()\n";
};

Blockly.Python["zumi_blink_senior"] = function(block) {
  return "eyes.blink()\n";
};

Blockly.Python["zumi_excited_junior"] = function(block) {
  return "eyes.excited()\n";
};

Blockly.Python["zumi_excited_senior"] = function(block) {
  return "eyes.excited()\n";
};

Blockly.Python["zumi_look_left_junior"] = function(block) {
  return "eyes.look_left()\n";
};

Blockly.Python["zumi_look_left_senior"] = function(block) {
  return "eyes.look_left()\n";
};

Blockly.Python["zumi_look_right_junior"] = function(block) {
  return "eyes.look_right()\n";
};

Blockly.Python["zumi_look_right_senior"] = function(block) {
  return "eyes.look_right()\n";
};

Blockly.Python["zumi_hello_junior"] = function(block) {
  return "eyes.hello()\n";
};

Blockly.Python["zumi_hello_senior"] = function(block) {
  return "eyes.hello()\n";
};

Blockly.Python["zumi_glimmer_junior"] = function(block) {
  return "eyes.glimmer()\n";
};

Blockly.Python["zumi_angry_eyes_junior"] = function(block) {
  return "eyes.glimmer()\n";
};

Blockly.Python["zumi_glimmer_junior"] = function(block) {
  return "eyes.glimmer()\n";
};

Blockly.Python["zumi_glimmer_senior"] = function(block) {
  return "eyes.glimmer()\n";
};

Blockly.Python["zumi_happy_junior"] = function(block) {
  return "eyes.happy()\n";
};

Blockly.Python["zumi_happy_senior"] = function(block) {
  return "eyes.happy()\n";
};
