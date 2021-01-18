document.onload = redirect()

function redirect(){
  window.setTimeout(function () {
        location.href = "/authorizator/login";
    }, 5000);
}
