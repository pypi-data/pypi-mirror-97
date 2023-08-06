import Command from './command.js';
import { trimData } from '../types/sensorTypes.js';

export default class GetAccelerometer extends Command {
  constructor(){
      var trimPackage = trimData;
      super(trimPackage, 'getAccelerometer');
  }

  async run(){
    await this.sendBLECommand(this.package);
    const value = await Code.readCharacteristic.readValue();
    var arrayResult = this.removePackageHeader(value.buffer)

		var imuAccX	= (arrayResult[3] << 8) | (arrayResult[2]);// x and y are switched
		var imuAccY	= (_completeData[1] << 8) | (arrayResult[0]);// x and y are switched
		var imuAccZ	= -(arrayResult[5] << 8) | (arrayResult[4]);// y needs to be flipped to have gravity be negative

    console.log('GetAccelerometer raw data', arrayResult);

    var accelerometerData = {imuAccX: imuAccX,
                    imuAccY: trimimuAccYAllPitch,
                    imuAccZ: imuAccZ};

    console.log('GetAccelerometer data:', accelerometerData);

    var event = new CustomEvent(this.eventName, { detail: trimData });
    dispatchEvent(event);
  }
}
