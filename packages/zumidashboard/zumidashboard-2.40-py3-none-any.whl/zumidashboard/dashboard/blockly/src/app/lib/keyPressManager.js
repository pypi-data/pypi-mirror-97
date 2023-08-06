class KeyPressManager {
  constructor() {
    this.keyPressMap = {};
    this.keydownCallback = null;

    //
    //window.KEYPRESS_EVENT[Keyboard.w] === Keyboard.w

    global.addEventListener("keyup", function(e) {
      if (e && e.keyCode) {
        global.KEY_PRESSED[e.keyCode] = null;
        if (this.keyPressMap && this.keyPressMap[e.keyCode]) {
          try {
            global.RUNNING = true;
            return this.keyPressMap[e.keyCode].callback();
          } catch (e) {
            //alert(MSG["badCode"].replace("%1", e));
          }
        }
      }
    });
  }

  addKeyPressCode(keyCode, callback) {
    if (keyCode) {
      this.keyPressMap[keyCode] = { callback: callback };
      console.log(this.keyPressMap);
    }

    if (this.keydownCallback) {
      return;
    }

    this.keydownCallback = async function(e) {
      if (e && e.keyCode) {
        global.KEY_PRESSED[e.keyCode] = e.keyCode;
        //alert("keydownCallBack");
      }
      if (this.keyPressMap && this.keyPressMap[e.keyCode]) {
        try {
          global.RUNNING = true;
          return this.keyPressMap[e.keyCode].callback();
        } catch (e) {
          alert(MSG["badCode"].replace("%1", e));
        }
      }
    }.bind(this);

    global.addEventListener("keydown", this.keydownCallback);
  }

  removeKeyPressEvents() {
    if (this.keydownCallback) {
      removeEventListener("keydown", this.keydownCallback);
      this.keyPressMap = {};
      this.keydownCallback = null;
    }
  }

  hasKeyEventsAttached() {
    return !Object.keys(this.keyPressMap).length == 0;
  }
}

export let keyPressManager = new KeyPressManager();
