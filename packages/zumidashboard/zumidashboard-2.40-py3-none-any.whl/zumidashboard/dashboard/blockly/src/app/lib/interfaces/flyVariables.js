import {  commandManager } from '../commandManager.js';
import SetArmColor from '../commands/setArmColor.js';
import SetEyeColor from '../commands/setEyeColor.js';
import { flyVariables } from '../model/data.js';

function getBytesFromType(type) {
    return packages[type];
}

global.setRoll = async function (rollValue) {
  flyVariables.roll = rollValue;
}.bind(this);

global.setPitch = async function (pitchValue) {
  flyVariables.pitch = pitchValue;
}.bind(this);

global.setYaw = async function (yawValue) {
  flyVariables.yaw = yawValue;
}.bind(this);

global.setThrottle = async function (throttleValue) {
  flyVariables.throttle = throttleValue;
}.bind(this);

global.getRoll = function () {
  return flyVariables.roll;
}.bind(this);

global.getPitch = function () {
  return flyVariables.pitch;
}.bind(this);

global.getYaw = function () {
  return flyVariables.yaw;
}.bind(this);

global.getThrottle = function () {
  return flyVariables.throttle;
}.bind(this);
