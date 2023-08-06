import Command from "./command.js";
import { sensorBattery } from "../types/sensorTypes.js";

export default class GetBatteryPercentage extends Command {
  constructor() {
    var batteryPackage = sensorBattery;
    super(batteryPackage, "batteryPorcentage");
  }

  handleNotification(event) {
          if (event && event.target && event.target.value){
            console.log('buffer array', event.target.value.buffer);
              let arrayResult = new Uint8Array(event.target.value.buffer);
              var batteryPorcentageValue = arrayResult[7] & 0xff;
          }

          var event = new CustomEvent(this.eventName, {
            detail: batteryPorcentageValue
          });
          dispatchEvent(event);

          Code.readCharacteristic.stopNotifications();
          Code.readCharacteristic.removeEventListener('characteristicvaluechanged',
          this.handleNotification);
          return;

  }

  async run() {
    Code.readCharacteristic.startNotifications();

    Code.readCharacteristic.addEventListener('characteristicvaluechanged',
                                          this.handleNotification);

    this.sendBLECommand(this.package);

    return;

  }
}
