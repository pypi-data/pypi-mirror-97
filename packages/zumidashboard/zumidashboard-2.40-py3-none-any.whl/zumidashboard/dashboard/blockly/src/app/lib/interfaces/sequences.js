import { commandManager } from "../commandManager.js";
import Move from "../commands/move.js";

var sequencesInteface = {};

global.flySequence = async function(sequenceType) {
  if (sequenceType === global.Sequence.SQUARE) {
    return sequencesInteface.square();
  } else if (sequenceType === global.Sequence.CIRCLE) {
    return sequencesInteface.circle();
  } else if (sequenceType === global.Sequence.TRIANGLE) {
    return sequencesInteface.triangle();
  } else if (sequenceType === global.Sequence.ZIGZAG) {
    return sequencesInteface.zigzag();
  } else if (sequenceType === global.Sequence.SWAY) {
    return sequencesInteface.sway();
  } else if (sequenceType === global.Sequence.HOP) {
    return sequencesInteface.hop();
  } else if (sequenceType === global.Sequence.SPIRAL) {
    return sequencesInteface.spiral();
  } else {
    alert(2);
  }
};

sequencesInteface.square = async function() {
  console.log("move in a square");

  if (!global.RUNNING) {
    return;
  }

  var promiseCommand = new Promise(async function(resolve, reject) {
    await global.move(2, 30, 0, 0, 0);
    await global.move(2, 0, 30, 0, 0);
    await global.move(2, -30, 0, 0, 0);
    await global.move(2, 0, -30, 0, 0);
  });
  return promiseCommand;
};

sequencesInteface.circle = async function() {
  console.log("move in a circle");

  if (!global.RUNNING) {
    return;
  }

  var promiseCommand = new Promise(async function(resolve, reject) {
    await global.move(10, 20, 0, -20, 0);
  });

  return promiseCommand;
};

sequencesInteface.triangle = async function() {
  console.log("move in a triangle");

  if (!global.RUNNING) {
    return;
  }

  var promiseCommand = new Promise(async function(resolve, reject) {
    console.log("first right 30");
    await turnDegree(Direction.RIGHT, 30);
    console.log("first move");
    await move(2, 0,30,0,0);
    //await global.go(Direction.FORWARD, 1.5, 30);
    console.log("second turn");
    await turnDegree(Direction.LEFT, 120);
    console.log("second move");
    await move(2, 0,30,0,0);
    //global.go(Direction.FORWARD, 1.5, 30)
    console.log("last turn");
    await turnDegree(Direction.LEFT, 120);
    await move(2, 0,30,0,0);
    // console.log("finish triangle");
  });

  return promiseCommand;
};

sequencesInteface.zigzag = async function() {
  console.log("move in a zigzag");

  if (!global.RUNNING) {
    return;
  }

  var promiseCommand = new Promise(async function(resolve, reject) {
    await global.move(1, 50, 50, 0, 0);
    await global.move(1, -50, 50, 0, 0);
    await global.move(1, 50, 50, 0, 0);
    await global.move(1, -50, 50, 0, 0);
    await global.hover(1);
  });
  return promiseCommand;
};

sequencesInteface.sway = async function() {
  console.log("move in a sway");

  if (!global.RUNNING) {
    return;
  }

  var promiseCommand = new Promise(async function(resolve, reject) {
    await global.go(Direction.LEFT, 1, 50);
    await global.go(Direction.RIGHT, 1, 50);
    await global.go(Direction.LEFT, 1, 50);
    await global.go(Direction.RIGHT, 1, 50);
  });
  return promiseCommand;
};

global.delay = async function(seconds) {
  var promiseDelay = new Promise(async function(resolve, reject) {
    setTimeout(
      async function() {
        resolve();
        return;
      }.bind(this),
      seconds * 1000
    );
  });
  return promiseDelay;
};

sequencesInteface.hop = async function() {
  console.log("move in a hop");

  if (!global.RUNNING) {
    return;
  }
  var promiseCommand = new Promise(async function(resolve, reject) {
    await global.move(1, 0, 30, 0, 50);
    console.log("delay hop 1");
    await global.delay(1);
    await global.move(1, 0, 30, 0, -50);
    console.log("delay hop 2");
    await global.delay(1);
    await global.hover(1);
  });
  return promiseCommand;
};

sequencesInteface.spiral = async function() {
  console.log("move in a spiral");

  if (!global.RUNNING) {
    return;
  }
  var promiseCommand = new Promise(async function(resolve, reject) {
    for (var i = 0; i < 100; i++) {
      console.log("iterator: ", i);
      global.setRoll(parseInt(i / 8));
      console.log("yaw: ", parseInt(i / 8));
      global.setYaw(-50);
      await global.move();
      await global.delay(0.1);
    }
    //  await hover(1);
    setRoll(0);
    setYaw(0);
  });
  return promiseCommand;
};
