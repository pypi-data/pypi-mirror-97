/**
 * @license
 * Visual Blocks Editor
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
 * @fileoverview Text blocks for Blockly.
 * @author fraser@google.com (Neil Fraser)
 */
"use strict";

goog.provide("Blockly.Blocks.codrone"); // Deprecated
goog.provide("Blockly.Constants.Codrone");

goog.require("Blockly.Blocks");
goog.require("Blockly");

/**
 * Common HSV hue for all blocks in this category.
 * Should be the same as Blockly.Msg.TEXTS_HUE
 * @readonly
 */
Blockly.Constants.Codrone.HUE = "#3353da";
Blockly.Constants.Codrone.HUE_Orange2 = "#EC5B29";
Blockly.Constants.Codrone.HUE_Orange = "#f29327";
Blockly.Constants.Codrone.HUE_Violet = "#b358d7";
Blockly.Constants.Codrone.HUE_Rose = "#ee42ae";
Blockly.Constants.Codrone.HUE_Cian = "#3399e4";
Blockly.Constants.Codrone.HUE_flight_variables = "#33DAD8";
Blockly.Constants.Codrone.HUE_keyboard_input = "#CACACA";
Blockly.Constants.Codrone.HUE_timming = "#9B9B9B";
/** @deprecated Use Blockly.Constants.Text.HUE */
Blockly.Blocks.codrone.HUE = Blockly.Constants.Codrone.HUE;

Blockly.defineBlocksWithJsonArray([
  // BEGIN JSON EXTRACT

  {
    type: "variables_get_roll",
    message0: "get %1",
    args0: [
      {
        type: "field_variable",
        name: "VAR",
        variable: "roll",
        variableTypes: ["Number"] // Specifies what types to put in the dropdown
      }
    ],
    output: "Number", // Returns a value of "Panda"
    colour: "%{BKY_TEXTS_HUE}",
    tooltip: "%{BKY_TEXT_JOIN_TOOLTIP}",
    helpUrl: "%{BKY_TEXT_JOIN_HELPURL}"
  },
  {
    type: "variables_set_roll",
    message0: "%{BKY_VARIABLES_SET}",
    args0: [
      {
        type: "field_variable",
        name: "VAR",
        variable: "roll",
        variableTypes: ["Number"]
      },
      {
        type: "input_value",
        name: "VALUE",
        check: "Number" // Checks that the input value is of type "Panda"
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: "%{BKY_TEXTS_HUE}",
    tooltip: "%{BKY_TEXT_JOIN_TOOLTIP}",
    helpUrl: "%{BKY_TEXT_JOIN_HELPURL}"
  },
  {
    type: "variables_get_pitch",
    message0: "get %1",
    args0: [
      {
        type: "field_variable",
        name: "VAR",
        variable: "pitch",
        variableTypes: ["Number"] // Specifies what types to put in the dropdown
      }
    ],
    output: "Number", // Returns a value of "Panda"
    colour: "%{BKY_TEXTS_HUE}",
    tooltip: "%{BKY_TEXT_JOIN_TOOLTIP}",
    helpUrl: "%{BKY_TEXT_JOIN_HELPURL}"
  },
  {
    type: "variables_set_pitch",
    message0: "%{BKY_VARIABLES_SET}",
    args0: [
      {
        type: "field_variable",
        name: "VAR",
        variable: "pitch",
        variableTypes: ["Number"]
      },
      {
        type: "input_value",
        name: "VALUE",
        check: "Number" // Checks that the input value is of type "Panda"
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: "%{BKY_TEXTS_HUE}",
    tooltip: "%{BKY_TEXT_JOIN_TOOLTIP}",
    helpUrl: "%{BKY_TEXT_JOIN_HELPURL}"
  },
  {
    type: "variables_get_yaw",
    message0: "get %1",
    args0: [
      {
        type: "field_variable",
        name: "VAR",
        variable: "yaw",
        variableTypes: ["Number"] // Specifies what types to put in the dropdown
      }
    ],
    output: "Number", // Returns a value of "Panda"
    colour: "%{BKY_TEXTS_HUE}",
    tooltip: "%{BKY_TEXT_JOIN_TOOLTIP}",
    helpUrl: "%{BKY_TEXT_JOIN_HELPURL}"
  },
  {
    type: "variables_set_yaw",
    message0: "%{BKY_VARIABLES_SET}",
    args0: [
      {
        type: "field_variable",
        name: "VAR",
        variable: "yaw",
        variableTypes: ["Number"]
      },
      {
        type: "input_value",
        name: "VALUE",
        check: "Number" // Checks that the input value is of type "Panda"
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: "%{BKY_TEXTS_HUE}",
    tooltip: "%{BKY_TEXT_JOIN_TOOLTIP}",
    helpUrl: "%{BKY_TEXT_JOIN_HELPURL}"
  },
  {
    type: "variables_get_throttle",
    message0: "get %1",
    args0: [
      {
        type: "field_variable",
        name: "VAR",
        variable: "throttle",
        variableTypes: ["Number"] // Specifies what types to put in the dropdown
      }
    ],
    output: "Number", // Returns a value of "Panda"
    colour: "%{BKY_TEXTS_HUE}",
    tooltip: "%{BKY_TEXT_JOIN_TOOLTIP}",
    helpUrl: "%{BKY_TEXT_JOIN_HELPURL}"
  },
  {
    type: "variables_set_throttle",
    message0: "%{BKY_VARIABLES_SET}",
    args0: [
      {
        type: "field_variable",
        name: "VAR",
        variable: "throttle",
        variableTypes: ["Number"]
      },
      {
        type: "input_value",
        name: "VALUE",
        check: "Number" // Checks that the input value is of type "Panda"
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: "%{BKY_TEXTS_HUE}",
    tooltip: "%{BKY_TEXT_JOIN_TOOLTIP}",
    helpUrl: "%{BKY_TEXT_JOIN_HELPURL}"
  },
  {
    type: "send_command",
    message0: "when %1 key press",
    args0: [
      {
        type: "field_dropdown",
        name: "WHENKEYPRESSVAR",
        options: [
          ["backspace", "BACKSPACE"],
          ["up", "UP"],
          ["down", "DOWN"],
          ["right", "RIGHT"],
          ["left", "LEFT"],
          ["0", "0"],
          ["1", "1"],
          ["2", "2"],
          ["3", "3"],
          ["4", "4"],
          ["5", "5"],
          ["6", "6"],
          ["7", "7"],
          ["8", "8"],
          ["9", "9"],
          ["a", "a"],
          ["b", "b"],
          ["c", "c"],
          ["d", "d"],
          ["e", "e"],
          ["f", "f"],
          ["g", "g"],
          ["h", "h"],
          ["i", "i"],
          ["j", "j"],
          ["l", "l"],
          ["m", "m"],
          ["n", "n"],
          ["o", "o"],
          ["p", "p"],
          ["q", "q"],
          ["r", "r"],
          ["s", "s"],
          ["t", "t"],
          ["u", "u"],
          ["v", "v"],
          ["w", "w"],
          ["x", "x"],
          ["y", "y"],
          ["z", "z"]
        ]
      }
    ],
    message1: "%1",
    args1: [
      {
        type: "input_statement",
        name: "DO"
      }
    ],
    inputsInline: false,
    colour: Blockly.Constants.Codrone.HUE_keyboard_input,
    tooltip: "%{BKY_TEXT_JOIN_TOOLTIP}",
    helpUrl: "%{BKY_TEXT_JOIN_HELPURL}"
  },
  {
    type: "text_join",
    message0: "",
    output: "String",
    colour: "%{BKY_TEXTS_HUE}",
    helpUrl: "%{BKY_TEXT_JOIN_HELPURL}",
    tooltip: "%{BKY_TEXT_JOIN_TOOLTIP}",
    mutator: "text_join_mutator"
  }
]); // END JSON EXTRACT (Do not delete this comment.)

Blockly.Blocks["take_off_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 take off",
      previousStatement: null,
      nextStatement: null,
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_takeoff.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      colour: Blockly.Blocks.codrone.HUE,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

// Blockly.Blocks['take_off_junior'] = {
//   init: function() {
//     this.jsonInit({
//       "message0": "%1",
//       "previousStatement": null,
//       "nextStatement": null,
//       "args0": [
//         {
//           "type": "field_image",
//           "src": "images/graph.png",
//           "width": 125,
//           "height": 85,
//           "alt": "*"
//         }
//       ],
//       "tooltip": Blockly.Msg.TEXT_JOIN_TOOLTIP,
//       "colour": Blockly.Constants.Codrone.HUE_Orange2,
//       "helpUrl": Blockly.Msg.TEXT_JOIN_HELPURL
//     });
//   }
// };

Blockly.Blocks["take_off_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "takeoff()",
      previousStatement: null,
      nextStatement: null,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      colour: Blockly.Blocks.codrone.HUE,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["take_off"] = {
  /**
   * Block for print statement.
   * @this Blockly.Block
   // Block for text value
   {
     "type": "take_off",
     "message0": "Take Off",
     "output": null,
     "colour": "%{BKY_TEXTS_HUE}",
     "tooltip": "%{BKY_TEXT_JOIN_TOOLTIP}",
     "helpUrl": "%{BKY_TEXT_JOIN_HELPURL}"
   },
   */
  init: function() {
    this.jsonInit({
      message0: "Take Off",
      previousStatement: null,
      nextStatement: null,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["go_5"] = {
  init: function() {
    this.jsonInit({
      message0:
        "go (roll %1%, pitch %2%, yaw %3%, throttle %4%, duration %5 miliseconds)",
      args0: [
        {
          type: "field_number",
          name: "NUM0",
          value: 0
        },
        {
          type: "field_number",
          name: "NUM1",
          value: 0
        },
        {
          type: "field_number",
          name: "NUM2",
          value: 0
        },
        {
          type: "field_number",
          name: "NUM3",
          value: 0
        },
        {
          type: "field_number",
          name: "NUM4",
          value: 0
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Blocks.codrone.HUE,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["go"] = {
  init: function() {
    this.jsonInit({
      message0: "go",
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Blocks.codrone.HUE,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["go_direction_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%3 go %1 for %2 seconds",
      args0: [
        {
          type: "field_dropdown",
          name: "TYPE",
          options: [
            ["forward", "Direction.FORWARD"],
            ["backward", "Direction.BACKWARD"],
            ["up", "Direction.UP"],
            ["down", "Direction.DOWN"],
            ["left", "Direction.LEFT"],
            ["right", "Direction.RIGHT"]
          ]
        },
        {
          type: "field_number",
          name: "NUM0",
          value: 0,
          min: 0
        },
        {
          type: "field_image",
          src: "images/icons/icon_forward.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["go_direction_junior_3"] = {
  init: function() {
    this.jsonInit({
      message0: "%4 go %1 for %2 seconds at %3% power",
      args0: [
        {
          type: "field_dropdown",
          name: "TYPE",
          options: [
            ["forward", "Direction.FORWARD"],
            ["backward", "Direction.BACKWARD"],
            ["up", "Direction.UP"],
            ["down", "Direction.DOWN"],
            ["left", "Direction.LEFT"],
            ["right", "Direction.RIGHT"]
          ]
        },
        {
          type: "field_number",
          name: "NUM0",
          value: 0,
          min: 0
        },
        {
          type: "field_number",
          name: "NUM1",
          max: 100,
          min: -100,
          value: 0
        },
        {
          type: "field_image",
          src: "images/icons/icon_forward.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["turn_junior_3"] = {
  init: function() {
    this.jsonInit({
      message0: "%4 turn %1 for %2 seconds at %3% power",
      args0: [
        {
          type: "field_dropdown",
          name: "TYPE",
          options: [["left", "Direction.LEFT"], ["right", "Direction.RIGHT"]]
        },
        {
          type: "field_number",
          name: "NUM0",
          value: 0,
          min: 0
        },
        {
          type: "field_number",
          name: "NUM1",
          value: 0,
          max: 100,
          min: -100
        },
        {
          type: "field_image",
          src: "images/icons/icon_turn.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["turn_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "turn(%1, %2 seconds, %3%)",
      args0: [
        {
          type: "field_dropdown",
          name: "TYPE",
          options: [["left", "Direction.LEFT"], ["right", "Direction.RIGHT"]]
        },
        {
          type: "field_number",
          name: "NUM0",
          value: 0,
          min: 0
        },
        {
          type: "field_number",
          name: "NUM1",
          value: 0,
          min: -100,
          max: 100
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["turn_90_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "turn 90° %1",
      args0: [
        {
          type: "field_dropdown",
          name: "DIRECTION",
          options: [["left", "Direction.LEFT"], ["right", "Direction.RIGHT"]]
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Cian,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["rotate_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "rotate %1°",
      args0: [
        {
          type: "field_dropdown",
          name: "DEGREE",
          options: [["180", "180"], ["360", "360"]]
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Cian,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["rotate_180_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 turn 180 degrees",
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_180.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["gotoheight_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%2 go to %1 millimeters above ground",
      args0: [
        {
          type: "field_dropdown",
          name: "HEIGHT",
          options: [
            ["200", "200"],
            ["400", "400"],
            ["600", "600"],
            ["800", "800"],
            ["1000", "1000"],
            ["1200", "1200"],
            ["1400", "1400"],
            ["1600", "1600"],
            ["1800", "1800"],
            ["2000", "2000"]
          ]
        },
        {
          type: "field_image",
          src: "images/icons/icon_height.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["gotoheight2_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%2 go to %1 millimeters above ground(2)",
      args0: [
        {
          type: "field_dropdown",
          name: "HEIGHT",
          options: [
            ["200", "200"],
            ["400", "400"],
            ["600", "600"],
            ["800", "800"],
            ["1000", "1000"],
            ["1200", "1200"],
            ["1400", "1400"],
            ["1600", "1600"],
            ["1800", "1800"],
            ["2000", "2000"]
          ]
        },
        {
          type: "field_image",
          src: "images/icons/icon_height.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["gotoheight_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "go_to_height(%1 mm)",
      args0: [
        {
          type: "field_number",
          name: "NUM1",
          value: 0,
          min: 0,
          max: 2000
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["turn_degree_junior_2"] = {
  init: function() {
    this.jsonInit({
      message0: "%3 turn %2 by %1 degrees",
      args0: [
        {
          type: "field_dropdown",
          name: "DIRECTIONDEGREE",
          options: [
            ["30", "Degree.ANGLE_30"],
            ["45", "Degree.ANGLE_45"],
            ["60", "Degree.ANGLE_60"],
            ["90", "Degree.ANGLE_90"],
            ["120", "Degree.ANGLE_120"],
            ["135", "Degree.ANGLE_135"],
            ["150", "Degree.ANGLE_150"],
            ["180", "Degree.ANGLE_180"],
            ["210", "Degree.ANGLE_210"],
            ["225", "Degree.ANGLE_225"],
            ["240", "Degree.ANGLE_240"],
            ["270", "Degree.ANGLE_270"],
            ["300", "Degree.ANGLE_300"],
            ["315", "Degree.ANGLE_315"],
            ["330", "Degree.ANGLE_330"]
          ]
        },
        {
          type: "field_dropdown",
          name: "DIRECTION",
          options: [["left", "Direction.LEFT"], ["right", "Direction.RIGHT"]]
        },
        {
          type: "field_image",
          src: "images/icons/icon_turn.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["turn_degree_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "turn_degree(%2, %1º)",
      args0: [
        {
          type: "field_dropdown",
          name: "DIRECTIONDEGREE",
          options: [
            ["30", "Degree.ANGLE_30"],
            ["45", "Degree.ANGLE_45"],
            ["60", "Degree.ANGLE_60"],
            ["90", "Degree.ANGLE_90"],
            ["120", "Degree.ANGLE_120"],
            ["135", "Degree.ANGLE_135"],
            ["150", "Degree.ANGLE_150"],
            ["180", "Degree.ANGLE_180"],
            ["210", "Degree.ANGLE_210"],
            ["225", "Degree.ANGLE_225"],
            ["240", "Degree.ANGLE_240"],
            ["270", "Degree.ANGLE_270"],
            ["300", "Degree.ANGLE_300"],
            ["315", "Degree.ANGLE_315"],
            ["330", "Degree.ANGLE_330"]
          ]
        },
        {
          type: "field_dropdown",
          name: "DIRECTION",
          options: [["left", "Direction.LEFT"], ["right", "Direction.RIGHT"]]
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["land_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 land",
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_land.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["land_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "land()",
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["isReadyToFly_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 is the drone ready to fly?",
      output: "Boolean",
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_ontakeoff.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["isCodeRunning_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "is code running?",
      output: "Boolean",
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["isCodeRunning_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "is_code_running()",
      output: "Boolean",
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["isUpsideDown_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 is the drone upside down?",
      output: "Boolean",
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_upsidedown.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["isFlying_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 is the drone flying?",
      output: "Boolean",
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_ontakeoff.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["isReadyToFly_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "isReadyToFly()",
      output: "Boolean",
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["isUpsideDown_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "isUpsideDown()",
      output: "Boolean",
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["isFlying_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "isFlying()",
      output: "Boolean",
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["getHeight_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 get height from ground",
      output: "Number",
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_getheight.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      colour: Blockly.Constants.Codrone.HUE_Orange,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["getHeight_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "getHeight()",
      output: "Number",
      colour: Blockly.Constants.Codrone.HUE_Orange,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["getPressure_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "getPressure()",
      output: "Number",
      colour: Blockly.Constants.Codrone.HUE_Orange,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["getBarometer_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "getBarometer",
      output: "Number",
      colour: Blockly.Constants.Codrone.HUE_Orange,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["getTemperature_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "getDroneTemp()",
      output: "Number",
      colour: Blockly.Constants.Codrone.HUE_Orange,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["getAngles_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "getGyroAngles()",
      output: "Number",
      colour: Blockly.Constants.Codrone.HUE_Orange,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["getAngularSpeed_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "getAngularSpeed()",
      output: "Number",
      colour: Blockly.Constants.Codrone.HUE_Orange,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["getAccelerometer_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "getAccelerometer()",
      output: "Number",
      colour: Blockly.Constants.Codrone.HUE_Orange,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["getState_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "getState()",
      output: "Number",
      colour: Blockly.Constants.Codrone.HUE_Orange,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["getOpticalFlow_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "getOptFlowPosition()",
      output: "Number",
      colour: Blockly.Constants.Codrone.HUE_Orange,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["getOpticalFlow_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "getOpticalFlow()",
      output: "Number",
      colour: Blockly.Constants.Codrone.HUE_Orange,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["getBatteryPercentage_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 get battery percentage",
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_getbattery.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      output: "Number",
      colour: Blockly.Constants.Codrone.HUE_Orange,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["getBatteryPercentage_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "getBatteryPercentage()",
      output: "Number",
      colour: Blockly.Constants.Codrone.HUE_Orange,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["getGyroData_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 get gyro data",
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_getgyro.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      output: "Number",
      colour: Blockly.Constants.Codrone.HUE_Orange,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["getBatteryVoltage_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "getBatteryVoltage()",
      output: "Number",
      colour: Blockly.Constants.Codrone.HUE_Orange,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["getTrim_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "getTrim()",
      output: "Number",
      colour: Blockly.Constants.Codrone.HUE_Orange,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setEyeRGB_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%2 set eye color to %1, mode to %3, and speed to %4",
      args0: [
        {
          type: "field_colour",
          name: "COLOUR",
          colour: "#ff0000"
        },
        {
          type: "field_image",
          src: "images/icons/icon_eye.svg",
          width: 25,
          height: 25,
          alt: "*"
        },
        {
          type: "field_dropdown",
          name: "LEDMODE",
          options: [
            ["solid", "Mode.SOLID"],
            ["strobe", "Mode.STROBE"],
            ["blink", "Mode.BLINK"],
            ["double blink", "Mode.DOUBLE_BLINK"],
            ["dimming", "Mode.DIMMING"],
            ["pulse", "Mode.PULSE"],
            ["reverse pulse", "Mode.REVERSE_PULSE"],
            ["off", "Mode.OFF"]
          ]
        },
        {
          type: "field_number",
          name: "INTERVAL",
          value: 1,
          min: 1
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setArmRGB_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%2 set arm color to %1, mode to %3, and speed to %4",
      args0: [
        {
          type: "field_colour",
          name: "COLOUR",
          colour: "#ff0000"
        },
        {
          type: "field_image",
          src: "images/icons/icon_armLED.svg",
          width: 25,
          height: 25,
          alt: "*"
        },
        {
          type: "field_dropdown",
          name: "LEDMODE",
          options: [
            ["solid", "Mode.SOLID"],
            ["strobe", "Mode.STROBE"],
            ["blink", "Mode.BLINK"],
            ["double blink", "Mode.DOUBLE_BLINK"],
            ["dimming", "Mode.DIMMING"],
            ["pulse", "Mode.PULSE"],
            ["reverse pulse", "Mode.REVERSE_PULSE"],
            ["off", "Mode.OFF"]
          ]
        },
        {
          type: "field_number",
          name: "INTERVAL",
          value: 1,
          min: 1
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setArmPattern_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%2 set arm color to %1, and pattern to %3, with a speed of %4",
      args0: [
        {
          type: "field_colour",
          name: "COLOUR",
          colour: "#ff0000"
        },
        {
          type: "field_image",
          src: "images/icons/icon_armLED.svg",
          width: 25,
          height: 25,
          alt: "*"
        },
        {
          type: "field_dropdown",
          name: "LEDMODE",
          options: [
            ["blink", "Mode.BLINK"],
            ["double blink", "Mode.BLINK_DOUBLE"],
            ["dimming", "Mode.DIMMING"],
            ["pulse", "Mode.PULSE"],
            ["reverse pulse", "Mode.REVERSE_PULSE"]
          ]
        },
        {
          type: "field_dropdown",
          name: "INTERVAL",
          options: [
            ["1", "1"],
            ["2", "2"],
            ["3", "3"],
            ["4", "4"],
            ["5", "5"],
            ["6", "6"],
            ["7", "7"],
            ["8", "8"],
            ["9", "9"],
            ["10", "10"]
          ]
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setEyePattern_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%2 set eye color to %1, and pattern to %3, with a speed of %4",
      args0: [
        {
          type: "field_colour",
          name: "COLOUR",
          colour: "#ff0000"
        },
        {
          type: "field_image",
          src: "images/icons/icon_eye.svg",
          width: 25,
          height: 25,
          alt: "*"
        },
        {
          type: "field_dropdown",
          name: "LEDMODE",
          options: [
            ["blink", "Mode.BLINK"],
            ["double blink", "Mode.BLINK_DOUBLE"],
            ["dimming", "Mode.DIMMING"]
          ]
        },
        {
          type: "field_dropdown",
          name: "INTERVAL",
          options: [
            ["1", "1"],
            ["2", "2"],
            ["3", "3"],
            ["4", "4"],
            ["5", "5"],
            ["6", "6"],
            ["7", "7"],
            ["8", "8"],
            ["9", "9"],
            ["10", "10"]
          ]
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setArmColor_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%2 set arm color to %1, with a brightness of %3",
      args0: [
        {
          type: "field_colour",
          name: "COLOUR",
          colour: "#ff0000"
        },
        {
          type: "field_image",
          src: "images/icons/icon_armLED.svg",
          width: 25,
          height: 25,
          alt: "*"
        },
        {
          type: "field_number",
          name: "INTERVAL",
          value: 1,
          min: 1,
          max: 100
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setEyeColor_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%2 set eye color to %1, with a brightness of %3",
      args0: [
        {
          type: "field_colour",
          name: "COLOUR",
          colour: "#ff0000"
        },
        {
          type: "field_image",
          src: "images/icons/icon_eye.svg",
          width: 25,
          height: 25,
          alt: "*"
        },
        {
          type: "field_number",
          name: "INTERVAL",
          value: 1,
          min: 1,
          max: 100
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setEyeColor_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%2 set eye color to %1, with a brightness of %3",
      args0: [
        {
          type: "field_colour",
          name: "COLOUR",
          colour: "#ff0000"
        },
        {
          type: "field_image",
          src: "images/icons/icon_eye.svg",
          width: 25,
          height: 25,
          alt: "*"
        },
        {
          type: "field_number",
          name: "INTERVAL",
          value: 1,
          min: 1,
          max: 100
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setArmRGB_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "set_arm_LED(%1, %2, %3, %4, %5 sec)",
      args0: [
        {
          type: "field_number",
          name: "red",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "green",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "blue",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_dropdown",
          name: "LEDMODE",
          options: [
            ["solid", "Mode.SOLID"],
            ["strobe", "Mode.STROBE"],
            ["blink", "Mode.BLINK"],
            ["double blink", "Mode.DOUBLE_BLINK"],
            ["dimming", "Mode.DIMMING"],
            ["pulse", "Mode.PULSE"],
            ["reverse pulse", "Mode.REVERSE_PULSE"],
            ["off", "Mode.OFF"]
          ]
        },
        {
          type: "field_number",
          name: "INTERVAL",
          value: 1,
          min: 1
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setArmPattern_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "arm_pattern(%1, %2, %3, %4, %5 speed)",
      args0: [
        {
          type: "field_number",
          name: "red",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "green",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "blue",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_dropdown",
          name: "LEDMODE",
          options: [
            ["blink", "Mode.BLINK"],
            ["double blink", "Mode.BLINK_DOUBLE"],
            ["dimming", "Mode.DIMMING"],
            ["pulse", "Mode.PULSE"],
            ["reverse pulse", "Mode.REVERSE_PULSE"]
          ]
        },
        {
          type: "field_dropdown",
          name: "INTERVAL",
          options: [
            ["1", "1"],
            ["2", "2"],
            ["3", "3"],
            ["4", "4"],
            ["5", "5"],
            ["6", "6"],
            ["7", "7"],
            ["8", "8"],
            ["9", "9"],
            ["10", "10"]
          ]
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setDefaultEyePattern_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "default_eye_pattern(%1, %2, %3, %4, %5 speed)",
      args0: [
        {
          type: "field_number",
          name: "red",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "green",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "blue",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_dropdown",
          name: "LEDMODE",
          options: [
            ["blink", "Mode.BLINK"],
            ["double blink", "Mode.BLINK_DOUBLE"],
            ["dimming", "Mode.DIMMING"]
          ]
        },
        {
          type: "field_dropdown",
          name: "INTERVAL",
          options: [
            ["1", "1"],
            ["2", "2"],
            ["3", "3"],
            ["4", "4"],
            ["5", "5"],
            ["6", "6"],
            ["7", "7"],
            ["8", "8"],
            ["9", "9"],
            ["10", "10"]
          ]
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setDefaultArmPattern_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "default_arm_pattern(%1, %2, %3, %4, %5 speed)",
      args0: [
        {
          type: "field_number",
          name: "red",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "green",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "blue",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_dropdown",
          name: "LEDMODE",
          options: [
            ["blink", "Mode.BLINK"],
            ["double blink", "Mode.BLINK_DOUBLE"],
            ["dimming", "Mode.DIMMING"],
            ["pulse", "Mode.PULSE"],
            ["reverse pulse", "Mode.REVERSE_PULSE"]
          ]
        },
        {
          type: "field_dropdown",
          name: "INTERVAL",
          options: [
            ["1", "1"],
            ["2", "2"],
            ["3", "3"],
            ["4", "4"],
            ["5", "5"],
            ["6", "6"],
            ["7", "7"],
            ["8", "8"],
            ["9", "9"],
            ["10", "10"]
          ]
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setEyePattern_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "eye_pattern(%1, %2, %3, %4, %5 speed)",
      args0: [
        {
          type: "field_number",
          name: "red",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "green",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "blue",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_dropdown",
          name: "LEDMODE",
          options: [
            ["blink", "Mode.BLINK"],
            ["double blink", "Mode.BLINK_DOUBLE"],
            ["dimming", "Mode.DIMMING"]
          ]
        },
        {
          type: "field_dropdown",
          name: "INTERVAL",
          options: [
            ["1", "1"],
            ["2", "2"],
            ["3", "3"],
            ["4", "4"],
            ["5", "5"],
            ["6", "6"],
            ["7", "7"],
            ["8", "8"],
            ["9", "9"],
            ["10", "10"]
          ]
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["arm_strobe_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "arm_strobe()",
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["arm_strobe_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 strobe arm lights",
      previousStatement: null,
      nextStatement: null,
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_armLED.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["arm_off_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 turm arms off",
      previousStatement: null,
      nextStatement: null,
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_armLED.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["eye_strobe_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "eye_strobe()",
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["eye_strobe_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 strobe eye lights",
      previousStatement: null,
      nextStatement: null,
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_eye.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["eye_off_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 turn eyes off",
      previousStatement: null,
      nextStatement: null,
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_eye.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["arm_off_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "arm_off()",
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["eye_off_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "eye_off()",
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["arms_off_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "turn arms off",
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["eye_default_strobe_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "eye_default_strobe()",
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["arm_default_strobe_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "arm_default_strobe()",
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setArmColor_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "arm_color(%1, %2, %3, %4 brightness)",
      args0: [
        {
          type: "field_number",
          name: "red",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "green",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "blue",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "INTERVAL",
          value: 1,
          min: 1,
          max: 100
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setEyeColor_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "eye_color(%1, %2, %3, %4 brightness)",
      args0: [
        {
          type: "field_number",
          name: "red",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "green",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "blue",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "INTERVAL",
          value: 1,
          min: 1,
          max: 100
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setArmDefaultColor_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "arm_default_color(%1, %2, %3, %4 brightness)",
      args0: [
        {
          type: "field_number",
          name: "red",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "green",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "blue",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "INTERVAL",
          value: 1,
          min: 1,
          max: 100
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setEyeDefaultColor_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "eye_default_color(%1, %2, %3, %4 brightness)",
      args0: [
        {
          type: "field_number",
          name: "red",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "green",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "blue",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "INTERVAL",
          value: 1,
          min: 1,
          max: 100
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setEyeRGB_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "set_eye_LED(%1, %2, %3, %4, %5 sec)",
      args0: [
        {
          type: "field_number",
          name: "red",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "green",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "blue",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_dropdown",
          name: "LEDMODE",
          options: [
            ["solid", "Mode.SOLID"],
            ["strobe", "Mode.STROBE"],
            ["blink", "Mode.BLINK"],
            ["double blink", "Mode.DOUBLE_BLINK"],
            ["dimming", "Mode.DIMMING"],
            ["pulse", "Mode.PULSE"],
            ["reverse pulse", "Mode.REVERSE_PULSE"],
            ["off", "Mode.OFF"]
          ]
        },
        {
          type: "field_number",
          name: "INTERVAL",
          value: 1,
          min: 1
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setAllLED_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "set_all_LED(%1, %2, %3, %4, %5 sec)",
      args0: [
        {
          type: "field_number",
          name: "red",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "green",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "blue",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_dropdown",
          name: "LEDMODE",
          options: [
            ["solid", "Mode.SOLID"],
            ["strobe", "Mode.STROBE"],
            ["blink", "Mode.BLINK"],
            ["double blink", "Mode.DOUBLE_BLINK"],
            ["dimming", "Mode.DIMMING"],
            ["pulse", "Mode.PULSE"],
            ["reverse pulse", "Mode.REVERSE_PULSE"],
            ["off", "Mode.OFF"]
          ]
        },
        {
          type: "field_number",
          name: "INTERVAL",
          value: 1,
          min: 1
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setAllLED_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%2 set all LED to %1, mode to %3, and speed to %4",
      args0: [
        {
          type: "field_colour",
          name: "COLOUR",
          colour: "#ff0000"
        },
        {
          type: "field_image",
          src: "images/icons/icon_light.svg",
          width: 25,
          height: 25,
          alt: "*"
        },
        {
          type: "field_dropdown",
          name: "LEDMODE",
          options: [
            ["solid", "Mode.SOLID"],
            ["strobe", "Mode.STROBE"],
            ["blink", "Mode.BLINK"],
            ["double blink", "Mode.DOUBLE_BLINK"],
            ["dimming", "Mode.DIMMING"],
            ["pulse", "Mode.PULSE"],
            ["reverse pulse", "Mode.REVERSE_PULSE"],
            ["off", "Mode.OFF"]
          ]
        },
        {
          type: "field_number",
          name: "INTERVAL",
          value: 1,
          min: 1
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setArmDefaltLED_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "set_arm_default_LED(%1, %2, %3, %4, %5 sec)",
      args0: [
        {
          type: "field_number",
          name: "red",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "green",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "blue",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_dropdown",
          name: "LEDMODE",
          options: [
            ["solid", "Mode.SOLID"],
            ["strobe", "Mode.STROBE"],
            ["blink", "Mode.BLINK"],
            ["double blink", "Mode.DOUBLE_BLINK"],
            ["dimming", "Mode.DIMMING"],
            ["pulse", "Mode.PULSE"],
            ["reverse pulse", "Mode.REVERSE_PULSE"],
            ["off", "Mode.OFF"]
          ]
        },
        {
          type: "field_number",
          name: "INTERVAL",
          value: 1,
          min: 1
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setEyeDefaltLED_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "set_eye_default_LED(%1, %2, %3, %4, %5 sec)",
      args0: [
        {
          type: "field_number",
          name: "red",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "green",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "blue",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_dropdown",
          name: "LEDMODE",
          options: [
            ["solid", "Mode.SOLID"],
            ["strobe", "Mode.STROBE"],
            ["blink", "Mode.BLINK"],
            ["double blink", "Mode.DOUBLE_BLINK"],
            ["dimming", "Mode.DIMMING"],
            ["pulse", "Mode.PULSE"],
            ["reverse pulse", "Mode.REVERSE_PULSE"],
            ["off", "Mode.OFF"]
          ]
        },
        {
          type: "field_number",
          name: "INTERVAL",
          value: 1,
          min: 1
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};
Blockly.Blocks["setAllDefaltLED_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "set_all_default_LED(%1, %2, %3, %4, %5 sec)",
      args0: [
        {
          type: "field_number",
          name: "red",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "green",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_number",
          name: "blue",
          value: 0,
          min: 0,
          max: 255
        },
        {
          type: "field_dropdown",
          name: "LEDMODE",
          options: [
            ["solid", "Mode.SOLID"],
            ["strobe", "Mode.STROBE"],
            ["blink", "Mode.BLINK"],
            ["double blink", "Mode.DOUBLE_BLINK"],
            ["dimming", "Mode.DIMMING"],
            ["pulse", "Mode.PULSE"],
            ["reverse pulse", "Mode.REVERSE_PULSE"],
            ["off", "Mode.OFF"]
          ]
        },
        {
          type: "field_number",
          name: "INTERVAL",
          value: 1,
          min: 1
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["resetLED_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "reset_default_LED()",
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Violet,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["playsound_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%2 play this sound %1",
      args0: [
        {
          type: "field_dropdown",
          name: "SOUND",
          options: [["jingle", "jingle"]]
        },
        {
          type: "field_image",
          src: "images/icons/icon_audio.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Rose,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["playsound_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "playSound(%1)",
      args0: [
        {
          type: "field_dropdown",
          name: "SOUND",
          options: [["mySound", "MYSOUND"], ["mySound2", "MYSOUND2"]]
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Rose,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["playmysound_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "my sound %1",
      args0: [
        {
          type: "field_input",
          name: "SOUND",
          text: ""
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Rose,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["playmysound_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "playMYSound(%1)",
      args0: [
        {
          type: "field_input",
          name: "SOUND",
          text: ""
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Rose,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setvolume_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%2 volume to %1",
      args0: [
        {
          type: "field_number",
          name: "VOLUME",
          value: 0
        },
        {
          type: "field_image",
          src: "images/icons/icon_audio.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Rose,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setvolume_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "setVolume(%1 %)",
      args0: [
        {
          type: "field_number",
          name: "VOLUME",
          max: 100,
          min: 0,
          value: 0
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Rose,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["flySequence_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "flySequence %1",
      args0: [
        {
          type: "field_dropdown",
          name: "SEQUENCE",
          options: [
            ["square", "SQUARE"],
            ["circle", "CIRCLE"],
            ["spiral", "SPIRAL"],
            ["triangle", "TRIANGLE"],
            ["hop", "HOP"],
            ["sway", "SWAY"],
            ["zigzag", "ZIGZAG"]
          ]
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Cian,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["flyRoulette_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "flyRoulette",
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Cian,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["turtleTurn_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "turtleTurn",
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Cian,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["whenKeyPress_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "when %1 key press",
      args0: [
        {
          type: "field_dropdown",
          name: "WHENKEYPRESSVAR",
          options: [
            ["backspace", "Keyboard.BACKSPACE"],
            ["spacebar", "Keyboard.SPACEBAR"],
            ["up", "Keyboard.UP"],
            ["down", "Keyboard.DOWN"],
            ["right", "Keyboard.RIGHT"],
            ["left", "Keyboard.LEFT"],
            ["0", "Keyboard._0"],
            ["1", "Keyboard._1"],
            ["2", "Keyboard._2"],
            ["3", "Keyboard._3"],
            ["4", "Keyboard._4"],
            ["5", "Keyboard._5"],
            ["6", "Keyboard._6"],
            ["7", "Keyboard._7"],
            ["8", "Keyboard._8"],
            ["9", "Keyboard._9"],
            ["a", "Keyboard.a"],
            ["b", "Keyboard.b"],
            ["c", "Keyboard.c"],
            ["d", "Keyboard.d"],
            ["e", "Keyboard.e"],
            ["f", "Keyboard.f"],
            ["g", "Keyboard.g"],
            ["h", "Keyboard.h"],
            ["i", "Keyboard.i"],
            ["j", "Keyboard.j"],
            ["l", "Keyboard.l"],
            ["m", "Keyboard.m"],
            ["n", "Keyboard.n"],
            ["o", "Keyboard.o"],
            ["p", "Keyboard.p"],
            ["q", "Keyboard.q"],
            ["r", "Keyboard.r"],
            ["s", "Keyboard.s"],
            ["t", "Keyboard.t"],
            ["u", "Keyboard.u"],
            ["v", "Keyboard.v"],
            ["w", "Keyboard.w"],
            ["x", "Keyboard.x"],
            ["y", "Keyboard.y"],
            ["z", "Keyboard.z"]
          ]
        }
      ],
      message1: "%1",
      args1: [
        {
          type: "input_statement",
          name: "DO"
        }
      ],
      inputsInline: false,
      colour: Blockly.Constants.Codrone.HUE_keyboard_input,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["console_log"] = {
  /**
   * Block for print statement.
   * @this Blockly.Block
   */
  init: function() {
    this.jsonInit({
      message0: "console.log %1",
      args0: [
        {
          type: "input_value",
          name: "TEXT"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Blocks.texts.HUE,
      tooltip: Blockly.Msg.TEXT_PRINT_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_PRINT_HELPURL
    });
  }
};

Blockly.Blocks["whenKeyPressGet_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "when %1 key press",
      args0: [
        {
          type: "field_dropdown",
          name: "KEYPRESS",
          options: [
            ["backspace", "Keyboard.BACKSPACE"],
            ["spacebar", "Keyboard.SPACEBAR"],
            ["up", "Keyboard.UP"],
            ["down", "Keyboard.DOWN"],
            ["right", "Keyboard.RIGHT"],
            ["left", "Keyboard.LEFT"],
            ["0", "Keyboard._0"],
            ["1", "Keyboard._1"],
            ["2", "Keyboard._2"],
            ["3", "Keyboard._3"],
            ["4", "Keyboard._4"],
            ["5", "Keyboard._5"],
            ["6", "Keyboard._6"],
            ["7", "Keyboard._7"],
            ["8", "Keyboard._8"],
            ["9", "Keyboard._9"],
            ["a", "Keyboard.a"],
            ["b", "Keyboard.b"],
            ["c", "Keyboard.c"],
            ["d", "Keyboard.d"],
            ["e", "Keyboard.e"],
            ["f", "Keyboard.f"],
            ["g", "Keyboard.g"],
            ["h", "Keyboard.h"],
            ["i", "Keyboard.i"],
            ["j", "Keyboard.j"],
            ["l", "Keyboard.l"],
            ["m", "Keyboard.m"],
            ["n", "Keyboard.n"],
            ["o", "Keyboard.o"],
            ["p", "Keyboard.p"],
            ["q", "Keyboard.q"],
            ["r", "Keyboard.r"],
            ["s", "Keyboard.s"],
            ["t", "Keyboard.t"],
            ["u", "Keyboard.u"],
            ["v", "Keyboard.v"],
            ["w", "Keyboard.w"],
            ["x", "Keyboard.x"],
            ["y", "Keyboard.y"],
            ["z", "Keyboard.z"]
          ]
        }
      ],
      output: "Boolean",
      colour: Blockly.Constants.Codrone.HUE_keyboard_input,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["text_prompt_ext"] = {
  /**
   * Block for prompt function (external message).
   * @this Blockly.Block
   */
  init: function() {
    var TYPES = [
      [Blockly.Msg.TEXT_PROMPT_TYPE_TEXT, "TEXT"],
      [Blockly.Msg.TEXT_PROMPT_TYPE_NUMBER, "NUMBER"]
    ];
    this.setHelpUrl(Blockly.Msg.TEXT_PROMPT_HELPURL);
    this.setColour(Blockly.Blocks.codrone.HUE);
    // Assign 'this' to a variable for use in the closures below.
    var thisBlock = this;
    var dropdown = new Blockly.FieldDropdown(TYPES, function(newOp) {
      thisBlock.updateType_(newOp);
    });
    this.appendValueInput("TEXT").appendField(dropdown, "TYPE");
    this.setOutput(true, "String");
    this.setTooltip(function() {
      return thisBlock.getFieldValue("TYPE") == "TEXT"
        ? Blockly.Msg.TEXT_PROMPT_TOOLTIP_TEXT
        : Blockly.Msg.TEXT_PROMPT_TOOLTIP_NUMBER;
    });
  },
  /**
   * Modify this block to have the correct output type.
   * @param {string} newOp Either 'TEXT' or 'NUMBER'.
   * @private
   * @this Blockly.Block
   */
  updateType_: function(newOp) {
    this.outputConnection.setCheck(newOp == "NUMBER" ? "Number" : "String");
  },
  /**
   * Create XML to represent the output type.
   * @return {!Element} XML storage element.
   * @this Blockly.Block
   */
  mutationToDom: function() {
    var container = document.createElement("mutation");
    container.setAttribute("type", this.getFieldValue("TYPE"));
    return container;
  },
  /**
   * Parse XML to restore the output type.
   * @param {!Element} xmlElement XML storage element.
   * @this Blockly.Block
   */
  domToMutation: function(xmlElement) {
    this.updateType_(xmlElement.getAttribute("type"));
  }
};

Blockly.Blocks["text_prompt"] = {
  /**
   * Block for prompt function (internal message).
   * The 'text_prompt_ext' block is preferred as it is more flexible.
   * @this Blockly.Block
   */
  init: function() {
    this.mixin(Blockly.Constants.Codrone.QUOTE_IMAGE_MIXIN);
    var TYPES = [
      [Blockly.Msg.TEXT_PROMPT_TYPE_TEXT, "TEXT"],
      [Blockly.Msg.TEXT_PROMPT_TYPE_NUMBER, "NUMBER"]
    ];

    // Assign 'this' to a variable for use in the closures below.
    var thisBlock = this;
    this.setHelpUrl(Blockly.Msg.TEXT_PROMPT_HELPURL);
    this.setColour(Blockly.Blocks.codrone.HUE);
    var dropdown = new Blockly.FieldDropdown(TYPES, function(newOp) {
      thisBlock.updateType_(newOp);
    });
    this.appendDummyInput()
      .appendField(dropdown, "TYPE")
      .appendField(this.newQuote_(true))
      .appendField(new Blockly.FieldTextInput(""), "TEXT")
      .appendField(this.newQuote_(false));
    this.setOutput(true, "String");
    this.setTooltip(function() {
      return thisBlock.getFieldValue("TYPE") == "TEXT"
        ? Blockly.Msg.TEXT_PROMPT_TOOLTIP_TEXT
        : Blockly.Msg.TEXT_PROMPT_TOOLTIP_NUMBER;
    });
  },
  updateType_: Blockly.Blocks["text_prompt_ext"].updateType_,
  mutationToDom: Blockly.Blocks["text_prompt_ext"].mutationToDom,
  domToMutation: Blockly.Blocks["text_prompt_ext"].domToMutation
};

Blockly.Blocks["text_count"] = {
  /**
   * Block for counting how many times one string appears within another string.
   * @this Blockly.Block
   */
  init: function() {
    this.jsonInit({
      message0: Blockly.Msg.TEXT_COUNT_MESSAGE0,
      args0: [
        {
          type: "input_value",
          name: "SUB",
          check: "String"
        },
        {
          type: "input_value",
          name: "TEXT",
          check: "String"
        }
      ],
      output: "Number",
      inputsInline: true,
      colour: Blockly.Blocks.codrone.HUE,
      tooltip: Blockly.Msg.TEXT_COUNT_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_COUNT_HELPURL
    });
  }
};

Blockly.Blocks["text_replace"] = {
  /**
   * Block for replacing one string with another in the text.
   * @this Blockly.Block
   */
  init: function() {
    this.jsonInit({
      message0: Blockly.Msg.TEXT_REPLACE_MESSAGE0,
      args0: [
        {
          type: "input_value",
          name: "FROM",
          check: "String"
        },
        {
          type: "input_value",
          name: "TO",
          check: "String"
        },
        {
          type: "input_value",
          name: "TEXT",
          check: "String"
        }
      ],
      output: "String",
      inputsInline: true,
      colour: Blockly.Blocks.codrone.HUE,
      tooltip: Blockly.Msg.TEXT_REPLACE_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_REPLACE_HELPURL
    });
  }
};

// Flight Variables
Blockly.Blocks["setRoll_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "set_roll(%1 %)",
      args0: [
        {
          type: "field_number",
          name: "ROLL",
          max: 100,
          min: -100,
          value: 0
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_flight_variables,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setPitch_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "set_pitch(%1 %)",
      args0: [
        {
          type: "field_number",
          name: "VAL",
          max: 100,
          min: -100,
          value: 0
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_flight_variables,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setYaw_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "set_yaw(%1 %)",
      args0: [
        {
          type: "field_number",
          name: "VAL",
          max: 100,
          min: -100,
          value: 0
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_flight_variables,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["setThrottle_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "set_throttle(%1 %)",
      args0: [
        {
          type: "field_number",
          name: "VAL",
          max: 100,
          min: -100,
          value: 0
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_flight_variables,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["getRoll_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "get_roll()",
      output: "Number",
      colour: Blockly.Constants.Codrone.HUE_flight_variables,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["getPitch_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "get_pitch()",
      output: "Number",
      colour: Blockly.Constants.Codrone.HUE_flight_variables,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["getYaw_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "get_yaw()",
      output: "Number",
      colour: Blockly.Constants.Codrone.HUE_flight_variables,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["getThrottle_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "get_throttle()",
      output: "Number",
      colour: Blockly.Constants.Codrone.HUE_flight_variables,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

// End

Blockly.Blocks["hover_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%2 hover for %1 seconds",
      args0: [
        {
          type: "field_number",
          name: "NUM0",
          min: 0,
          value: 0
        },
        {
          type: "field_image",
          src: "images/icons/icon_hover.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Blocks.codrone.HUE,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["hover_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "hover(%1 sec)",
      args0: [
        {
          type: "field_number",
          name: "NUM0",
          min: 0,
          value: 0
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Blocks.codrone.HUE,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["wait_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%2 wait %1 seconds",
      args0: [
        {
          type: "field_number",
          name: "NUM0",
          value: 0
        },
        {
          type: "field_image",
          src: "images/icons/icon_wait.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_timming,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["wait_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "%2 sleep(%1 sec)",
      args0: [
        {
          type: "field_number",
          name: "NUM0",
          value: 0
        },
        {
          type: "field_image",
          src: "images/icons/icon_wait.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_timming,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["emergencyStop_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 emergency stop",
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_stop.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["emergencyStop_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "emergency_stop()",
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["move_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "move(%1 sec, %2 %, %3 %, %4 %, %5 %)",
      args0: [
        {
          type: "field_number",
          name: "NUM0",
          value: 0
        },
        {
          type: "field_number",
          name: "roll",
          max: 100,
          min: -100,
          value: 0
        },
        {
          type: "field_number",
          name: "pitch",
          max: 100,
          min: -100,
          value: 0
        },
        {
          type: "field_number",
          name: "yaw",
          max: 100,
          min: -100,
          value: 0
        },
        {
          type: "field_number",
          name: "throttle",
          max: 100,
          min: -100,
          value: 0
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Blocks.codrone.HUE,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["moveFlight_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "move(%1 sec)",
      args0: [
        {
          type: "field_number",
          name: "NUM0",
          min: 0,
          value: 0
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_flight_variables,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["moveNoParams_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "move()",
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_flight_variables,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["onUpsideDown_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 on upside Down",
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_upsidedown.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      message1: "%1",
      args1: [
        {
          type: "input_statement",
          name: "DO"
        }
      ],
      inputsInline: false,
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["onUpsideDown_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "onUpsideDown()",
      inputsInline: false,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["onTakeoff_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 on take off",
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_ontakeoff.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      message1: "%1",
      args1: [
        {
          type: "input_statement",
          name: "DO"
        }
      ],
      inputsInline: false,
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["onTakeoff_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "onTakeoff()",
      inputsInline: false,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["onCrash_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 on crash",
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_oncrash.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      message1: "%1",
      args1: [
        {
          type: "input_statement",
          name: "DO"
        }
      ],
      inputsInline: false,
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["onCrash_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "onCrash()",
      inputsInline: false,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["onFreeFall_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "onFreeFall()",
      inputsInline: false,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["onLowBattery_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 on low battery",
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_lowbattery.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      message1: "%1",
      args1: [
        {
          type: "input_statement",
          name: "DO"
        }
      ],
      inputsInline: false,
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["isFlying_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "isFlying()",
      output: "Boolean",
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["onLowBattery_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "onLowBattery()",
      inputsInline: false,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["onSideways_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "onSideways()",
      inputsInline: false,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["onFlying_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "onFlying()",
      inputsInline: false,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["onLanding_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "onLanding()",
      inputsInline: false,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["onEmergencyStop_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "onEmergencyStop()",
      inputsInline: false,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["onIdle_senior"] = {
  init: function() {
    this.jsonInit({
      message0: "onIdle()",
      inputsInline: false,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Orange2,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["flySquare_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 fly in a square",
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_square.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Cian,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};
Blockly.Blocks["flyCircle_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 fly in a circle",
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_flycircle.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Cian,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};
Blockly.Blocks["flySpiral_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 fly in a spiral",
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_spiral.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Cian,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};
Blockly.Blocks["flyTriangle_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 fly in a triangle",
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_triangle.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Cian,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};
Blockly.Blocks["flyHop_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 hop forward",
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_hop.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Cian,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};
Blockly.Blocks["flysway_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 sway",
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_sway.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Cian,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};
Blockly.Blocks["flyZigzag_junior"] = {
  init: function() {
    this.jsonInit({
      message0: "%1 zigzag",
      args0: [
        {
          type: "field_image",
          src: "images/icons/icon_zigzag.svg",
          width: 25,
          height: 25,
          alt: "*"
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: Blockly.Constants.Codrone.HUE_Cian,
      tooltip: Blockly.Msg.TEXT_JOIN_TOOLTIP,
      helpUrl: Blockly.Msg.TEXT_JOIN_HELPURL
    });
  }
};

Blockly.Blocks["var_block"] = {
  init: function() {
    this.appendValueInput("MYVAR")
      .setCheck("Number")
      .appendField("value: ");
    this.setColour(Blockly.Constants.Codrone.HUE_Orange);
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    var thisBlock = this;
  }
};

Blockly.Blocks["show_var_data"] = {
  init: function() {
    this.appendValueInput("MYVAR")
      .setCheck("Number")
      .appendField("Value: ");
    this.setColour(Blockly.Constants.Codrone.HUE_Orange);
    var thisBlock = this;
  }
};
