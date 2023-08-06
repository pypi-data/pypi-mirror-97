import { commandManager } from "../commandManager.js";
import SetArmColor from "../commands/setArmColor.js";
import SetEyeColor from "../commands/setEyeColor.js";
import SetArmDefaultLED from "../commands/setArmDefaultLED.js";
import SetEyeDefaultLED from "../commands/setEyeDefaultLED.js";
import SetAllDefaultLED from "../commands/setAllDefaultLED.js";
import ResetDefaultLED from "../commands/resetDefaultLED.js";
import { dataLedMode } from "../model/data.js";

function getBytesFromType(type) {
  return packages[type];
}

global.setArmLED = async function(rValue, gValue, bValue, mode, interval) {
  if (!global.RUNNING) {
    return;
  }

  var promiseCommand = new Promise(async function(resolve, reject) {
    var setArmColor = new SetArmColor(
      rValue,
      gValue,
      bValue,
      mode + 0x30,
      interval
    );
    await setArmColor.run();
    resolve();
    return;
  });

  return promiseCommand;
}.bind(this);

global.setAllLED = async function(red, green, blue, mode, interval) {
  if (!global.RUNNING) {
    return;
  }

  var promiseCommand = new Promise(async function(resolve, reject) {
    await global.setArmLED(red, green, blue, mode, interval);
    await global.setEyeLED(red, green, blue, mode, interval);

    resolve();
    return;
  });

  return promiseCommand;
}.bind(this);

global.setEyeLED = async function(rValue, gValue, bValue, mode, interval) {
  if (!global.RUNNING) {
    return;
  }

  var promiseCommand = new Promise(async function(resolve, reject) {
    var setEyeColor = new SetEyeColor(rValue, gValue, bValue, mode, interval);
    await commandManager.runCommand(setEyeColor);

    resolve();
    return;
  });

  return promiseCommand;
}.bind(this);

global.setArmDefaultLED = async function(
  rValue,
  gValue,
  bValue,
  mode,
  interval
) {
  if (!global.RUNNING) {
    return;
  }

  var promiseCommand = new Promise(async function(resolve, reject) {
    var setArmDefault = new SetArmDefaultLED(
      rValue,
      gValue,
      bValue,
      mode + 0x30,
      interval
    );
    await commandManager.runCommand(setArmDefault);
    setTimeout(
      async function() {
        console.log("------------ resolv set arm");
        resolve();
        return;
      }.bind(this),
      200
    );
    return;
  });

  return promiseCommand;
}.bind(this);

global.setEyeDefaultLED = async function(
  rValue,
  gValue,
  bValue,
  mode,
  interval
) {
  if (!global.RUNNING) {
    return;
  }

  var promiseCommand = new Promise(async function(resolve, reject) {
    var setEyeDefault = new SetEyeDefaultLED(
      rValue,
      gValue,
      bValue,
      mode,
      interval
    );
    await commandManager.runCommand(setEyeDefault);
    setTimeout(
      async function() {
        console.log("------------ resolv set eye");
        resolve();
        return;
      }.bind(this),
      200
    );
  });

  return promiseCommand;
}.bind(this);

global.setAllDefaultLED = async function(
  rValue,
  gValue,
  bValue,
  mode,
  interval
) {
  if (!global.RUNNING) {
    return;
  }

  var promiseCommand = new Promise(async function(resolve, reject) {
    var setAllDefault = new SetAllDefaultLED(
      rValue,
      gValue,
      bValue,
      mode,
      interval,
      rValue,
      gValue,
      bValue,
      mode + 0x30,
      interval
    );
    await commandManager.runCommand(setAllDefault);
    setTimeout(
      async function() {
        console.log("------------ resolv set eye");
        resolve();
        return;
      }.bind(this),
      200
    );
  });

  return promiseCommand;
}.bind(this);

global.resetDefaultLED = async function() {
  if (!global.RUNNING) {
    return;
  }

  var promiseCommand = new Promise(async function(resolve, reject) {
    var resetDefault = new ResetDefaultLED();
    await resetDefault.run();
    resolve();
    return;
  });

  return promiseCommand;
}.bind(this);
