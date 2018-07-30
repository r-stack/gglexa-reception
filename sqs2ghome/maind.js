/**
 Check SQS Queue and notify to google home on the local network if a new message is coming.

 Requires EnvVar AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.
 Their IAM has to have SQS:ReceiveMessage and SQS:DeleteMessage.

  Refs
  https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/sqs-examples-send-receive-messages.html
  https://github.com/noelportugal/google-home-notifier#after-npm-install
  https://qiita.com/SatoTakumi/items/c9de7ff27e5b70508066
*/


// Google Home settings
const msg_tts = 'アレクサ、お客様がご来場でございます。';

// Setup
const gpio = require('pigpio').Gpio;
const button = new gpio(27, {
  mode: gpio.INPUT,
  pullUpDown: gpio.PUD_UP,
  edge: gpio.EITHER_EDGE
});

googlehome = require('google-home-notifier');
googlehome.device('Google-Home', 'ja');

// Main part

button.on('interrupt', function (level) {
   console.log(level);
   if(level){
     googlehome.notify(msg_tts, function (res) {});
   }
   else{
     
   }
}
);

setInterval(function(){console.log('aa')}, 1000);
