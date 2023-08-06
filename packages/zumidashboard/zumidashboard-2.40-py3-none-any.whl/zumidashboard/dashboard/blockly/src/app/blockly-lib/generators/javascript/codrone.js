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

goog.provide("Blockly.JavaScript.codrone");

goog.require("Blockly.JavaScript");

Blockly.JavaScript["take_off"] = function(block) {
  return "Code.device.getPrimaryService('c320df00-7891-11e5-8bcf-feff819cdc9f')\n.then(service => service.getCharacteristic('c320df02-7891-11e5-8bcf-feff819cdc9f'))\n.then(characteristic => {\n var uint8 = new Uint8Array(3);\n uint8[0] = 17;\n uint8[1] = 34;\n uint8[2] = 1;\n return characteristic.writeValue(uint8);\n})";
};

Blockly.JavaScript["take_off_junior"] = function(block) {
  return "await takeoff();\n";
};

Blockly.JavaScript["take_off_senior"] = function(block) {
  return "await takeoff();\n";
};

Blockly.JavaScript["go"] = function(block) {
  return "go();\n";
};

Blockly.JavaScript["go_5"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  var arg1 = parseInt(block.getFieldValue("NUM1"));
  var arg2 = parseInt(block.getFieldValue("NUM2"));
  var arg3 = parseInt(block.getFieldValue("NUM3"));
  var arg4 = parseInt(block.getFieldValue("NUM4"));
  return (
    "go(" + arg0 + "," + arg1 + "," + arg2 + "," + arg3 + "," + arg4 + ");\n"
  );
};

Blockly.JavaScript["flyforward"] = function(block) {
  return "flyForward();\n";
};

Blockly.JavaScript["flyright_2"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  var arg1 = parseInt(block.getFieldValue("NUM1"));
  return "flyRight(" + arg0 + "," + arg1 + ");\n";
};

Blockly.JavaScript["var_block"] = function(block) {
  var blockIndex = -1;

  if (window.blocksSaved) {
    var idBlock = window.blocksSaved.findIndex(function(blk) {
      return blk.id == block.id;
    });

    if (idBlock >= 0) {
      window.idBlock = idBlock;
    } else {
      window.blocksSaved.push(block);
      window.idBlock = window.blocksSaved.length - 1;
    }
  } else {
    window.blocksSaved = [block];
    window.idBlock = window.blocksSaved.length - 1;
  }

  if (block.childBlocks_.length > 0) {
    blockIndex = block.childBlocks_.findIndex(function(item) {
      return (
        item.type == "getHeight_junior" ||
        item.type == "getBatteryPercentage_junior" ||
        item.type == "getGyroData_junior"
      );
    });
  }

  if (blockIndex >= 0) {
    var index = window.idBlock;
    var value = "";
    var fc = "";

    switch (block.childBlocks_[blockIndex].type) {
      case "getHeight_junior":
        value = "Height: ";
        fc = "GET_HEIGHT";
        break;
      case "getBatteryPercentage_junior":
        value = "Battery Percentage: ";
        fc = "GET_BATTERY_PERCENTAGE";
        break;
      case "getGyroData_junior":
        value = "Gyro Data: ";
        fc = "GET_GYRO_ANGLES";
        break;
      default:
        value = "Value: ";
    }
    if (!window.dirtyVar || window.dirtyVar != block.childBlocks_[0].type) {
      window.dirtyVar = block.childBlocks_[0].type;
      block.setFieldValue(
        value + window.displaySingleValue[window.Sensors[fc].value]
      );
    }

    block.value = value;
    window.blockSave = block;
  } else {
    window.dirtyVar = false;
    block.setFieldValue("Value: ");
  }

  var command = "";
  if (fc) {
    window.Sensors[fc].index = index;
    command = "Sensors." + fc;
  } else {
    command = '""';
  }
  return "await plotSensor(" + command + ");\n";
};

Blockly.JavaScript["show_var_data"] = function(block) {
  var commandDisplay = null;
  if (window.blocksSaved) {
    var idBlock = window.blocksSaved.findIndex(function(blk) {
      return blk.id == block.id;
    });

    if (idBlock >= 0) {
      window.idBlock = idBlock;
    } else {
      window.blocksSaved.push(block);
      window.idBlock = window.blocksSaved.length - 1;
    }
  } else {
    window.blocksSaved = [block];
    window.idBlock = window.blocksSaved.length - 1;
  }

  if (block.childBlocks_[0]) {
    if (window.blocksSaved[window.idBlock].blockInterval) {
      console.log("block disengage");
    }
    var index = window.idBlock;
    window.DISPLAY_INTERVAL = true;
    console.log("interval");
    var value = "";
    var fc = "";

    switch (block.childBlocks_[0].type) {
      case "getHeight_junior":
        value = "Height: ";
        fc = Sensors.GET_HEIGHT;
        window.blocksSaved[index].methodName = fc;
        break;
      case "getBatteryPercentage_junior":
        value = "Battery Percentage: ";
        fc = Sensors.GET_BATTERY_PERCENTAGE;
        window.blocksSaved[index].methodName = fc;
        break;
      case "getGyroData_junior":
        value = "Gyro Data: ";
        fc = Sensors.GET_GYRO_ANGLES;
        window.blocksSaved[index].methodName = fc;
        break;
      default:
        value = "Value: ";
        fc = "getData";
    }
    if (!window.dirtyVar || window.dirtyVar != block.childBlocks_[0].type) {
      window.dirtyVar = block.childBlocks_[0].type;
      block.setFieldValue(value);
    }

    block.value = value;
    window.blocksSaved[index].blockSave = block;

    fc.index = index;
    fc.labelDescription = value;
    block.setFieldValue(value + global.displayValue[fc.value]);
  } else {
    clearInterval(window.blocksSaved[window.idBlock].blockInterval);
    block.setFieldValue("Value: ");
  }

  var commmandType =
    window.blocksSaved[index] && window.blocksSaved[index].methodName
      ? window.blocksSaved[index].methodName.displayName
      : '""';

  if (commmandType.value) {
    commmandType.index = index;
    console.log(index);
  }

  return "setWorkspaceInterval(2," + commmandType + ");\n";
};

Blockly.JavaScript["go_direction_junior_3"] = function(block) {
  var type = block.getFieldValue("TYPE");
  var arg0 = parseFloat(block.getFieldValue("NUM0"));
  var arg1 = parseInt(block.getFieldValue("NUM1"));
  return "await go(" + type + "," + arg0 + "," + arg1 + ");\n";
};

Blockly.JavaScript["go_direction_junior"] = function(block) {
  var type = block.getFieldValue("TYPE");
  var arg0 = parseFloat(block.getFieldValue("NUM0"));
  return "await go(" + type + "," + arg0 + ");\n";
};

Blockly.JavaScript["turn_junior_3"] = function(block) {
  var type = block.getFieldValue("TYPE");
  var arg0 = parseFloat(block.getFieldValue("NUM0"));
  var arg1 = parseInt(block.getFieldValue("NUM1"));
  return "await turn(" + type + "," + arg0 + "," + arg1 + ");\n";
};

Blockly.JavaScript["turn_senior"] = function(block) {
  var type = block.getFieldValue("TYPE");
  var arg0 = parseFloat(block.getFieldValue("NUM0"));
  var arg1 = parseInt(block.getFieldValue("NUM1"));
  return "await turn(" + type + "," + arg0 + "," + arg1 + ");\n";
};

Blockly.JavaScript["turn_degree_junior_2"] = function(block) {
  var direction = block.getFieldValue("DIRECTION");
  var arg0 = block.getFieldValue("DIRECTIONDEGREE");
  return "await turnDegree(" + direction + ", " + arg0 + ");\n";
};

Blockly.JavaScript["turn_degree_senior"] = function(block) {
  var direction = block.getFieldValue("DIRECTION");
  var arg0 = block.getFieldValue("DIRECTIONDEGREE");
  return "await turnDegree(" + direction + ", " + arg0 + ");\n";
};

Blockly.JavaScript["turn_90_junior"] = function(block) {
  var direction = block.getFieldValue("DIRECTION");
  return "turn90(" + direction + ");\n";
};

Blockly.JavaScript["rotate_180_junior"] = function(block) {
  return "await rotate180();\n";
};

Blockly.JavaScript["rotate_360_junior"] = function(block) {
  return "rotate360();\n";
};

Blockly.JavaScript["rotate_junior"] = function(block) {
  var degree = block.getFieldValue("DEGREE");
  return "rotate(" + degree + ");\n";
};

Blockly.JavaScript["getHeight_junior"] = function(block) {
  return ["await getHeight()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["isReadyToFly_junior"] = function(block) {
  return ["isReadyToFly()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["isUpsideDown_junior"] = function(block) {
  return ["isUpsideDown()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["isFlying_junior"] = function(block) {
  return ["isFlying()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["isReadyToFly_senior"] = function(block) {
  return ["isReadyToFly()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["isUpsideDown_senior"] = function(block) {
  return ["isUpsideDown()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["isFlying_senior"] = function(block) {
  return ["isFlying()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

// Gets
Blockly.JavaScript["getHeight_senior"] = function(block) {
  return ["await getHeight()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["getPressure_senior"] = function(block) {
  return ["await getPressure()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["getOpticalFlow_senior"] = function(block) {
  return ["await getOptFlowPosition()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["getState_senior"] = function(block) {
  return ["await getState()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["getBarometer_senior"] = function(block) {
  return ["getBarometer()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["getTemperature_senior"] = function(block) {
  return ["await getDroneTemp()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["getAngles_senior"] = function(block) {
  return ["await getGyroAngles()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["getAngularSpeed_senior"] = function(block) {
  return ["await getAngularSpeed()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["getAccelerometer_senior"] = function(block) {
  return ["await getAccelerometer()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["getBatteryPercentage_junior"] = function(block) {
  return [
    "await getBatteryPercentage()",
    Blockly.JavaScript.ORDER_FUNCTION_CALL
  ];
};

Blockly.JavaScript["getBatteryPercentage_senior"] = function(block) {
  return [
    "await getBatteryPercentage()",
    Blockly.JavaScript.ORDER_FUNCTION_CALL
  ];
};

Blockly.JavaScript["getGyroData_junior"] = function(block) {
  return ["await getGyroAngles()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["getBatteryVoltage_senior"] = function(block) {
  return ["await getBatteryVoltage()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["getTrim_senior"] = function(block) {
  return ["await getTrim()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};
// End Gets

Blockly.JavaScript["gotoheight_junior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("HEIGHT"));
  return "await goToHeight(" + arg0 + ");\n";
};

Blockly.JavaScript["gotoheight_senior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM1"));
  return "await goToHeight(" + arg0 + ");\n";
};

Blockly.JavaScript["setEyeRGB_junior"] = function(block) {
  var arg0 = Blockly.JavaScript.quote_(block.getFieldValue("COLOUR"));

  var rColor = parseInt("0x" + arg0.substring(2, 4));

  var gColor = parseInt("0x" + arg0.substring(4, 6));

  var bColor = parseInt("0x" + arg0.substring(6, 8));

  var arg1 = block.getFieldValue("LEDMODE");
  var arg2 = block.getFieldValue("INTERVAL");

  return (
    "await setEyeLED(" +
    rColor +
    "," +
    gColor +
    "," +
    bColor +
    "," +
    arg1 +
    "," +
    arg2 +
    ");\n"
  );
};

Blockly.JavaScript["setArmRGB_junior"] = function(block) {
  var arg0 = Blockly.JavaScript.quote_(block.getFieldValue("COLOUR"));

  var rColor = parseInt("0x" + arg0.substring(2, 4));

  var gColor = parseInt("0x" + arg0.substring(4, 6));

  var bColor = parseInt("0x" + arg0.substring(6, 8));

  var arg1 = block.getFieldValue("LEDMODE");
  var arg2 = block.getFieldValue("INTERVAL");

  return (
    "await setArmLED(" +
    rColor +
    "," +
    gColor +
    "," +
    bColor +
    "," +
    arg1 +
    "," +
    arg2 +
    ");\n"
  );
};

Blockly.JavaScript["setEyeRGB_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg3 = block.getFieldValue("LEDMODE");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "await setEyeLED(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ");\n"
  );
};

Blockly.JavaScript["setArmColor_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "await armColor(" + arg0 + "," + arg1 + "," + arg2 + "," + arg4 + ");\n"
  );
};

Blockly.JavaScript["setArmColor_junior"] = function(block) {
  var arg0 = Blockly.Python.quote_(block.getFieldValue("COLOUR"));

  var rColor = parseInt("0x" + arg0.substring(2, 4));

  var gColor = parseInt("0x" + arg0.substring(4, 6));

  var bColor = parseInt("0x" + arg0.substring(6, 8));

  var arg2 = block.getFieldValue("INTERVAL");

  return (
    "await armColor(" +
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

Blockly.JavaScript["setEyeColor_junior"] = function(block) {
  var arg0 = Blockly.Python.quote_(block.getFieldValue("COLOUR"));

  var rColor = parseInt("0x" + arg0.substring(2, 4));

  var gColor = parseInt("0x" + arg0.substring(4, 6));

  var bColor = parseInt("0x" + arg0.substring(6, 8));

  var arg2 = block.getFieldValue("INTERVAL");

  return (
    "await eyeColor(" +
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

Blockly.JavaScript["setEyeColor_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "await eyeColor(" + arg0 + "," + arg1 + "," + arg2 + "," + arg4 + ");\n"
  );
};

Blockly.JavaScript["setArmRGB_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg3 = block.getFieldValue("LEDMODE");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "await setArmLED(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ");\n"
  );
};

Blockly.JavaScript["setAllLED_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg3 = block.getFieldValue("LEDMODE");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "await setAllLED(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ");\n"
  );
};

Blockly.JavaScript["setArmDefaltLED_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg3 = block.getFieldValue("LEDMODE");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "await setArmDefaultLED(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ");\n"
  );
};

Blockly.JavaScript["setArmDefaultColor_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "await armDefaultColor(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg4 +
    ");\n"
  );
};

Blockly.JavaScript["setEyeDefaultColor_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "await eyeDefaultColor(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg4 +
    ");\n"
  );
};

Blockly.JavaScript["setArmPattern_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg3 = block.getFieldValue("LEDMODE");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "await armPattern(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ");\n"
  );
};

Blockly.JavaScript["setEyePattern_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg3 = block.getFieldValue("LEDMODE");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "await eyePattern(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ");\n"
  );
};

Blockly.JavaScript["setDefaultEyePattern_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg3 = block.getFieldValue("LEDMODE");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "await eyeDefaultPattern(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ");\n"
  );
};

Blockly.JavaScript["setDefaultArmPattern_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg3 = block.getFieldValue("LEDMODE");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "await armDefaultPattern(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ");\n"
  );
};

Blockly.JavaScript["setEyeDefaltLED_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg3 = block.getFieldValue("LEDMODE");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "await setEyeDefaultLED(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ");\n"
  );
};

Blockly.JavaScript["setAllDefaltLED_senior"] = function(block) {
  var arg0 = block.getFieldValue("red");
  var arg1 = block.getFieldValue("green");
  var arg2 = block.getFieldValue("blue");
  var arg3 = block.getFieldValue("LEDMODE");
  var arg4 = block.getFieldValue("INTERVAL");
  return (
    "await setAllDefaultLED(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ");\n"
  );
};

Blockly.JavaScript["resetLED_senior"] = function(block) {
  return "await resetDefaultLED();\n";
};

Blockly.JavaScript["setEyeRGB_junior"] = function(block) {
  var arg0 = Blockly.JavaScript.quote_(block.getFieldValue("COLOUR"));

  var rColor = parseInt("0x" + arg0.substring(2, 4));

  var gColor = parseInt("0x" + arg0.substring(4, 6));

  var bColor = parseInt("0x" + arg0.substring(6, 8));

  var arg1 = block.getFieldValue("LEDMODE");
  var arg2 = block.getFieldValue("INTERVAL");

  return (
    "await setEyeLED(" +
    rColor +
    "," +
    gColor +
    "," +
    bColor +
    "," +
    arg1 +
    "," +
    arg2 +
    ");\n"
  );
};

Blockly.JavaScript["setArmPattern_junior"] = function(block) {
  var arg0 = Blockly.JavaScript.quote_(block.getFieldValue("COLOUR"));

  var rColor = parseInt("0x" + arg0.substring(2, 4));

  var gColor = parseInt("0x" + arg0.substring(4, 6));

  var bColor = parseInt("0x" + arg0.substring(6, 8));

  var arg1 = block.getFieldValue("LEDMODE");
  var arg2 = block.getFieldValue("INTERVAL");

  return (
    "await armPattern(" +
    rColor +
    "," +
    gColor +
    "," +
    bColor +
    "," +
    arg1 +
    "," +
    arg2 +
    ");\n"
  );
};

Blockly.JavaScript["setEyePattern_junior"] = function(block) {
  var arg0 = Blockly.JavaScript.quote_(block.getFieldValue("COLOUR"));

  var rColor = parseInt("0x" + arg0.substring(2, 4));

  var gColor = parseInt("0x" + arg0.substring(4, 6));

  var bColor = parseInt("0x" + arg0.substring(6, 8));

  var arg1 = block.getFieldValue("LEDMODE");
  var arg2 = block.getFieldValue("INTERVAL");

  return (
    "await eyePattern(" +
    rColor +
    "," +
    gColor +
    "," +
    bColor +
    "," +
    arg1 +
    "," +
    arg2 +
    ");\n"
  );
};

Blockly.JavaScript["setAllLED_junior"] = function(block) {
  var arg0 = Blockly.JavaScript.quote_(block.getFieldValue("COLOUR"));

  var rColor = parseInt("0x" + arg0.substring(2, 4));

  var gColor = parseInt("0x" + arg0.substring(4, 6));

  var bColor = parseInt("0x" + arg0.substring(6, 8));

  var arg1 = block.getFieldValue("LEDMODE");
  var arg2 = block.getFieldValue("INTERVAL");

  return (
    "await setAllLED(" +
    rColor +
    "," +
    gColor +
    "," +
    bColor +
    "," +
    arg1 +
    "," +
    arg2 +
    ");\n"
  );
};

Blockly.JavaScript["setAllRGB_senior"] = function(block) {
  var arg0 = Blockly.JavaScript.quote_(block.getFieldValue("COLOUR"));

  var rColor = parseInt("0x" + arg0.substring(2, 4));

  var gColor = parseInt("0x" + arg0.substring(4, 6));

  var bColor = parseInt("0x" + arg0.substring(6, 8));

  return "await setAllRGB(" + rColor + "," + gColor + "," + bColor + ");\n";
};

Blockly.JavaScript["playsound_junior"] = function(block) {
  var arg0 = block.getFieldValue("SOUND");
  return "playSound(" + arg0 + ");\n";
};

Blockly.JavaScript["playsound_senior"] = function(block) {
  var arg0 = block.getFieldValue("SOUND");
  return "playSound(" + arg0 + ");\n";
};

Blockly.JavaScript["playmysound_junior"] = function(block) {
  var arg0 = block.getFieldValue("SOUND");
  return "playMySound(" + arg0 + ");\n";
};

Blockly.JavaScript["setvolume_junior"] = function(block) {
  var arg0 = block.getFieldValue("VOLUME");
  return "setVolume(" + arg0 + ");\n";
};

Blockly.JavaScript["flySequence_junior"] = function(block) {
  var arg0 = block.getFieldValue("SEQUENCE");
  return "flySequence(" + arg0 + ");\n";
};

Blockly.JavaScript["flyRoulette_junior"] = function(block) {
  return "flyRoulette();\n";
};

Blockly.JavaScript["turtleTurn_junior"] = function(block) {
  return "turtleTurn();\n";
};

Blockly.JavaScript["land_junior"] = function(block) {
  return "await land();\n";
};

Blockly.JavaScript["land_senior"] = function(block) {
  return "await land();\n";
};

Blockly.JavaScript["send_command"] = function(block) {
  var branch = Blockly.JavaScript.statementToCode(block, "DO");
  branch = Blockly.JavaScript.addLoopTrap(branch, block.id);
  return "function whenKeyPress()\n{\n" + branch + "\n}\n";
};

Blockly.JavaScript["whenKeyPress_junior"] = function(block) {
  var arg0 = block.getFieldValue("WHENKEYPRESSVAR");
  if (isNaN(arg0)) {
    arg0 = arg0.toString();
  }
  var branch = Blockly.JavaScript.statementToCode(block, "DO");
  branch = Blockly.JavaScript.addLoopTrap(branch, block.id);

  return (
    "onKeyPressEvent(" +
    arg0.toString() +
    ", async function (){\n" +
    branch +
    "})\n"
  );
};

Blockly.JavaScript["variables_get_roll"] = function(block) {
  // Variable getter.
  var code = Blockly.JavaScript.variableDB_.getName(
    block.getFieldValue("VAR"),
    Blockly.Variables.NAME_TYPE
  );
  return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript["variables_set_roll"] = function(block) {
  // Variable setter.
  var argument0 =
    Blockly.JavaScript.valueToCode(
      block,
      "VALUE",
      Blockly.JavaScript.ORDER_ASSIGNMENT
    ) || "0";
  var varName = Blockly.JavaScript.variableDB_.getName(
    block.getFieldValue("VAR"),
    Blockly.Variables.NAME_TYPE
  );
  return varName + " = " + argument0 + ";\n";
};

Blockly.JavaScript["variables_get_yaw"] = function(block) {
  // Variable getter.
  var code = Blockly.JavaScript.variableDB_.getName(
    block.getFieldValue("VAR"),
    Blockly.Variables.NAME_TYPE
  );
  return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript["variables_set_yaw"] = function(block) {
  // Variable setter.
  var argument0 =
    Blockly.JavaScript.valueToCode(
      block,
      "VALUE",
      Blockly.JavaScript.ORDER_ASSIGNMENT
    ) || "0";
  var varName = Blockly.JavaScript.variableDB_.getName(
    block.getFieldValue("VAR"),
    Blockly.Variables.NAME_TYPE
  );
  return varName + " = " + argument0 + ";\n";
};

Blockly.JavaScript["variables_get_pitch"] = function(block) {
  // Variable getter.
  var code = Blockly.JavaScript.variableDB_.getName(
    block.getFieldValue("VAR"),
    Blockly.Variables.NAME_TYPE
  );
  return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript["variables_set_pitch"] = function(block) {
  // Variable setter.
  var argument0 =
    Blockly.JavaScript.valueToCode(
      block,
      "VALUE",
      Blockly.JavaScript.ORDER_ASSIGNMENT
    ) || "0";
  var varName = Blockly.JavaScript.variableDB_.getName(
    block.getFieldValue("VAR"),
    Blockly.Variables.NAME_TYPE
  );
  return varName + " = " + argument0 + ";\n";
};

Blockly.JavaScript["variables_get_throttle"] = function(block) {
  // Variable getter.
  var code = Blockly.JavaScript.variableDB_.getName(
    block.getFieldValue("VAR"),
    Blockly.Variables.NAME_TYPE
  );
  return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript["variables_set_throttle"] = function(block) {
  // Variable setter.
  var argument0 =
    Blockly.JavaScript.valueToCode(
      block,
      "VALUE",
      Blockly.JavaScript.ORDER_ASSIGNMENT
    ) || "0";
  var varName = Blockly.JavaScript.variableDB_.getName(
    block.getFieldValue("VAR"),
    Blockly.Variables.NAME_TYPE
  );
  return varName + " = " + argument0 + ";\n";
};

Blockly.JavaScript["text"] = function(block) {
  // Text value.
  var code = Blockly.JavaScript.quote_(block.getFieldValue("TEXT"));
  return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript["text_join"] = function(block) {
  // Create a string made up of any number of elements of any type.
  switch (block.itemCount_) {
    case 0:
      return ["''", Blockly.JavaScript.ORDER_ATOMIC];
    case 1:
      var element =
        Blockly.JavaScript.valueToCode(
          block,
          "ADD0",
          Blockly.JavaScript.ORDER_NONE
        ) || "''";
      var code = "String(" + element + ")";
      return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];
    case 2:
      var element0 =
        Blockly.JavaScript.valueToCode(
          block,
          "ADD0",
          Blockly.JavaScript.ORDER_NONE
        ) || "''";
      var element1 =
        Blockly.JavaScript.valueToCode(
          block,
          "ADD1",
          Blockly.JavaScript.ORDER_NONE
        ) || "''";
      var code = "String(" + element0 + ") + String(" + element1 + ")";
      return [code, Blockly.JavaScript.ORDER_ADDITION];
    default:
      var elements = new Array(block.itemCount_);
      for (var i = 0; i < block.itemCount_; i++) {
        elements[i] =
          Blockly.JavaScript.valueToCode(
            block,
            "ADD" + i,
            Blockly.JavaScript.ORDER_COMMA
          ) || "''";
      }
      var code = "[" + elements.join(",") + "].join('')";
      return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];
  }
};

Blockly.JavaScript["text_append"] = function(block) {
  // Append to a variable in place.
  var varName = Blockly.JavaScript.variableDB_.getName(
    block.getFieldValue("VAR"),
    Blockly.Variables.NAME_TYPE
  );
  var value =
    Blockly.JavaScript.valueToCode(
      block,
      "TEXT",
      Blockly.JavaScript.ORDER_NONE
    ) || "''";
  return varName + " = String(" + varName + ") + String(" + value + ");\n";
};

Blockly.JavaScript["text_length"] = function(block) {
  // String or array length.
  var text =
    Blockly.JavaScript.valueToCode(
      block,
      "VALUE",
      Blockly.JavaScript.ORDER_FUNCTION_CALL
    ) || "''";
  return [text + ".length", Blockly.JavaScript.ORDER_MEMBER];
};

Blockly.JavaScript["text_isEmpty"] = function(block) {
  // Is the string null or array empty?
  var text =
    Blockly.JavaScript.valueToCode(
      block,
      "VALUE",
      Blockly.JavaScript.ORDER_MEMBER
    ) || "''";
  return ["!" + text + ".length", Blockly.JavaScript.ORDER_LOGICAL_NOT];
};

Blockly.JavaScript["text_indexOf"] = function(block) {
  // Search the text for a substring.
  var operator =
    block.getFieldValue("END") == "FIRST" ? "indexOf" : "lastIndexOf";
  var substring =
    Blockly.JavaScript.valueToCode(
      block,
      "FIND",
      Blockly.JavaScript.ORDER_NONE
    ) || "''";
  var text =
    Blockly.JavaScript.valueToCode(
      block,
      "VALUE",
      Blockly.JavaScript.ORDER_MEMBER
    ) || "''";
  var code = text + "." + operator + "(" + substring + ")";
  // Adjust index if using one-based indices.
  if (block.workspace.options.oneBasedIndex) {
    return [code + " + 1", Blockly.JavaScript.ORDER_ADDITION];
  }
  return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["text_charAt"] = function(block) {
  // Get letter at index.
  // Note: Until January 2013 this block did not have the WHERE input.
  var where = block.getFieldValue("WHERE") || "FROM_START";
  var textOrder =
    where == "RANDOM"
      ? Blockly.JavaScript.ORDER_NONE
      : Blockly.JavaScript.ORDER_MEMBER;
  var text = Blockly.JavaScript.valueToCode(block, "VALUE", textOrder) || "''";
  switch (where) {
    case "FIRST":
      var code = text + ".charAt(0)";
      return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];
    case "LAST":
      var code = text + ".slice(-1)";
      return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];
    case "FROM_START":
      var at = Blockly.JavaScript.getAdjusted(block, "AT");
      // Adjust index if using one-based indices.
      var code = text + ".charAt(" + at + ")";
      return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];
    case "FROM_END":
      var at = Blockly.JavaScript.getAdjusted(block, "AT", 1, true);
      var code = text + ".slice(" + at + ").charAt(0)";
      return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];
    case "RANDOM":
      var functionName = Blockly.JavaScript.provideFunction_(
        "textRandomLetter",
        [
          "function " +
            Blockly.JavaScript.FUNCTION_NAME_PLACEHOLDER_ +
            "(text) {",
          "  var x = Math.floor(Math.random() * text.length);",
          "  return text[x];",
          "}"
        ]
      );
      var code = functionName + "(" + text + ")";
      return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];
  }
  throw "Unhandled option (text_charAt).";
};

/**
 * Returns an expression calculating the index into a string.
 * @private
 * @param {string} stringName Name of the string, used to calculate length.
 * @param {string} where The method of indexing, selected by dropdown in Blockly
 * @param {string=} opt_at The optional offset when indexing from start/end.
 * @return {string} Index expression.
 */
Blockly.JavaScript.text.getIndex_ = function(stringName, where, opt_at) {
  if (where == "FIRST") {
    return "0";
  } else if (where == "FROM_END") {
    return stringName + ".length - 1 - " + opt_at;
  } else if (where == "LAST") {
    return stringName + ".length - 1";
  } else {
    return opt_at;
  }
};

Blockly.JavaScript["text_getSubstring"] = function(block) {
  // Get substring.
  var text =
    Blockly.JavaScript.valueToCode(
      block,
      "STRING",
      Blockly.JavaScript.ORDER_FUNCTION_CALL
    ) || "''";
  var where1 = block.getFieldValue("WHERE1");
  var where2 = block.getFieldValue("WHERE2");
  if (where1 == "FIRST" && where2 == "LAST") {
    var code = text;
  } else if (
    text.match(/^'?\w+'?$/) ||
    (where1 != "FROM_END" &&
      where1 != "LAST" &&
      where2 != "FROM_END" &&
      where2 != "LAST")
  ) {
    // If the text is a variable or literal or doesn't require a call for
    // length, don't generate a helper function.
    switch (where1) {
      case "FROM_START":
        var at1 = Blockly.JavaScript.getAdjusted(block, "AT1");
        break;
      case "FROM_END":
        var at1 = Blockly.JavaScript.getAdjusted(
          block,
          "AT1",
          1,
          false,
          Blockly.JavaScript.ORDER_SUBTRACTION
        );
        at1 = text + ".length - " + at1;
        break;
      case "FIRST":
        var at1 = "0";
        break;
      default:
        throw "Unhandled option (text_getSubstring).";
    }
    switch (where2) {
      case "FROM_START":
        var at2 = Blockly.JavaScript.getAdjusted(block, "AT2", 1);
        break;
      case "FROM_END":
        var at2 = Blockly.JavaScript.getAdjusted(
          block,
          "AT2",
          0,
          false,
          Blockly.JavaScript.ORDER_SUBTRACTION
        );
        at2 = text + ".length - " + at2;
        break;
      case "LAST":
        var at2 = text + ".length";
        break;
      default:
        throw "Unhandled option (text_getSubstring).";
    }
    code = text + ".slice(" + at1 + ", " + at2 + ")";
  } else {
    var at1 = Blockly.JavaScript.getAdjusted(block, "AT1");
    var at2 = Blockly.JavaScript.getAdjusted(block, "AT2");
    var getIndex_ = Blockly.JavaScript.text.getIndex_;
    var wherePascalCase = {
      FIRST: "First",
      LAST: "Last",
      FROM_START: "FromStart",
      FROM_END: "FromEnd"
    };
    var functionName = Blockly.JavaScript.provideFunction_(
      "subsequence" + wherePascalCase[where1] + wherePascalCase[where2],
      [
        "function " +
          Blockly.JavaScript.FUNCTION_NAME_PLACEHOLDER_ +
          "(sequence" +
          // The value for 'FROM_END' and'FROM_START' depends on `at` so
          // we add it as a parameter.
          (where1 == "FROM_END" || where1 == "FROM_START" ? ", at1" : "") +
          (where2 == "FROM_END" || where2 == "FROM_START" ? ", at2" : "") +
          ") {",
        "  var start = " + getIndex_("sequence", where1, "at1") + ";",
        "  var end = " + getIndex_("sequence", where2, "at2") + " + 1;",
        "  return sequence.slice(start, end);",
        "}"
      ]
    );
    var code =
      functionName +
      "(" +
      text +
      // The value for 'FROM_END' and 'FROM_START' depends on `at` so we
      // pass it.
      (where1 == "FROM_END" || where1 == "FROM_START" ? ", " + at1 : "") +
      (where2 == "FROM_END" || where2 == "FROM_START" ? ", " + at2 : "") +
      ")";
  }
  return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["text_changeCase"] = function(block) {
  // Change capitalization.
  var OPERATORS = {
    UPPERCASE: ".toUpperCase()",
    LOWERCASE: ".toLowerCase()",
    TITLECASE: null
  };
  var operator = OPERATORS[block.getFieldValue("CASE")];
  var textOrder = operator
    ? Blockly.JavaScript.ORDER_MEMBER
    : Blockly.JavaScript.ORDER_NONE;
  var text = Blockly.JavaScript.valueToCode(block, "TEXT", textOrder) || "''";
  if (operator) {
    // Upper and lower case are functions built into JavaScript.
    var code = text + operator;
  } else {
    // Title case is not a native JavaScript function.  Define one.
    var functionName = Blockly.JavaScript.provideFunction_("textToTitleCase", [
      "function " + Blockly.JavaScript.FUNCTION_NAME_PLACEHOLDER_ + "(str) {",
      "  return str.replace(/\\S+/g,",
      "      function(txt) {return txt[0].toUpperCase() + " +
        "txt.substring(1).toLowerCase();});",
      "}"
    ]);
    var code = functionName + "(" + text + ")";
  }
  return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["text_trim"] = function(block) {
  // Trim spaces.
  var OPERATORS = {
    LEFT: ".replace(/^[\\s\\xa0]+/, '')",
    RIGHT: ".replace(/[\\s\\xa0]+$/, '')",
    BOTH: ".trim()"
  };
  var operator = OPERATORS[block.getFieldValue("MODE")];
  var text =
    Blockly.JavaScript.valueToCode(
      block,
      "TEXT",
      Blockly.JavaScript.ORDER_MEMBER
    ) || "''";
  return [text + operator, Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["text_print"] = function(block) {
  // Print statement.
  var msg =
    Blockly.JavaScript.valueToCode(
      block,
      "TEXT",
      Blockly.JavaScript.ORDER_NONE
    ) || "''";
  return "window.alert(" + msg + ");\n";
};

Blockly.JavaScript["console_log"] = function(block) {
  // Print statement.
  var msg =
    Blockly.JavaScript.valueToCode(
      block,
      "TEXT",
      Blockly.JavaScript.ORDER_NONE
    ) || "''";
  return "console.log(" + msg + ");\n";
};

Blockly.JavaScript["text_prompt_ext"] = function(block) {
  // Prompt function.
  if (block.getField("TEXT")) {
    // Internal message.
    var msg = Blockly.JavaScript.quote_(block.getFieldValue("TEXT"));
  } else {
    // External message.
    var msg =
      Blockly.JavaScript.valueToCode(
        block,
        "TEXT",
        Blockly.JavaScript.ORDER_NONE
      ) || "''";
  }
  var code = "window.prompt(" + msg + ")";
  var toNumber = block.getFieldValue("TYPE") == "NUMBER";
  if (toNumber) {
    code = "parseFloat(" + code + ")";
  }
  return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["text_prompt"] = Blockly.JavaScript["text_prompt_ext"];

Blockly.JavaScript["text_count"] = function(block) {
  var text =
    Blockly.JavaScript.valueToCode(
      block,
      "TEXT",
      Blockly.JavaScript.ORDER_MEMBER
    ) || "''";
  var sub =
    Blockly.JavaScript.valueToCode(
      block,
      "SUB",
      Blockly.JavaScript.ORDER_NONE
    ) || "''";
  var functionName = Blockly.JavaScript.provideFunction_("textCount", [
    "function " +
      Blockly.JavaScript.FUNCTION_NAME_PLACEHOLDER_ +
      "(haystack, needle) {",
    "  if (needle.length === 0) {",
    "    return haystack.length + 1;",
    "  } else {",
    "    return haystack.split(needle).length - 1;",
    "  }",
    "}"
  ]);
  var code = functionName + "(" + text + ", " + sub + ")";
  return [code, Blockly.JavaScript.ORDER_SUBTRACTION];
};

Blockly.JavaScript["text_replace"] = function(block) {
  var text =
    Blockly.JavaScript.valueToCode(
      block,
      "TEXT",
      Blockly.JavaScript.ORDER_MEMBER
    ) || "''";
  var from =
    Blockly.JavaScript.valueToCode(
      block,
      "FROM",
      Blockly.JavaScript.ORDER_NONE
    ) || "''";
  var to =
    Blockly.JavaScript.valueToCode(
      block,
      "TO",
      Blockly.JavaScript.ORDER_NONE
    ) || "''";
  // The regex escaping code below is taken from the implementation of
  // goog.string.regExpEscape.
  var functionName = Blockly.JavaScript.provideFunction_("textReplace", [
    "function " +
      Blockly.JavaScript.FUNCTION_NAME_PLACEHOLDER_ +
      "(haystack, needle, replacement) {",
    "  needle = " +
      'needle.replace(/([-()\\[\\]{}+?*.$\\^|,:#<!\\\\])/g,"\\\\$1")',
    '                 .replace(/\\x08/g,"\\\\x08");',
    "  return haystack.replace(new RegExp(needle, 'g'), replacement);",
    "}"
  ]);
  var code = functionName + "(" + text + ", " + from + ", " + to + ")";
  return [code, Blockly.JavaScript.ORDER_MEMBER];
};

Blockly.JavaScript["text_reverse"] = function(block) {
  var text =
    Blockly.JavaScript.valueToCode(
      block,
      "TEXT",
      Blockly.JavaScript.ORDER_MEMBER
    ) || "''";
  var code = text + ".split('').reverse().join('')";
  return [code, Blockly.JavaScript.ORDER_MEMBER];
};

// Flight commands

Blockly.JavaScript["setRoll_senior"] = function(block) {
  var arg0 = block.getFieldValue("ROLL");
  return "setRoll(" + arg0 + ");\n";
};

Blockly.JavaScript["setPitch_senior"] = function(block) {
  var arg0 = block.getFieldValue("VAL");
  return "setPitch(" + arg0 + ");\n";
};

Blockly.JavaScript["setYaw_senior"] = function(block) {
  var arg0 = block.getFieldValue("VAL");
  return "setYaw(" + arg0 + ");\n";
};

Blockly.JavaScript["setThrottle_senior"] = function(block) {
  var arg0 = block.getFieldValue("VAL");
  return "setThrottle(" + arg0 + ");\n";
};

Blockly.JavaScript["getRoll_senior"] = function(block) {
  return ["getRoll()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["getPitch_senior"] = function(block) {
  return ["getPitch()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["getYaw_senior"] = function(block) {
  return ["getYaw()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["getThrottle_senior"] = function(block) {
  return ["getThrottle()", Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.JavaScript["hover_junior"] = function(block) {
  var arg0 = parseFloat(block.getFieldValue("NUM0"));
  return "await hover(" + arg0 + ");\n";
};

Blockly.JavaScript["wait_junior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  return "await delay(" + arg0 + ");\n";
};

Blockly.JavaScript["wait_senior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  return "await delay(" + arg0 + ");\n";
};

Blockly.JavaScript["hover_senior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  return "await hover(" + arg0 + ");\n";
};

Blockly.JavaScript["hover_senior"] = function(block) {
  var arg0 = parseFloat(block.getFieldValue("NUM0"));
  return "await hover(" + arg0 + ");\n";
};

Blockly.JavaScript["emergencyStop_junior"] = function(block) {
  return "await emergencyStop();\n";
};

Blockly.JavaScript["emergencyStop_senior"] = function(block) {
  return "await emergencyStop();\n";
};

Blockly.JavaScript["onUpsideDown_junior"] = function(block) {
  var branch = Blockly.JavaScript.statementToCode(block, "DO");
  branch = Blockly.JavaScript.addLoopTrap(branch, block.id);

  return "onEvent(UPSIDE_DOWN, function (){\n" + branch + "})\n";
};

Blockly.JavaScript["onUpsideDown_senior"] = function(block) {
  return "onUpsideDown();\n";
};

Blockly.JavaScript["onTakeoff_junior"] = function(block) {
  var branch = Blockly.JavaScript.statementToCode(block, "DO");
  branch = Blockly.JavaScript.addLoopTrap(branch, block.id);

  return "onEvent(TAKEOFF, function (){\n" + branch + "})\n";
};

Blockly.JavaScript["onTakeoff_senior"] = function(block) {
  return "onTakeoff();\n";
};

Blockly.JavaScript["arm_strobe_senior"] = function(block) {
  return "await armStrobe();\n";
};

Blockly.JavaScript["eye_strobe_senior"] = function(block) {
  return "await eyeStrobe();\n";
};

Blockly.JavaScript["arm_strobe_junior"] = function(block) {
  return "await armStrobe();\n";
};

Blockly.JavaScript["eye_strobe_junior"] = function(block) {
  return "await eyeStrobe();\n";
};

Blockly.JavaScript["arm_default_strobe_senior"] = function(block) {
  return "await armDefaultStrobe();\n";
};

Blockly.JavaScript["eye_default_strobe_senior"] = function(block) {
  return "await eyeDefaultStrobe();\n";
};

Blockly.JavaScript["eye_off_senior"] = function(block) {
  return "await eyeOff();\n";
};

Blockly.JavaScript["arm_off_senior"] = function(block) {
  return "await armOff();\n";
};

Blockly.JavaScript["eye_off_junior"] = function(block) {
  return "await eyeOff();\n";
};

Blockly.JavaScript["arm_off_junior"] = function(block) {
  return "await armOff();\n";
};

Blockly.JavaScript["onCrash_junior"] = function(block) {
  var branch = Blockly.JavaScript.statementToCode(block, "DO");
  branch = Blockly.JavaScript.addLoopTrap(branch, block.id);

  return "onEvent(CRASH, function (){\n" + branch + "})\n";
};

Blockly.JavaScript["onCrash_senior"] = function(block) {
  return "onCrash();\n";
};

Blockly.JavaScript["onFreeFall_senior"] = function(block) {
  return "onFreeFall();\n";
};

Blockly.JavaScript["onLowBattery_junior"] = function(block) {
  var branch = Blockly.JavaScript.statementToCode(block, "DO");
  branch = Blockly.JavaScript.addLoopTrap(branch, block.id);

  return "onEvent(LOW_BATTERY, function (){\n" + branch + "})\n";
};

Blockly.JavaScript["onLowBattery_senior"] = function(block) {
  return "onLowBattery();\n";
};

Blockly.JavaScript["onSideways_senior"] = function(block) {
  return "onSideways();\n";
};

Blockly.JavaScript["onFlying_senior"] = function(block) {
  return "onFlying();\n";
};

Blockly.JavaScript["onLanding_senior"] = function(block) {
  return "onLanding();\n";
};

Blockly.JavaScript["onEmergencyStop_senior"] = function(block) {
  return "onEmergencyStop();\n";
};

Blockly.JavaScript["onIdle_senior"] = function(block) {
  return "onIdle();\n";
};

Blockly.JavaScript["move_senior"] = function(block) {
  var arg0 = parseFloat(block.getFieldValue("NUM0"));
  var arg1 = parseInt(block.getFieldValue("roll"));
  var arg2 = parseInt(block.getFieldValue("pitch"));
  var arg3 = parseInt(block.getFieldValue("yaw"));
  var arg4 = parseInt(block.getFieldValue("throttle"));
  return (
    "await move(" +
    arg0 +
    "," +
    arg1 +
    "," +
    arg2 +
    "," +
    arg3 +
    "," +
    arg4 +
    ");\n"
  );
};

Blockly.JavaScript["isCodeRunning_junior"] = function(block) {
  return ["await isCodeRunning()", Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript["isCodeRunning_senior"] = function(block) {
  return ["isCodeRunning()", Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript["whenKeyPressGet_junior"] = function(block) {
  var arg0 = block.getFieldValue("KEYPRESS");
  if (isNaN(arg0)) {
    arg0 = arg0.toString();
  }
  return [
    "window.KEY_PRESSED[" + arg0 + "] == " + arg0,
    Blockly.JavaScript.ORDER_ATOMIC
  ];
};

Blockly.JavaScript["whenKeyPressGet_senior"] = function(block) {
  var arg0 = block.getFieldValue("KEYPRESS");
  if (isNaN(arg0)) {
    arg0 = arg0.toString();
  }
  return ["window.KEY_PRESSED == " + arg0, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript["moveNoParams_junior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  return "await move();\n";
};

Blockly.JavaScript["moveNoParams_senior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  return "await move();\n";
};

Blockly.JavaScript["moveFlight_senior"] = function(block) {
  var arg0 = parseInt(block.getFieldValue("NUM0"));
  return "await move(" + arg0 + ");\n";
};

Blockly.JavaScript["flySquare_junior"] = function(block) {
  return "await flySequence(Sequence.SQUARE);\n";
};

Blockly.JavaScript["flyCircle_junior"] = function(block) {
  return "await flySequence(Sequence.CIRCLE);\n";
};

Blockly.JavaScript["flySpiral_junior"] = function(block) {
  return "await flySequence(Sequence.SPIRAL);\n";
};

Blockly.JavaScript["flyTriangle_junior"] = function(block) {
  return "await flySequence(Sequence.TRIANGLE);\n";
};

Blockly.JavaScript["flyHop_junior"] = function(block) {
  return "await flySequence(Sequence.HOP);\n";
};

Blockly.JavaScript["flysway_junior"] = function(block) {
  return "await flySequence(Sequence.SWAY);\n";
};

Blockly.JavaScript["flyZigzag_junior"] = function(block) {
  return "await flySequence(Sequence.ZIGZAG);\n";
};
