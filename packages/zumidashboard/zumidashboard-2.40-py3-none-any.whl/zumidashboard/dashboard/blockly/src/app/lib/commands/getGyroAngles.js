import Command from "./command.js";
import { sensorAngles } from "../types/sensorTypes.js";

export default class GetGyroAngles extends Command {
  constructor() {
    var sensorPackage = sensorAngles;
    var randomNumb = Math.floor((Math.random() * 90000) + 1);
    super(sensorPackage, 'getGyroAngles'+randomNumb);
  }

  async handleNotification(event) {
    if (event && event.target && event.target.value) {
      var gyroAngles = null;
      let arrayResult = new Uint8Array(event.target.value.buffer);
      if (arrayResult.length > 0) {
        await Code.readCharacteristic.stopNotifications();
        var attitudeRoll = (arrayResult[1] << 8) | (arrayResult[0] & 0xff);
        var attitudePitch = (arrayResult[3] << 8) | (arrayResult[2] & 0xff);
        var attitudeYaw = (arrayResult[6] << 8) | (arrayResult[5] & 0xff);

        var binaryAtittudeYaw = (attitudeYaw >>> 0).toString(2);

        var [signedValue] = new Int16Array(["0b" + binaryAtittudeYaw]);

        var yawDegree = signedValue >= 0 ? signedValue : 360 + signedValue;
        gyroAngles = {
          attitudeRoll: attitudeRoll,
          attitudePitch: attitudePitch,
          attitudeYaw: attitudeYaw,
          yawDegree: yawDegree
        };
        Code.readCharacteristic.removeEventListener(
          "characteristicvaluechanged",
          this.handleNotification
        );
        var event = new CustomEvent(this.eventName, { detail: gyroAngles });
        dispatchEvent(event);
        return;
      }
    }

    return;
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
