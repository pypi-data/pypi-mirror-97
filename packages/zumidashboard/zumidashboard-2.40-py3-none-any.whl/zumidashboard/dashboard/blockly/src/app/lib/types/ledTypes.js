var dataArray = new Uint8Array(4);
dataArray[0] = 0x20;
dataArray[1] = 0x41;
dataArray[2] = 0x00;
dataArray[3] = 0x15;
exports.bytesLedPackage = dataArray;

var resetEyeArray = new Uint8Array(4);
resetEyeArray[0] = 0x20;
resetEyeArray[1] = 0x11;
resetEyeArray[2] = global.COLORS.Red;
resetEyeArray[3] = 0x15;

var resetArmsArray = new Uint8Array(4);
resetArmsArray[0] = 0x20;
resetArmsArray[1] = 0x41;
resetArmsArray[2] = global.COLORS.Red;
resetArmsArray[3] = 0x15;
exports.bytesResetLedPackage = {eye: resetEyeArray, arms: resetArmsArray};
