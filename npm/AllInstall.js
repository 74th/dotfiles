#!/usr/local/bin/node
var p = [];

// jasmin-node
p.push("jasmine-node");

// jshhint
p.push("jshint");

// typescript
p.push("typescript");

// jsontool
p.push("jsontool");

// nodeclipse
// nodejsをEclipseでデバッグする
// http://www.nodeclipse.org/
p.push("nodeclipse");

// AWS
// http://aws.amazon.com/jp/sdkfornodejs/
p.push("aws-sdk");

var exec = require('child_process').exec;
var chain = [];
var chainNext = function(){
    chain.shift().apply(v,arguments);
};
chain.push(function() {

    console.log("-- checking installed.");
    exec("npm -g list",chainNext);

});
chain.push(function(error,stdout,stderr) {

    console.log(stderr);

    var s = stdout.split("\n");
    var already = [];
    var saisho = "└";
    var saisho2 = "├";
    var re = "^([" + saisho + "|" + saisho2 + "])";
    s.forEach(function(s){
        var m = s.match(re);
        if( m ){
            m = s.match(/\w[^@]*/);
            already.push(m[0]);
        }
    });
    this.installPackageNum = 0;

    var i = 0;
    var oneInstall = function(){
        if( p.length == i){
            chainNext();
            return;
        }
        var name = p[i++];
        var isAlreadyInstall = false;
        already.forEach(function(a){
            if( a == name ){
                isAlreadyInstall = true;
            }
        });
        if(! isAlreadyInstall ){

            this.installPackageNum++;

            exec("npm -g install " + name,function(error,stdout,stderr){
                //console.log(stdout);
                console.log(stderr);
                oneInstall();
            });

        }else{
            oneInstall();
        }
    };
    oneInstall();
});
chain.push(function() {

    console.log("-- checking update");
    exec("npm -g update",chainNext);

});
chain.push(function(error,stdout,stderr) {

    //console.log(stdout);
    console.log(stderr);
    chainNext();

});
chain.push(function(){

    console.log("-- All done!");
    console.log("installing " + this.installPackageNum + " packages");

});

chainNext();
