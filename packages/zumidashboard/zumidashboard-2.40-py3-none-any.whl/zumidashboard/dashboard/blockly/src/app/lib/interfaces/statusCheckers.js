import { commandManager } from "../commandManager.js";
import { flyVariables } from "../model/data.js";
import { keyPressManager } from "../keyPressManager.js";

var statusCheckersInteface = {};

global.isCodeRunning = function() {
  return global.RUNNING;
};

global.getKeyPressed = function(arg){
  return global.KEY_PRESSED == arg;
};
