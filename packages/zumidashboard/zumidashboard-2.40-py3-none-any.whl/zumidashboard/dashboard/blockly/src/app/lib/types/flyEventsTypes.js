var dataArrayTakeOff = new Uint8Array(3);
dataArrayTakeOff[0] = 17;
dataArrayTakeOff[1] = 34;
dataArrayTakeOff[2] = 1;
exports.bytesTakeOff = dataArrayTakeOff;

var dataArrayLand = new Uint8Array(3);
dataArrayLand[0] = 17;
dataArrayLand[1] = 34;
dataArrayLand[2] = 7;
exports.bytesLand = dataArrayLand;

var dataArrayStop = new Uint8Array(3);
dataArrayStop[0] = 17;
dataArrayStop[1] = 36;
dataArrayStop[2] = 0;
exports.bytesEmergencyStop = dataArrayStop;

var dataArrayRotate180 = new Uint8Array(3);
dataArrayRotate180[0] = 17;
dataArrayRotate180[1] = 34;
dataArrayRotate180[2] = 14;
exports.bytesRotate180 = dataArrayRotate180;

var dataArrayGoForward = new Uint8Array(5);
dataArrayGoForward[0] = 16;
dataArrayGoForward[1] = 0;
dataArrayGoForward[2] = 50;
dataArrayGoForward[3] = 0;
dataArrayGoForward[4] = 0;
exports.bytesFlyForward = dataArrayGoForward;

var dataArrayGoBackward = new Uint8Array(5);
dataArrayGoBackward[0] = 16;
dataArrayGoBackward[1] = 0;
dataArrayGoBackward[2] = -50;
dataArrayGoBackward[3] = 0;
dataArrayGoBackward[4] = 0;
exports.bytesFlyBackward = dataArrayGoBackward;

var dataArrayUp = new Uint8Array(5);
dataArrayUp[0] = 16;
dataArrayUp[1] = 0;
dataArrayUp[2] = 0;
dataArrayUp[3] = 0;
dataArrayUp[4] = 50;
exports.bytesFlyUp = dataArrayUp;

var dataArrayDown = new Uint8Array(5);
dataArrayDown[0] = 16;
dataArrayDown[1] = 0;
dataArrayDown[2] = 0;
dataArrayDown[3] = 0;
dataArrayDown[4] = -50;
exports.bytesFlyDown = dataArrayDown;

var dataArrayRight = new Uint8Array(5);
dataArrayRight[0] = 16;
dataArrayRight[1] = 50;
dataArrayRight[2] = 0;
dataArrayRight[3] = 0;
dataArrayRight[4] = 0;
exports.bytesFlyRight = dataArrayRight;

var dataArrayLeft = new Uint8Array(5);
dataArrayLeft[0] = 16;
dataArrayLeft[1] = -50;
dataArrayLeft[2] = 0;
dataArrayLeft[3] = 0;
dataArrayLeft[4] = 0;
exports.bytesFlyLeft = dataArrayLeft;

var dataArrayHover = new Uint8Array(5);
dataArrayHover[0] = 16;
dataArrayHover[1] = 0;
dataArrayHover[2] = 0;
dataArrayHover[3] = 0;
dataArrayHover[4] = 0;
exports.bytesHover = dataArrayHover;
