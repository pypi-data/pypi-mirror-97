export default class LowBattery {
  constructor(callback){
      this.callback = callback;
      this.intervalId = null;
      this.intervalTime = 1500;
      this.batteryLowLevelValue = 15;
  }

  async run(){
      console.log('start iteration: ');
      this.intervalId = setInterval(async function(){
       var batteryPorcentage = await global.getBatteryPercentage();
       if(this.callback && batteryPorcentage<this.batteryLowLevelValue) {
          this.callback();
          clearInterval(this.intervalId);
          this.callback = null;
       }
    }.bind(this), this.intervalTime);
  }
}
