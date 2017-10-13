function setup() {
    noCanvas();

    let bot = new RiveScript();
    let conv = "";
    //bot.loadFile("http://tom.moulard.org/assets/brains/EN-tom.rive", brainReady, brainError);
    bot.loadFile("assets/brains/EN-tom.rive", brainReady, brainError);

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
    function brainError(){
        console.log("Chat bot ERROR!");
    }
    function ask(things){
        conv += "<font color='blue'><p><b>You</b>: " + betterstr(things) + "</p></font>";
        response.html(conv);
        anwser(bot.reply("local-user", things));
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
