/**
 This is a function for Lambda invoked when the IoT Button is clicked.
 The SQS queue called by this has to accept "SQS:SendMessage" by the role driving this function.
*/

var AWS = require('aws-sdk');

exports.handler = (event, context, callback) => {
    
    const sqs = new AWS.SQS({apiVersion: '2012-11-05'});
    const queueUrl = "https://sqs.ap-northeast-1.amazonaws.com/981111930280/hackaday2018-gglexa-trigger";
    const params = {
                       MessageBody: "button pushed.",
                       QueueUrl: queueUrl,
                    };

    sqs.sendMessage(params, function(err, data) {
        if (err) {
            console.log("Errors in calling SQS");
            console.log(err, err.stack);
            callback(err.stack, "Errors in calling SQS");
        } else {
            console.log("Succeeded in calling SQS");
            console.log(data);
            callback(null, "Succeeded in calling SQS");
        }
    });
    console.log("Lambda completed.");
};
