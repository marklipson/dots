
function run() {
    var canvas = document.getElementById('dots');
    var ctx = canvas.getContext('2d');
    var name = "me";
    var player_data = {x: 200, y: 200};
    var everything = {};

    function check_in() {
        // send player data to server, receive data for all players
        $.ajax({
            url: "/run/" + name,
            data: {data: JSON.stringify(player_data)},
            dataType: "json",
            success: function(resp){
                // received updates for all players
                everything = resp;
            }
        })
    }

    function update(dt) {
      // Update the state of the world for the elapsed time since last render
    }

    function draw() {
        ctx.fillStyle = "black";
        ctx.fillRect(0, 0, 800, 800);
        ctx.fillStyle = "white";
        // Draw the state of the world
        for (var name in everything){
            var data = everything[name];
            // draw each player
            ctx.fillText(name, data.x, data.y);
        }
    }

    // game loop
    var lastRender = 0;
    function loop(timestamp) {
      var dt = timestamp - lastRender;
      if (lastRender) {
          update(dt);
      }
      draw();
      lastRender = timestamp;
      window.requestAnimationFrame(loop);
    }
    window.requestAnimationFrame(loop);
    // keep game data up to date with server
    setInterval(check_in, 500);
}
