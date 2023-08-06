import Command from './command.js';
import { sensorOptFlow } from '../types/sensorTypes.js';

export default class GetOptFlowPosition extends Command {
  constructor(){
      var sensorPackage = sensorOptFlow;
      super(sensorPackage, 'getOptFlowPosition');
  }

  async run(){
    await this.sendBLECommand(this.package);
    const value = await Code.readCharacteristic.readValue();
    var arrayResult = this.removePackageHeader(value.buffer)
    var fVelocitySumX	= ((arrayResult[3] << 32)  |(arrayResult[2] << 16)  |(arrayResult[1] << 8)  | (arrayResult[0]  & 0xff));
    var fVelocitySumY	= ((arrayResult[7] << 32)  |(arrayResult[6] << 16)  |(arrayResult[5] << 8)  | (arrayResult[4]  & 0xff));
    var result = { x: fVelocitySumX, y: fVelocitySumY }
    var event = new CustomEvent(this.eventName, { detail: result });
    dispatchEvent(event);
  }
}
