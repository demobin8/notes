### 1. Change url resource request
example: hijack js

replace the origin js file, and modify some important method
```
var fs = require('fs');
dirname = fs.workingDirectory
page.onResourceRequested = function(requestData, networkRequest) {
      var match = requestData.url.match(/app-8f71f5f5.js/g);
      if (match != null) {
          console.log('Request (#' + requestData.id + '): ' + JSON.stringify(requestData));
          networkRequest.changeUrl('file://' + dirname + '/app-beautified.js'); 
      }
}; 
```
### 2. Send event
example: send keypress event to pass js detect
```
function keypress(){
    page.sendEvent('keypress', 32);
    page.sendEvent('keypress', 16777219);
}
```
### 3. Evaluate
example: deep into the html document playground
```            
page.evaluate(function() {
    $("#loginUser")[0].value = 'username';
    $("#loginPwd")[0].value = 'password'; 
    $(".btn-login")[0].click();
});
```
### 4. InjectJs
```
page.injectJs('inject.js')
```
### 5. Settings
```
page.settings.userAgent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0';
page.customHeaders = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    //"Accept-Language": "en-US,en;q=0.5",
    //"Accept-Encoding": "gzip, deflate",
};
page.onInitialized = function() {
    page.customHeaders = {};
};
```
### 6. Render
```
page.render('home.png');
```
