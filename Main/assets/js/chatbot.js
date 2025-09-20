function setup() {
    noCanvas();

    let bot = new RiveScript();
    let conv = "";
    //bot.loadFile("http://tom.moulard.org/assets/brains/EN-tom.rive", brainReady, brainError);
    bot.loadFile("/assets/brains/EN-tom.rive")
        .then(brainReady)
        .catch(brainError);

    // let button = select("#submit");
    let user_input = select('#user_input');
    let response = select("#dialogue");

    user_input.changed(function (e) {
            ask(user_input.value());
            user_input.value("");
    });
    function brainReady(){
        console.log("Chat bot ready!");
        bot.sortReplies();
    }
    function brainError(error){
        console.log("Chat bot ERROR!", error);
    }
    function ask(things){
        things = betterstr(things);
        conv += "<font color='blue'><p><b>You</b>: " + things + "</p></font>";
        response.html(conv);
        console.log(things);
        bot.reply("local-user", things).then(function(reply) {
            anwser(reply);
        });
    }
    function anwser(things){
        conv += "<font color='red'><p><b>Bot</b>: " + things + "</p></font>";
        response.html(conv);
    }
    function betterstr(inpu){
        return inpu.replace(/</g, "&lt;")
                   .replace(/>/g, "&gt;")
                   .replace(/\'/g, "&apos;")
                   .replace(/\"/g, "&apos;&apos;");
    }
}
