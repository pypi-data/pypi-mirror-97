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

goog.provide("Blockly.Python.codrone");

goog.require("Blockly.Python");

Blockly.Python["take_off_junior"] = function(block) {
  return "drone.takeoff()\n";
};

Blockly.Python["take_off_senior"] = function(block) {
  return "drone.takeoff()\n";
};

Blockly.Python["go"] = function(block) {
  return "go()\n";
};

Blockly.Python["go_5"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  var arg1 = parseInt(block.getFieldValue("NUM1"));
  var arg2 = parseInt(block.getFieldValue("NUM2"));
  var arg3 = parseInt(block.getFieldValue("NUM3"));
  var arg4 = parseInt(block.getFieldValue("NUM4"));
  return (
    "go(" + arg0 + "," + arg1 + "," + arg2 + "," + arg3 + "," + arg4 + ")\n"
  );
};

Blockly.Python["turn_degree_junior_2"] = function(block) {
  var direction = block.getFieldValue("DIRECTION");
  var arg0 = block.getFieldValue("DIRECTIONDEGREE");
  return "drone.turn_degree(" + direction + "," + arg0 + ")\n";
};

Blockly.Python["turn_degree_senior"] = function(block) {
  var direction = block.getFieldValue("DIRECTION");
  var arg0 = block.getFieldValue("DIRECTIONDEGREE");
  return "drone.turn_degree(" + arg0 + "," + direction + ")\n";
};

Blockly.Python["turn_junior_3"] = function(block) {
  var type = block.getFieldValue("TYPE");
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  var arg1 = parseInt(block.getFieldValue("NUM1"));
  return "drone.turn(" + type + "," + arg0 + "," + arg1 + ")\n";
};

Blockly.Python["turn_senior"] = function(block) {
  var type = block.getFieldValue("TYPE");
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  var arg1 = parseInt(block.getFieldValue("NUM1"));
  return "drone.turn(" + type + "," + arg0 + "," + arg1 + ")\n";
};

Blockly.Python["turn_90_junior"] = function(block) {
  var direction = block.getFieldValue("DIRECTION");
  return "turn90(" + direction + ")\n";
};

Blockly.Python["rotate_junior"] = function(block) {
  var degree = block.getFieldValue("DEGREE");
  return "rotate(" + degree + ")\n";
};

Blockly.Python["isReadyToFly_junior"] = function(block) {
  return ["drone.is_ready_to_fly()", Blockly.Python.ORDER_FUNCTION_CALL];
};

Blockly.Python["isUpsideDown_junior"] = function(block) {
  return ["drone.is_upside_down()", Blockly.Python.ORDER_FUNCTION_CALL];
};

Blockly.Python["isFlying_junior"] = function(block) {
  return ["drone.is_flying()", Blockly.Python.ORDER_FUNCTION_CALL];
};

Blockly.Python["isReadyToFly_senior"] = function(block) {
  return ["drone.is_ready_to_fly()", Blockly.Python.ORDER_FUNCTION_CALL];
};

Blockly.Python["isUpsideDown_senior"] = function(block) {
  return ["drone.is_upside_down()", Blockly.Python.ORDER_FUNCTION_CALL];
};

Blockly.Python["isFlying_senior"] = function(block) {
  return ["drone.is_flying()", Blockly.Python.ORDER_FUNCTION_CALL];
};

Blockly.Python["getHeight_junior"] = function(block) {
  return ["drone.get_height()", Blockly.Python.ORDER_FUNCTION_CALL];
};

Blockly.Python["getState_senior"] = function(block) {
  return ["drone.get_state()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

// Gets
Blockly.Python["getHeight_senior"] = function(block) {
  return ["drone.get_height()", Blockly.Python.ORDER_FUNCTION_CALL];
};

Blockly.Python["getPressure_senior"] = function(block) {
  return ["drone.get_pressure()", Blockly.Python.ORDER_FUNCTION_CALL];
};

Blockly.Python["getOpticalFlow_senior"] = function(block) {
  return ["drone.get_opt_flow_position()", Blockly.Python.ORDER_FUNCTION_CALL];
};

Blockly.Python["getBarometer_senior"] = function(block) {
  return ["drone.get_barometer()", Blockly.Python.ORDER_FUNCTION_CALL];
};

Blockly.Python["getTemperature_senior"] = function(block) {
  return ["drone.get_temperature()", Blockly.Python.ORDER_FUNCTION_CALL];
};

Blockly.Python["getAngles_senior"] = function(block) {
  return ["drone.get_gyro_angles()", Blockly.Python.ORDER_FUNCTION_CALL];
};

Blockly.Python["getAngularSpeed_senior"] = function(block) {
  return ["drone.get_angular_speed()", Blockly.Python.ORDER_FUNCTION_CALL];
};

Blockly.Python["getAccelerometer_senior"] = function(block) {
  return ["drone.get_accelerometer()", Blockly.Python.ORDER_FUNCTION_CALL];
};

Blockly.Python["getBatteryPercentage_junior"] = function(block) {
  return ["drone.get_battery_percentage()", Blockly.Python.ORDER_FUNCTION_CALL];
};

Blockly.Python["getBatteryPercentage_senior"] = function(block) {
  return ["drone.get_battery_percentage()", Blockly.Python.ORDER_FUNCTION_CALL];
};

Blockly.Python["getGyroData_junior"] = function(block) {
  return ["drone.get_gyro_angles()", Blockly.Python.ORDER_FUNCTION_CALL];
};

Blockly.Python["getBatteryVoltage_senior"] = function(block) {
  return ["drone.get_battery_voltage()", Blockly.Python.ORDER_FUNCTION_CALL];
};

Blockly.Python["getTrim_senior"] = function(block) {
  return ["drone.get_trim()", Blockly.Python.ORDER_FUNCTION_CALL];
};

// End Gets

Blockly.Python["gotoheight_junior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("HEIGHT"));
  return "drone.go_to_height(" + arg0 + ")\n";
};

Blockly.Python["gotoheight2_junior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("HEIGHT"));
  return "drone.go_to_height(" + arg0 + ");\n";
};

Blockly.Python["gotoheight_senior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM1"));
  return "drone.go_to_height(" + arg0 + ")\n";
};

Blockly.Python["hover_junior"] = function(block) {
  var arg0 = parseFloat(block.getFieldValue("NUM0"));
  return "drone.hover(" + arg0 + ")\n";
};

Blockly.Python["setArmRGB_junior"] = function(block) {
  var arg0 = Blockly.Python.quote_(block.getFieldValue("COLOUR"));

  var rColor = parseInt("0x" + arg0.substring(2, 4));

  var gColor = parseInt("0x" + arg0.substring(4, 6));

  var bColor = parseInt("0x" + arg0.substring(6, 8));

  var arg1 = block.getFieldValue("LEDMODE");
  var arg2 = block.getFieldValue("INTERVAL");

  return (
    "drone.set_arm_LED(" +
    rColor +
    "," +
    gColor +
    "," +
    bColor +
    "," +
    arg1 +
    "," +
    arg2 +
    ")\n"
  );
};

Blockly.Python["setEyeRGB_junior"] = function(block) {
  var arg0 = Blockly.Python.quote_(block.getFieldValue("COLOUR"));

  var rColor = parseInt("0x" + arg0.substring(2, 4));

  var gColor = parseInt("0x" + arg0.substring(4, 6));

  var bColor = parseInt("0x" + arg0.substring(6, 8));

  var arg1 = block.getFieldValue("LEDMODE");
  var arg2 = block.getFieldValue("INTERVAL");

  return (
    "drone.set_eye_LED(" +
    rColor +
    "," +
    gColor +
    "," +
    bColor +
    "," +
    arg1 +
    "," +
    arg2 +
    ")\n"
  );
};

Blockly.Python["setArmRGB_junior"] = function(block) {
  var arg0 = Blockly.Python.quote_(block.getFieldValue("COLOUR"));

  var rColor = parseInt("0x" + arg0.substring(2, 4));

  var gColor = parseInt("0x" + arg0.substring(4, 6));

  var bColor = parseInt("0x" + arg0.substring(6, 8));

  var arg1 = block.getFieldValue("LEDMODE");
  var arg2 = block.getFieldValue("INTERVAL");

  return (
    "drone.set_arm_LED(" +
    rColor +
    "," +
    gColor +
    "," +
    bColor +
    "," +
    arg1 +
    "," +
    arg2 +
    ")\n"
  );
};

Blockly.Python["setEyeRGB_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg3 = block.getFieldValue("LEDMODE");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "drone.set_eye_LED(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ")\n"
  );
};

Blockly.Python["setArmRGB_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg3 = block.getFieldValue("LEDMODE");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "drone.set_arm_LED(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ")\n"
  );
};

Blockly.Python["setAllLED_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg3 = block.getFieldValue("LEDMODE");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "drone.set_all_LED(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ")\n"
  );
};

Blockly.Python["setArmDefaltLED_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg3 = block.getFieldValue("LEDMODE");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "drone.set_arm_default_LED(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ")\n"
  );
};

Blockly.Python["setArmDefaultColor_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "drone.arm_default_color(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg4 +
    ")\n"
  );
};

Blockly.Python["setEyeDefaultColor_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "drone.eye_default_color(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg4 +
    ")\n"
  );
};

Blockly.Python["setArmPattern_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg3 = block.getFieldValue("LEDMODE");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "drone.arm_pattern(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ")\n"
  );
};

Blockly.Python["setEyePattern_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg3 = block.getFieldValue("LEDMODE");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "drone.eye_pattern(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ")\n"
  );
};

Blockly.Python["setDefaultEyePattern_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg3 = block.getFieldValue("LEDMODE");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "drone.eye_default_pattern(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ")\n"
  );
};

Blockly.Python["setDefaultArmPattern_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg3 = block.getFieldValue("LEDMODE");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "drone.arm_default_pattern(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ")\n"
  );
};

Blockly.Python["setEyeDefaltLED_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg3 = block.getFieldValue("LEDMODE");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "drone.set_eye_default_LED(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ")\n"
  );
};

Blockly.Python["setAllDefaltLED_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg3 = block.getFieldValue("LEDMODE");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "drone.set_all_default_LED(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ")\n"
  );
};

Blockly.Python["resetLED_senior"] = function(block) {
  return "drone.reset_default_LED()\n";
};

Blockly.Python["setLEDto_junior"] = function(block) {
  var arg0 = block.getFieldValue("LEDCOLOR");
  return "setLEDto(" + arg0 + ")\n";
};

Blockly.Python["setAllLED_junior"] = function(block) {
  var arg0 = Blockly.Python.quote_(block.getFieldValue("COLOUR"));

  var rColor = parseInt("0x" + arg0.substring(2, 4));

  var gColor = parseInt("0x" + arg0.substring(4, 6));

  var bColor = parseInt("0x" + arg0.substring(6, 8));

  var arg1 = block.getFieldValue("LEDMODE");
  var arg2 = block.getFieldValue("INTERVAL");

  return (
    "drone.set_all_LED(" +
    rColor +
    "," +
    gColor +
    "," +
    bColor +
    "," +
    arg1 +
    "," +
    arg2 +
    ")\n"
  );
};

Blockly.Python["playsound_junior"] = function(block) {
  var arg0 = block.getFieldValue("SOUND");
  return "playSound(" + arg0 + ")\n";
};

Blockly.Python["playsound_senior"] = function(block) {
  var arg0 = block.getFieldValue("SOUND");
  return "playSound(" + arg0 + ")\n";
};

Blockly.Python["playmysound_junior"] = function(block) {
  var arg0 = block.getFieldValue("SOUND");
  return "playMySound(" + arg0 + ")\n";
};

Blockly.Python["setvolume_junior"] = function(block) {
  var arg0 = block.getFieldValue("VOLUME");
  return "setVolume(" + arg0 + ")\n";
};

Blockly.Python["flySequence_junior"] = function(block) {
  var arg0 = block.getFieldValue("SEQUENCE");
  return "flySequence(" + arg0 + ")\n";
};

Blockly.Python["flyRoulette_junior"] = function(block) {
  return "flyRoulette()\n";
};

Blockly.Python["turtleTurn_junior"] = function(block) {
  return "turtleTurn()\n";
};

Blockly.Python["land_junior"] = function(block) {
  return "drone.land()\n";
};

Blockly.Python["land_senior"] = function(block) {
  return "drone.land()\n";
};

Blockly.Python["emergencyStop_junior"] = function(block) {
  return "drone.emergency_stop()\n";
};

Blockly.Python["emergencyStop_senior"] = function(block) {
  return "drone.emergency_stop()\n";
};

Blockly.Python["go_direction_junior_3"] = function(block) {
  var type = block.getFieldValue("TYPE");
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  var arg1 = parseInt(block.getFieldValue("NUM1"));
  return "drone.go(" + type + "," + arg0 + "," + arg1 + ")\n";
};

Blockly.Python["go_direction_junior"] = function(block) {
  var type = block.getFieldValue("TYPE");
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  return "drone.go(" + type + "," + arg0 + ")\n";
};

Blockly.Python["whenKeyPress_junior"] = function(block) {
  var branch = Blockly.Python.statementToCode(block, "DO");
  branch = Blockly.Python.addLoopTrap(branch, block.id);

  var arg0 = block.getFieldValue("WHENKEYPRESSVAR");
  var branch = Blockly.Python.statementToCode(block, "DO");
  branch = Blockly.Python.addLoopTrap(branch, block.id);
  return (
    "addEvent('whenKeyPress', function (" + arg0 + "){\n" + branch + "})\n"
  );
};

Blockly.Python["rotate_180_junior"] = function(block) {
  return "drone.rotate180()\n";
};

Blockly.Python["onUpsideDown_junior"] = function(block) {
  var branch = Blockly.Python.statementToCode(block, "DO");
  branch = Blockly.Python.addLoopTrap(branch, block.id);

  return "onEvent(UPSIDE_DOWN, function (){\n" + branch + "})\n";
};

Blockly.Python["onUpsideDown_senior"] = function(block) {
  return "onUpsideDown()\n";
};

Blockly.Python["onTakeoff_junior"] = function(block) {
  var branch = Blockly.Python.statementToCode(block, "DO");
  branch = Blockly.Python.addLoopTrap(branch, block.id);

  return "onEvent(TAKEOFF, function (){\n" + branch + "})\n";
};

Blockly.Python["onTakeoff_senior"] = function(block) {
  return "onTakeoff()\n";
};

Blockly.Python["arm_strobe_senior"] = function(block) {
  return "drone.arm_strobe()\n";
};

Blockly.Python["eye_strobe_senior"] = function(block) {
  return "drone.eye_strobe()\n";
};

Blockly.Python["arm_strobe_junior"] = function(block) {
  return "drone.arm_strobe()\n";
};

Blockly.Python["eye_strobe_junior"] = function(block) {
  return "drone.eye_strobe()\n";
};

Blockly.Python["arm_default_strobe_senior"] = function(block) {
  return "drone.arm_default_strobe()\n";
};

Blockly.Python["eye_default_strobe_senior"] = function(block) {
  return "drone.eye_default_strobe()\n";
};

Blockly.Python["eye_off_senior"] = function(block) {
  return "drone.eye_off()\n";
};

Blockly.Python["arm_off_senior"] = function(block) {
  return "drone.arm_off()\n";
};

Blockly.Python["eye_off_junior"] = function(block) {
  return "drone.eye_off()\n";
};

Blockly.Python["arm_off_junior"] = function(block) {
  return "drone.arm_off()\n";
};

Blockly.Python["onCrash_junior"] = function(block) {
  var branch = Blockly.Python.statementToCode(block, "DO");
  branch = Blockly.Python.addLoopTrap(branch, block.id);

  return "onEvent(CRASH, function (){\n" + branch + "})\n";
};

Blockly.Python["onFreeFall_senior"] = function(block) {
  return "onFreeFall()\n";
};

Blockly.Python["onCrash_senior"] = function(block) {
  return "onCrash()\n";
};

Blockly.Python["onLowBattery_junior"] = function(block) {
  var branch = Blockly.Python.statementToCode(block, "DO");
  branch = Blockly.Python.addLoopTrap(branch, block.id);

  return "onEvent(LOW_BATTERY, function (){\n" + branch + "})\n";
};

Blockly.Python["onLowBattery_senior"] = function(block) {
  return "onLowBattery()\n";
};

Blockly.Python["onSideways_senior"] = function(block) {
  return "onSideways()\n";
};

Blockly.Python["onFlying_senior"] = function(block) {
  return "onFlying()\n";
};

Blockly.Python["onLanding_senior"] = function(block) {
  return "onLanding()\n";
};

Blockly.Python["onEmergencyStop_senior"] = function(block) {
  return "onEmergencyStop()\n";
};

Blockly.Python["onIdle_senior"] = function(block) {
  return "onIdle()\n";
};

Blockly.Python["flySquare_junior"] = function(block) {
  return "drone.fly_sequence(Sequence.SQUARE)\n";
};

Blockly.Python["flyCircle_junior"] = function(block) {
  return "drone.fly_sequence(Sequence.CIRCLE)\n";
};

Blockly.Python["flySpiral_junior"] = function(block) {
  return "drone.fly_sequence(Sequence.SPIRAL)\n";
};

Blockly.Python["flyTriangle_junior"] = function(block) {
  return "drone.fly_sequence(Sequence.TRIANGLE)\n";
};

Blockly.Python["var_block"] = function(block) {
  var command = '""';
  var fc = "";

  if (block.childBlocks_[0]) {
    switch (block.childBlocks_[0].type) {
      case "getHeight_junior":
        fc = "GET_HEIGHT";
        break;
      case "getBatteryPercentage_junior":
        fc = "GET_BATTERY_PERCENTAGE";
        break;
      case "getGyroData_junior":
        fc = "GET_GYRO_ANGLES";
        break;
      default:
        fc = "DEFAULT_VALUE";
    }

    command = "Sensors." + fc;
  }

  return "plot_sensor(" + command + ");\n";
};

Blockly.Python["show_var_data"] = function(block) {
  var command = '""';
  var fc = "";

  if (block.childBlocks_[0]) {
    switch (block.childBlocks_[0].type) {
      case "getHeight_junior":
        fc = "GET_HEIGHT";
        break;
      case "getBatteryPercentage_junior":
        fc = "GET_BATTERY_PERCENTAGE";
        break;
      case "getGyroData_junior":
        fc = "GET_GYRO_ANGLES";
        break;
      default:
        fc = "DEFAULT_VALUE";
    }

    command = "Sensors." + fc;
  }

  return "set_workspace_interval(2, " + command + ");\n";
};

Blockly.Python["setArmColor_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "drone.arm_color(" + arg0 + "," + arg1 + "," + arg2 + "," + arg4 + ")\n"
  );
};

Blockly.Python["setArmColor_junior"] = function(block) {
  var arg0 = Blockly.Python.quote_(block.getFieldValue("COLOUR"));

  var rColor = parseInt("0x" + arg0.substring(2, 4));

  var gColor = parseInt("0x" + arg0.substring(4, 6));

  var bColor = parseInt("0x" + arg0.substring(6, 8));

  var arg2 = block.getFieldValue("INTERVAL");

  return (
    "drone.arm_color(" +
    rColor +
    "," +
    gColor +
    "," +
    bColor +
    "," +
    arg2 +
    ")\n"
  );
};

Blockly.Python["setEyeColor_junior"] = function(block) {
  var arg0 = Blockly.Python.quote_(block.getFieldValue("COLOUR"));

  var rColor = parseInt("0x" + arg0.substring(2, 4));

  var gColor = parseInt("0x" + arg0.substring(4, 6));

  var bColor = parseInt("0x" + arg0.substring(6, 8));

  var arg2 = block.getFieldValue("INTERVAL");

  return (
    "drone.eye_color(" +
    rColor +
    "," +
    gColor +
    "," +
    bColor +
    "," +
    arg2 +
    ")\n"
  );
};

Blockly.Python["setArmPattern_junior"] = function(block) {
  var arg0 = Blockly.JavaScript.quote_(block.getFieldValue("COLOUR"));

  var rColor = parseInt("0x" + arg0.substring(2, 4));

  var gColor = parseInt("0x" + arg0.substring(4, 6));

  var bColor = parseInt("0x" + arg0.substring(6, 8));

  var arg1 = block.getFieldValue("LEDMODE");
  var arg2 = block.getFieldValue("INTERVAL");

  return (
    "drone.arm_pattern(" +
    rColor +
    "," +
    gColor +
    "," +
    bColor +
    "," +
    arg1 +
    "," +
    arg2 +
    ")\n"
  );
};

Blockly.Python["setEyePattern_junior"] = function(block) {
  var arg0 = Blockly.JavaScript.quote_(block.getFieldValue("COLOUR"));

  var rColor = parseInt("0x" + arg0.substring(2, 4));

  var gColor = parseInt("0x" + arg0.substring(4, 6));

  var bColor = parseInt("0x" + arg0.substring(6, 8));

  var arg1 = block.getFieldValue("LEDMODE");
  var arg2 = block.getFieldValue("INTERVAL");

  return (
    "drone.eye_pattern(" +
    rColor +
    "," +
    gColor +
    "," +
    bColor +
    "," +
    arg1 +
    "," +
    arg2 +
    ")\n"
  );
};

Blockly.Python["setEyeColor_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "drone.eye_color(" + arg0 + "," + arg1 + "," + arg2 + "," + arg4 + ")\n"
  );
};

Blockly.Python["flyHop_junior"] = function(block) {
  return "drone.fly_sequence(Sequence.HOP)\n";
};

Blockly.Python["flysway_junior"] = function(block) {
  return "drone.fly_sequence(Sequence.SWAY)\n";
};

Blockly.Python["flyZigzag_junior"] = function(block) {
  return "drone.fly_sequence(Sequence.ZIGZAG)\n";
};
