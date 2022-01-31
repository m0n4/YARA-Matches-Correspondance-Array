function trigger(endpoint) {
  fetch(endpoint)
    .then((resp) => resp.json())
    .then(function (data) {
      let draw = new Boolean("true");
      Object.keys(data).forEach(function (key) {
        if (key == "draw") {
          document.getElementById(key).innerHTML = data[key];
          draw = Boolean("false");
          var table = document.getElementsByTagName("table");
          var classes = [
            "table",
            "table-striped",
            "caption-top",
            "text-center",
            "table-hover",
            "table-header-rotated",
            "table-borderless",
            "table-sm",
          ];
          for (var i = 0; i < table.length; i++) {
            for (var j = 0; j < classes.length; j++) {
              table[i].classList.add(classes[j]);
            }
          }
          var th = document.getElementsByTagName("th");
          for (var i = 2; i < th.length; i++) {
            th[i].classList.add('rotate');
          }
        } else {
          document.getElementById(key).innerText = data[key];
          document.getElementById(key).value = data[key];
        }
      })
      if ((draw) && (endpoint != "draw")) trigger("draw");
    })
    .catch(function (error) { });
}