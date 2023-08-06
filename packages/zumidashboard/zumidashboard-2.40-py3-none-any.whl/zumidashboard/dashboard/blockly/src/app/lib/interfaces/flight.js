import { commandManager } from "../commandManager.js";
import Move from "../commands/move.js";
import TakeOff from "../commands/takeOff.js";
import Go from "../commands/go.js";
import Hover from "../commands/hover.js";
import Rotate180 from "../commands/rotate180.js";
import Land from "../commands/land.js";
import EmergencyStop from "../commands/emergencyStop.js";
import { flyVariables } from "../model/data.js";
import { keyPressManager } from "../keyPressManager.js";

var flightInteface = {};

global.stopExecution = function(skipForceLanding) {
  global.loopInProgress = false;
  global.RUNNING = false;
};

global.takeoff = async function() {
  if (!global.RUNNING) {
    return;
  }

  var promiseCommand = new Promise(async function(resolve, reject) {
    var takeOff = new TakeOff();
    await commandManager.runCommand(takeOff);
    setTimeout(
      async function() {
        console.log("------------ En take off 3 sec");
        resolve();
        return;
      }.bind(this),
      3000
    );
  });
  return promiseCommand;
};

global.rotate180 = async function() {
  if (!global.RUNNING) {
    return;
  }

  var promiseCommand = new Promise(async function(resolve, reject) {
    var rotate180 = new Rotate180();
    await commandManager.runCommand(rotate180);
    resolve();
    return;
  });

  return promiseCommand;
};

global.land = async function() {
  if (!global.RUNNING) {
    return;
  }

  var landCommand = new Land();
  return landCommand.run();
  return promiseCommand;
};

global.emergencyStop = async function(force) {
  if (!global.RUNNING) {
    return;
  }

  global.stopExecution(false);

  setTimeout(
    async function() {
      global.RUNNING = true;
      await global.emergencyStopInternal(true);
      global.stopExecution(false);
    }.bind(this),
    400
  );

  global.blockInterval = null;
  global.RUN_ONLY_DISPLAY_BLOCKS = false;
  global.DISPLAY_INTERVAL = false;

  keyPressManager.removeKeyPressEvents();

  $(".playButton").removeClass("disabled");
};

global.emergencyStopInternal = async function(force) {
  if (!global.RUNNING) {
    return;
  }
  var emergencyStop = new EmergencyStop();
  return await commandManager.runCommand(emergencyStop);
};

global.hover = async function(seconds) {
  var promiseCommand = new Promise(function(resolve, reject) {
    if (seconds === 0) {
      resolve();
      return;
    }
    global.loopInProgress = false;
    flightInteface.hoverLoop = async function() {
      var hoverCommand = new Hover();
      await commandManager.runCommand(hoverCommand);

      if (global.loopInProgress) {
        flightInteface.hoverLoop();
      } else {
        resolve();
        return;
      }
    };

    global.loopInProgress = true;

    setTimeout(
      function() {
        global.loopInProgress = false;
      }.bind(this),
      seconds * 1000
    );

    flightInteface.hoverLoop();
  });

  return promiseCommand;
};

global.go = function(direction, seconds, power) {
  if (!global.RUNNING) {
    return;
  }

  var promiseCommand = new Promise(function(resolve, reject) {
    if (seconds === 0) {
      resolve();
      return;
    }
    global.loopInProgress = false;
    flightInteface.goLoop = async function() {
      var goCommand = new Go(direction, power);
      await commandManager.runCommand(goCommand);

      if (global.loopInProgress) {
        flightInteface.goLoop();
      } else {
        await global.hover(1);
        resolve();
        return;
      }
    };

    global.loopInProgress = true;

    setTimeout(
      function() {
        global.loopInProgress = false;
      }.bind(this),
      seconds * 1000
    );

    flightInteface.goLoop();
  });

  return promiseCommand;
};

global.moveInternal = async function(roll, pitch, yaw, throttle) {
  if (!global.RUNNING) {
    return;
  }

  var moveCommand = new Move(roll, pitch, yaw, throttle);
  await commandManager.runCommand(moveCommand);
};

global.move = async function(seconds, roll, pitch, yaw, throttle) {
  if (!global.RUNNING) {
    return;
  }

  if (seconds && !roll && !pitch && !yaw && !throttle) {
    roll = flyVariables.roll;
    pitch = flyVariables.pitch;
    yaw = flyVariables.yaw;
    throttle = flyVariables.throttle;
  } else if (!seconds && !roll && !pitch && !yaw && !throttle) {
    return moveInternal(
      flyVariables.roll,
      flyVariables.pitch,
      flyVariables.yaw,
      flyVariables.throttle
    );
  }

  var promiseCommand = new Promise(function(resolve, reject) {
    global.loopInProgress = false;
    flightInteface.moveLoop = async function() {
      var moveCommand = new Move(roll, pitch, yaw, throttle);
      await commandManager.runCommand(moveCommand);

      if (global.loopInProgress) {
        flightInteface.moveLoop();
      } else {
        await global.hover(1);
        resolve();
        return;
      }
    };

    global.loopInProgress = true;

    setTimeout(
      function() {
        global.loopInProgress = false;
      }.bind(this),
      seconds * 1000
    );

    flightInteface.moveLoop();
  });

  return promiseCommand;
};

global.turnDegree = async function(direction, degree) {
  if (!global.RUNNING) {
    return;
  }

  var angle = await getGyroAngles();

  var speed = direction * 15;

  var dest = 360 + angle.yawDegree + parseInt(degree) * direction;

  var min = (dest - 5) % 360;

  var max = (dest + 5) % 360;

  var promiseCommand = new Promise(function(resolve, reject) {
    global.loopInProgress = true;

    flightInteface.adjustDegree = async function() {
      var angle = await getGyroAngles();
      console.log("Adjust Value is ", angle.yawDegree);

      if (min > max) {
        if (min < angle.yawDegree || max > angle.yawDegree) {
          global.loopInProgress = false;
          await global.hover(1);
          console.log("---- Running command: Ending turn", angle.yawDegree);
          resolve();
          return;
        }
      } else {
        if (min < angle.yawDegree && max > angle.yawDegree) {
          global.loopInProgress = false;
          await global.hover(1);
          console.log("---- Running command: Ending turn2", angle.yawDegree);
          resolve();
          return;
        }
      }

      await moveInternal(0, 0, speed, 0);

      if (global.loopInProgress) {
        flightInteface.adjustDegree();
      }
    }.bind(this);

    flightInteface.adjustDegree();
  });

  return promiseCommand;
};

global.turn = function(direction, seconds, power) {
  if (!global.RUNNING) {
    return;
  }
  var speed = direction * power;

  var promiseCommand = new Promise(function(resolve, reject) {
    global.loopInProgress = false;
    flightInteface.turnLoop = async function() {
      await moveInternal(0, 0, speed, 0);

      if (global.loopInProgress) {
        flightInteface.turnLoop();
      } else {
        await hover(1);
        resolve();
        return;
      }
    };

    global.loopInProgress = true;

    setTimeout(
      function() {
        global.loopInProgress = false;
      }.bind(this),
      seconds * 1000
    );

    flightInteface.turnLoop();
  });

  return promiseCommand;
};

// global.goToHeight = function(heightSet) {
//   if (!global.RUNNING) {
//     return;
//   }
//   var promiseCommand = new Promise(function(resolve, reject) {
//     global.loopInProgress = true;
//
//     flightInteface.adjustHeight = async function() {
//       var height = await getHeight();
//       console.log("Current height is ", height);
//
//       if (height < heightSet - 100) await moveInternal(0, 0, 0, 30);
//       else if (height > heightSet + 100) await moveInternal(0, 0, 0, -30);
//       else if (height > heightSet - 100 || height < heightSet + 100) {
//         await hover(0.5);
//         global.loopInProgress = false;
//         resolve();
//         return;
//       }
//
//       if (global.loopInProgress) {
//         flightInteface.adjustHeight();
//       }
//     }.bind(this);
//
//     flightInteface.adjustHeight();
//   });
//
//   return promiseCommand;
// };

global.goToHeight = function(height) {
  if (!global.RUNNING) {
    return;
  }
  var promiseCommand = new Promise(function(resolve, reject) {
    var power = 30;
    var interval = 20; // height - 10 ~ height + 10
    global.loopInProgress = true;

    flightInteface.adjustHeight = async function() {
      var state = await getHeight();
      console.log("Current height is ", height);
      var differ = height - state;
      if (differ > interval) {
        // Up
        await moveInternal(0, 0, 0, 30);
        global.delay(0.1);
      } else if (differ < -interval) {
        await moveInternal(0, 0, 0, -30);
        global.delay(0.1);
      } else {
        global.loopInProgress = false;
        resolve();
        return;
      }

      if (global.loopInProgress) {
        flightInteface.adjustHeight();
      }
    }.bind(this);

    flightInteface.adjustHeight();
  });

  return promiseCommand;
};

global.removeFlightIntervals = function() {
  clearInterval(flightInteface.moveIntevalId);
  clearInterval(flightInteface.goToHeightIntevalId);
  clearInterval(flightInteface.intervalId);
};
