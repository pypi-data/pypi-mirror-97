import Command from "./command.js";
import { sensorHeight } from "../types/sensorTypes.js";

export default class GetHeight extends Command {
  constructor() {
    var sensorPackage = sensorHeight;
    super(sensorPackage, "getHeight");
  }

  handleNotification(event) {
    if (event && event.target && event.target.value) {
      console.log("buffer array", event.target.value.buffer);
      let arrayResult = new Uint8Array(event.target.value.buffer);
      let heightValue = 0;
      if (arrayResult.length > 11) {
        heightValue = (arrayResult[12] << 8) | (arrayResult[11] & 0xff);

        var binaryHeightValue = (heightValue >>> 0).toString(2);

        var [signedValue] = new Int16Array(["0b" + binaryHeightValue]);
      }
      Code.readCharacteristic.stopNotifications();

      Code.readCharacteristic.removeEventListener(
        "characteristicvaluechanged",
        this.handleNotification
      );

      var event = new CustomEvent(this.eventName, { detail: signedValue });
      dispatchEvent(event);
      return;
    }
  }

  async run() {
    await Code.readCharacteristic.startNotifications();
    Code.readCharacteristic.addEventListener(
      "characteristicvaluechanged",
      this.handleNotification
    );
    await this.sendBLECommand(this.package);

    return;
  }
}
