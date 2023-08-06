export default class Command {
  constructor(packageData, eventName) {
    this.package = packageData;
    this.eventName = eventName;
    this.handleNotification = this.handleNotification.bind(this);
  }

  async run() {
    console.log(this.package);
  }

  async handleNotification(){

  }

  async sendBLECommand(packageValue) {
    console.log("---- Running command: " + this.eventName);
    try {
      return await Code.writeCharacteristic.writeValue(packageValue);
    } catch (e) {
      console.log("error in command " + this.eventName);
      //global.stopExecution();
      if (e) {
        console.log(e);
      }
    }
  }

  async readBLEValue(packageValue) {
    console.log("---- reading value for command: " + this.eventName);
    try {
      return await Code.readCharacteristic.readValue();
    } catch (e) {
      console.log("error reading value for command " + this.eventName);
      //global.stopExecution();
      if (e) {
        console.log(e);
      }
    }
  }

  removePackageHeader(buffer) {
    var packageValue = new Uint8Array(buffer);
    console.log(packageValue);
    return packageValue.slice(1, packageValue.length);
  }

  async getValue() {
    return new Promise(
      function(resolve, reject) {
        addEventListener(
          this.eventName,
          function(e) {
            resolve(e.detail);
          },
          false
        );
      }.bind(this)
    );
  }
}
