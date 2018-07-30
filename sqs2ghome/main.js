/**
 Check SQS Queue and notify to google home on the local network if a new message is coming.

 Requires EnvVar AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.
 Their IAM has to have SQS:ReceiveMessage and SQS:DeleteMessage.

  Refs
  https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/sqs-examples-send-receive-messages.html
  https://github.com/noelportugal/google-home-notifier#after-npm-install
  https://qiita.com/SatoTakumi/items/c9de7ff27e5b70508066
*/

const AWS = require('aws-sdk');
const googlehome = require('google-home-notifier')

// AWS settings
const AWS_REGION = 'ap-northeast-1';
const SQS_URL = 'https://sqs.ap-northeast-1.amazonaws.com/981111930280/hackaday2018-gglexa-trigger';
const QUEUE_CHECK_INTVL_SEC = 1
// Google Home settings
const msg_tts = 'アレクサ、お客様がご来場でございます。';

// Setup
AWS.config.update({ region:  AWS_REGION});
const sqs = new AWS.SQS({ apiVersion: '2012-11-05' });
const queueURL = SQS_URL;
const params = {
    AttributeNames: [
        'SentTimestamp'
    ],
    MaxNumberOfMessages: 1,
    MessageAttributeNames: [
        'All'
    ],
    QueueUrl: queueURL,
    VisibilityTimeout: 0,
    WaitTimeSeconds: 0
};
googlehome.device('Google-Home', 'ja');

// Main part
const receiveMsg = function () {
    sqs.receiveMessage(params, function (err, data) {
        if (err) {
            // Failed to get SQS message.
            console.log("Receive Error", err);
            setTimeout(receiveMsg, QUEUE_CHECK_INTVL_SEC * 1000);
        } else if (data.Messages) {
            // Got message. Notify Google Home.
            console.log(data.Messages)
            googlehome.notify(msg_tts, function (res) {
                console.log(res);
                // Delete SQS message after notifying Google Home.
                const deleteParams = {
                    QueueUrl: queueURL,
                    ReceiptHandle: data.Messages[0].ReceiptHandle
                };
                sqs.deleteMessage(deleteParams, function (err, data) {
                    if (err) {
                        console.log("Delete Error", err);
                    } else {
                        console.log("Message Deleted", data);
                    }
                });
                // Repeat to wait for another message.
                setTimeout(receiveMsg, QUEUE_CHECK_INTVL_SEC * 1000);
            })
        } else {
            // No message. Repeat to wait for another message.
            setTimeout(receiveMsg, QUEUE_CHECK_INTVL_SEC * 1000);
        }
    })
};

receiveMsg()
