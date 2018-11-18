let get_end = function(len) {
  let end = ""
  for(var i = 0; i < 14 - len; i++) {
    end += "|"
  }
  return end
}

window.onload = function() {
    var optionsLeft = {
        zone: document.getElementById("left_controller"),
        mode: 'static',
        position: {left: '50%', top: '50%'}
    }
    
    var optionsRight = {
        zone: document.getElementById("right_controller"),
        mode: 'static',
        position: {left: '50%', top: '50%'}
    }
    
    var managerRight = nipplejs.create(optionsRight);
    var managerLeft = nipplejs.create(optionsLeft);
    var exampleSocket = new WebSocket("ws:130.236.181.72:8000");

    var url = new URL(window.location.href);
    var c = url.searchParams.get("nick");
    var open = false;

    exampleSocket.onopen = function() {
      exampleSocket.send(";" +c + get_end(c.length - 1));
      open = true;
    }

    managerRight.on('start', function(evt, data) {
      if(open) {
        var s ="RIGHTSTART"
        exampleSocket.send(s + get_end(s.length));
      }
        
    }).on('end', function(evt, data) {
      if(open) {
        var s = "RIGHTEND"
        exampleSocket.send(s + get_end(s.length));
      }
        
    }).on('move', function(evt, data) {
      if(open) {
        let str = "_"+data.angle.radian.toString().substring(0, 4)+":"+data.distance.toString().substring(0, 4)
        let end = get_end(str.length)
        exampleSocket.send(str + end);
      }
      
    });

    managerLeft.on('start', function(evt, data) {
      if(open) {
        var s = "LEFTSTART"
        exampleSocket.send(s + get_end(s.length));
      }
      
    }).on('end', function(evt, data) {
      if(open) {
        var s = "LEFTEND"
        exampleSocket.send(s + get_end(s.length));
        exampleSocket.send(s + get_end(s.length));
      }
      
    }).on('move', function(evt, data) {
      if(open) {
        let str = "*"+data.angle.radian.toString().substring(0, 4)+":"+data.distance.toString().substring(0, 4)
        let end = get_end(str.length)
        exampleSocket.send(str + end);
      }
      
    });
}


