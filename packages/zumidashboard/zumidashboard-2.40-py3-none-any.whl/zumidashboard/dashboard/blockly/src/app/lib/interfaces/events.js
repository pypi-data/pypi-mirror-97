import '../../constants/consts.js';
import LowBattery from '../events/lowBattery.js';
import { eventManager } from '../eventManager.js';
import { keyPressManager } from '../keyPressManager.js';

var EventLib = {};

global.onEvent = function(eventType, callback){
  switch (eventType) {
   case LOW_BATTERY:
      var batteryEvent = new LowBattery(callback);
      eventManager.addEvent(batteryEvent, eventType);
      break;
   }
};

global.onKeyPressEvent = function(keyCode, callback){
  keyPressManager.addKeyPressCode(keyCode, callback);
};
